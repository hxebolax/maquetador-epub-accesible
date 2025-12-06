# -*- coding: utf-8 -*-
"""
Diálogo de Importación Múltiple.
Permite importar múltiples archivos a la vez.
"""

import wx
import os
from typing import List, Tuple

from ...modelo.seccion import TipoSeccion
from ...servicios.servicio_importacion import ServicioImportacion


class DialogoImportacionMultiple(wx.Dialog):
	"""
	Diálogo accesible para importación de múltiples archivos.
	"""
	
	def __init__(self, parent):
		"""
		Inicializa el diálogo.
		
		Args:
			parent: Ventana padre
		"""
		super().__init__(
			parent,
			title="Importar múltiples archivos",
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		
		self.servicio = ServicioImportacion()
		self.archivos: List[Tuple[str, str, TipoSeccion]] = []  # (ruta, titulo, tipo)
		
		self._crear_controles()
		self._configurar_layout()
		self._configurar_eventos()
		
		self.SetSize((600, 450))
		self.Centre()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del diálogo."""
		# Información
		self.lbl_info = wx.StaticText(
			self,
			label="Seleccione los archivos a importar. Puede seleccionar múltiples archivos."
		)
		
		# Lista de archivos
		self.lbl_archivos = wx.StaticText(self, label="&Archivos seleccionados:")
		self.lst_archivos = wx.ListCtrl(
			self,
			style=wx.LC_REPORT | wx.LC_SINGLE_SEL
		)
		self.lst_archivos.SetName("Lista de archivos a importar")
		self.lst_archivos.InsertColumn(0, "Archivo", width=200)
		self.lst_archivos.InsertColumn(1, "Título", width=150)
		self.lst_archivos.InsertColumn(2, "Tipo", width=100)
		
		# Botones de archivos
		self.btn_agregar = wx.Button(self, label="A&gregar archivos...")
		self.btn_quitar = wx.Button(self, label="&Quitar seleccionado")
		self.btn_quitar.Enable(False)
		
		# Tipo de sección por defecto
		self.lbl_tipo = wx.StaticText(self, label="&Tipo por defecto:")
		
		tipos = [
			("Capítulo", TipoSeccion.CAPITULO),
			("Prólogo", TipoSeccion.PROLOGO),
			("Epílogo", TipoSeccion.EPILOGO),
			("Introducción", TipoSeccion.INTRODUCCION),
			("Anexo", TipoSeccion.ANEXO),
		]
		self.tipos_seccion = tipos
		nombres_tipos = [t[0] for t in tipos]
		
		self.cmb_tipo = wx.ComboBox(
			self,
			choices=nombres_tipos,
			style=wx.CB_READONLY
		)
		self.cmb_tipo.SetSelection(0)
		self.cmb_tipo.SetName("Tipo de sección por defecto")
		
		# Botones principales
		self.btn_ok = wx.Button(self, wx.ID_OK, label="&Importar")
		self.btn_ok.Enable(False)
		self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, label="&Cancelar")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del diálogo."""
		# Botones de archivos
		sizer_btns_archivos = wx.BoxSizer(wx.HORIZONTAL)
		sizer_btns_archivos.Add(self.btn_agregar, 0, wx.RIGHT, 5)
		sizer_btns_archivos.Add(self.btn_quitar, 0)
		
		# Tipo por defecto
		sizer_tipo = wx.BoxSizer(wx.HORIZONTAL)
		sizer_tipo.Add(self.lbl_tipo, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
		sizer_tipo.Add(self.cmb_tipo, 0)
		
		# Botones principales
		sizer_botones = wx.StdDialogButtonSizer()
		sizer_botones.AddButton(self.btn_ok)
		sizer_botones.AddButton(self.btn_cancelar)
		sizer_botones.Realize()
		
		# Sizer principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.lbl_info, 0, wx.ALL, 10)
		sizer.Add(sizer_tipo, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		sizer.Add(self.lbl_archivos, 0, wx.LEFT | wx.RIGHT, 10)
		sizer.Add(self.lst_archivos, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		sizer.Add(sizer_btns_archivos, 0, wx.ALL, 10)
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		sizer.Add(sizer_botones, 0, wx.EXPAND | wx.ALL, 10)
		
		self.SetSizer(sizer)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del diálogo."""
		self.btn_agregar.Bind(wx.EVT_BUTTON, self.on_agregar)
		self.btn_quitar.Bind(wx.EVT_BUTTON, self.on_quitar)
		self.lst_archivos.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_seleccion)
		self.lst_archivos.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_seleccion)
		self.btn_ok.Bind(wx.EVT_BUTTON, self.on_importar)
	
	def on_agregar(self, event) -> None:
		"""Muestra diálogo para seleccionar archivos."""
		dialogo = wx.FileDialog(
			self,
			message="Seleccionar archivos para importar",
			wildcard=self.servicio.obtener_filtro_archivos(),
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
		)
		
		if dialogo.ShowModal() == wx.ID_OK:
			rutas = dialogo.GetPaths()
			
			# Obtener tipo por defecto
			indice_tipo = self.cmb_tipo.GetSelection()
			tipo = self.tipos_seccion[indice_tipo][1] if indice_tipo != wx.NOT_FOUND else TipoSeccion.CAPITULO
			
			for ruta in rutas:
				# Verificar que no esté ya en la lista
				ya_existe = any(a[0] == ruta for a in self.archivos)
				if ya_existe:
					continue
				
				# Obtener título sugerido
				titulo = self.servicio.obtener_titulo_sugerido(ruta)
				
				# Agregar a la lista
				self.archivos.append((ruta, titulo, tipo))
				
				# Agregar a la lista visual
				indice = self.lst_archivos.InsertItem(
					self.lst_archivos.GetItemCount(),
					os.path.basename(ruta)
				)
				self.lst_archivos.SetItem(indice, 1, titulo)
				self.lst_archivos.SetItem(indice, 2, TipoSeccion.obtener_nombre_legible(tipo))
			
			self._actualizar_estado()
		
		dialogo.Destroy()
	
	def on_quitar(self, event) -> None:
		"""Quita el archivo seleccionado de la lista."""
		sel = self.lst_archivos.GetFirstSelected()
		if sel != -1:
			self.archivos.pop(sel)
			self.lst_archivos.DeleteItem(sel)
			self._actualizar_estado()
	
	def on_seleccion(self, event) -> None:
		"""Maneja cambios en la selección."""
		self._actualizar_estado()
		event.Skip()
	
	def on_importar(self, event) -> None:
		"""Valida y acepta la importación."""
		if not self.archivos:
			wx.MessageBox(
				"Debe agregar al menos un archivo para importar.",
				"Error",
				wx.OK | wx.ICON_ERROR
			)
			return
		
		event.Skip()
	
	def _actualizar_estado(self) -> None:
		"""Actualiza el estado de los botones."""
		tiene_archivos = len(self.archivos) > 0
		tiene_seleccion = self.lst_archivos.GetFirstSelected() != -1
		
		self.btn_ok.Enable(tiene_archivos)
		self.btn_quitar.Enable(tiene_seleccion)
	
	def obtener_archivos(self) -> List[Tuple[str, str, TipoSeccion]]:
		"""
		Obtiene la lista de archivos a importar.
		
		Returns:
			Lista de tuplas (ruta, titulo, tipo)
		"""
		return self.archivos
