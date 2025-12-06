# -*- coding: utf-8 -*-
"""
Servicio EPUB.
Gestiona la generación de archivos EPUB 3 accesibles.
"""

import os
import shutil
from typing import List, Optional, Tuple
from dataclasses import dataclass, field

from ..modelo.proyecto import Proyecto
from ..modelo.seccion import Seccion, TipoSeccion
from ..modelo.imagen import Imagen
from .servicio_xhtml import ServicioXHTML


@dataclass
class ResultadoExportacion:
	"""Resultado de una exportación EPUB."""
	exito: bool
	ruta_epub: str = ""
	archivos_generados: List[str] = field(default_factory=list)
	advertencias: List[str] = field(default_factory=list)
	errores: List[str] = field(default_factory=list)


class ErrorEPUB(Exception):
	"""Excepción para errores de generación EPUB."""
	pass


class ServicioEPUB:
	"""
	Servicio para generación de archivos EPUB 3.
	
	Utiliza EbookLib como biblioteca base con una capa de abstracción
	para facilitar cambios futuros.
	"""
	
	def __init__(self):
		"""Inicializa el servicio EPUB."""
		self.servicio_xhtml = ServicioXHTML()
		self._ebooklib = None
	
	def _obtener_ebooklib(self):
		"""Obtiene la biblioteca ebooklib (carga diferida)."""
		if self._ebooklib is None:
			try:
				from ebooklib import epub
				self._ebooklib = epub
			except ImportError:
				raise ImportError(
					"La biblioteca 'ebooklib' no está instalada. "
					"Instálela con: pip install ebooklib"
				)
		return self._ebooklib
	
	def generar_epub(self, proyecto: Proyecto, ruta_salida: str) -> ResultadoExportacion:
		"""
		Genera un archivo EPUB 3 a partir de un proyecto.
		
		Args:
			proyecto: Proyecto a exportar
			ruta_salida: Ruta del archivo EPUB de salida
		
		Returns:
			ResultadoExportacion: Resultado de la exportación
		"""
		resultado = ResultadoExportacion(exito=False, ruta_epub=ruta_salida)
		
		try:
			epub = self._obtener_ebooklib()
			
			# Crear libro
			libro = epub.EpubBook()
			
			# Configurar metadatos
			self._configurar_metadatos(libro, proyecto)
			
			# Configurar metadatos de accesibilidad
			self._configurar_accesibilidad(libro, proyecto)
			
			# Agregar CSS
			css_item = self._crear_css()
			libro.add_item(css_item)
			resultado.archivos_generados.append("css/estilos.css")
			
			# Agregar portada si existe
			if proyecto.portada:
				self._agregar_portada(libro, proyecto.portada, resultado)
			
			# Verificar que hay secciones
			if not proyecto.secciones:
				resultado.errores.append("El proyecto no tiene secciones para exportar")
				return resultado
			
			# Agregar secciones
			capitulos = []
			for seccion in proyecto.secciones:
				capitulo = self._crear_capitulo(libro, seccion, proyecto, resultado)
				if capitulo:
					libro.add_item(capitulo)
					capitulos.append(capitulo)
			
			# Verificar que se crearon capítulos
			if not capitulos:
				resultado.errores.append("No se pudo crear ningún capítulo")
				return resultado
			
			# Crear tabla de contenidos
			libro.toc = self._generar_toc(capitulos, proyecto.secciones)
			
			# Agregar navegación
			libro.add_item(epub.EpubNcx())
			libro.add_item(epub.EpubNav())
			
			# Configurar spine
			spine_items = ['nav']
			if proyecto.portada:
				spine_items.insert(0, 'cover')
			spine_items.extend(capitulos)
			libro.spine = spine_items
			
			# Escribir EPUB
			epub.write_epub(ruta_salida, libro, {})
			
			resultado.exito = True
			resultado.archivos_generados.append(os.path.basename(ruta_salida))
			
		except ImportError as e:
			resultado.errores.append(str(e))
		except Exception as e:
			import traceback
			resultado.errores.append(f"Error al generar EPUB: {e}")
			resultado.errores.append(f"Detalle: {traceback.format_exc()}")
		
		return resultado
	
	def _configurar_metadatos(self, libro, proyecto: Proyecto) -> None:
		"""Configura los metadatos Dublin Core del libro."""
		meta = proyecto.metadatos
		
		# Identificador
		libro.set_identifier(meta.identificador)
		
		# Título
		libro.set_title(meta.titulo or "Sin título")
		
		# Idioma
		libro.set_language(meta.idioma or "es")
		
		# Autores
		for autor in meta.autores:
			libro.add_author(autor)
		
		# Editor
		if meta.editor:
			libro.add_metadata('DC', 'publisher', meta.editor)
		
		# Fecha
		if meta.fecha:
			libro.add_metadata('DC', 'date', meta.fecha)
		
		# Derechos
		if meta.derechos:
			libro.add_metadata('DC', 'rights', meta.derechos)
		
		# Descripción
		if meta.descripcion:
			libro.add_metadata('DC', 'description', meta.descripcion)
		
		# Temas
		for tema in meta.temas:
			libro.add_metadata('DC', 'subject', tema)
	
	def _configurar_accesibilidad(self, libro, proyecto: Proyecto) -> None:
		"""Configura los metadatos de accesibilidad."""
		acc = proyecto.metadatos_accesibilidad
		
		# Modos de acceso
		for modo in acc.access_mode:
			libro.add_metadata(
				None, 'meta',
				modo,
				{'property': 'schema:accessMode'}
			)
		
		# Modos de acceso suficientes
		for modo in acc.access_mode_sufficient:
			libro.add_metadata(
				None, 'meta',
				modo,
				{'property': 'schema:accessModeSufficient'}
			)
		
		# Características de accesibilidad
		for feature in acc.accessibility_feature:
			libro.add_metadata(
				None, 'meta',
				feature,
				{'property': 'schema:accessibilityFeature'}
			)
		
		# Peligros de accesibilidad
		for hazard in acc.accessibility_hazard:
			libro.add_metadata(
				None, 'meta',
				hazard,
				{'property': 'schema:accessibilityHazard'}
			)
		
		# Resumen de accesibilidad
		if acc.accessibility_summary:
			libro.add_metadata(
				None, 'meta',
				acc.accessibility_summary,
				{'property': 'schema:accessibilitySummary'}
			)
		
		# Conformidad WCAG
		conformance_url = acc.obtener_conformance_url()
		libro.add_metadata(
			None, 'link',
			None,
			{'rel': 'dcterms:conformsTo', 'href': conformance_url}
		)
	
	def _crear_css(self):
		"""Crea el archivo CSS para el EPUB."""
		epub = self._obtener_ebooklib()
		
		css_contenido = '''/* Estilos para EPUB accesible */
body {
	font-family: Georgia, "Times New Roman", serif;
	font-size: 1em;
	line-height: 1.6;
	margin: 1em;
	padding: 0;
}

h1, h2, h3, h4, h5, h6 {
	font-family: Arial, Helvetica, sans-serif;
	line-height: 1.3;
	margin-top: 1.5em;
	margin-bottom: 0.5em;
}

h1 { font-size: 1.8em; }
h2 { font-size: 1.5em; }
h3 { font-size: 1.3em; }
h4 { font-size: 1.1em; }
h5 { font-size: 1em; }
h6 { font-size: 0.9em; }

p {
	margin: 0.5em 0;
	text-align: justify;
}

blockquote {
	margin: 1em 2em;
	padding-left: 1em;
	border-left: 3px solid #ccc;
	font-style: italic;
}

ul, ol {
	margin: 0.5em 0;
	padding-left: 2em;
}

li {
	margin: 0.3em 0;
}

figure {
	margin: 1em 0;
	text-align: center;
}

figcaption {
	font-size: 0.9em;
	font-style: italic;
	margin-top: 0.5em;
}

img {
	max-width: 100%;
	height: auto;
}

.portada {
	text-align: center;
	padding: 0;
	margin: 0;
	height: 100vh;
	display: flex;
	align-items: center;
	justify-content: center;
}

.portada img {
	max-width: 100%;
	max-height: 100vh;
	object-fit: contain;
}
'''
		
		css_item = epub.EpubItem(
			uid="estilo_principal",
			file_name="css/estilos.css",
			media_type="text/css",
			content=css_contenido.encode('utf-8')
		)
		
		return css_item
	
	def _agregar_portada(
		self,
		libro,
		portada: Imagen,
		resultado: ResultadoExportacion
	) -> None:
		"""Agrega la imagen de portada al libro."""
		epub = self._obtener_ebooklib()
		
		try:
			# Leer imagen
			if not os.path.exists(portada.ruta):
				resultado.advertencias.append(
					f"Archivo de portada no encontrado: {portada.ruta}"
				)
				return
			
			with open(portada.ruta, 'rb') as f:
				contenido_imagen = f.read()
			
			# Crear item de imagen
			nombre_archivo = f"imagenes/{portada.obtener_nombre_epub()}"
			imagen_item = epub.EpubItem(
				uid="cover-image",
				file_name=nombre_archivo,
				media_type=portada.obtener_tipo_mime(),
				content=contenido_imagen
			)
			# Marcar como imagen de portada en los metadatos
			imagen_item.is_linear = False
			libro.add_item(imagen_item)
			
			# Agregar metadato de portada
			libro.add_metadata(None, 'meta', '', {'name': 'cover', 'content': 'cover-image'})
			
			# Crear página de portada personalizada con accesibilidad
			alt_text = portada.texto_alternativo or "Portada del libro"
			descripcion_larga = portada.descripcion_larga or ""
			
			# Construir el HTML de la imagen con accesibilidad
			# nombre_archivo ya incluye "imagenes/", usar ruta relativa desde texto/
			ruta_imagen = f"../{nombre_archivo}"
			
			# Si hay descripción larga, usar figure con figcaption
			if descripcion_larga:
				imagen_html = f'''<figure role="img" aria-labelledby="portada-desc">
    <img src="{ruta_imagen}" alt="{alt_text}"/>
    <figcaption id="portada-desc" class="visually-hidden">{descripcion_larga}</figcaption>
  </figure>'''
			else:
				imagen_html = f'<img src="{ruta_imagen}" alt="{alt_text}"/>'
			
			portada_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <meta charset="UTF-8"/>
  <title>Portada</title>
  <link rel="stylesheet" type="text/css" href="../css/estilos.css"/>
  <style type="text/css">
    * {{
      margin: 0;
      padding: 0;
    }}
    body {{
      text-align: center;
    }}
    figure {{
      margin: 0;
      padding: 0;
    }}
    img {{
      max-width: 100%;
      max-height: 100%;
    }}
    .visually-hidden {{
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }}
  </style>
