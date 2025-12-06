# -*- coding: utf-8 -*-
"""
Modelo de Plantilla.
Define estructuras predefinidas para diferentes tipos de libros.
"""

import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

from .seccion import TipoSeccion
from .metadatos import MetadatosAccesibilidad


@dataclass
class PlantillaSeccion:
	"""Define una sección dentro de una plantilla."""
	tipo: TipoSeccion
	titulo_sugerido: str
	contenido_ejemplo: str = ""
	nivel_encabezado: int = 1


@dataclass
class Plantilla:
	"""
	Plantilla de estructura de libro.
	
	Define una estructura predefinida con secciones y metadatos
	de accesibilidad configurados.
	"""
	id: str
	nombre: str
	descripcion: str
	secciones: List[PlantillaSeccion] = field(default_factory=list)
	metadatos_accesibilidad: Optional[MetadatosAccesibilidad] = None
	es_personalizada: bool = False
	ruta_archivo: Optional[str] = None
	
	def to_dict(self) -> dict:
		"""Serializa la plantilla a diccionario."""
		return {
			'id': self.id,
			'nombre': self.nombre,
			'descripcion': self.descripcion,
			'secciones': [
				{
					'tipo': s.tipo.value,
					'titulo_sugerido': s.titulo_sugerido,
					'contenido_ejemplo': s.contenido_ejemplo,
					'nivel_encabezado': s.nivel_encabezado
				}
				for s in self.secciones
			],
			'metadatos_accesibilidad': (
				self.metadatos_accesibilidad.to_dict()
				if self.metadatos_accesibilidad else None
			),
			'es_personalizada': self.es_personalizada
		}
	
	@classmethod
	def from_dict(cls, data: dict) -> 'Plantilla':
		"""Crea una plantilla desde un diccionario."""
		secciones = []
		for s in data.get('secciones', []):
			try:
				tipo = TipoSeccion(s['tipo'])
			except ValueError:
				tipo = TipoSeccion.CAPITULO
			
			secciones.append(PlantillaSeccion(
				tipo=tipo,
				titulo_sugerido=s.get('titulo_sugerido', ''),
				contenido_ejemplo=s.get('contenido_ejemplo', ''),
				nivel_encabezado=s.get('nivel_encabezado', 1)
			))
		
		meta_acc = None
		if data.get('metadatos_accesibilidad'):
			meta_acc = MetadatosAccesibilidad.from_dict(
				data['metadatos_accesibilidad']
			)
		
		return cls(
			id=data.get('id', ''),
			nombre=data.get('nombre', ''),
			descripcion=data.get('descripcion', ''),
			secciones=secciones,
			metadatos_accesibilidad=meta_acc,
			es_personalizada=data.get('es_personalizada', False)
		)


