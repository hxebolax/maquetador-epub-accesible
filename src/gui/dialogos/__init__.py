# -*- coding: utf-8 -*-
"""
Módulo de diálogos de la aplicación.
Contiene los diálogos accesibles para metadatos, preferencias, etc.
"""

from .dialogo_metadatos import DialogoMetadatos
from .dialogo_accesibilidad import DialogoAccesibilidad
from .dialogo_preferencias import DialogoPreferencias
from .dialogo_importacion import DialogoImportacion
from .dialogo_importacion_multiple import DialogoImportacionMultiple
from .dialogo_manual import DialogoManual
from .dialogo_atajos import DialogoAtajos
from .dialogo_acerca import DialogoAcerca

__all__ = [
	'DialogoMetadatos',
	'DialogoAccesibilidad',
	'DialogoPreferencias',
	'DialogoImportacion',
	'DialogoImportacionMultiple',
	'DialogoManual',
	'DialogoAtajos',
	'DialogoAcerca'
]
