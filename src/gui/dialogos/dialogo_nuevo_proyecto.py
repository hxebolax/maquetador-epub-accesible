# -*- coding: utf-8 -*-
"""
Diálogo para crear nuevo proyecto.
Permite seleccionar una plantilla o crear un proyecto en blanco.
"""

import wx
from typing import Optional

from ...modelo.plantilla import Plantilla, ServicioPlantillas


class DialogoNuevoProyecto(wx.Dialog):
	"""
	Diálogo accesible para crear un nuevo proyecto.
	"""
	
	def __init__(self, parent, directorio_plantillas: str = ""):
		"""
		Inicializa el diálogo.
		
		Args:
			parent: Ventana padre
			directorio_plantillas: Directorio de plantillas personalizadas
		"""
		super().__init__(
			parent,
			title="Nuevo proyecto",
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		
		self.servicio_plantillas = ServicioPlantillas()
		
		# Cargar plantillas personalizadas si hay directorio
		if directorio_plantillas:
			self.servicio_plantillas.cargar_plantillas_personalizadas(directorio_plantillas)
		
		self.plantilla_seleccionada: Optional[Plantilla] = None
		
		self._crear_controles()
		self._configurar_layout()
		self._configurar_eventos()
		self._cargar_plantillas()
		
		self.SetSize((500, 400))
		self.Centre()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del diálogo."""
		# Opciones
		self.rb_blanco = wx.RadioButton(
			self,
			label="Proyecto en &blanco",
			style=wx.RB_GROUP
		)
		self.rb_blanco.SetToolTip("Crear un proyecto vacío sin secciones predefinidas")
		
		self.rb_plantilla = wx.RadioButton(
			self,
			label="Usar &plantilla"
		)
		self.rb_plantilla.SetToolTip("Crear un proyecto basado en una plantilla")
		
		# Lista de plantillas
		self.lbl_plantillas = wx.StaticText(
			self,
			label="Seleccione una plantilla:"
		)
		self.lst_plantillas = wx.ListBox(self)
		self.lst_plantillas.SetName("Lista de plantillas disponibles")
		
		# Descripción de la plantilla
		self.lbl_descripcion = wx.StaticText(
			self,
			label="Descripción:"
		)
		self.txt_descripcion = wx.TextCtrl(
			self,
			style=wx.TE_MULTILINE | wx.TE_READONLY,
			size=(-1, 80)
		)
		self.txt_descripcion.SetName("Descripción de la plantilla seleccionada")
		
		# Botones
		self.btn_ok = wx.Button(self, wx.ID_OK, label="&Crear")
		self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, label="&Cancelar")
		self.btn_ok.SetDefault()
		
		# Estado inicial
		self.rb_blanco.SetValue(True)
		self._actualizar_estado_plantillas()
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del diálogo."""
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Opciones
		sizer.Add(self.rb_blanco, 0, wx.ALL, 10)
		sizer.Add(self.rb_plantilla, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		
		# Plantillas
		sizer.Add(self.lbl_plantillas, 0, wx.LEFT | wx.RIGHT, 10)
		sizer.Add(self.lst_plantillas, 1, wx.EXPAND | wx.ALL, 10)
		
		# Descripción
		sizer.Add(self.lbl_descripcion, 0, wx.LEFT | wx.RIGHT, 10)
		sizer.Add(self.txt_descripcion, 0, wx.EXPAND | wx.ALL, 10)
		
		# Botones
		sizer_botones = wx.StdDialogButtonSizer()
		sizer_botones.AddButton(self.btn_ok)
		sizer_botones.AddButton(self.btn_cancelar)
		sizer_botones.Realize()
		sizer.Add(sizer_botones, 0, wx.EXPAND | wx.ALL, 10)
		
		self.SetSizer(sizer)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del diálogo."""
		self.rb_blanco.Bind(wx.EVT_RADIOBUTTON, self.on_opcion_cambiada)
		self.rb_plantilla.Bind(wx.EVT_RADIOBUTTON, self.on_opcion_cambiada)
		self.lst_plantillas.Bind(wx.EVT_LISTBOX, self.on_plantilla_seleccionada)
		self.btn_ok.Bind(wx.EVT_BUTTON, self.on_crear)
	
	def _cargar_plantillas(self) -> None:
		"""Carga las plantillas en la lista."""
		self.lst_plantillas.Clear()
		
		plantillas = self.servicio_plantillas.obtener_plantillas()
		for plantilla in plantillas:
			prefijo = "📁 " if plantilla.es_personalizada else "📋 "
			self.lst_plantillas.Append(f"{prefijo}{plantilla.nombre}")
		
		if self.lst_plantillas.GetCount() > 0:
			self.lst_plantillas.SetSelection(0)
			self._mostrar_descripcion(0)
	
	def _actualizar_estado_plantillas(self) -> None:
		"""Actualiza el estado de los controles de plantillas."""
		usar_plantilla = self.rb_plantilla.GetValue()
		self.lbl_plantillas.Enable(usar_plantilla)
		self.lst_plantillas.Enable(usar_plantilla)
		self.lbl_descripcion.Enable(usar_plantilla)
		self.txt_descripcion.Enable(usar_plantilla)
	
	def _mostrar_descripcion(self, indice: int) -> None:
		"""Muestra la descripción de una plantilla."""
		plantillas = self.servicio_plantillas.obtener_plantillas()
		if 0 <= indice < len(plantillas):
			plantilla = plantillas[indice]
			self.txt_descripcion.SetValue(plantilla.descripcion)
	
	def on_opcion_cambiada(self, event) -> None:
		"""Maneja el cambio de opción."""
		self._actualizar_estado_plantillas()
	
	def on_plantilla_seleccionada(self, event) -> None:
		"""Maneja la selección de una plantilla."""
		indice = self.lst_plantillas.GetSelection()
		if indice != wx.NOT_FOUND:
			self._mostrar_descripcion(indice)
	
	def on_crear(self, event) -> None:
		"""Crea el proyecto."""
		if self.rb_plantilla.GetValue():
			indice = self.lst_plantillas.GetSelection()
			if indice != wx.NOT_FOUND:
				plantillas = self.servicio_plantillas.obtener_plantillas()
				if indice < len(plantillas):
					self.plantilla_seleccionada = plantillas[indice]
		
		event.Skip()
	
	def obtener_plantilla_seleccionada(self) -> Optional[Plantilla]:
		"""
		Obtiene la plantilla seleccionada.
		
		Returns:
			Plantilla: Plantilla seleccionada o None si es proyecto en blanco
		"""
		return self.plantilla_seleccionada
	
	def usar_plantilla(self) -> bool:
		"""
		Indica si se debe usar una plantilla.
		
		Returns:
			bool: True si se seleccionó usar plantilla
		"""
		return self.rb_plantilla.GetValue()
