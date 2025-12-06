# -*- coding: utf-8 -*-
"""
Diálogo para insertar/editar imágenes.
Permite seleccionar una imagen y configurar su texto alternativo y descripción larga.
"""

import wx
import os
from typing import Optional

from ...modelo.imagen import Imagen


class DialogoInsertarImagen(wx.Dialog):
	"""
	Diálogo accesible para insertar o editar imágenes con accesibilidad.
	"""
	
	# Filtro de archivos de imagen
	FILTRO_IMAGENES = (
		"Imágenes|*.jpg;*.jpeg;*.png;*.gif;*.svg;*.webp|"
		"JPEG (*.jpg;*.jpeg)|*.jpg;*.jpeg|"
		"PNG (*.png)|*.png|"
		"GIF (*.gif)|*.gif|"
		"SVG (*.svg)|*.svg|"
		"WebP (*.webp)|*.webp|"
		"Todos los archivos (*.*)|*.*"
	)
	
	def __init__(
		self,
		parent,
		imagen_existente: Optional[Imagen] = None,
		directorio_inicial: str = ""
	):
		"""
		Inicializa el diálogo.
		
		Args:
			parent: Ventana padre
			imagen_existente: Imagen a editar (None para nueva)
			directorio_inicial: Directorio inicial para el selector
		"""
		titulo = "Editar imagen" if imagen_existente else "Insertar imagen"
		super().__init__(
			parent,
			title=titulo,
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		
		self.imagen_existente = imagen_existente
		self.directorio_inicial = directorio_inicial or os.path.expanduser("~")
		self.ruta_imagen: str = ""
		
		self._crear_controles()
		self._configurar_layout()
		self._configurar_eventos()
		
		if imagen_existente:
			self._cargar_imagen_existente()
		
		self.SetSize((550, 450))
		self.Centre()
		
		# Foco inicial
		if imagen_existente:
			self.txt_alt.SetFocus()
		else:
			self.btn_seleccionar.SetFocus()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del diálogo."""
		# Selección de archivo
		self.lbl_archivo = wx.StaticText(
			self,
			label="&Archivo de imagen:"
		)
		self.txt_archivo = wx.TextCtrl(
			self,
			style=wx.TE_READONLY
		)
		self.txt_archivo.SetName("Ruta del archivo de imagen")
		self.btn_seleccionar = wx.Button(
			self,
			label="&Seleccionar..."
		)
		self.btn_seleccionar.SetToolTip("Seleccionar archivo de imagen")
		
		# Vista previa
		self.lbl_preview = wx.StaticText(
			self,
			label="Vista previa:"
		)
		self.panel_preview = wx.Panel(self, size=(200, 150))
		self.panel_preview.SetBackgroundColour(wx.Colour(240, 240, 240))
		self.bitmap_preview: Optional[wx.StaticBitmap] = None
		
		# Texto alternativo (obligatorio)
		self.lbl_alt = wx.StaticText(
			self,
			label="&Texto alternativo (obligatorio):"
		)
		self.txt_alt = wx.TextCtrl(self)
		self.txt_alt.SetName("Texto alternativo para la imagen")
		self.txt_alt.SetToolTip(
			"Descripción breve de la imagen para lectores de pantalla. "
			"Este campo es obligatorio para accesibilidad."
		)
		
		# Descripción larga (opcional)
		self.lbl_desc = wx.StaticText(
			self,
			label="&Descripción larga (opcional):"
		)
		self.txt_desc = wx.TextCtrl(
			self,
			style=wx.TE_MULTILINE,
			size=(-1, 80)
		)
		self.txt_desc.SetName("Descripción larga de la imagen")
		self.txt_desc.SetToolTip(
			"Descripción detallada para imágenes complejas como gráficos o diagramas. "
			"Opcional pero recomendado para imágenes que transmiten información importante."
		)
		
		# Mensaje de error
		self.lbl_error = wx.StaticText(self, label="")
		self.lbl_error.SetForegroundColour(wx.Colour(200, 0, 0))
		
		# Botones
		self.btn_ok = wx.Button(self, wx.ID_OK, label="&Aceptar")
		self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, label="&Cancelar")
		self.btn_ok.SetDefault()
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del diálogo."""
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Archivo
		sizer_archivo = wx.BoxSizer(wx.HORIZONTAL)
		sizer_archivo.Add(self.txt_archivo, 1, wx.EXPAND | wx.RIGHT, 5)
		sizer_archivo.Add(self.btn_seleccionar, 0)
		
		sizer.Add(self.lbl_archivo, 0, wx.ALL, 10)
		sizer.Add(sizer_archivo, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		
		# Vista previa
		sizer.Add(self.lbl_preview, 0, wx.ALL, 10)
		sizer.Add(
			self.panel_preview, 0,
			wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10
		)
		
		# Texto alternativo
		sizer.Add(self.lbl_alt, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
		sizer.Add(self.txt_alt, 0, wx.EXPAND | wx.ALL, 10)
		
		# Descripción larga
		sizer.Add(self.lbl_desc, 0, wx.LEFT | wx.RIGHT, 10)
		sizer.Add(self.txt_desc, 1, wx.EXPAND | wx.ALL, 10)
		
		# Error
		sizer.Add(self.lbl_error, 0, wx.LEFT | wx.RIGHT, 10)
		
		# Botones
		sizer_botones = wx.StdDialogButtonSizer()
		sizer_botones.AddButton(self.btn_ok)
		sizer_botones.AddButton(self.btn_cancelar)
		sizer_botones.Realize()
		sizer.Add(sizer_botones, 0, wx.EXPAND | wx.ALL, 10)
		
		self.SetSizer(sizer)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del diálogo."""
		self.btn_seleccionar.Bind(wx.EVT_BUTTON, self.on_seleccionar)
		self.btn_ok.Bind(wx.EVT_BUTTON, self.on_aceptar)
		self.txt_alt.Bind(wx.EVT_TEXT, self.on_texto_cambiado)
	
	def _cargar_imagen_existente(self) -> None:
		"""Carga los datos de una imagen existente."""
		if not self.imagen_existente:
			return
		
		self.ruta_imagen = self.imagen_existente.ruta
		self.txt_archivo.SetValue(self.ruta_imagen)
		self.txt_alt.SetValue(self.imagen_existente.texto_alternativo)
		
		if self.imagen_existente.descripcion_larga:
			self.txt_desc.SetValue(self.imagen_existente.descripcion_larga)
		
		self._actualizar_preview()
	
	def on_seleccionar(self, event) -> None:
		"""Muestra el diálogo de selección de archivo."""
		dialogo = wx.FileDialog(
			self,
			message="Seleccionar imagen",
			defaultDir=self.directorio_inicial,
			wildcard=self.FILTRO_IMAGENES,
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		)
		
		if dialogo.ShowModal() == wx.ID_OK:
			self.ruta_imagen = dialogo.GetPath()
			self.txt_archivo.SetValue(self.ruta_imagen)
			self._actualizar_preview()
			
			# Actualizar directorio inicial
			self.directorio_inicial = os.path.dirname(self.ruta_imagen)
		
		dialogo.Destroy()
	
	def _actualizar_preview(self) -> None:
		"""Actualiza la vista previa de la imagen."""
		if not self.ruta_imagen or not os.path.exists(self.ruta_imagen):
			return
		
		try:
			# Cargar imagen
			imagen = wx.Image(self.ruta_imagen, wx.BITMAP_TYPE_ANY)
			
			if not imagen.IsOk():
				return
			
			# Escalar manteniendo proporción
			ancho_max, alto_max = 200, 150
			ancho, alto = imagen.GetWidth(), imagen.GetHeight()
			
			ratio = min(ancho_max / ancho, alto_max / alto)
			nuevo_ancho = int(ancho * ratio)
			nuevo_alto = int(alto * ratio)
			
			imagen = imagen.Scale(nuevo_ancho, nuevo_alto, wx.IMAGE_QUALITY_HIGH)
			bitmap = wx.Bitmap(imagen)
			
			# Mostrar en panel
			if self.bitmap_preview:
				self.bitmap_preview.Destroy()
			
			self.bitmap_preview = wx.StaticBitmap(
				self.panel_preview,
				bitmap=bitmap
			)
			
			# Centrar en panel
			panel_w, panel_h = self.panel_preview.GetSize()
			x = (panel_w - nuevo_ancho) // 2
			y = (panel_h - nuevo_alto) // 2
			self.bitmap_preview.SetPosition((x, y))
			
		except Exception as e:
			self.lbl_error.SetLabel(f"Error al cargar imagen: {e}")
	
	def on_texto_cambiado(self, event) -> None:
		"""Limpia el mensaje de error cuando se escribe."""
		self.lbl_error.SetLabel("")
		event.Skip()
	
	def on_aceptar(self, event) -> None:
		"""Valida y acepta el diálogo."""
		if not self.validar_campos():
			return
		
		event.Skip()
	
	def validar_campos(self) -> bool:
		"""
		Valida los campos del diálogo.
		
		Returns:
			bool: True si los campos son válidos
		"""
		# Validar archivo
		if not self.ruta_imagen:
			self.lbl_error.SetLabel("Debe seleccionar un archivo de imagen")
			self.btn_seleccionar.SetFocus()
			return False
		
		if not os.path.exists(self.ruta_imagen):
			self.lbl_error.SetLabel("El archivo seleccionado no existe")
			self.btn_seleccionar.SetFocus()
			return False
		
		# Validar texto alternativo
		texto_alt = self.txt_alt.GetValue().strip()
		if not texto_alt:
			self.lbl_error.SetLabel(
				"El texto alternativo es obligatorio para accesibilidad"
			)
			self.txt_alt.SetFocus()
			return False
		
		return True
	
	def obtener_imagen(self) -> Optional[Imagen]:
		"""
		Obtiene la imagen configurada.
		
		Returns:
			Imagen: Imagen con los datos del diálogo, o None si no es válida
		"""
		if not self.validar_campos():
			return None
		
		# Crear o actualizar imagen
		if self.imagen_existente:
			imagen = self.imagen_existente
			imagen.ruta = self.ruta_imagen
		else:
			imagen = Imagen(ruta=self.ruta_imagen)
		
		imagen.texto_alternativo = self.txt_alt.GetValue().strip()
		
		desc_larga = self.txt_desc.GetValue().strip()
		imagen.descripcion_larga = desc_larga if desc_larga else None
		
		return imagen
