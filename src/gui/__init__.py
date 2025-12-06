# -*- coding: utf-8 -*-
"""
Módulo de interfaz gráfica.
Contiene los componentes de la GUI accesible en wxPython.
"""

from .ventana_principal import VentanaPrincipal
from .panel_secciones import PanelSecciones
from .panel_editor import PanelEditor
from .panel_logs import PanelLogs

__all__ = [
	'VentanaPrincipal',
	'PanelSecciones',
	'PanelEditor',
	'PanelLogs'
]
