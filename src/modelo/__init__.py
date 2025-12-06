# -*- coding: utf-8 -*-
"""
Módulo de modelos de datos.
Contiene las clases que representan la estructura del libro y sus componentes.
"""

from .proyecto import Proyecto
from .seccion import Seccion, TipoSeccion
from .metadatos import MetadatosDC, MetadatosAccesibilidad
from .imagen import Imagen
from .preferencias import Preferencias

__all__ = [
	'Proyecto',
	'Seccion',
	'TipoSeccion',
	'MetadatosDC',
	'MetadatosAccesibilidad',
	'Imagen',
	'Preferencias'
]
