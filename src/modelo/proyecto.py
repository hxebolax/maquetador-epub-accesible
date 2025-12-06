# -*- coding: utf-8 -*-
"""
Modelo de Proyecto.
Representa un proyecto de libro completo con todas sus secciones y metadatos.
"""

from typing import List, Optional
from .seccion import Seccion, TipoSeccion
from .metadatos import MetadatosDC, MetadatosAccesibilidad
from .imagen import Imagen
from ..utils.helpers import generar_uuid
from ..utils.constantes import VERSION_FORMATO_PROYECTO


class Proyecto:
	"""
	Representa un proyecto de libro completo.
	
	Contiene toda la información necesaria para generar un EPUB:
	metadatos, secciones, portada y configuración de accesibilidad.
	"""
	
	def __init__(self):
		"""Inicializa un proyecto vacío con valores por defecto."""
		self.version = VERSION_FORMATO_PROYECTO
		self.ruta_archivo: Optional[str] = None
		self.modificado: bool = False
		
		# Metadatos del libro
		self.metadatos = MetadatosDC()
		self.metadatos_accesibilidad = MetadatosAccesibilidad()
		
		# Contenido del libro
		self.secciones: List[Seccion] = []
		self.portada: Optional[Imagen] = None
	
	def agregar_seccion(self, tipo: TipoSeccion, titulo: str) -> Seccion:
		"""
		Agrega una nueva sección al libro.
		
		Args:
			tipo: Tipo de sección (capítulo, prólogo, etc.)
			titulo: Título de la sección
		
		Returns:
			Seccion: La sección creada y agregada
		"""
		seccion = Seccion(tipo=tipo, titulo=titulo)
		self.secciones.append(seccion)
		self.modificado = True
		return seccion
	
	def eliminar_seccion(self, seccion: Seccion) -> bool:
		"""
		Elimina una sección del libro.
		
		Args:
			seccion: Sección a eliminar
		
		Returns:
			bool: True si se eliminó correctamente, False si no se encontró
		"""
		try:
			self.secciones.remove(seccion)
			self.modificado = True
			return True
		except ValueError:
			return False
	
	def eliminar_seccion_por_id(self, id_seccion: str) -> bool:
		"""
		Elimina una sección por su ID.
		
		Args:
			id_seccion: ID de la sección a eliminar
		
		Returns:
			bool: True si se eliminó correctamente
		"""
		for seccion in self.secciones:
			if seccion.id == id_seccion:
				return self.eliminar_seccion(seccion)
		return False
	
	def obtener_seccion_por_id(self, id_seccion: str) -> Optional[Seccion]:
		"""
		Busca una sección por su ID.
		
		Args:
			id_seccion: ID de la sección a buscar
		
		Returns:
			Seccion o None si no se encuentra
		"""
		for seccion in self.secciones:
			if seccion.id == id_seccion:
				return seccion
		return None
	
	def mover_seccion(self, seccion: Seccion, direccion: int) -> bool:
		"""
		Mueve una sección arriba o abajo en la lista.
		
		Args:
			seccion: Sección a mover
			direccion: -1 para subir, 1 para bajar
		
		Returns:
			bool: True si se movió correctamente
		"""
		try:
			indice_actual = self.secciones.index(seccion)
			nuevo_indice = indice_actual + direccion
			
			# Verificar límites
			if nuevo_indice < 0 or nuevo_indice >= len(self.secciones):
				return False
			
			# Intercambiar posiciones
			self.secciones[indice_actual], self.secciones[nuevo_indice] = \
				self.secciones[nuevo_indice], self.secciones[indice_actual]
			
			self.modificado = True
			return True
		except ValueError:
			return False
	
	def mover_seccion_arriba(self, seccion: Seccion) -> bool:
		"""Mueve una sección una posición hacia arriba."""
		return self.mover_seccion(seccion, -1)
	
	def mover_seccion_abajo(self, seccion: Seccion) -> bool:
		"""Mueve una sección una posición hacia abajo."""
		return self.mover_seccion(seccion, 1)
	
	def establecer_portada(self, imagen: Imagen) -> None:
		"""
		Establece la imagen de portada del libro.
		
		Args:
			imagen: Imagen a usar como portada
		"""
		imagen.es_portada = True
		self.portada = imagen
		self.modificado = True
	
	def marcar_modificado(self) -> None:
		"""Marca el proyecto como modificado."""
		self.modificado = True
	
	def marcar_guardado(self) -> None:
		"""Marca el proyecto como guardado (sin modificaciones pendientes)."""
		self.modificado = False
	
	def to_dict(self) -> dict:
		"""
		Serializa el proyecto a un diccionario.
		
		Returns:
			dict: Representación del proyecto como diccionario
		"""
		return {
			'version': self.version,
			'metadatos': self.metadatos.to_dict(),
			'accesibilidad': self.metadatos_accesibilidad.to_dict(),
			'portada': self.portada.to_dict() if self.portada else None,
			'secciones': [s.to_dict() for s in self.secciones]
		}
	
	@classmethod
	def from_dict(cls, data: dict) -> 'Proyecto':
		"""
		Crea un proyecto desde un diccionario.
		
		Args:
			data: Diccionario con los datos del proyecto
		
		Returns:
			Proyecto: Instancia del proyecto
		"""
		proyecto = cls()
		proyecto.version = data.get('version', VERSION_FORMATO_PROYECTO)
		
		# Cargar metadatos
		if 'metadatos' in data:
			proyecto.metadatos = MetadatosDC.from_dict(data['metadatos'])
		
		if 'accesibilidad' in data:
			proyecto.metadatos_accesibilidad = MetadatosAccesibilidad.from_dict(
				data['accesibilidad']
			)
		
		# Cargar portada
		if data.get('portada'):
			proyecto.portada = Imagen.from_dict(data['portada'])
		
		# Cargar secciones
		proyecto.secciones = [
			Seccion.from_dict(s) for s in data.get('secciones', [])
		]
		
		proyecto.modificado = False
		return proyecto
	
	def __repr__(self) -> str:
		"""Representación en texto del proyecto."""
		titulo = self.metadatos.titulo or "Sin título"
		num_secciones = len(self.secciones)
		return f"Proyecto('{titulo}', {num_secciones} secciones)"
