# -*- coding: utf-8 -*-
"""
Modelo de Sección.
Representa una sección del libro (capítulo, prólogo, anexo, etc.).
"""

from enum import Enum
from typing import List, Optional
from ..utils.helpers import generar_id_seccion


class TipoSeccion(Enum):
	"""
	Tipos de sección disponibles para el libro.
	El valor corresponde al epub:type de EPUB 3.
	"""
	PORTADA = "cover"
	CONTRAPORTADA = "backmatter"
	SINOPSIS = "abstract"
	PROLOGO = "foreword"
	EPILOGO = "afterword"
	DEDICATORIA = "dedication"
	AGRADECIMIENTOS = "acknowledgments"
	INDICE = "toc"
	CAPITULO = "chapter"
	ANEXO = "appendix"
	COLOFON = "colophon"
	PREFACIO = "preface"
	INTRODUCCION = "introduction"
	BIBLIOGRAFIA = "bibliography"
	GLOSARIO = "glossary"
	
	@classmethod
	def obtener_nombre_legible(cls, tipo: 'TipoSeccion') -> str:
		"""
		Obtiene el nombre legible en español del tipo de sección.
		
		Args:
			tipo: Tipo de sección
		
		Returns:
			str: Nombre en español
		"""
		nombres = {
			cls.PORTADA: "Portada",
			cls.CONTRAPORTADA: "Contraportada",
			cls.SINOPSIS: "Sinopsis",
			cls.PROLOGO: "Prólogo",
			cls.EPILOGO: "Epílogo",
			cls.DEDICATORIA: "Dedicatoria",
			cls.AGRADECIMIENTOS: "Agradecimientos",
			cls.INDICE: "Índice",
			cls.CAPITULO: "Capítulo",
			cls.ANEXO: "Anexo",
			cls.COLOFON: "Colofón",
			cls.PREFACIO: "Prefacio",
			cls.INTRODUCCION: "Introducción",
			cls.BIBLIOGRAFIA: "Bibliografía",
			cls.GLOSARIO: "Glosario"
		}
		return nombres.get(tipo, tipo.value)


class Seccion:
	"""
	Representa una sección del libro.
	
	Una sección puede ser un capítulo, prólogo, anexo, etc.
	Contiene el contenido en formato XHTML y metadatos asociados.
	"""
	
	def __init__(
		self,
		tipo: TipoSeccion = TipoSeccion.CAPITULO,
		titulo: str = "",
		contenido_xhtml: str = ""
	):
		"""
		Inicializa una nueva sección.
		
		Args:
			tipo: Tipo de sección
			titulo: Título de la sección
			contenido_xhtml: Contenido en formato XHTML
		"""
		self.id: str = generar_id_seccion()
		self.titulo: str = titulo
		self.tipo: TipoSeccion = tipo
		self.epub_type: str = tipo.value
		self.contenido_xhtml: str = contenido_xhtml
		self.nivel_encabezado: int = 1
		self.imagenes: List = []  # Lista de Imagen
	
	def establecer_tipo(self, tipo: TipoSeccion) -> None:
		"""
		Establece el tipo de sección y actualiza el epub:type.
		
		Args:
			tipo: Nuevo tipo de sección
		"""
		self.tipo = tipo
		self.epub_type = tipo.value
	
	def establecer_epub_type(self, epub_type: str) -> None:
		"""
		Establece un epub:type personalizado.
		
		Args:
			epub_type: Valor de epub:type
		"""
		self.epub_type = epub_type
	
	def establecer_contenido(self, contenido: str) -> None:
		"""
		Establece el contenido XHTML de la sección.
		
		Args:
			contenido: Contenido en formato XHTML
		"""
		self.contenido_xhtml = contenido
	
	def establecer_titulo(self, titulo: str) -> None:
		"""
		Establece el título de la sección.
		
		Args:
			titulo: Nuevo título
		"""
		self.titulo = titulo
	
	def agregar_imagen(self, imagen) -> None:
		"""
		Agrega una imagen a la sección.
		
		Args:
			imagen: Imagen a agregar
		"""
		self.imagenes.append(imagen)
	
	def eliminar_imagen(self, imagen) -> bool:
		"""
		Elimina una imagen de la sección.
		
		Args:
			imagen: Imagen a eliminar
		
		Returns:
			bool: True si se eliminó correctamente
		"""
		try:
			self.imagenes.remove(imagen)
			return True
		except ValueError:
			return False
	
	def obtener_nombre_archivo(self) -> str:
		"""
		Genera un nombre de archivo para esta sección.
		
		Returns:
			str: Nombre de archivo sin extensión
		"""
		from ..utils.helpers import sanitizar_nombre_archivo
		
		# Usar el ID para garantizar unicidad
		base = sanitizar_nombre_archivo(self.titulo) if self.titulo else self.tipo.value
		return f"{base}-{self.id[-8:]}"
	
	def obtener_nombre_legible(self) -> str:
		"""
		Obtiene una representación legible de la sección.
		
		Returns:
			str: Nombre legible (tipo + título)
		"""
		tipo_nombre = TipoSeccion.obtener_nombre_legible(self.tipo)
		if self.titulo:
			return f"{tipo_nombre}: {self.titulo}"
		return tipo_nombre
	
	def to_dict(self) -> dict:
		"""
		Serializa la sección a un diccionario.
		
		Returns:
			dict: Representación de la sección como diccionario
		"""
		return {
			'id': self.id,
			'titulo': self.titulo,
			'tipo': self.tipo.value,
			'epub_type': self.epub_type,
			'contenido_xhtml': self.contenido_xhtml,
			'nivel_encabezado': self.nivel_encabezado,
			'imagenes': [img.to_dict() for img in self.imagenes]
		}
	
	@classmethod
	def from_dict(cls, data: dict) -> 'Seccion':
		"""
		Crea una sección desde un diccionario.
		
		Args:
			data: Diccionario con los datos de la sección
		
		Returns:
			Seccion: Instancia de la sección
		"""
		# Importación diferida para evitar ciclos
		from .imagen import Imagen
		
		# Obtener el tipo de sección
		tipo_valor = data.get('tipo', 'chapter')
		try:
			tipo = TipoSeccion(tipo_valor)
		except ValueError:
			tipo = TipoSeccion.CAPITULO
		
		seccion = cls(
			tipo=tipo,
			titulo=data.get('titulo', ''),
			contenido_xhtml=data.get('contenido_xhtml', '')
		)
		
		# Restaurar ID original si existe
		if 'id' in data:
			seccion.id = data['id']
		
		seccion.epub_type = data.get('epub_type', tipo.value)
		seccion.nivel_encabezado = data.get('nivel_encabezado', 1)
		
		# Cargar imágenes
		seccion.imagenes = [
			Imagen.from_dict(img) for img in data.get('imagenes', [])
		]
		
		return seccion
	
	def __repr__(self) -> str:
		"""Representación en texto de la sección."""
		return f"Seccion('{self.titulo}', tipo={self.tipo.value})"
	
	def __eq__(self, other) -> bool:
		"""Compara dos secciones por su ID."""
		if not isinstance(other, Seccion):
			return False
		return self.id == other.id
