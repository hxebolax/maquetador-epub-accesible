# -*- coding: utf-8 -*-
"""
Módulo de interfaz gráfica.
Contiene los componentes de la GUI accesible en wxPython.
"""

from .ventana_principal import VentanaPrincipal
from .panel_secciones import PanelSecciones
from .panel_editor import PanelEditor
from .panel_editor_wysiwyg import PanelEditorWYSIWYG
from .panel_logs import PanelLogs
from .ventana_vista_previa import VentanaVistaPrevia

__all__ = [
	'VentanaPrincipal',
	'PanelSecciones',
	'PanelEditor',
	'PanelEditorWYSIWYG',
	'PanelLogs',
	'VentanaVistaPrevia'
]
