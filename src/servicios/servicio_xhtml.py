# -*- coding: utf-8 -*-
"""
Servicio XHTML.
Gestiona la conversión y manipulación de contenido XHTML para EPUB.
"""

import re
import html
from typing import List, Optional
from xml.etree import ElementTree as ET


class ServicioXHTML:
	"""
	Servicio para manipulación de contenido XHTML.
	
	Proporciona métodos para convertir diferentes formatos a XHTML
	válido para EPUB 3.
	"""
	
	# Namespace XHTML
	XHTML_NS = "http://www.w3.org/1999/xhtml"
	
	# Plantilla de documento XHTML
	PLANTILLA_XHTML = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{idioma}" lang="{idioma}">
<head>
	<meta charset="UTF-8"/>
	<title>{titulo}</title>
	<link rel="stylesheet" type="text/css" href="../css/estilos.css"/>
</head>
<body epub:type="{epub_type}">
{contenido}
</body>
</html>'''
	
	def __init__(self):
		"""Inicializa el servicio XHTML."""
		self._markdown = None
		self._bs4 = None
	
	def _obtener_markdown(self):
		"""Obtiene la instancia de markdown (carga diferida)."""
		if self._markdown is None:
			try:
				import markdown
				self._markdown = markdown.Markdown(
					extensions=['extra', 'sane_lists'],
					output_format='xhtml'
				)
			except ImportError:
				raise ImportError(
					"La biblioteca 'markdown' no está instalada. "
					"Instálela con: pip install markdown"
				)
		return self._markdown
	
	def _obtener_beautifulsoup(self):
		"""Obtiene BeautifulSoup (carga diferida)."""
		if self._bs4 is None:
			try:
				from bs4 import BeautifulSoup
				self._bs4 = BeautifulSoup
			except ImportError:
				raise ImportError(
					"La biblioteca 'beautifulsoup4' no está instalada. "
					"Instálela con: pip install beautifulsoup4 lxml"
				)
		return self._bs4
	
	def txt_a_xhtml(self, texto: str) -> str:
		"""
		Convierte texto plano a XHTML.
		
		Los saltos de línea dobles se convierten en párrafos separados.
		Los saltos de línea simples se preservan como <br/>.
		
		Args:
			texto: Texto plano a convertir
		
		Returns:
			str: Contenido XHTML (solo el cuerpo, sin documento completo)
		"""
		if not texto:
			return ""
		
		# Escapar caracteres HTML
		texto = html.escape(texto)
		
		# Normalizar saltos de línea
		texto = texto.replace('\r\n', '\n').replace('\r', '\n')
		
		# Dividir en párrafos (líneas vacías separan párrafos)
		parrafos = re.split(r'\n\s*\n', texto)
		
		resultado = []
		for parrafo in parrafos:
			parrafo = parrafo.strip()
			if parrafo:
				# Convertir saltos de línea simples a <br/>
				parrafo = parrafo.replace('\n', '<br/>\n')
				resultado.append(f"<p>{parrafo}</p>")
		
		return '\n'.join(resultado)
	
	def markdown_a_xhtml(self, md: str) -> str:
		"""
		Convierte Markdown a XHTML.
		
		Args:
			md: Contenido Markdown
		
		Returns:
			str: Contenido XHTML
		"""
		if not md:
			return ""
		
		markdown_parser = self._obtener_markdown()
		markdown_parser.reset()
		
		# Convertir Markdown a HTML
		html_content = markdown_parser.convert(md)
		
		# Limpiar y normalizar
		return self.limpiar_html(html_content)
	
	def limpiar_html(self, html_content: str) -> str:
		"""
		Limpia y normaliza HTML a XHTML válido para EPUB.
		
		Args:
			html_content: Contenido HTML a limpiar
		
		Returns:
			str: XHTML limpio y válido
		"""
		if not html_content:
			return ""
		
		BeautifulSoup = self._obtener_beautifulsoup()
		
		# Parsear HTML
		soup = BeautifulSoup(html_content, 'html.parser')
		
		# Eliminar scripts y estilos inline peligrosos
		for tag in soup.find_all(['script', 'style']):
			tag.decompose()
		
		# Eliminar atributos peligrosos
		for tag in soup.find_all(True):
			attrs_a_eliminar = []
			for attr in tag.attrs:
				if attr.startswith('on') or attr in ['style']:
					attrs_a_eliminar.append(attr)
			for attr in attrs_a_eliminar:
				del tag[attr]
		
		# Cerrar etiquetas vacías correctamente para XHTML
		resultado = str(soup)
		
		# Asegurar que las etiquetas vacías estén cerradas
		etiquetas_vacias = ['br', 'hr', 'img', 'meta', 'link', 'input']
		for tag in etiquetas_vacias:
			# Convertir <tag> a <tag/>
			resultado = re.sub(
				rf'<{tag}(\s[^>]*)?>(?!</{tag}>)',
				rf'<{tag}\1/>',
				resultado,
				flags=re.IGNORECASE
			)
		
		return resultado
	
	def aplicar_encabezado(self, texto: str, nivel: int) -> str:
		"""
		Crea un elemento de encabezado XHTML.
		
		Args:
			texto: Texto del encabezado
			nivel: Nivel del encabezado (1-6)
		
		Returns:
			str: Elemento de encabezado XHTML
		"""
		# Validar nivel
		nivel = max(1, min(6, nivel))
		
		# Escapar texto
		texto_escapado = html.escape(texto)
		
		return f"<h{nivel}>{texto_escapado}</h{nivel}>"
	
	def aplicar_lista(self, items: List[str], ordenada: bool = False) -> str:
		"""
		Crea una lista XHTML.
		
		Args:
			items: Lista de elementos
			ordenada: True para lista ordenada (ol), False para no ordenada (ul)
		
		Returns:
			str: Lista XHTML
		"""
		if not items:
			return ""
		
		tag = "ol" if ordenada else "ul"
		
		items_html = []
		for item in items:
			item_escapado = html.escape(str(item))
			items_html.append(f"  <li>{item_escapado}</li>")
		
		return f"<{tag}>\n" + "\n".join(items_html) + f"\n</{tag}>"
	
	def aplicar_parrafo(self, texto: str) -> str:
		"""
		Crea un párrafo XHTML.
		
		Args:
			texto: Texto del párrafo
		
		Returns:
			str: Párrafo XHTML
		"""
		texto_escapado = html.escape(texto)
		return f"<p>{texto_escapado}</p>"
	
	def aplicar_cita(self, texto: str, fuente: Optional[str] = None) -> str:
		"""
		Crea una cita XHTML.
		
		Args:
			texto: Texto de la cita
			fuente: Fuente de la cita (opcional)
		
		Returns:
			str: Cita XHTML
		"""
		texto_escapado = html.escape(texto)
		
		if fuente:
			fuente_escapada = html.escape(fuente)
			return f"<blockquote>\n  <p>{texto_escapado}</p>\n  <cite>{fuente_escapada}</cite>\n</blockquote>"
		
		return f"<blockquote>\n  <p>{texto_escapado}</p>\n</blockquote>"
	
	def generar_imagen_xhtml(
		self,
		src: str,
		alt: str,
		descripcion_larga: Optional[str] = None,
		id_imagen: Optional[str] = None
	) -> str:
		"""
		Genera el XHTML para una imagen con accesibilidad.
		
		Args:
			src: Ruta de la imagen
			alt: Texto alternativo
			descripcion_larga: Descripción larga (opcional)
			id_imagen: ID de la imagen (opcional)
		
		Returns:
			str: XHTML de la imagen con atributos de accesibilidad
		"""
		alt_escapado = html.escape(alt)
		src_escapado = html.escape(src)
		
		atributos = [f'src="{src_escapado}"', f'alt="{alt_escapado}"']
		
		if id_imagen:
			atributos.append(f'id="{html.escape(id_imagen)}"')
		
		resultado = []
		
		if descripcion_larga:
			# Crear ID para la descripción
			desc_id = f"desc-{id_imagen}" if id_imagen else "desc-img"
			atributos.append(f'aria-describedby="{desc_id}"')
			
			# Imagen con referencia a descripción
			resultado.append(f'<figure>')
			resultado.append(f'  <img {" ".join(atributos)}/>')
			resultado.append(f'  <figcaption id="{desc_id}">{html.escape(descripcion_larga)}</figcaption>')
			resultado.append(f'</figure>')
		else:
			resultado.append(f'<img {" ".join(atributos)}/>')
		
		return '\n'.join(resultado)
	
	def generar_documento_xhtml(
		self,
		contenido: str,
		titulo: str,
		epub_type: str = "bodymatter",
		idioma: str = "es"
	) -> str:
		"""
		Genera un documento XHTML completo para EPUB.
		
		Args:
			contenido: Contenido del cuerpo
			titulo: Título del documento
			epub_type: Tipo epub:type
			idioma: Código de idioma
		
		Returns:
			str: Documento XHTML completo
		"""
		# Limpiar caracteres de control que pueden causar problemas en XML
		contenido_limpio = self._limpiar_caracteres_control(contenido)
		titulo_limpio = self._limpiar_caracteres_control(titulo)
		
		return self.PLANTILLA_XHTML.format(
			idioma=idioma,
			titulo=html.escape(titulo_limpio),
			epub_type=epub_type,
			contenido=contenido_limpio
		)
	
	def _limpiar_caracteres_control(self, texto: str) -> str:
		"""
		Elimina caracteres de control que no son válidos en XML.
		
		Args:
			texto: Texto a limpiar
		
		Returns:
			str: Texto sin caracteres de control problemáticos
		"""
		if not texto:
			return ""
		
		# Eliminar caracteres de control excepto tab, newline y carriage return
		# Los caracteres de control 0x00-0x08, 0x0B, 0x0C, 0x0E-0x1F no son válidos en XML
		resultado = []
		for char in texto:
			code = ord(char)
			# Permitir: tab (9), newline (10), carriage return (13), y caracteres >= 32
			if code == 9 or code == 10 or code == 13 or code >= 32:
				resultado.append(char)
		
		return ''.join(resultado)
	
	def serializar(self, contenido: str) -> str:
		"""
		Serializa contenido XHTML (normaliza para almacenamiento).
		
		Args:
			contenido: Contenido XHTML
		
		Returns:
			str: Contenido serializado
		"""
		if not contenido:
			return ""
		
		# Normalizar espacios en blanco
		contenido = re.sub(r'\s+', ' ', contenido)
		contenido = re.sub(r'>\s+<', '>\n<', contenido)
		
		return contenido.strip()
	
	def deserializar(self, xhtml: str) -> str:
		"""
		Deserializa contenido XHTML (restaura formato).
		
		Args:
			xhtml: Contenido XHTML serializado
		
		Returns:
			str: Contenido deserializado
		"""
		if not xhtml:
			return ""
		
		# El contenido ya está en formato XHTML, solo limpiar
		return self.limpiar_html(xhtml)
	
	def extraer_texto_plano(self, xhtml: str) -> str:
		"""
		Extrae el texto plano de contenido XHTML.
		
		Args:
			xhtml: Contenido XHTML
		
		Returns:
			str: Texto plano sin etiquetas
		"""
		if not xhtml:
			return ""
		
		BeautifulSoup = self._obtener_beautifulsoup()
		soup = BeautifulSoup(xhtml, 'html.parser')
		return soup.get_text(separator=' ', strip=True)
	
	def es_xhtml_valido(self, contenido: str) -> bool:
		"""
		Verifica si el contenido es XHTML válido.
		
		Args:
			contenido: Contenido a verificar
		
		Returns:
			bool: True si es XHTML válido
		"""
		if not contenido:
			return False
		
		try:
			# Intentar parsear como XML
			# Envolver en un elemento raíz si no lo tiene
			if not contenido.strip().startswith('<?xml'):
				contenido = f'<root xmlns="http://www.w3.org/1999/xhtml">{contenido}</root>'
			
			ET.fromstring(contenido)
			return True
		except ET.ParseError:
			return False
