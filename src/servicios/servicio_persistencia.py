# -*- coding: utf-8 -*-
"""
Servicio de Persistencia.
Gestiona el guardado y carga de proyectos en formato JSON.
"""

import json
import os
from typing import Optional
from ..modelo.proyecto import Proyecto


class ErrorPersistencia(Exception):
	"""Excepción para errores de persistencia."""
	pass


class ServicioPersistencia:
	"""
	Servicio para guardar y cargar proyectos.
	
	Maneja la serialización y deserialización de proyectos
	en formato JSON.
	"""
	
	# Extensión de archivo de proyecto
	EXTENSION = ".mepub"
	
	# Filtro para diálogos de archivo
	FILTRO_ARCHIVO = "Proyecto EPUB (*.mepub)|*.mepub|Todos los archivos (*.*)|*.*"
	
	def __init__(self):
		"""Inicializa el servicio de persistencia."""
		pass
	
	def guardar_proyecto(self, proyecto: Proyecto, ruta: str) -> None:
		"""
		Guarda un proyecto en un archivo JSON.
		
		Args:
			proyecto: Proyecto a guardar
			ruta: Ruta del archivo de destino
		
		Raises:
			ErrorPersistencia: Si hay error al guardar
		"""
		try:
			# Asegurar extensión correcta
			if not ruta.lower().endswith(self.EXTENSION):
				ruta += self.EXTENSION
			
			# Crear directorio si no existe
			directorio = os.path.dirname(ruta)
			if directorio and not os.path.exists(directorio):
				os.makedirs(directorio)
			
			# Serializar y guardar
			contenido = self.serializar_proyecto(proyecto)
			
			with open(ruta, 'w', encoding='utf-8') as f:
				f.write(contenido)
			
			# Actualizar ruta del proyecto
			proyecto.ruta_archivo = ruta
			proyecto.marcar_guardado()
			
		except (IOError, OSError) as e:
			raise ErrorPersistencia(f"Error al guardar el proyecto: {e}")
		except Exception as e:
			raise ErrorPersistencia(f"Error inesperado al guardar: {e}")
	
	def cargar_proyecto(self, ruta: str) -> Proyecto:
		"""
		Carga un proyecto desde un archivo JSON.
		
		Args:
			ruta: Ruta del archivo a cargar
		
		Returns:
			Proyecto: Proyecto cargado
		
		Raises:
			ErrorPersistencia: Si hay error al cargar
		"""
		try:
			if not os.path.exists(ruta):
				raise ErrorPersistencia(f"El archivo no existe: {ruta}")
			
			with open(ruta, 'r', encoding='utf-8') as f:
				contenido = f.read()
			
			proyecto = self.deserializar_proyecto(contenido)
			proyecto.ruta_archivo = ruta
			proyecto.marcar_guardado()
			
			return proyecto
			
		except json.JSONDecodeError as e:
			raise ErrorPersistencia(f"El archivo no tiene formato válido: {e}")
		except (IOError, OSError) as e:
			raise ErrorPersistencia(f"Error al leer el archivo: {e}")
		except Exception as e:
			raise ErrorPersistencia(f"Error inesperado al cargar: {e}")
	
	def serializar_proyecto(self, proyecto: Proyecto) -> str:
		"""
		Serializa un proyecto a JSON.
		
		Args:
			proyecto: Proyecto a serializar
		
		Returns:
			str: Contenido JSON del proyecto
		"""
		data = proyecto.to_dict()
		return json.dumps(data, indent=2, ensure_ascii=False)
	
	def deserializar_proyecto(self, json_str: str) -> Proyecto:
		"""
		Deserializa un proyecto desde JSON.
		
		Args:
			json_str: Contenido JSON del proyecto
		
		Returns:
			Proyecto: Proyecto deserializado
		
		Raises:
			ErrorPersistencia: Si el JSON no es válido
		"""
		try:
			data = json.loads(json_str)
			return Proyecto.from_dict(data)
		except json.JSONDecodeError as e:
			raise ErrorPersistencia(f"JSON no válido: {e}")
		except Exception as e:
			raise ErrorPersistencia(f"Error al deserializar proyecto: {e}")
	
	def existe_proyecto(self, ruta: str) -> bool:
		"""
		Verifica si existe un archivo de proyecto.
		
		Args:
			ruta: Ruta a verificar
		
		Returns:
			bool: True si el archivo existe
		"""
		return os.path.isfile(ruta)
	
	def obtener_nombre_proyecto(self, ruta: str) -> str:
		"""
		Obtiene el nombre del proyecto desde la ruta.
		
		Args:
			ruta: Ruta del archivo
		
		Returns:
			str: Nombre del proyecto sin extensión
		"""
		nombre = os.path.basename(ruta)
		if nombre.lower().endswith(self.EXTENSION):
			nombre = nombre[:-len(self.EXTENSION)]
		return nombre
	
	def crear_copia_seguridad(self, ruta: str) -> Optional[str]:
		"""
		Crea una copia de seguridad del proyecto.
		
		Args:
			ruta: Ruta del archivo original
		
		Returns:
			str: Ruta de la copia de seguridad o None si falla
		"""
		try:
			if not os.path.exists(ruta):
				return None
			
			# Crear nombre de copia de seguridad
			ruta_backup = ruta + ".bak"
			
			# Copiar archivo
			with open(ruta, 'r', encoding='utf-8') as f:
				contenido = f.read()
			
			with open(ruta_backup, 'w', encoding='utf-8') as f:
				f.write(contenido)
			
			return ruta_backup
			
		except Exception:
			return None
	
	def restaurar_copia_seguridad(self, ruta: str) -> bool:
		"""
		Restaura un proyecto desde su copia de seguridad.
		
		Args:
			ruta: Ruta del archivo original
		
		Returns:
			bool: True si se restauró correctamente
		"""
		try:
			ruta_backup = ruta + ".bak"
			
			if not os.path.exists(ruta_backup):
				return False
			
			with open(ruta_backup, 'r', encoding='utf-8') as f:
				contenido = f.read()
			
			with open(ruta, 'w', encoding='utf-8') as f:
				f.write(contenido)
			
			return True
			
		except Exception:
			return False
