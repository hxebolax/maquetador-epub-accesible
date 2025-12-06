# -*- coding: utf-8 -*-
"""
Diálogo de Metadatos de Accesibilidad.
Permite configurar los metadatos de accesibilidad del EPUB.
"""

import wx

from ...modelo.metadatos import MetadatosAccesibilidad
from ...utils.constantes import (
	ACCESSIBILITY_FEATURES,
	ACCESSIBILITY_HAZARDS,
	ACCESS_MODES,
	WCAG_LEVELS,
	WCAG_VERSIONS
)


class DialogoAccesibilidad(wx.Dialog):
	"""
	Diálogo accesible para configuración de metadatos de accesibilidad.
	"""
	
	# Nombres legibles para características
	NOMBRES_FEATURES = {
		'tableOfContents': 'Tabla de contenidos',
		'structuralNavigation': 'Navegación estructural',
		'alternativeText': 'Texto alternativo',
		'longDescription': 'Descripciones largas',
		'readingOrder': 'Orden de lectura',
		'displayTransformability': 'Transformabilidad de visualización',
		'printPageNumbers': 'Números de página impresos',
		'pageBreakMarkers': 'Marcadores de salto de página',
		'index': 'Índice',
		'ARIA': 'Atributos ARIA'
	}
	
	# Nombres legibles para peligros
	NOMBRES_HAZARDS = {
		'none': 'Ninguno',
		'flashing': 'Contenido parpadeante',
		'motionSimulation': 'Simulación de movimiento',
		'sound': 'Sonido',
		'noFlashingHazard': 'Sin peligro de parpadeo',
		'noMotionSimulationHazard': 'Sin peligro de movimiento',
		'noSoundHazard': 'Sin peligro de sonido'
	}
	
	# Nombres legibles para modos de acceso
	NOMBRES_MODES = {
		'textual': 'Textual',
		'visual': 'Visual',
		'auditory': 'Auditivo',
		'tactile': 'Táctil'
	}
	
	def __init__(self, parent, metadatos: MetadatosAccesibilidad):
		"""
		Inicializa el diálogo.
		
		Args:
			parent: Ventana padre
			metadatos: Metadatos de accesibilidad actuales
		"""
		super().__init__(
			parent,
			title="Metadatos de accesibilidad",
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		
		self.metadatos = MetadatosAccesibilidad.from_dict(metadatos.to_dict())
		
		self._crear_controles()
		self._configurar_layout()
		self._cargar_datos()
		self._configurar_eventos()
		
		self.SetSize((550, 650))
		self.Centre()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del diálogo."""
		# Nivel WCAG
		self.lbl_wcag = wx.StaticText(self, label="Nivel &WCAG objetivo:")
		
		self.cmb_wcag_version = wx.ComboBox(
			self,
			choices=WCAG_VERSIONS,
			style=wx.CB_READONLY
		)
		self.cmb_wcag_version.SetName("Versión WCAG")
		
		self.cmb_wcag_nivel = wx.ComboBox(
			self,
			choices=WCAG_LEVELS,
			style=wx.CB_READONLY
		)
		self.cmb_wcag_nivel.SetName("Nivel de conformidad")
		
		# Modos de acceso
		self.lbl_modes = wx.StaticText(self, label="&Modos de acceso:")
		self.chk_modes = {}
		for modo in ACCESS_MODES:
			nombre = self.NOMBRES_MODES.get(modo, modo)
			self.chk_modes[modo] = wx.CheckBox(self, label=nombre)
			self.chk_modes[modo].SetName(f"Modo de acceso: {nombre}")
		
		# Características de accesibilidad
		self.lbl_features = wx.StaticText(
			self,
			label="&Características de accesibilidad:"
		)
		self.chk_features = {}
		for feature in ACCESSIBILITY_FEATURES:
			nombre = self.NOMBRES_FEATURES.get(feature, feature)
			self.chk_features[feature] = wx.CheckBox(self, label=nombre)
			self.chk_features[feature].SetName(f"Característica: {nombre}")
		
		# Peligros
		self.lbl_hazards = wx.StaticText(self, label="&Peligros:")
		self.chk_hazards = {}
		for hazard in ACCESSIBILITY_HAZARDS:
			nombre = self.NOMBRES_HAZARDS.get(hazard, hazard)
			self.chk_hazards[hazard] = wx.CheckBox(self, label=nombre)
			self.chk_hazards[hazard].SetName(f"Peligro: {nombre}")
		
		# Resumen de accesibilidad
		self.lbl_resumen = wx.StaticText(
			self,
			label="&Resumen de accesibilidad:"
		)
		self.txt_resumen = wx.TextCtrl(
			self,
			style=wx.TE_MULTILINE
		)
		self.txt_resumen.SetName("Resumen de accesibilidad en lenguaje natural")
		self.txt_resumen.SetHint(
			"Ejemplo: Este libro es accesible para lectores de pantalla. "
			"Incluye navegación estructural y texto alternativo en imágenes."
		)
		
		# Botones
		self.btn_ok = wx.Button(self, wx.ID_OK, label="&Aceptar")
		self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, label="&Cancelar")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del diálogo."""
		# WCAG
		sizer_wcag = wx.BoxSizer(wx.HORIZONTAL)
		sizer_wcag.Add(
			wx.StaticText(self, label="Versión:"),
			0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5
		)
		sizer_wcag.Add(self.cmb_wcag_version, 0, wx.RIGHT, 15)
		sizer_wcag.Add(
			wx.StaticText(self, label="Nivel:"),
			0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5
		)
		sizer_wcag.Add(self.cmb_wcag_nivel, 0)
		
		# Modos de acceso
		sizer_modes = wx.BoxSizer(wx.HORIZONTAL)
		for chk in self.chk_modes.values():
			sizer_modes.Add(chk, 0, wx.RIGHT, 15)
		
		# Características
		sizer_features = wx.GridSizer(5, 2, 5, 10)
		for chk in self.chk_features.values():
			sizer_features.Add(chk, 0)
		
		# Peligros
		sizer_hazards = wx.GridSizer(4, 2, 5, 10)
		for chk in self.chk_hazards.values():
			sizer_hazards.Add(chk, 0)
		
		# Botones
		sizer_botones = wx.StdDialogButtonSizer()
		sizer_botones.AddButton(self.btn_ok)
		sizer_botones.AddButton(self.btn_cancelar)
		sizer_botones.Realize()
		
		# Sizer principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		sizer.Add(self.lbl_wcag, 0, wx.ALL, 10)
		sizer.Add(sizer_wcag, 0, wx.LEFT | wx.BOTTOM, 20)
		
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		
		sizer.Add(self.lbl_modes, 0, wx.ALL, 10)
		sizer.Add(sizer_modes, 0, wx.LEFT | wx.BOTTOM, 20)
		
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		
		sizer.Add(self.lbl_features, 0, wx.ALL, 10)
		sizer.Add(sizer_features, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
		
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		
		sizer.Add(self.lbl_hazards, 0, wx.ALL, 10)
		sizer.Add(sizer_hazards, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
		
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		
		sizer.Add(self.lbl_resumen, 0, wx.ALL, 10)
		sizer.Add(self.txt_resumen, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		
		sizer.Add(sizer_botones, 0, wx.EXPAND | wx.ALL, 10)
		
		self.SetSizer(sizer)
	
	def _cargar_datos(self) -> None:
		"""Carga los datos en los controles."""
		# WCAG
		self.cmb_wcag_version.SetValue(self.metadatos.wcag_version)
		self.cmb_wcag_nivel.SetValue(self.metadatos.wcag_level)
		
		# Modos de acceso
		for modo, chk in self.chk_modes.items():
			chk.SetValue(modo in self.metadatos.access_mode)
		
		# Características
		for feature, chk in self.chk_features.items():
			chk.SetValue(feature in self.metadatos.accessibility_feature)
		
		# Peligros
		for hazard, chk in self.chk_hazards.items():
			chk.SetValue(hazard in self.metadatos.accessibility_hazard)
		
		# Resumen
		self.txt_resumen.SetValue(self.metadatos.accessibility_summary)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del diálogo."""
		self.btn_ok.Bind(wx.EVT_BUTTON, self.on_aceptar)
	
	def on_aceptar(self, event) -> None:
		"""Guarda los cambios y cierra el diálogo."""
		# WCAG
		self.metadatos.wcag_version = self.cmb_wcag_version.GetValue()
		self.metadatos.wcag_level = self.cmb_wcag_nivel.GetValue()
		
		# Modos de acceso
		self.metadatos.access_mode = [
			modo for modo, chk in self.chk_modes.items()
			if chk.GetValue()
		]
		self.metadatos.access_mode_sufficient = self.metadatos.access_mode.copy()
		
		# Características
		self.metadatos.accessibility_feature = [
			feature for feature, chk in self.chk_features.items()
			if chk.GetValue()
		]
		
		# Peligros
		self.metadatos.accessibility_hazard = [
			hazard for hazard, chk in self.chk_hazards.items()
			if chk.GetValue()
		]
		if not self.metadatos.accessibility_hazard:
			self.metadatos.accessibility_hazard = ['none']
		
		# Resumen
		self.metadatos.accessibility_summary = self.txt_resumen.GetValue()
		
		event.Skip()
	
	def obtener_metadatos(self) -> MetadatosAccesibilidad:
		"""
		Obtiene los metadatos editados.
		
		Returns:
			MetadatosAccesibilidad: Metadatos actualizados
		"""
		return self.metadatos
