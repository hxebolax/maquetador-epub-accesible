# -*- coding: utf-8 -*-
"""
Modelos de Metadatos.
Contiene las clases para metadatos Dublin Core y de accesibilidad EPUB.
"""

from typing import List, Optional
from datetime import date
from ..utils.helpers import generar_uuid, validar_codigo_idioma
from ..utils.constantes import (
	ACCESSIBILITY_FEATURES,
	ACCESSIBILITY_HAZARDS,
	ACCESS_MODES,
	WCAG_LEVELS,
	WCAG_VERSIONS
)


class MetadatosDC:
	"""
	Metadatos Dublin Core del libro.
	
	Contiene la información bibliográfica estándar según Dublin Core.
	"""
	
	def __init__(self):
		"""Inicializa los metadatos con valores por defecto."""
		self.identificador: str = generar_uuid()
		self.titulo: str = ""
		self.idioma: str = "es"
		self.autores: List[str] = []
		self.editor: Optional[str] = None
		self.fecha: Optional[str] = None
		self.derechos: Optional[str] = None
		self.descripcion: Optional[str] = None
		self.temas: List[str] = []
	
	def agregar_autor(self, autor: str) -> None:
		"""
		Agrega un autor a la lista.
		
		Args:
			autor: Nombre del autor
		"""
		if autor and autor not in self.autores:
			self.autores.append(autor)
	
	def eliminar_autor(self, autor: str) -> bool:
		"""
		Elimina un autor de la lista.
		
		Args:
			autor: Nombre del autor a eliminar
		
		Returns:
			bool: True si se eliminó correctamente
		"""
		try:
			self.autores.remove(autor)
			return True
		except ValueError:
			return False
	
	def mover_autor(self, autor: str, direccion: int) -> bool:
		"""
		Mueve un autor arriba o abajo en la lista.
		
		Args:
			autor: Nombre del autor
			direccion: -1 para subir, 1 para bajar
		
		Returns:
			bool: True si se movió correctamente
		"""
		try:
			indice = self.autores.index(autor)
			nuevo_indice = indice + direccion
			
			if nuevo_indice < 0 or nuevo_indice >= len(self.autores):
				return False
			
			self.autores[indice], self.autores[nuevo_indice] = \
				self.autores[nuevo_indice], self.autores[indice]
			return True
		except ValueError:
			return False
	
	def agregar_tema(self, tema: str) -> None:
		"""
		Agrega un tema/etiqueta a la lista.
		
		Args:
			tema: Tema a agregar
		"""
		if tema and tema not in self.temas:
			self.temas.append(tema)
	
	def eliminar_tema(self, tema: str) -> bool:
		"""
		Elimina un tema de la lista.
		
		Args:
			tema: Tema a eliminar
		
		Returns:
			bool: True si se eliminó correctamente
		"""
		try:
			self.temas.remove(tema)
			return True
		except ValueError:
			return False
	
	def establecer_fecha_actual(self) -> None:
		"""Establece la fecha actual como fecha de publicación."""
		self.fecha = date.today().isoformat()
	
	def validar(self) -> List[str]:
		"""
		Valida los metadatos obligatorios.
		
		Returns:
			List[str]: Lista de errores encontrados (vacía si todo es válido)
		"""
		errores = []
		
		# Validar campos obligatorios
		if not self.titulo or not self.titulo.strip():
			errores.append("El título es obligatorio")
		
		if not self.idioma or not self.idioma.strip():
			errores.append("El idioma es obligatorio")
		elif not validar_codigo_idioma(self.idioma):
			errores.append(f"El código de idioma '{self.idioma}' no es válido (use formato BCP 47: es, es-ES, en-US)")
		
		if not self.identificador or not self.identificador.strip():
			errores.append("El identificador es obligatorio")
		
		return errores
	
	def es_valido(self) -> bool:
		"""
		Verifica si los metadatos son válidos.
		
		Returns:
			bool: True si no hay errores de validación
		"""
		return len(self.validar()) == 0
	
	def to_dict(self) -> dict:
		"""
		Serializa los metadatos a un diccionario.
		
		Returns:
			dict: Representación como diccionario
		"""
		return {
			'identificador': self.identificador,
			'titulo': self.titulo,
			'idioma': self.idioma,
			'autores': self.autores.copy(),
			'editor': self.editor,
			'fecha': self.fecha,
			'derechos': self.derechos,
			'descripcion': self.descripcion,
			'temas': self.temas.copy()
		}
	
	@classmethod
	def from_dict(cls, data: dict) -> 'MetadatosDC':
		"""
		Crea metadatos desde un diccionario.
		
		Args:
			data: Diccionario con los datos
		
		Returns:
			MetadatosDC: Instancia de metadatos
		"""
		metadatos = cls()
		metadatos.identificador = data.get('identificador', generar_uuid())
		metadatos.titulo = data.get('titulo', '')
		metadatos.idioma = data.get('idioma', 'es')
		metadatos.autores = data.get('autores', []).copy()
		metadatos.editor = data.get('editor')
		metadatos.fecha = data.get('fecha')
		metadatos.derechos = data.get('derechos')
		metadatos.descripcion = data.get('descripcion')
		metadatos.temas = data.get('temas', []).copy()
		return metadatos
	
	def __repr__(self) -> str:
		"""Representación en texto."""
		return f"MetadatosDC(titulo='{self.titulo}', idioma='{self.idioma}')"


