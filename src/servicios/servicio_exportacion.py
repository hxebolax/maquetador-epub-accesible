# -*- coding: utf-8 -*-
"""
Servicio de Exportación.
Gestiona la exportación a múltiples formatos: PDF, MOBI, HTML.
"""

import os
import shutil
import subprocess
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from ..modelo.proyecto import Proyecto
from ..modelo.seccion import TipoSeccion


@dataclass
class ResultadoExportacion:
	"""Resultado de una exportación."""
	exito: bool
	ruta_salida: str = ""
	archivos_generados: List[str] = field(default_factory=list)
	advertencias: List[str] = field(default_factory=list)
	errores: List[str] = field(default_factory=list)


class ServicioExportacion:
	"""
	Servicio unificado de exportación a múltiples formatos.
	"""
	
	def __init__(self):
		"""Inicializa el servicio de exportación."""
		self._weasyprint = None
	
	def verificar_dependencias(self, formato: str) -> Tuple[bool, str]:
		"""
		Verifica si las dependencias para un formato están disponibles.
		
		Args:
			formato: Formato de exportación (pdf, mobi, html)
		
		Returns:
			Tuple[bool, str]: (disponible, mensaje)
		"""
		if formato == 'pdf':
			try:
				import weasyprint
				return True, "WeasyPrint disponible"
			except ImportError:
				return False, (
					"WeasyPrint no está instalado. "
					"Instálelo con: pip install weasyprint"
				)
		
		elif formato == 'mobi':
			# Verificar Calibre (ebook-convert)
			try:
				result = subprocess.run(
					['ebook-convert', '--version'],
					capture_output=True,
					text=True
				)
				if result.returncode == 0:
					return True, "Calibre disponible"
			except FileNotFoundError:
				pass
			
			return False, (
				"Calibre no está instalado. "
				"Descárguelo de: https://calibre-ebook.com/download"
			)
		
		elif formato == 'html':
			return True, "Exportación HTML nativa"
		
		return False, f"Formato no soportado: {formato}"
	
	def exportar_pdf(
		self,
		proyecto: Proyecto,
		ruta_salida: str
	) -> ResultadoExportacion:
		"""
		Exporta el proyecto a PDF.
		
		Args:
			proyecto: Proyecto a exportar
			ruta_salida: Ruta del archivo PDF de salida
		
		Returns:
			ResultadoExportacion: Resultado de la exportación
		"""
		resultado = ResultadoExportacion(exito=False, ruta_salida=ruta_salida)
		
		# Verificar dependencias
		disponible, mensaje = self.verificar_dependencias('pdf')
		if not disponible:
			resultado.errores.append(mensaje)
			return resultado
		
		try:
			import weasyprint
			
			# Generar HTML completo
			html_contenido = self._generar_html_completo(proyecto)
			
			# Crear PDF
			doc = weasyprint.HTML(string=html_contenido)
			doc.write_pdf(ruta_salida)
			
			resultado.exito = True
			resultado.archivos_generados.append(ruta_salida)
			
		except Exception as e:
			resultado.errores.append(f"Error al generar PDF: {e}")
		
		return resultado
	
	def exportar_mobi(
		self,
		proyecto: Proyecto,
		ruta_salida: str,
		ruta_epub_temporal: Optional[str] = None
	) -> ResultadoExportacion:
		"""
		Exporta el proyecto a MOBI usando Calibre.
		
		Args:
			proyecto: Proyecto a exportar
			ruta_salida: Ruta del archivo MOBI de salida
			ruta_epub_temporal: Ruta del EPUB temporal (se genera si no se proporciona)
		
		Returns:
			ResultadoExportacion: Resultado de la exportación
		"""
		resultado = ResultadoExportacion(exito=False, ruta_salida=ruta_salida)
		
		# Verificar dependencias
		disponible, mensaje = self.verificar_dependencias('mobi')
		if not disponible:
			resultado.errores.append(mensaje)
			return resultado
		
		try:
			# Si no hay EPUB temporal, generarlo
			epub_temporal = ruta_epub_temporal
			eliminar_epub = False
			
			if not epub_temporal:
				from .servicio_epub import ServicioEPUB
				
				epub_temporal = ruta_salida.replace('.mobi', '_temp.epub')
				servicio_epub = ServicioEPUB()
				resultado_epub = servicio_epub.generar_epub(proyecto, epub_temporal)
				
				if not resultado_epub.exito:
					resultado.errores.extend(resultado_epub.errores)
					return resultado
				
				eliminar_epub = True
			
			# Convertir con Calibre
			cmd = ['ebook-convert', epub_temporal, ruta_salida]
			
			# Agregar metadatos
			if proyecto.metadatos.titulo:
				cmd.extend(['--title', proyecto.metadatos.titulo])
			if proyecto.metadatos.autores:
				cmd.extend(['--authors', ', '.join(proyecto.metadatos.autores)])
			
			process = subprocess.run(cmd, capture_output=True, text=True)
			
			if process.returncode == 0:
				resultado.exito = True
				resultado.archivos_generados.append(ruta_salida)
			else:
				resultado.errores.append(f"Error de Calibre: {process.stderr}")
			
			# Limpiar EPUB temporal
			if eliminar_epub and os.path.exists(epub_temporal):
				os.remove(epub_temporal)
			
		except Exception as e:
			resultado.errores.append(f"Error al generar MOBI: {e}")
		
		return resultado
	
	def exportar_html(
		self,
		proyecto: Proyecto,
		carpeta_salida: str
	) -> ResultadoExportacion:
		"""
		Exporta el proyecto a HTML navegable.
		
		Args:
			proyecto: Proyecto a exportar
			carpeta_salida: Carpeta de salida
		
		Returns:
			ResultadoExportacion: Resultado de la exportación
		"""
		resultado = ResultadoExportacion(exito=False, ruta_salida=carpeta_salida)
		
		try:
			# Crear carpeta si no existe
			if not os.path.exists(carpeta_salida):
				os.makedirs(carpeta_salida)
			
			# Crear subcarpetas
			carpeta_css = os.path.join(carpeta_salida, 'css')
			carpeta_img = os.path.join(carpeta_salida, 'imagenes')
			os.makedirs(carpeta_css, exist_ok=True)
			os.makedirs(carpeta_img, exist_ok=True)
			
			# Generar CSS
			css_contenido = self._generar_css()
			ruta_css = os.path.join(carpeta_css, 'estilos.css')
			with open(ruta_css, 'w', encoding='utf-8') as f:
				f.write(css_contenido)
			resultado.archivos_generados.append(ruta_css)
			
			# Copiar portada si existe
			if proyecto.portada and os.path.exists(proyecto.portada.ruta):
				nombre_portada = proyecto.portada.obtener_nombre_epub()
				ruta_portada = os.path.join(carpeta_img, nombre_portada)
				shutil.copy2(proyecto.portada.ruta, ruta_portada)
				resultado.archivos_generados.append(ruta_portada)
			
			# Generar archivos HTML para cada sección
			archivos_secciones = []
			for i, seccion in enumerate(proyecto.secciones):
				nombre_archivo = f"seccion_{i+1:03d}.html"
				ruta_seccion = os.path.join(carpeta_salida, nombre_archivo)
				
				html_seccion = self._generar_html_seccion(
					proyecto, seccion, i,
					len(proyecto.secciones)
				)
				
				with open(ruta_seccion, 'w', encoding='utf-8') as f:
					f.write(html_seccion)
				
				archivos_secciones.append((nombre_archivo, seccion.titulo or f"Sección {i+1}"))
				resultado.archivos_generados.append(ruta_seccion)
				
				# Copiar imágenes de la sección
				for imagen in seccion.imagenes:
					if os.path.exists(imagen.ruta):
						nombre_img = imagen.obtener_nombre_epub()
						ruta_img = os.path.join(carpeta_img, nombre_img)
						shutil.copy2(imagen.ruta, ruta_img)
						resultado.archivos_generados.append(ruta_img)
			
			# Generar index.html
			ruta_index = os.path.join(carpeta_salida, 'index.html')
			html_index = self._generar_html_index(proyecto, archivos_secciones)
			with open(ruta_index, 'w', encoding='utf-8') as f:
				f.write(html_index)
			resultado.archivos_generados.append(ruta_index)
			
			resultado.exito = True
			
		except Exception as e:
			resultado.errores.append(f"Error al generar HTML: {e}")
		
		return resultado
	
	def _generar_html_completo(self, proyecto: Proyecto) -> str:
		"""Genera un HTML completo del proyecto para PDF."""
		titulo = proyecto.metadatos.titulo or "Sin título"
		idioma = proyecto.metadatos.idioma or "es"
		
		contenido = []
		
		# Portada
		if proyecto.portada and os.path.exists(proyecto.portada.ruta):
			import base64
			with open(proyecto.portada.ruta, 'rb') as f:
				datos = base64.b64encode(f.read()).decode('utf-8')
			mime = proyecto.portada.obtener_tipo_mime()
			contenido.append(f'''
<div class="portada" style="text-align: center; page-break-after: always;">
	<h1>{titulo}</h1>
	<img src="data:{mime};base64,{datos}" alt="{proyecto.portada.texto_alternativo}" style="max-width: 80%;"/>
	<p><em>{", ".join(proyecto.metadatos.autores)}</em></p>
</div>
''')
		
		# Secciones
		for seccion in proyecto.secciones:
			nivel = seccion.nivel_encabezado
			titulo_seccion = seccion.titulo or TipoSeccion.obtener_nombre_legible(seccion.tipo)
			contenido.append(f'<section style="page-break-before: always;">')
			contenido.append(f'<h{nivel}>{titulo_seccion}</h{nivel}>')
			contenido.append(seccion.contenido_xhtml or '')
			contenido.append('</section>')
		
		return f'''<!DOCTYPE html>
<html lang="{idioma}">
<head>
<meta charset="UTF-8">
<title>{titulo}</title>
<style>
{self._generar_css()}
@page {{ margin: 2cm; }}
</style>
</head>
<body>
{"".join(contenido)}
</body>
</html>'''
	
	def _generar_html_seccion(
		self,
		proyecto: Proyecto,
		seccion,
		indice: int,
		total: int
	) -> str:
		"""Genera HTML para una sección individual."""
		titulo = seccion.titulo or TipoSeccion.obtener_nombre_legible(seccion.tipo)
		idioma = proyecto.metadatos.idioma or "es"
		nivel = seccion.nivel_encabezado
		
		# Navegación
		nav_anterior = ""
		nav_siguiente = ""
		
		if indice > 0:
			nav_anterior = f'<a href="seccion_{indice:03d}.html">← Anterior</a>'
		if indice < total - 1:
			nav_siguiente = f'<a href="seccion_{indice+2:03d}.html">Siguiente →</a>'
		
		return f'''<!DOCTYPE html>
<html lang="{idioma}">
<head>
<meta charset="UTF-8">
<title>{titulo} - {proyecto.metadatos.titulo or "Libro"}</title>
<link rel="stylesheet" href="css/estilos.css">
</head>
<body>
<nav class="navegacion">
	{nav_anterior}
	<a href="index.html">Índice</a>
	{nav_siguiente}
</nav>
<main>
<h{nivel}>{titulo}</h{nivel}>
{seccion.contenido_xhtml or '<p><em>Sin contenido</em></p>'}
</main>
<nav class="navegacion">
	{nav_anterior}
	<a href="index.html">Índice</a>
	{nav_siguiente}
</nav>
</body>
</html>'''
	
	def _generar_html_index(
		self,
		proyecto: Proyecto,
		archivos_secciones: List[Tuple[str, str]]
	) -> str:
		"""Genera el archivo index.html."""
		titulo = proyecto.metadatos.titulo or "Sin título"
		idioma = proyecto.metadatos.idioma or "es"
		autores = ", ".join(proyecto.metadatos.autores) or "Autor desconocido"
		
		# Lista de secciones
		lista_secciones = []
		for archivo, titulo_seccion in archivos_secciones:
			lista_secciones.append(f'<li><a href="{archivo}">{titulo_seccion}</a></li>')
		
		return f'''<!DOCTYPE html>
<html lang="{idioma}">
<head>
<meta charset="UTF-8">
<title>{titulo}</title>
<link rel="stylesheet" href="css/estilos.css">
</head>
<body>
<header>
	<h1>{titulo}</h1>
	<p class="autor">{autores}</p>
</header>
<nav>
	<h2>Índice</h2>
	<ol>
		{"".join(lista_secciones)}
	</ol>
</nav>
</body>
</html>'''
	
	def _generar_css(self) -> str:
		"""Genera el CSS para exportación."""
		return '''
body {
	font-family: Georgia, "Times New Roman", serif;
	font-size: 14px;
	line-height: 1.6;
	max-width: 800px;
	margin: 0 auto;
	padding: 20px;
}
h1, h2, h3, h4, h5, h6 {
	font-family: Arial, Helvetica, sans-serif;
	margin-top: 1.5em;
	margin-bottom: 0.5em;
}
h1 { font-size: 1.8em; }
h2 { font-size: 1.5em; }
h3 { font-size: 1.3em; }
p { margin: 0.5em 0; text-align: justify; }
blockquote {
	margin: 1em 2em;
	padding: 0.5em 1em;
	border-left: 3px solid #666;
	font-style: italic;
}
ul, ol { margin: 0.5em 0; padding-left: 2em; }
img { max-width: 100%; height: auto; }
figure { margin: 1em 0; text-align: center; }
figcaption { font-size: 0.9em; font-style: italic; }
.navegacion {
	padding: 1em 0;
	border-bottom: 1px solid #ccc;
	margin-bottom: 1em;
}
.navegacion a {
	margin-right: 1em;
	color: #0066cc;
}
.autor { font-style: italic; color: #666; }
.portada { text-align: center; }
'''