</head>
<body epub:type="cover">
  {imagen_html}
</body>
</html>'''
			
			portada_item = epub.EpubItem(
				uid="cover",
				file_name="texto/portada.xhtml",
				media_type="application/xhtml+xml",
				content=portada_xhtml.encode('utf-8')
			)
			libro.add_item(portada_item)
			
			resultado.archivos_generados.append(nombre_archivo)
			resultado.archivos_generados.append("texto/portada.xhtml")
			
		except Exception as e:
			resultado.advertencias.append(f"Error al agregar portada: {e}")
	
	def _crear_capitulo(
		self,
		libro,
		seccion: Seccion,
		proyecto: Proyecto,
		resultado: ResultadoExportacion
	) -> Optional[object]:
		"""Crea un capítulo EPUB a partir de una sección."""
		epub = self._obtener_ebooklib()
		
		try:
			# Generar nombre de archivo
			nombre_archivo = f"texto/{seccion.obtener_nombre_archivo()}.xhtml"
			
			# Preparar contenido
			contenido = seccion.contenido_xhtml or ""
			
			# Agregar encabezado si hay título
			if seccion.titulo:
				encabezado = self.servicio_xhtml.aplicar_encabezado(
					seccion.titulo,
					seccion.nivel_encabezado
				)
				contenido = encabezado + "\n" + contenido
			
			# Si el contenido está vacío, agregar un párrafo vacío para evitar errores
			if not contenido.strip():
				contenido = "<p></p>"
			
			# Agregar imágenes de la sección
			for imagen in seccion.imagenes:
				self._agregar_imagen_seccion(libro, imagen, resultado)
			
			# Generar documento XHTML completo
			xhtml_completo = self.servicio_xhtml.generar_documento_xhtml(
				contenido=contenido,
				titulo=seccion.titulo or seccion.tipo.value,
				epub_type=seccion.epub_type,
				idioma=proyecto.metadatos.idioma
			)
			
			# Asegurar que el contenido no esté vacío
			if not xhtml_completo or not xhtml_completo.strip():
				resultado.advertencias.append(
					f"Sección '{seccion.titulo}' tiene contenido vacío"
				)
				return None
			
			# Crear capítulo usando EpubItem para evitar el parseo de lxml
			capitulo = epub.EpubItem(
				uid=seccion.id,
				file_name=nombre_archivo,
				media_type='application/xhtml+xml',
				content=xhtml_completo.encode('utf-8')
			)
			
			# Guardar título para la TOC
			capitulo.title = seccion.titulo or TipoSeccion.obtener_nombre_legible(seccion.tipo)
			
			resultado.archivos_generados.append(nombre_archivo)
			
			return capitulo
			
		except Exception as e:
			resultado.errores.append(
				f"Error al crear capítulo '{seccion.titulo}': {e}"
			)
			return None
	
	def _agregar_imagen_seccion(
		self,
		libro,
		imagen: Imagen,
		resultado: ResultadoExportacion
	) -> None:
		"""Agrega una imagen de sección al libro."""
		epub = self._obtener_ebooklib()
		
		try:
			if not os.path.exists(imagen.ruta):
				resultado.advertencias.append(
					f"Imagen no encontrada: {imagen.ruta}"
				)
				return
			
			with open(imagen.ruta, 'rb') as f:
				contenido = f.read()
			
			nombre_archivo = f"imagenes/{imagen.obtener_nombre_epub()}"
			
			imagen_item = epub.EpubItem(
				uid=imagen.id,
				file_name=nombre_archivo,
				media_type=imagen.obtener_tipo_mime(),
				content=contenido
			)
			libro.add_item(imagen_item)
			
			resultado.archivos_generados.append(nombre_archivo)
			
		except Exception as e:
			resultado.advertencias.append(f"Error al agregar imagen: {e}")
	
	def _generar_toc(
		self,
		capitulos: List,
		secciones: List[Seccion]
	) -> List:
		"""Genera la tabla de contenidos."""
		epub = self._obtener_ebooklib()
		
		toc = []
		for i, capitulo in enumerate(capitulos):
			if i < len(secciones):
				seccion = secciones[i]
				titulo = seccion.titulo or TipoSeccion.obtener_nombre_legible(seccion.tipo)
			else:
				titulo = getattr(capitulo, 'title', f'Capítulo {i+1}')
			
			# Usar uid o id según el tipo de objeto
			item_id = getattr(capitulo, 'uid', None) or getattr(capitulo, 'id', f'cap_{i}')
			
			toc.append(epub.Link(capitulo.file_name, titulo, item_id))
		
		return toc
	
	def generar_nav_xhtml(self, proyecto: Proyecto) -> str:
		"""
		Genera el contenido del archivo nav.xhtml.
		
		Args:
			proyecto: Proyecto del libro
		
		Returns:
			str: Contenido XHTML del archivo de navegación
		"""
		idioma = proyecto.metadatos.idioma or "es"
		
		# Generar TOC
		toc_items = []
		for seccion in proyecto.secciones:
			nombre_archivo = f"texto/{seccion.obtener_nombre_archivo()}.xhtml"
			titulo = seccion.titulo or TipoSeccion.obtener_nombre_legible(seccion.tipo)
			toc_items.append(f'      <li><a href="{nombre_archivo}">{titulo}</a></li>')
		
		toc_html = '\n'.join(toc_items)
		
		# Generar landmarks
		landmarks = []
		
		# Portada
		if proyecto.portada:
			landmarks.append(
				'      <li><a epub:type="cover" href="texto/portada.xhtml">Portada</a></li>'
			)
		
		# TOC
		landmarks.append(
			'      <li><a epub:type="toc" href="nav.xhtml">Índice</a></li>'
		)
		
		# Inicio del contenido
		if proyecto.secciones:
			primera = proyecto.secciones[0]
			nombre = f"texto/{primera.obtener_nombre_archivo()}.xhtml"
			landmarks.append(
				f'      <li><a epub:type="bodymatter" href="{nombre}">Inicio del contenido</a></li>'
			)
		
		landmarks_html = '\n'.join(landmarks)
		
		nav_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{idioma}" lang="{idioma}">
<head>
  <meta charset="UTF-8"/>
  <title>Índice</title>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Índice</h1>
    <ol>
{toc_html}
    </ol>
  </nav>
  <nav epub:type="landmarks" id="landmarks" hidden="">
    <h1>Puntos de referencia</h1>
    <ol>
{landmarks_html}
    </ol>
  </nav>
</body>
</html>'''
		
		return nav_xhtml
	
	def validar_proyecto_para_epub(self, proyecto: Proyecto) -> List[str]:
		"""
		Valida un proyecto antes de exportar.
		
		Args:
			proyecto: Proyecto a validar
		
		Returns:
			List[str]: Lista de advertencias/errores
		"""
		problemas = []
		
		# Validar metadatos
		errores_meta = proyecto.metadatos.validar()
		problemas.extend(errores_meta)
		
		# Validar que haya contenido
		if not proyecto.secciones:
			problemas.append("El libro no tiene secciones")
		
		# Validar secciones
		for i, seccion in enumerate(proyecto.secciones):
			if not seccion.titulo:
				problemas.append(f"La sección {i+1} no tiene título")
			
			# Validar imágenes de la sección
			for imagen in seccion.imagenes:
				errores_img = imagen.validar()
				for error in errores_img:
					problemas.append(f"Sección '{seccion.titulo}': {error}")
		
		# Validar portada
		if proyecto.portada:
			errores_portada = proyecto.portada.validar()
			for error in errores_portada:
				problemas.append(f"Portada: {error}")
		
		return problemas
