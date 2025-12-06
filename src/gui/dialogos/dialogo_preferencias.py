# -*- coding: utf-8 -*-
"""
Diálogo de Preferencias.
Permite configurar las preferencias de la aplicación.
"""

import wx
import os

from ...modelo.preferencias import Preferencias
from ...servicios.servicio_i18n import ServicioI18n


class DialogoPreferencias(wx.Dialog):
	"""
	Diálogo accesible para configuración de preferencias.
	"""
	
	def __init__(self, parent, preferencias: Preferencias):
		"""
		Inicializa el diálogo.
		
		Args:
			parent: Ventana padre
			preferencias: Preferencias actuales
		"""
		super().__init__(
			parent,
			title="Preferencias",
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		
		self.preferencias = Preferencias.from_dict(preferencias.to_dict())
		
		self._crear_controles()
		self._configurar_layout()
		self._cargar_datos()
		self._configurar_eventos()
		
		self.SetSize((500, 400))
		self.Centre()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del diálogo."""
		# Idioma
		self.lbl_idioma = wx.StaticText(
			self,
			label="&Idioma de la interfaz:"
		)
		self.i18n = ServicioI18n()
		idiomas = self.i18n.obtener_idiomas_disponibles()
		self.idiomas_codigos = [codigo for codigo, _ in idiomas]
		self.idiomas_nombres = [nombre for _, nombre in idiomas]
		self.cmb_idioma = wx.Choice(self, choices=self.idiomas_nombres)
		self.cmb_idioma.SetName("Idioma de la interfaz")
		
		self.lbl_idioma_nota = wx.StaticText(
			self,
			label="(Requiere reiniciar la aplicación)"
		)
		self.lbl_idioma_nota.SetForegroundColour(wx.Colour(128, 128, 128))
		
		# Directorios
		self.lbl_dir_proyectos = wx.StaticText(
			self,
			label="Directorio de &proyectos:"
		)
		self.txt_dir_proyectos = wx.TextCtrl(self)
		self.btn_dir_proyectos = wx.Button(self, label="...")
		self.btn_dir_proyectos.SetToolTip("Seleccionar directorio")
		
		self.lbl_dir_importacion = wx.StaticText(
			self,
			label="Directorio de &importación:"
		)
		self.txt_dir_importacion = wx.TextCtrl(self)
		self.btn_dir_importacion = wx.Button(self, label="...")
		
		self.lbl_dir_exportacion = wx.StaticText(
			self,
			label="Directorio de &exportación:"
		)
		self.txt_dir_exportacion = wx.TextCtrl(self)
		self.btn_dir_exportacion = wx.Button(self, label="...")
		
		# Comportamiento
		self.chk_guardado_auto = wx.CheckBox(
			self,
			label="&Guardado automático"
		)
		self.chk_guardado_auto.SetName("Activar guardado automático")
		
		self.lbl_intervalo = wx.StaticText(
			self,
			label="&Intervalo (segundos):"
		)
		self.spin_intervalo = wx.SpinCtrl(
			self,
			min=60,
			max=3600,
			initial=300
		)
		self.spin_intervalo.SetName("Intervalo de guardado automático")
		
		self.chk_confirmar_eliminar = wx.CheckBox(
			self,
			label="&Confirmar antes de eliminar"
		)
		
		self.chk_mostrar_logs = wx.CheckBox(
			self,
			label="&Mostrar panel de mensajes"
		)
		
		# Botones
		self.btn_ok = wx.Button(self, wx.ID_OK, label="&Aceptar")
		self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, label="&Cancelar")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del diálogo."""
		# Idioma
		box_idioma = wx.StaticBox(self, label="Idioma")
		sizer_idioma = wx.StaticBoxSizer(box_idioma, wx.VERTICAL)
		
		sizer_idioma_row = wx.BoxSizer(wx.HORIZONTAL)
		sizer_idioma_row.Add(self.lbl_idioma, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		sizer_idioma_row.Add(self.cmb_idioma, 0, wx.RIGHT, 10)
		sizer_idioma_row.Add(self.lbl_idioma_nota, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer_idioma.Add(sizer_idioma_row, 0, wx.ALL, 5)
		
		# Directorios
		box_dirs = wx.StaticBox(self, label="Directorios")
		sizer_dirs = wx.StaticBoxSizer(box_dirs, wx.VERTICAL)
		
		grid_dirs = wx.FlexGridSizer(3, 3, 5, 5)
		grid_dirs.AddGrowableCol(1)
		
		grid_dirs.Add(self.lbl_dir_proyectos, 0, wx.ALIGN_CENTER_VERTICAL)
		grid_dirs.Add(self.txt_dir_proyectos, 1, wx.EXPAND)
		grid_dirs.Add(self.btn_dir_proyectos, 0)
		
		grid_dirs.Add(self.lbl_dir_importacion, 0, wx.ALIGN_CENTER_VERTICAL)
		grid_dirs.Add(self.txt_dir_importacion, 1, wx.EXPAND)
		grid_dirs.Add(self.btn_dir_importacion, 0)
		
		grid_dirs.Add(self.lbl_dir_exportacion, 0, wx.ALIGN_CENTER_VERTICAL)
		grid_dirs.Add(self.txt_dir_exportacion, 1, wx.EXPAND)
		grid_dirs.Add(self.btn_dir_exportacion, 0)
		
		sizer_dirs.Add(grid_dirs, 1, wx.EXPAND | wx.ALL, 5)
		
		# Comportamiento
		box_comp = wx.StaticBox(self, label="Comportamiento")
		sizer_comp = wx.StaticBoxSizer(box_comp, wx.VERTICAL)
		
		sizer_guardado = wx.BoxSizer(wx.HORIZONTAL)
		sizer_guardado.Add(self.chk_guardado_auto, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)
		sizer_guardado.Add(self.lbl_intervalo, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		sizer_guardado.Add(self.spin_intervalo, 0)
		
		sizer_comp.Add(sizer_guardado, 0, wx.ALL, 5)
		sizer_comp.Add(self.chk_confirmar_eliminar, 0, wx.ALL, 5)
		sizer_comp.Add(self.chk_mostrar_logs, 0, wx.ALL, 5)
		
		# Botones
		sizer_botones = wx.StdDialogButtonSizer()
		sizer_botones.AddButton(self.btn_ok)
		sizer_botones.AddButton(self.btn_cancelar)
		sizer_botones.Realize()
		
		# Sizer principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(sizer_idioma, 0, wx.EXPAND | wx.ALL, 10)
		sizer.Add(sizer_dirs, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		sizer.Add(sizer_comp, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		sizer.Add(sizer_botones, 0, wx.EXPAND | wx.ALL, 10)
		
		self.SetSizer(sizer)
	
	def _cargar_datos(self) -> None:
		"""Carga los datos en los controles."""
		# Idioma
		idioma_actual = self.preferencias.idioma
		if idioma_actual in self.idiomas_codigos:
			idx = self.idiomas_codigos.index(idioma_actual)
			self.cmb_idioma.SetSelection(idx)
		else:
			self.cmb_idioma.SetSelection(0)  # Español por defecto
		
		self.txt_dir_proyectos.SetValue(self.preferencias.directorio_proyectos)
		self.txt_dir_importacion.SetValue(self.preferencias.directorio_importacion)
		self.txt_dir_exportacion.SetValue(self.preferencias.directorio_exportacion)
		
		self.chk_guardado_auto.SetValue(self.preferencias.guardado_automatico)
		self.spin_intervalo.SetValue(self.preferencias.intervalo_guardado)
		self.chk_confirmar_eliminar.SetValue(self.preferencias.confirmar_eliminacion)
		self.chk_mostrar_logs.SetValue(self.preferencias.mostrar_panel_logs)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del diálogo."""
		self.btn_dir_proyectos.Bind(
			wx.EVT_BUTTON,
			lambda e: self._seleccionar_directorio(self.txt_dir_proyectos)
		)
		self.btn_dir_importacion.Bind(
			wx.EVT_BUTTON,
			lambda e: self._seleccionar_directorio(self.txt_dir_importacion)
		)
		self.btn_dir_exportacion.Bind(
			wx.EVT_BUTTON,
			lambda e: self._seleccionar_directorio(self.txt_dir_exportacion)
		)
		
		self.btn_ok.Bind(wx.EVT_BUTTON, self.on_aceptar)
	
	def _seleccionar_directorio(self, control: wx.TextCtrl) -> None:
		"""
		Muestra diálogo para seleccionar directorio.
		
		Args:
			control: Control de texto donde poner la ruta
		"""
		ruta_actual = control.GetValue()
		if not ruta_actual or not os.path.isdir(ruta_actual):
			ruta_actual = os.path.expanduser("~")
		
		dialogo = wx.DirDialog(
			self,
			message="Seleccionar directorio",
			defaultPath=ruta_actual,
			style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
		)
		
		if dialogo.ShowModal() == wx.ID_OK:
			control.SetValue(dialogo.GetPath())
		
		dialogo.Destroy()
	
	def on_aceptar(self, event) -> None:
		"""Guarda los cambios y cierra el diálogo."""
		# Idioma
		idx = self.cmb_idioma.GetSelection()
		if idx >= 0 and idx < len(self.idiomas_codigos):
			self.preferencias.idioma = self.idiomas_codigos[idx]
		
		self.preferencias.directorio_proyectos = self.txt_dir_proyectos.GetValue()
		self.preferencias.directorio_importacion = self.txt_dir_importacion.GetValue()
		self.preferencias.directorio_exportacion = self.txt_dir_exportacion.GetValue()
		
		self.preferencias.guardado_automatico = self.chk_guardado_auto.GetValue()
		self.preferencias.intervalo_guardado = self.spin_intervalo.GetValue()
		self.preferencias.confirmar_eliminacion = self.chk_confirmar_eliminar.GetValue()
		self.preferencias.mostrar_panel_logs = self.chk_mostrar_logs.GetValue()
		
		event.Skip()
	
	def obtener_preferencias(self) -> Preferencias:
		"""
		Obtiene las preferencias editadas.
		
		Returns:
			Preferencias: Preferencias actualizadas
		"""
		return self.preferencias
