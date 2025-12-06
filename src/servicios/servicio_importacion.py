# -*- coding: utf-8 -*-
"""
Servicio de Importación.
Gestiona la importación de contenido desde archivos externos.
"""

import os
from typing import Optional
from .servicio_xhtml import ServicioXHTML


class ErrorImportacion(Exception):
	"""Excepción para errores de importación."""
	pass


class ServicioImportacion:
	"""
	Servicio para importar contenido de archivos externos.
	
	Soporta importación de archivos TXT, Markdown y HTML,
	convirtiéndolos a XHTML válido para EPUB.
	"""
	
	# Extensiones soportadas
	EXTENSIONES_TXT = ['.txt', '.text']
	EXTENSIONES_MD = ['.md', '.markdown', '.mdown']
	EXTENSIONES_HTML = ['.html', '.htm', '.xhtml']
	
	def __init__(self):
		"""Inicializa el servicio de importación."""
		self.servicio_xhtml = ServicioXHTML()
	
	def importar_archivo(self, ruta: str) -> str:
		"""
		Importa un archivo y lo convierte a XHTML.
		
		Detecta automáticamente el tipo de archivo por su extensión.
		
		Args:
			ruta: Ruta del archivo a importar
		
		Returns:
			str: Contenido convertido a XHTML
		
		Raises:
			ErrorImportacion: Si hay error al importar
		"""
		if not os.path.exists(ruta):
			raise ErrorImportacion(f"El archivo no existe: {ruta}")
		
		extension = os.path.splitext(ruta)[1].lower()
		
		if extension in self.EXTENSIONES_TXT:
			return self.importar_txt(ruta)
		elif extension in self.EXTENSIONES_MD:
			return self.importar_markdown(ruta)
		elif extension in self.EXTENSIONES_HTML:
			return self.importar_html(ruta)
		else:
			raise ErrorImportacion(
				f"Tipo de archivo no soportado: {extension}. "
				f"Use archivos .txt, .md o .html"
			)
	
	def importar_txt(self, ruta: str) -> str:
		"""
		Importa un archivo de texto plano.
		
		Args:
			ruta: Ruta del archivo TXT
		
		Returns:
			str: Contenido convertido a XHTML
		
		Raises:
			ErrorImportacion: Si hay error al leer el archivo
		"""
		try:
			contenido = self._leer_archivo(ruta)
			return self.servicio_xhtml.txt_a_xhtml(contenido)
		except Exception as e:
			raise ErrorImportacion(f"Error al importar archivo TXT: {e}")
	
	def importar_markdown(self, ruta: str) -> str:
		"""
		Importa un archivo Markdown.
		
		Args:
			ruta: Ruta del archivo Markdown
		
		Returns:
			str: Contenido convertido a XHTML
		
		Raises:
			ErrorImportacion: Si hay error al leer o convertir
		"""
		try:
			contenido = self._leer_archivo(ruta)
			return self.servicio_xhtml.markdown_a_xhtml(contenido)
		except ImportError as e:
			raise ErrorImportacion(
				f"No se puede importar Markdown: {e}. "
				"Instale la biblioteca 'markdown' con: pip install markdown"
			)
		except Exception as e:
			raise ErrorImportacion(f"Error al importar archivo Markdown: {e}")
	
	def importar_html(self, ruta: str) -> str:
		"""
		Importa un archivo HTML.
		
		Args:
			ruta: Ruta del archivo HTML
		
		Returns:
			str: Contenido normalizado a XHTML
		
		Raises:
			ErrorImportacion: Si hay error al leer o normalizar
		"""
		try:
			contenido = self._leer_archivo(ruta)
			return self._extraer_body_html(contenido)
		except ImportError as e:
			raise ErrorImportacion(
				f"No se puede importar HTML: {e}. "
				"Instale la biblioteca 'beautifulsoup4' con: pip install beautifulsoup4 lxml"
			)
		except Exception as e:
			raise ErrorImportacion(f"Error al importar archivo HTML: {e}")
	
	def importar_texto(self, texto: str, formato: str = "txt") -> str:
		"""
		Importa texto directamente (sin archivo).
		
		Args:
			texto: Texto a importar
			formato: Formato del texto ('txt', 'md', 'html')
		
		Returns:
			str: Contenido convertido a XHTML
		"""
		formato = formato.lower()
		
		if formato in ['txt', 'text']:
			return self.servicio_xhtml.txt_a_xhtml(texto)
		elif formato in ['md', 'markdown']:
			return self.servicio_xhtml.markdown_a_xhtml(texto)
		elif formato in ['html', 'htm', 'xhtml']:
			return self._extraer_body_html(texto)
		else:
			# Por defecto, tratar como texto plano
			return self.servicio_xhtml.txt_a_xhtml(texto)
	
	def _leer_archivo(self, ruta: str) -> str:
		"""
		Lee el contenido de un archivo.
		
		Intenta detectar la codificación automáticamente.
		
		Args:
			ruta: Ruta del archivo
		
		Returns:
			str: Contenido del archivo
		
		Raises:
			ErrorImportacion: Si no se puede leer el archivo
		"""
		# Codificaciones a intentar
		codificaciones = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
		
		for codificacion in codificaciones:
			try:
				with open(ruta, 'r', encoding=codificacion) as f:
					return f.read()
			except UnicodeDecodeError:
				continue
			except (IOError, OSError) as e:
				raise ErrorImportacion(f"Error al leer el archivo: {e}")
		
		raise ErrorImportacion(
			f"No se pudo determinar la codificación del archivo: {ruta}"
		)
	
	def _extraer_body_html(self, html_content: str) -> str:
		"""
		Extrae y limpia el contenido del body de un HTML.
		
		Args:
			html_content: Contenido HTML completo
		
		Returns:
			str: Contenido del body limpio
		"""
		try:
			from bs4 import BeautifulSoup
			
			soup = BeautifulSoup(html_content, 'html.parser')
			
			# Buscar el body
			body = soup.find('body')
			
			if body:
				# Extraer contenido del body
				contenido = ''.join(str(child) for child in body.children)
			else:
				# Si no hay body, usar todo el contenido
				contenido = html_content
			
			# Limpiar y normalizar
			return self.servicio_xhtml.limpiar_html(contenido)
			
		except ImportError:
			# Si no hay BeautifulSoup, hacer limpieza básica
			return self.servicio_xhtml.limpiar_html(html_content)
	
	def obtener_titulo_sugerido(self, ruta: str) -> str:
		"""
		Sugiere un título basado en el nombre del archivo.
		
		Args:
			ruta: Ruta del archivo
		
		Returns:
			str: Título sugerido
		"""
		nombre = os.path.basename(ruta)
		nombre_sin_ext = os.path.splitext(nombre)[0]
		
		# Convertir guiones y guiones bajos a espacios
		titulo = nombre_sin_ext.replace('-', ' ').replace('_', ' ')
		
		# Capitalizar primera letra de cada palabra
		titulo = titulo.title()
		
		return titulo
	
	def detectar_tipo_archivo(self, ruta: str) -> Optional[str]:
		"""
		Detecta el tipo de archivo por su extensión.
		
		Args:
			ruta: Ruta del archivo
		
		Returns:
			str: Tipo de archivo ('txt', 'md', 'html') o None si no es soportado
		"""
		extension = os.path.splitext(ruta)[1].lower()
		
		if extension in self.EXTENSIONES_TXT:
			return 'txt'
		elif extension in self.EXTENSIONES_MD:
			return 'md'
		elif extension in self.EXTENSIONES_HTML:
			return 'html'
		
		return None
	
	def es_archivo_soportado(self, ruta: str) -> bool:
		"""
		Verifica si un archivo tiene una extensión soportada.
		
		Args:
			ruta: Ruta del archivo
		
		Returns:
			bool: True si el archivo es soportado
		"""
		return self.detectar_tipo_archivo(ruta) is not None
	
	def obtener_filtro_archivos(self) -> str:
		"""
		Obtiene el filtro de archivos para diálogos de selección.
		
		Returns:
			str: Filtro en formato wxPython
		"""
		return (
			"Todos los soportados (*.txt;*.md;*.html)|*.txt;*.md;*.markdown;*.html;*.htm|"
			"Archivos de texto (*.txt)|*.txt|"
			"Archivos Markdown (*.md)|*.md;*.markdown|"
			"Archivos HTML (*.html)|*.html;*.htm|"
			"Todos los archivos (*.*)|*.*"
		)