class MetadatosAccesibilidad:
	"""
	Metadatos de accesibilidad EPUB.
	
	Contiene la información de accesibilidad según EPUB Accessibility 1.1
	y schema.org.
	"""
	
	def __init__(self):
		"""Inicializa los metadatos de accesibilidad con valores por defecto."""
		# Modos de acceso del contenido
		self.access_mode: List[str] = ['textual']
		self.access_mode_sufficient: List[str] = ['textual']
		
		# Características de accesibilidad
		self.accessibility_feature: List[str] = [
			'tableOfContents',
			'structuralNavigation',
			'readingOrder'
		]
		
		# Peligros de accesibilidad
		self.accessibility_hazard: List[str] = ['none']
		
		# Resumen de accesibilidad
		self.accessibility_summary: str = ""
		
		# Nivel WCAG objetivo
		self.wcag_version: str = "2.1"
		self.wcag_level: str = "AA"
	
	def agregar_access_mode(self, modo: str) -> None:
		"""
		Agrega un modo de acceso.
		
		Args:
			modo: Modo de acceso (textual, visual, auditory, tactile)
		"""
		if modo in ACCESS_MODES and modo not in self.access_mode:
			self.access_mode.append(modo)
	
	def eliminar_access_mode(self, modo: str) -> bool:
		"""
		Elimina un modo de acceso.
		
		Args:
			modo: Modo a eliminar
		
		Returns:
			bool: True si se eliminó
		"""
		try:
			self.access_mode.remove(modo)
			return True
		except ValueError:
			return False
	
	def agregar_feature(self, feature: str) -> None:
		"""
		Agrega una característica de accesibilidad.
		
		Args:
			feature: Característica a agregar
		"""
		if feature in ACCESSIBILITY_FEATURES and feature not in self.accessibility_feature:
			self.accessibility_feature.append(feature)
	
	def eliminar_feature(self, feature: str) -> bool:
		"""
		Elimina una característica de accesibilidad.
		
		Args:
			feature: Característica a eliminar
		
		Returns:
			bool: True si se eliminó
		"""
		try:
			self.accessibility_feature.remove(feature)
			return True
		except ValueError:
			return False
	
	def establecer_hazard(self, hazards: List[str]) -> None:
		"""
		Establece los peligros de accesibilidad.
		
		Args:
			hazards: Lista de peligros
		"""
		self.accessibility_hazard = [
			h for h in hazards if h in ACCESSIBILITY_HAZARDS
		]
		if not self.accessibility_hazard:
			self.accessibility_hazard = ['none']
	
	def establecer_wcag(self, version: str, nivel: str) -> None:
		"""
		Establece el nivel WCAG objetivo.
		
		Args:
			version: Versión de WCAG (2.0, 2.1, 2.2)
			nivel: Nivel de conformidad (A, AA, AAA)
		"""
		if version in WCAG_VERSIONS:
			self.wcag_version = version
		if nivel in WCAG_LEVELS:
			self.wcag_level = nivel
	
	def obtener_conformance_url(self) -> str:
		"""
		Obtiene la URL de conformidad WCAG.
		
		Returns:
			str: URL de conformidad
		"""
		return f"http://www.w3.org/WAI/WCAG{self.wcag_version.replace('.', '')}/" \
			   f"{self.wcag_level.lower()}-conformance"
	
	def to_dict(self) -> dict:
		"""
		Serializa los metadatos a un diccionario.
		
		Returns:
			dict: Representación como diccionario
		"""
		return {
			'access_mode': self.access_mode.copy(),
			'access_mode_sufficient': self.access_mode_sufficient.copy(),
			'accessibility_feature': self.accessibility_feature.copy(),
			'accessibility_hazard': self.accessibility_hazard.copy(),
			'accessibility_summary': self.accessibility_summary,
			'wcag_version': self.wcag_version,
			'wcag_level': self.wcag_level
		}
	
	@classmethod
	def from_dict(cls, data: dict) -> 'MetadatosAccesibilidad':
		"""
		Crea metadatos desde un diccionario.
		
		Args:
			data: Diccionario con los datos
		
		Returns:
			MetadatosAccesibilidad: Instancia de metadatos
		"""
		metadatos = cls()
		metadatos.access_mode = data.get('access_mode', ['textual']).copy()
		metadatos.access_mode_sufficient = data.get(
			'access_mode_sufficient', ['textual']
		).copy()
		metadatos.accessibility_feature = data.get(
			'accessibility_feature', []
		).copy()
		metadatos.accessibility_hazard = data.get(
			'accessibility_hazard', ['none']
		).copy()
		metadatos.accessibility_summary = data.get('accessibility_summary', '')
		metadatos.wcag_version = data.get('wcag_version', '2.1')
		metadatos.wcag_level = data.get('wcag_level', 'AA')
		return metadatos
	
	def __repr__(self) -> str:
		"""Representación en texto."""
		return f"MetadatosAccesibilidad(WCAG {self.wcag_version} {self.wcag_level})"
