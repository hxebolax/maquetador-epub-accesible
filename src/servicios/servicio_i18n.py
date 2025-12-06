# -*- coding: utf-8 -*-
"""
Servicio de Internacionalización (i18n).
Gestiona las traducciones de la interfaz de usuario.
"""

import json
import locale
import os
from typing import Dict, List, Optional, Tuple


class ServicioI18n:
	"""
	Servicio de internacionalización.
	
	Gestiona la carga de traducciones y proporciona métodos
	para obtener textos traducidos.
	"""
	
	# Idiomas soportados: código -> nombre
	IDIOMAS_SOPORTADOS = {
		'es': 'Español',
		'en': 'English',
		'fr': 'Français',
		'pt': 'Português',
		'ca': 'Català'
	}
	
	# Idioma por defecto
	IDIOMA_DEFECTO = 'es'
	
	# Instancia singleton
	_instancia: Optional['ServicioI18n'] = None
	
	def __new__(cls):
		"""Implementa patrón singleton."""
		if cls._instancia is None:
			cls._instancia = super().__new__(cls)
			cls._instancia._inicializado = False
		return cls._instancia
	
	def __init__(self):
		"""Inicializa el servicio de i18n."""
		if self._inicializado:
			return
		
		self._idioma_actual: str = self.IDIOMA_DEFECTO
		self._traducciones: Dict[str, str] = {}
		self._traducciones_defecto: Dict[str, str] = {}
		self._ruta_locales: str = self._obtener_ruta_locales()
		
		# Cargar traducciones por defecto (español)
		self._cargar_traducciones_defecto()
		
		self._inicializado = True
	
	def _obtener_ruta_locales(self) -> str:
		"""Obtiene la ruta a la carpeta de locales."""
		# Obtener directorio del módulo actual
		dir_actual = os.path.dirname(os.path.abspath(__file__))
		# Subir un nivel y entrar a locales
		return os.path.join(os.path.dirname(dir_actual), 'locales')
	
	def _cargar_traducciones_defecto(self) -> None:
		"""Carga las traducciones del idioma por defecto."""
		ruta = os.path.join(self._ruta_locales, f'{self.IDIOMA_DEFECTO}.json')
		if os.path.exists(ruta):
			try:
				with open(ruta, 'r', encoding='utf-8') as f:
					self._traducciones_defecto = json.load(f)
			except (json.JSONDecodeError, IOError):
				self._traducciones_defecto = {}
	
	def cargar_idioma(self, codigo: str) -> bool:
		"""
		Carga un idioma específico.
		
		Args:
			codigo: Código del idioma (es, en, fr, pt, ca)
		
		Returns:
			bool: True si se cargó correctamente
		"""
		if codigo not in self.IDIOMAS_SOPORTADOS:
			return False
		
		ruta = os.path.join(self._ruta_locales, f'{codigo}.json')
		
		if not os.path.exists(ruta):
			# Si no existe el archivo, usar idioma por defecto
			if codigo != self.IDIOMA_DEFECTO:
				self._traducciones = self._traducciones_defecto.copy()
				self._idioma_actual = codigo
				return True
			return False
		
		try:
			with open(ruta, 'r', encoding='utf-8') as f:
				self._traducciones = json.load(f)
			self._idioma_actual = codigo
			return True
		except (json.JSONDecodeError, IOError):
			return False
	
	def obtener_texto(self, clave: str, **kwargs) -> str:
		"""
		Obtiene el texto traducido para una clave.
		
		Args:
			clave: Clave de traducción (ej: "menu.file.new")
			**kwargs: Variables para interpolación
		
		Returns:
			str: Texto traducido o clave si no existe
		"""
		# Buscar en traducciones actuales
		texto = self._traducciones.get(clave)
		
		# Si no existe, buscar en traducciones por defecto
		if texto is None:
			texto = self._traducciones_defecto.get(clave)
		
		# Si tampoco existe, devolver la clave
		if texto is None:
			return clave
		
		# Interpolar variables si las hay
		if kwargs:
			try:
				texto = texto.format(**kwargs)
			except KeyError:
				pass
		
		return texto
	
	def _(self, clave: str, **kwargs) -> str:
		"""
		Alias corto para obtener_texto.
		
		Args:
			clave: Clave de traducción
			**kwargs: Variables para interpolación
		
		Returns:
			str: Texto traducido
		"""
		return self.obtener_texto(clave, **kwargs)
	
	def obtener_idioma_actual(self) -> str:
		"""
		Obtiene el código del idioma actual.
		
		Returns:
			str: Código del idioma
		"""
		return self._idioma_actual
	
	def obtener_idiomas_disponibles(self) -> List[Tuple[str, str]]:
		"""
		Obtiene la lista de idiomas disponibles.
		
		Returns:
			List[Tuple[str, str]]: Lista de (código, nombre)
		"""
		return [(codigo, nombre) for codigo, nombre in self.IDIOMAS_SOPORTADOS.items()]
	
	def detectar_idioma_sistema(self) -> str:
		"""
		Detecta el idioma del sistema operativo.
		
		Returns:
			str: Código del idioma detectado o idioma por defecto
		"""
		try:
			# Obtener locale del sistema
			idioma_sistema, _ = locale.getdefaultlocale()
			
			if idioma_sistema:
				# Extraer código de idioma (primeros 2 caracteres)
				codigo = idioma_sistema[:2].lower()
				
				if codigo in self.IDIOMAS_SOPORTADOS:
					return codigo
		except Exception:
			pass
		
		return self.IDIOMA_DEFECTO
	
	def tiene_traduccion(self, clave: str) -> bool:
		"""
		Verifica si existe traducción para una clave.
		
		Args:
			clave: Clave de traducción
		
		Returns:
			bool: True si existe traducción
		"""
		return clave in self._traducciones or clave in self._traducciones_defecto


# Función de conveniencia global
def _(clave: str, **kwargs) -> str:
	"""
	Función global de traducción.
	
	Args:
		clave: Clave de traducción
		**kwargs: Variables para interpolación
	
	Returns:
		str: Texto traducido
	"""
	return ServicioI18n().obtener_texto(clave, **kwargs)
