# -*- coding: utf-8 -*-
"""
Modelo de Preferencias.
Gestiona las preferencias de usuario de la aplicación.
"""

import json
import os
from typing import Optional


class Preferencias:
	"""
	Preferencias de la aplicación.
	
	Almacena configuraciones del usuario como directorios por defecto
	y opciones de comportamiento.
	"""
	
	# Nombre del archivo de preferencias
	NOMBRE_ARCHIVO = "preferencias.json"
	
	def __init__(self):
		"""Inicializa las preferencias con valores por defecto."""
		# Directorios por defecto
		self.directorio_importacion: str = ""
		self.directorio_exportacion: str = ""
		self.directorio_proyectos: str = ""
		
		# Opciones de comportamiento
		self.guardado_automatico: bool = False
		self.intervalo_guardado: int = 300  # segundos (5 minutos)
		
		# Opciones de interfaz
		self.confirmar_eliminacion: bool = True
		self.mostrar_panel_logs: bool = True
		
		# Último proyecto abierto
		self.ultimo_proyecto: Optional[str] = None
		
		# Proyectos recientes
		self.proyectos_recientes: list = []
		self.max_proyectos_recientes: int = 10
	
	def establecer_directorio_importacion(self, ruta: str) -> None:
		"""
		Establece el directorio por defecto para importación.
		
		Args:
			ruta: Ruta del directorio
		"""
		if os.path.isdir(ruta):
			self.directorio_importacion = ruta
	
	def establecer_directorio_exportacion(self, ruta: str) -> None:
		"""
		Establece el directorio por defecto para exportación.
		
		Args:
			ruta: Ruta del directorio
		"""
		if os.path.isdir(ruta):
			self.directorio_exportacion = ruta
	
	def establecer_directorio_proyectos(self, ruta: str) -> None:
		"""
		Establece el directorio por defecto para proyectos.
		
		Args:
			ruta: Ruta del directorio
		"""
		if os.path.isdir(ruta):
			self.directorio_proyectos = ruta
	
	def activar_guardado_automatico(self, intervalo: int = 300) -> None:
		"""
		Activa el guardado automático.
		
		Args:
			intervalo: Intervalo en segundos entre guardados
		"""
		self.guardado_automatico = True
		self.intervalo_guardado = max(60, intervalo)  # Mínimo 1 minuto
	
	def desactivar_guardado_automatico(self) -> None:
		"""Desactiva el guardado automático."""
		self.guardado_automatico = False
	
	def agregar_proyecto_reciente(self, ruta: str) -> None:
		"""
		Agrega un proyecto a la lista de recientes.
		
		Args:
			ruta: Ruta del proyecto
		"""
		# Eliminar si ya existe para moverlo al principio
		if ruta in self.proyectos_recientes:
			self.proyectos_recientes.remove(ruta)
		
		# Agregar al principio
		self.proyectos_recientes.insert(0, ruta)
		
		# Limitar la lista
		self.proyectos_recientes = self.proyectos_recientes[:self.max_proyectos_recientes]
		
		# Actualizar último proyecto
		self.ultimo_proyecto = ruta
	
	def limpiar_proyectos_recientes(self) -> None:
		"""Limpia la lista de proyectos recientes."""
		self.proyectos_recientes = []
		self.ultimo_proyecto = None
	
	def obtener_directorio_inicial(self, tipo: str = "proyectos") -> str:
		"""
		Obtiene el directorio inicial para un diálogo de archivo.
		
		Args:
			tipo: Tipo de directorio (proyectos, importacion, exportacion)
		
		Returns:
			str: Ruta del directorio o directorio de usuario
		"""
		directorios = {
			'proyectos': self.directorio_proyectos,
			'importacion': self.directorio_importacion,
			'exportacion': self.directorio_exportacion
		}
		
		directorio = directorios.get(tipo, "")
		
		if directorio and os.path.isdir(directorio):
			return directorio
		
		# Fallback al directorio de documentos del usuario
		return os.path.expanduser("~")
	
	def to_dict(self) -> dict:
		"""
		Serializa las preferencias a un diccionario.
		
		Returns:
			dict: Representación como diccionario
		"""
		return {
			'directorio_importacion': self.directorio_importacion,
			'directorio_exportacion': self.directorio_exportacion,
			'directorio_proyectos': self.directorio_proyectos,
			'guardado_automatico': self.guardado_automatico,
			'intervalo_guardado': self.intervalo_guardado,
			'confirmar_eliminacion': self.confirmar_eliminacion,
			'mostrar_panel_logs': self.mostrar_panel_logs,
			'ultimo_proyecto': self.ultimo_proyecto,
			'proyectos_recientes': self.proyectos_recientes.copy(),
			'max_proyectos_recientes': self.max_proyectos_recientes
		}
	
	@classmethod
	def from_dict(cls, data: dict) -> 'Preferencias':
		"""
		Crea preferencias desde un diccionario.
		
		Args:
			data: Diccionario con los datos
		
		Returns:
			Preferencias: Instancia de preferencias
		"""
		prefs = cls()
		prefs.directorio_importacion = data.get('directorio_importacion', '')
		prefs.directorio_exportacion = data.get('directorio_exportacion', '')
		prefs.directorio_proyectos = data.get('directorio_proyectos', '')
		prefs.guardado_automatico = data.get('guardado_automatico', False)
		prefs.intervalo_guardado = data.get('intervalo_guardado', 300)
		prefs.confirmar_eliminacion = data.get('confirmar_eliminacion', True)
		prefs.mostrar_panel_logs = data.get('mostrar_panel_logs', True)
		prefs.ultimo_proyecto = data.get('ultimo_proyecto')
		prefs.proyectos_recientes = data.get('proyectos_recientes', []).copy()
		prefs.max_proyectos_recientes = data.get('max_proyectos_recientes', 10)
		return prefs
	
	def guardar(self, ruta: Optional[str] = None) -> bool:
		"""
		Guarda las preferencias en un archivo JSON.
		
		Args:
			ruta: Ruta del archivo (opcional, usa ubicación por defecto)
		
		Returns:
			bool: True si se guardó correctamente
		"""
		if ruta is None:
			ruta = self._obtener_ruta_preferencias()
		
		try:
			# Crear directorio si no existe
			directorio = os.path.dirname(ruta)
			if directorio and not os.path.exists(directorio):
				os.makedirs(directorio)
			
			with open(ruta, 'w', encoding='utf-8') as f:
				json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
			return True
		except (IOError, OSError) as e:
			print(f"Error al guardar preferencias: {e}")
			return False
	
	@classmethod
	def cargar(cls, ruta: Optional[str] = None) -> 'Preferencias':
		"""
		Carga las preferencias desde un archivo JSON.
		
		Args:
			ruta: Ruta del archivo (opcional, usa ubicación por defecto)
		
		Returns:
			Preferencias: Instancia de preferencias (por defecto si hay error)
		"""
		if ruta is None:
			ruta = cls._obtener_ruta_preferencias_estatica()
		
		try:
			if os.path.exists(ruta):
				with open(ruta, 'r', encoding='utf-8') as f:
					data = json.load(f)
				return cls.from_dict(data)
		except (IOError, OSError, json.JSONDecodeError) as e:
			print(f"Error al cargar preferencias: {e}")
		
		return cls()
	
	def _obtener_ruta_preferencias(self) -> str:
		"""
		Obtiene la ruta del archivo de preferencias.
		
		Returns:
			str: Ruta completa del archivo
		"""
		return self._obtener_ruta_preferencias_estatica()
	
	@staticmethod
	def _obtener_ruta_preferencias_estatica() -> str:
		"""
		Obtiene la ruta del archivo de preferencias (método estático).
		
		Returns:
			str: Ruta completa del archivo
		"""
		# Usar directorio de configuración del usuario
		if os.name == 'nt':  # Windows
			base = os.environ.get('APPDATA', os.path.expanduser('~'))
		else:  # Linux/Mac
			base = os.path.expanduser('~/.config')
		
		directorio = os.path.join(base, 'MaquetadorEPUB')
		return os.path.join(directorio, Preferencias.NOMBRE_ARCHIVO)
	
	def __repr__(self) -> str:
		"""Representación en texto."""
		return f"Preferencias(guardado_auto={self.guardado_automatico})"