class ServicioPlantillas:
	"""
	Servicio para gestionar plantillas de libro.
	"""
	
	# Plantillas predefinidas
	PLANTILLAS_PREDEFINIDAS: List[Plantilla] = []
	
	def __init__(self):
		"""Inicializa el servicio de plantillas."""
		self._inicializar_plantillas_predefinidas()
		self._plantillas_personalizadas: List[Plantilla] = []
	
	def _inicializar_plantillas_predefinidas(self) -> None:
		"""Inicializa las plantillas predefinidas."""
		# Plantilla: Novela
		novela = Plantilla(
			id="novela",
			nombre="Novela",
			descripcion="Estructura para novelas: portada, dedicatoria, prólogo, capítulos y epílogo",
			secciones=[
				PlantillaSeccion(TipoSeccion.DEDICATORIA, "Dedicatoria", "<p>A...</p>"),
				PlantillaSeccion(TipoSeccion.PROLOGO, "Prólogo", "<p>Introducción a la historia...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "Capítulo 1", "<p>El comienzo...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "Capítulo 2", "<p>Continuación...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "Capítulo 3", "<p>Desarrollo...</p>"),
				PlantillaSeccion(TipoSeccion.EPILOGO, "Epílogo", "<p>Conclusión...</p>"),
			],
			metadatos_accesibilidad=MetadatosAccesibilidad()
		)
		
		# Plantilla: Manual técnico
		manual = Plantilla(
			id="manual",
			nombre="Manual técnico",
			descripcion="Estructura para manuales: índice, introducción, capítulos, anexos, glosario y bibliografía",
			secciones=[
				PlantillaSeccion(TipoSeccion.INTRODUCCION, "Introducción", "<p>Propósito de este manual...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "Capítulo 1: Conceptos básicos", "<p>Fundamentos...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "Capítulo 2: Procedimientos", "<p>Pasos a seguir...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "Capítulo 3: Casos prácticos", "<p>Ejemplos...</p>"),
				PlantillaSeccion(TipoSeccion.ANEXO, "Anexo A: Referencias", "<p>Material adicional...</p>"),
				PlantillaSeccion(TipoSeccion.GLOSARIO, "Glosario", "<dl>\n  <dt>Término</dt>\n  <dd>Definición</dd>\n</dl>"),
				PlantillaSeccion(TipoSeccion.BIBLIOGRAFIA, "Bibliografía", "<ul>\n  <li>Referencia 1</li>\n</ul>"),
			],
			metadatos_accesibilidad=MetadatosAccesibilidad()
		)
		
		# Plantilla: Poemario
		poemario = Plantilla(
			id="poemario",
			nombre="Poemario",
			descripcion="Estructura para poesía: portada, dedicatoria y secciones de poemas",
			secciones=[
				PlantillaSeccion(TipoSeccion.DEDICATORIA, "Dedicatoria", "<p>Para...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "I. Primera parte", "<p>Poema 1...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "II. Segunda parte", "<p>Poema 2...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "III. Tercera parte", "<p>Poema 3...</p>"),
			],
			metadatos_accesibilidad=MetadatosAccesibilidad()
		)
		
		# Plantilla: Ensayo
		ensayo = Plantilla(
			id="ensayo",
			nombre="Ensayo",
			descripcion="Estructura para ensayos: resumen, introducción, desarrollo, conclusiones y bibliografía",
			secciones=[
				PlantillaSeccion(TipoSeccion.SINOPSIS, "Resumen", "<p>Síntesis del ensayo...</p>"),
				PlantillaSeccion(TipoSeccion.INTRODUCCION, "Introducción", "<p>Planteamiento del tema...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "Desarrollo", "<p>Argumentación principal...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "Análisis", "<p>Profundización...</p>"),
				PlantillaSeccion(TipoSeccion.CAPITULO, "Conclusiones", "<p>Síntesis y reflexiones finales...</p>"),
				PlantillaSeccion(TipoSeccion.BIBLIOGRAFIA, "Bibliografía", "<ul>\n  <li>Fuente 1</li>\n</ul>"),
			],
			metadatos_accesibilidad=MetadatosAccesibilidad()
		)
		
		ServicioPlantillas.PLANTILLAS_PREDEFINIDAS = [novela, manual, poemario, ensayo]
	
	def obtener_plantillas(self) -> List[Plantilla]:
		"""Obtiene todas las plantillas disponibles."""
		return ServicioPlantillas.PLANTILLAS_PREDEFINIDAS + self._plantillas_personalizadas
	
	def obtener_plantilla(self, id_plantilla: str) -> Optional[Plantilla]:
		"""Obtiene una plantilla por su ID."""
		for plantilla in self.obtener_plantillas():
			if plantilla.id == id_plantilla:
				return plantilla
		return None
	
	def aplicar_plantilla(self, proyecto, plantilla: Plantilla) -> None:
		"""
		Aplica una plantilla a un proyecto.
		
		Args:
			proyecto: Proyecto destino
			plantilla: Plantilla a aplicar
		"""
		from .seccion import Seccion
		
		# Limpiar secciones existentes
		proyecto.secciones.clear()
		
		# Crear secciones desde la plantilla
		for ps in plantilla.secciones:
			seccion = Seccion(
				tipo=ps.tipo,
				titulo=ps.titulo_sugerido,
				contenido_xhtml=ps.contenido_ejemplo
			)
			seccion.nivel_encabezado = ps.nivel_encabezado
			proyecto.secciones.append(seccion)
		
		# Aplicar metadatos de accesibilidad si existen
		if plantilla.metadatos_accesibilidad:
			proyecto.metadatos_accesibilidad = MetadatosAccesibilidad.from_dict(
				plantilla.metadatos_accesibilidad.to_dict()
			)
	
	def crear_plantilla_desde_proyecto(
		self,
		proyecto,
		nombre: str,
		descripcion: str = ""
	) -> Plantilla:
		"""
		Crea una plantilla desde un proyecto existente.
		
		Args:
			proyecto: Proyecto fuente
			nombre: Nombre de la plantilla
			descripcion: Descripción de la plantilla
		
		Returns:
			Plantilla: Nueva plantilla
		"""
		from ..utils.helpers import generar_id_seccion
		
		secciones = []
		for seccion in proyecto.secciones:
			secciones.append(PlantillaSeccion(
				tipo=seccion.tipo,
				titulo_sugerido=seccion.titulo,
				contenido_ejemplo=seccion.contenido_xhtml,
				nivel_encabezado=seccion.nivel_encabezado
			))
		
		plantilla = Plantilla(
			id=f"custom_{generar_id_seccion()[:8]}",
			nombre=nombre,
			descripcion=descripcion,
			secciones=secciones,
			metadatos_accesibilidad=MetadatosAccesibilidad.from_dict(
				proyecto.metadatos_accesibilidad.to_dict()
			),
			es_personalizada=True
		)
		
		return plantilla
	
	def guardar_plantilla_personalizada(
		self,
		plantilla: Plantilla,
		directorio: str
	) -> bool:
		"""
		Guarda una plantilla personalizada en disco.
		
		Args:
			plantilla: Plantilla a guardar
			directorio: Directorio donde guardar
		
		Returns:
			bool: True si se guardó correctamente
		"""
		try:
			if not os.path.exists(directorio):
				os.makedirs(directorio)
			
			ruta = os.path.join(directorio, f"{plantilla.id}.json")
			
			with open(ruta, 'w', encoding='utf-8') as f:
				json.dump(plantilla.to_dict(), f, indent=2, ensure_ascii=False)
			
			plantilla.ruta_archivo = ruta
			
			# Agregar a la lista si no existe
			if plantilla not in self._plantillas_personalizadas:
				self._plantillas_personalizadas.append(plantilla)
			
			return True
		except Exception:
			return False
	
	def cargar_plantillas_personalizadas(self, directorio: str) -> List[Plantilla]:
		"""
		Carga plantillas personalizadas desde un directorio.
		
		Args:
			directorio: Directorio con plantillas
		
		Returns:
			List[Plantilla]: Plantillas cargadas
		"""
		self._plantillas_personalizadas.clear()
		
		if not os.path.exists(directorio):
			return []
		
		for archivo in os.listdir(directorio):
			if archivo.endswith('.json'):
				ruta = os.path.join(directorio, archivo)
				try:
					with open(ruta, 'r', encoding='utf-8') as f:
						data = json.load(f)
					
					plantilla = Plantilla.from_dict(data)
					plantilla.ruta_archivo = ruta
					plantilla.es_personalizada = True
					self._plantillas_personalizadas.append(plantilla)
				except Exception:
					continue
		
		return self._plantillas_personalizadas
