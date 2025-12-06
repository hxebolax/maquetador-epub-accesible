# -*- coding: utf-8 -*-
"""
Servicio de Validación.
Gestiona la validación de proyectos y archivos EPUB.
"""

import os
import subprocess
import shutil
from typing import List, Optional, Tuple
from dataclasses import dataclass, field

from ..modelo.proyecto import Proyecto
from ..modelo.seccion import TipoSeccion


@dataclass
class ResultadoValidacion:
	"""Resultado de una validación."""
	exito: bool
	herramienta: str
	errores: List[str] = field(default_factory=list)
	advertencias: List[str] = field(default_factory=list)
	info: List[str] = field(default_factory=list)


class ServicioValidacion:
	"""
	Servicio para validación de EPUB.
	
	Proporciona validación interna y soporte para herramientas
	externas como EPUBCheck y Ace by DAISY.
	"""
	
	def __init__(self):
		"""Inicializa el servicio de validación."""
		self._epubcheck_path: Optional[str] = None
		self._ace_path: Optional[str] = None
	
	def epubcheck_disponible(self) -> bool:
		"""
		Verifica si EPUBCheck está disponible.
		
		Returns:
			bool: True si EPUBCheck está instalado
		"""
		# Buscar en PATH
		epubcheck = shutil.which('epubcheck')
		if epubcheck:
			self._epubcheck_path = epubcheck
			return True
		
		# Buscar archivo JAR común
		rutas_comunes = [
			os.path.expanduser('~/epubcheck/epubcheck.jar'),
			'C:/epubcheck/epubcheck.jar',
			'/usr/local/bin/epubcheck',
			'/opt/epubcheck/epubcheck.jar'
		]
		
		for ruta in rutas_comunes:
			if os.path.exists(ruta):
				self._epubcheck_path = ruta
				return True
		
		return False
	
	def ace_disponible(self) -> bool:
		"""
		Verifica si Ace by DAISY está disponible.
		
		Returns:
			bool: True si Ace está instalado
		"""
		# Buscar en PATH
		ace = shutil.which('ace')
		if ace:
			self._ace_path = ace
			return True
		
		# Buscar instalación npm global
		try:
			resultado = subprocess.run(
				['npm', 'list', '-g', '@daisy/ace'],
				capture_output=True,
				text=True,
				timeout=10
			)
			if resultado.returncode == 0:
				self._ace_path = 'ace'
				return True
		except (subprocess.SubprocessError, FileNotFoundError):
			pass
		
		return False
	
	def ejecutar_epubcheck(self, ruta_epub: str) -> ResultadoValidacion:
		"""
		Ejecuta EPUBCheck en un archivo EPUB.
		
		Args:
			ruta_epub: Ruta del archivo EPUB
		
		Returns:
			ResultadoValidacion: Resultado de la validación
		"""
		resultado = ResultadoValidacion(
			exito=False,
			herramienta="EPUBCheck"
		)
		
		if not self.epubcheck_disponible():
			resultado.errores.append(
				"EPUBCheck no está instalado. "
				"Descárguelo de: https://github.com/w3c/epubcheck/releases"
			)
			return resultado
		
		try:
			# Determinar comando según tipo de instalación
			if self._epubcheck_path.endswith('.jar'):
				comando = ['java', '-jar', self._epubcheck_path, ruta_epub]
			else:
				comando = [self._epubcheck_path, ruta_epub]
			
			# Ejecutar EPUBCheck
			proceso = subprocess.run(
				comando,
				capture_output=True,
				text=True,
				timeout=120
			)
			
			# Parsear salida
			self._parsear_salida_epubcheck(
				proceso.stdout + proceso.stderr,
				resultado
			)
			
			resultado.exito = proceso.returncode == 0
			
		except subprocess.TimeoutExpired:
			resultado.errores.append("EPUBCheck tardó demasiado en responder")
		except FileNotFoundError:
			resultado.errores.append("No se pudo ejecutar EPUBCheck")
		except Exception as e:
			resultado.errores.append(f"Error al ejecutar EPUBCheck: {e}")
		
		return resultado
	
	def ejecutar_ace(self, ruta_epub: str, directorio_salida: Optional[str] = None) -> ResultadoValidacion:
		"""
		Ejecuta Ace by DAISY en un archivo EPUB.
		
		Args:
			ruta_epub: Ruta del archivo EPUB
			directorio_salida: Directorio para el informe (opcional)
		
		Returns:
			ResultadoValidacion: Resultado de la validación
		"""
		resultado = ResultadoValidacion(
			exito=False,
			herramienta="Ace by DAISY"
		)
		
		if not self.ace_disponible():
			resultado.errores.append(
				"Ace by DAISY no está instalado. "
				"Instálelo con: npm install -g @daisy/ace"
			)
			return resultado
		
		try:
			comando = [self._ace_path, ruta_epub]
			
			if directorio_salida:
				comando.extend(['-o', directorio_salida])
			
			# Ejecutar Ace
			proceso = subprocess.run(
				comando,
				capture_output=True,
				text=True,
				timeout=300
			)
			
			# Parsear salida
			self._parsear_salida_ace(
				proceso.stdout + proceso.stderr,
				resultado
			)
			
			resultado.exito = proceso.returncode == 0
			
			if directorio_salida:
				resultado.info.append(
					f"Informe generado en: {directorio_salida}"
				)
			
		except subprocess.TimeoutExpired:
			resultado.errores.append("Ace tardó demasiado en responder")
		except FileNotFoundError:
			resultado.errores.append("No se pudo ejecutar Ace")
		except Exception as e:
			resultado.errores.append(f"Error al ejecutar Ace: {e}")
		
		return resultado
	
	def _parsear_salida_epubcheck(
		self,
		salida: str,
		resultado: ResultadoValidacion
	) -> None:
		"""Parsea la salida de EPUBCheck."""
		for linea in salida.split('\n'):
			linea = linea.strip()
			if not linea:
				continue
			
			linea_lower = linea.lower()
			
			if 'error' in linea_lower:
				resultado.errores.append(linea)
			elif 'warning' in linea_lower or 'advertencia' in linea_lower:
				resultado.advertencias.append(linea)
			elif 'info' in linea_lower:
				resultado.info.append(linea)
	
	def _parsear_salida_ace(
		self,
		salida: str,
		resultado: ResultadoValidacion
	) -> None:
		"""Parsea la salida de Ace."""
		for linea in salida.split('\n'):
			linea = linea.strip()
			if not linea:
				continue
			
			linea_lower = linea.lower()
			
			if 'error' in linea_lower or 'critical' in linea_lower:
				resultado.errores.append(linea)
			elif 'warning' in linea_lower or 'serious' in linea_lower:
				resultado.advertencias.append(linea)
			elif 'minor' in linea_lower or 'moderate' in linea_lower:
				resultado.info.append(linea)
	
	def validar_proyecto(self, proyecto: Proyecto) -> List[str]:
		"""
		Realiza validación interna del proyecto.
		
		Args:
			proyecto: Proyecto a validar
		
		Returns:
			List[str]: Lista de problemas encontrados
		"""
		problemas = []
		
		# Validar metadatos
		errores_meta = proyecto.metadatos.validar()
		problemas.extend(errores_meta)
		
		# Validar que haya contenido
		if not proyecto.secciones:
			problemas.append("El libro no tiene ninguna sección")
		
		# Validar secciones
		nivel_anterior = 0
		for i, seccion in enumerate(proyecto.secciones):
			# Título obligatorio
			if not seccion.titulo or not seccion.titulo.strip():
				problemas.append(
					f"Sección {i+1}: No tiene título definido"
				)
			
			# Verificar saltos de nivel de encabezado
			if seccion.nivel_encabezado > nivel_anterior + 1 and nivel_anterior > 0:
				problemas.append(
					f"Sección '{seccion.titulo}': Salto de nivel de encabezado "
					f"(de h{nivel_anterior} a h{seccion.nivel_encabezado})"
				)
			nivel_anterior = seccion.nivel_encabezado
			
			# Validar imágenes
			for imagen in seccion.imagenes:
				errores_img = imagen.validar()
				for error in errores_img:
					problemas.append(f"Sección '{seccion.titulo}' - Imagen: {error}")
				
				# Verificar que el archivo existe
				if imagen.ruta and not os.path.exists(imagen.ruta):
					problemas.append(
						f"Sección '{seccion.titulo}': "
						f"Archivo de imagen no encontrado: {imagen.ruta}"
					)
		
		# Validar portada
		if proyecto.portada:
			errores_portada = proyecto.portada.validar()
			for error in errores_portada:
				problemas.append(f"Portada: {error}")
			
			if proyecto.portada.ruta and not os.path.exists(proyecto.portada.ruta):
				problemas.append(
					f"Archivo de portada no encontrado: {proyecto.portada.ruta}"
				)
		else:
			problemas.append(
				"Advertencia: El libro no tiene imagen de portada definida"
			)
		
		# Validar accesibilidad
		acc = proyecto.metadatos_accesibilidad
		if not acc.accessibility_summary:
			problemas.append(
				"Advertencia: No se ha definido un resumen de accesibilidad"
			)
		
		return problemas
	
	def verificar_enlaces_toc(self, proyecto: Proyecto) -> List[str]:
		"""
		Verifica que los enlaces de la TOC sean válidos.
		
		Args:
			proyecto: Proyecto a verificar
		
		Returns:
			List[str]: Lista de enlaces inválidos
		"""
		problemas = []
		
		# Obtener IDs de secciones
		ids_secciones = {seccion.id for seccion in proyecto.secciones}
		
		# Verificar que cada sección tenga un ID único
		ids_vistos = set()
		for seccion in proyecto.secciones:
			if seccion.id in ids_vistos:
				problemas.append(
					f"ID duplicado en sección: {seccion.id}"
				)
			ids_vistos.add(seccion.id)
		
		return problemas
	
	def obtener_resumen_validacion(
		self,
		resultado_epubcheck: Optional[ResultadoValidacion],
		resultado_ace: Optional[ResultadoValidacion],
		problemas_internos: List[str]
	) -> str:
		"""
		Genera un resumen de todas las validaciones.
		
		Args:
			resultado_epubcheck: Resultado de EPUBCheck
			resultado_ace: Resultado de Ace
			problemas_internos: Problemas de validación interna
		
		Returns:
			str: Resumen formateado
		"""
		lineas = ["=== Resumen de Validación ===\n"]
		
		# Validación interna
		lineas.append("--- Validación Interna ---")
		if problemas_internos:
			for problema in problemas_internos:
				lineas.append(f"  • {problema}")
		else:
			lineas.append("  ✓ Sin problemas detectados")
		lineas.append("")
		
		# EPUBCheck
		if resultado_epubcheck:
			lineas.append("--- EPUBCheck ---")
			if resultado_epubcheck.exito:
				lineas.append("  ✓ Validación exitosa")
			else:
				for error in resultado_epubcheck.errores:
					lineas.append(f"  ✗ {error}")
			for adv in resultado_epubcheck.advertencias:
				lineas.append(f"  ⚠ {adv}")
			lineas.append("")
		
		# Ace
		if resultado_ace:
			lineas.append("--- Ace by DAISY ---")
			if resultado_ace.exito:
				lineas.append("  ✓ Validación exitosa")
			else:
				for error in resultado_ace.errores:
					lineas.append(f"  ✗ {error}")
			for adv in resultado_ace.advertencias:
				lineas.append(f"  ⚠ {adv}")
			lineas.append("")
		
		return '\n'.join(lineas)
	
	def obtener_instrucciones_instalacion(self) -> str:
		"""
		Obtiene instrucciones para instalar herramientas de validación.
		
		Returns:
			str: Instrucciones de instalación
		"""
		instrucciones = []
		
		if not self.epubcheck_disponible():
			instrucciones.append(
				"EPUBCheck:\n"
				"  1. Descargue desde: https://github.com/w3c/epubcheck/releases\n"
				"  2. Extraiga el archivo ZIP\n"
				"  3. Agregue la carpeta al PATH del sistema\n"
				"  4. Requiere Java instalado"
			)
		
		if not self.ace_disponible():
			instrucciones.append(
				"Ace by DAISY:\n"
				"  1. Instale Node.js desde: https://nodejs.org/\n"
				"  2. Ejecute: npm install -g @daisy/ace"
			)
		
		if not instrucciones:
			return "Todas las herramientas de validación están instaladas."
		
		return "\n\n".join(instrucciones)
