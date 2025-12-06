# -*- coding: utf-8 -*-
"""
Modelo de Imagen.
Representa una imagen del libro con información de accesibilidad.
"""

from typing import List, Optional
import os
from ..utils.helpers import generar_id_imagen, obtener_extension_archivo


class Imagen:
	"""
	Representa una imagen del libro.
	
	Incluye información de accesibilidad obligatoria (texto alternativo)
	y opcional (descripción larga).
	"""
	
	# Extensiones de imagen soportadas
	EXTENSIONES_VALIDAS = ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']
	
	def __init__(
		self,
		ruta: str = "",
		texto_alternativo: str = "",
		descripcion_larga: Optional[str] = None,
		es_portada: bool = False
	):
		"""
		Inicializa una nueva imagen.
		
		Args:
			ruta: Ruta al archivo de imagen
			texto_alternativo: Texto alternativo (obligatorio para accesibilidad)
			descripcion_larga: Descripción extendida para imágenes complejas
			es_portada: Indica si es la imagen de portada
		"""
		self.id: str = generar_id_imagen()
		self.ruta: str = ruta
		self.texto_alternativo: str = texto_alternativo
		self.descripcion_larga: Optional[str] = descripcion_larga
		self.es_portada: bool = es_portada
	
	def establecer_texto_alternativo(self, texto: str) -> None:
		"""
		Establece el texto alternativo de la imagen.
		
		Args:
			texto: Texto alternativo
		"""
		self.texto_alternativo = texto
	
	def establecer_descripcion_larga(self, descripcion: str) -> None:
		"""
		Establece la descripción larga de la imagen.
		
		Args:
			descripcion: Descripción extendida
		"""
		self.descripcion_larga = descripcion if descripcion else None
	
	def tiene_descripcion_larga(self) -> bool:
		"""
		Verifica si la imagen tiene descripción larga.
		
		Returns:
			bool: True si tiene descripción larga
		"""
		return bool(self.descripcion_larga and self.descripcion_larga.strip())
	
	def obtener_extension(self) -> str:
		"""
		Obtiene la extensión del archivo de imagen.
		
		Returns:
			str: Extensión en minúsculas sin punto
		"""
		return obtener_extension_archivo(self.ruta)
	
	def obtener_tipo_mime(self) -> str:
		"""
		Obtiene el tipo MIME de la imagen.
		
		Returns:
			str: Tipo MIME (ej: image/jpeg)
		"""
		extension = self.obtener_extension()
		tipos_mime = {
			'jpg': 'image/jpeg',
			'jpeg': 'image/jpeg',
			'png': 'image/png',
			'gif': 'image/gif',
			'svg': 'image/svg+xml',
			'webp': 'image/webp'
		}
		return tipos_mime.get(extension, 'application/octet-stream')
	
	def obtener_nombre_archivo(self) -> str:
		"""
		Obtiene el nombre del archivo de imagen.
		
		Returns:
			str: Nombre del archivo sin ruta
		"""
		return os.path.basename(self.ruta) if self.ruta else ""
	
	def obtener_nombre_epub(self) -> str:
		"""
		Genera un nombre de archivo para usar dentro del EPUB.
		
		Returns:
			str: Nombre de archivo para el EPUB
		"""
		extension = self.obtener_extension()
		if self.es_portada:
			return f"portada.{extension}" if extension else "portada.jpg"
		return f"{self.id}.{extension}" if extension else f"{self.id}.jpg"
	
	def validar(self) -> List[str]:
		"""
		Valida la imagen.
		
		Returns:
			List[str]: Lista de errores (vacía si es válida)
		"""
		errores = []
		
		# El texto alternativo es obligatorio
		if not self.texto_alternativo or not self.texto_alternativo.strip():
			errores.append("El texto alternativo es obligatorio para la imagen")
		
		# Verificar que la ruta no esté vacía
		if not self.ruta or not self.ruta.strip():
			errores.append("La ruta de la imagen es obligatoria")
		
		# Verificar extensión válida
		extension = self.obtener_extension()
		if extension and extension not in self.EXTENSIONES_VALIDAS:
			errores.append(
				f"Extensión de imagen no soportada: {extension}. "
				f"Use: {', '.join(self.EXTENSIONES_VALIDAS)}"
			)
		
		return errores
	
	def es_valida(self) -> bool:
		"""
		Verifica si la imagen es válida.
		
		Returns:
			bool: True si no hay errores de validación
		"""
		return len(self.validar()) == 0
	
	def existe_archivo(self) -> bool:
		"""
		Verifica si el archivo de imagen existe.
		
		Returns:
			bool: True si el archivo existe
		"""
		return os.path.isfile(self.ruta) if self.ruta else False
	
	def to_dict(self) -> dict:
		"""
		Serializa la imagen a un diccionario.
		
		Returns:
			dict: Representación como diccionario
		"""
		return {
			'id': self.id,
			'ruta': self.ruta,
			'texto_alternativo': self.texto_alternativo,
			'descripcion_larga': self.descripcion_larga,
			'es_portada': self.es_portada
		}
	
	@classmethod
	def from_dict(cls, data: dict) -> 'Imagen':
		"""
		Crea una imagen desde un diccionario.
		
		Args:
			data: Diccionario con los datos
		
		Returns:
			Imagen: Instancia de imagen
		"""
		imagen = cls(
			ruta=data.get('ruta', ''),
			texto_alternativo=data.get('texto_alternativo', ''),
			descripcion_larga=data.get('descripcion_larga'),
			es_portada=data.get('es_portada', False)
		)
		
		# Restaurar ID original si existe
		if 'id' in data:
			imagen.id = data['id']
		
		return imagen
	
	def __repr__(self) -> str:
		"""Representación en texto."""
		nombre = self.obtener_nombre_archivo() or "sin archivo"
		return f"Imagen('{nombre}', portada={self.es_portada})"
	
	def __eq__(self, other) -> bool:
		"""Compara dos imágenes por su ID."""
		if not isinstance(other, Imagen):
			return False
		return self.id == other.id
