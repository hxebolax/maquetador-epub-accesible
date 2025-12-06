# -*- coding: utf-8 -*-
"""
Diálogo de Importación.
Permite importar contenido desde archivos externos.
"""

import wx
import os

from ...modelo.seccion import TipoSeccion
from ...servicios.servicio_importacion import ServicioImportacion


class DialogoImportacion(wx.Dialog):
	"""
	Diálogo accesible para importación de archivos.
	"""
	
	def __init__(self, parent):
		"""
		Inicializa el diálogo.
		
		Args:
			parent: Ventana padre
		"""
		super().__init__(
			parent,
			title="Importar archivo",
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		
		self.servicio = ServicioImportacion()
		self.ruta_archivo = ""
		
		self._crear_controles()
		self._configurar_layout()
		self._configurar_eventos()
		
		self.SetSize((500, 300))
		self.Centre()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del diálogo."""
		# Archivo
		self.lbl_archivo = wx.StaticText(self, label="&Archivo:")
		self.txt_archivo = wx.TextCtrl(self, style=wx.TE_READONLY)
		self.txt_archivo.SetName("Ruta del archivo a importar")
		self.btn_examinar = wx.Button(self, label="E&xaminar...")
		
		# Título de la sección
		self.lbl_titulo = wx.StaticText(self, label="&Título de la sección:")
		self.txt_titulo = wx.TextCtrl(self)
		self.txt_titulo.SetName("Título para la nueva sección")
		
		# Tipo de sección
		self.lbl_tipo = wx.StaticText(self, label="T&ipo de sección:")
		
		tipos = [
			("Capítulo", TipoSeccion.CAPITULO),
			("Prólogo", TipoSeccion.PROLOGO),
			("Epílogo", TipoSeccion.EPILOGO),
			("Introducción", TipoSeccion.INTRODUCCION),
			("Prefacio", TipoSeccion.PREFACIO),
			("Dedicatoria", TipoSeccion.DEDICATORIA),
			("Agradecimientos", TipoSeccion.AGRADECIMIENTOS),
			("Anexo", TipoSeccion.ANEXO),
			("Bibliografía", TipoSeccion.BIBLIOGRAFIA),
			("Glosario", TipoSeccion.GLOSARIO),
			("Sinopsis", TipoSeccion.SINOPSIS)
		]
		
		self.tipos_seccion = tipos
		nombres_tipos = [t[0] for t in tipos]
		
		self.cmb_tipo = wx.ComboBox(
			self,
			choices=nombres_tipos,
			style=wx.CB_READONLY
		)
		self.cmb_tipo.SetSelection(0)
		self.cmb_tipo.SetName("Tipo de sección")
		
		# Información del archivo
		self.lbl_info = wx.StaticText(
			self,
			label="Seleccione un archivo TXT, Markdown o HTML para importar."
		)
		
		# Botones
		self.btn_ok = wx.Button(self, wx.ID_OK, label="&Importar")
		self.btn_ok.Enable(False)
		self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, label="&Cancelar")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del diálogo."""
		# Archivo
		sizer_archivo = wx.BoxSizer(wx.HORIZONTAL)
		sizer_archivo.Add(self.txt_archivo, 1, wx.EXPAND | wx.RIGHT, 5)
		sizer_archivo.Add(self.btn_examinar, 0)
		
		# Grid principal
		grid = wx.FlexGridSizer(3, 2, 10, 10)
		grid.AddGrowableCol(1)
		
		grid.Add(self.lbl_archivo, 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(sizer_archivo, 1, wx.EXPAND)
		
		grid.Add(self.lbl_titulo, 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(self.txt_titulo, 1, wx.EXPAND)
		
		grid.Add(self.lbl_tipo, 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(self.cmb_tipo, 0)
		
		# Botones
		sizer_botones = wx.StdDialogButtonSizer()
		sizer_botones.AddButton(self.btn_ok)
		sizer_botones.AddButton(self.btn_cancelar)
		sizer_botones.Realize()
		
		# Sizer principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.lbl_info, 0, wx.ALL, 10)
		sizer.Add(grid, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		sizer.AddStretchSpacer()
		sizer.Add(sizer_botones, 0, wx.EXPAND | wx.ALL, 10)
		
		self.SetSizer(sizer)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del diálogo."""
		self.btn_examinar.Bind(wx.EVT_BUTTON, self.on_examinar)
		self.btn_ok.Bind(wx.EVT_BUTTON, self.on_importar)
	
	def on_examinar(self, event) -> None:
		"""Muestra diálogo para seleccionar archivo."""
		dialogo = wx.FileDialog(
			self,
			message="Seleccionar archivo para importar",
			wildcard=self.servicio.obtener_filtro_archivos(),
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		)
		
		if dialogo.ShowModal() == wx.ID_OK:
			ruta = dialogo.GetPath()
			self.ruta_archivo = ruta
			self.txt_archivo.SetValue(ruta)
			
			# Sugerir título basado en nombre de archivo
			titulo_sugerido = self.servicio.obtener_titulo_sugerido(ruta)
			self.txt_titulo.SetValue(titulo_sugerido)
			
			# Habilitar botón de importar
			self.btn_ok.Enable(True)
			
			# Actualizar información
			tipo = self.servicio.detectar_tipo_archivo(ruta)
			if tipo:
				self.lbl_info.SetLabel(
					f"Archivo {tipo.upper()} seleccionado: {os.path.basename(ruta)}"
				)
		
		dialogo.Destroy()
	
	def on_importar(self, event) -> None:
		"""Valida y acepta la importación."""
		if not self.ruta_archivo:
			wx.MessageBox(
				"Debe seleccionar un archivo para importar.",
				"Error",
				wx.OK | wx.ICON_ERROR
			)
			return
		
		if not self.txt_titulo.GetValue().strip():
			wx.MessageBox(
				"Debe ingresar un título para la sección.",
				"Error",
				wx.OK | wx.ICON_ERROR
			)
			return
		
		event.Skip()
	
	def obtener_ruta(self) -> str:
		"""
		Obtiene la ruta del archivo seleccionado.
		
		Returns:
			str: Ruta del archivo
		"""
		return self.ruta_archivo
	
	def obtener_titulo(self) -> str:
		"""
		Obtiene el título ingresado.
		
		Returns:
			str: Título de la sección
		"""
		return self.txt_titulo.GetValue().strip()
	
	def obtener_tipo_seccion(self) -> TipoSeccion:
		"""
		Obtiene el tipo de sección seleccionado.
		
		Returns:
			TipoSeccion: Tipo de sección
		"""
		indice = self.cmb_tipo.GetSelection()
		if indice != wx.NOT_FOUND and indice < len(self.tipos_seccion):
			return self.tipos_seccion[indice][1]
		return TipoSeccion.CAPITULO
