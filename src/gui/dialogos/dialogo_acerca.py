# -*- coding: utf-8 -*-
"""
Diálogo Acerca de.
Muestra información sobre la aplicación.
"""

import wx

from ...utils.constantes import NOMBRE_APP, VERSION_APP


class DialogoAcerca(wx.Dialog):
	"""
	Diálogo accesible con información sobre la aplicación.
	"""
	
	def __init__(self, parent):
		"""
		Inicializa el diálogo.
		
		Args:
			parent: Ventana padre
		"""
		super().__init__(
			parent,
			title="Acerca de",
			style=wx.DEFAULT_DIALOG_STYLE
		)
		
		self._crear_controles()
		self._configurar_layout()
		
		self.SetSize((400, 350))
		self.Centre()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del diálogo."""
		# Nombre de la aplicación
		self.lbl_nombre = wx.StaticText(
			self,
			label=NOMBRE_APP
		)
		fuente_titulo = wx.Font(
			16,
			wx.FONTFAMILY_DEFAULT,
			wx.FONTSTYLE_NORMAL,
			wx.FONTWEIGHT_BOLD
		)
		self.lbl_nombre.SetFont(fuente_titulo)
		
		# Versión
		self.lbl_version = wx.StaticText(
			self,
			label=f"Versión {VERSION_APP}"
		)
		
		# Descripción
		descripcion = (
			"Aplicación para crear libros EPUB 3 totalmente accesibles,\n"
			"cumpliendo con las pautas WCAG 2.1/2.2 y\n"
			"EPUB Accessibility 1.1.\n\n"
			"Diseñada para ser completamente usable con\n"
			"teclado y lectores de pantalla."
		)
		self.lbl_descripcion = wx.StaticText(
			self,
			label=descripcion,
			style=wx.ALIGN_CENTER
		)
		
		# Tecnologías
		tecnologias = (
			"Desarrollado con:\n"
			"• Python 3\n"
			"• wxPython (interfaz gráfica)\n"
			"• EbookLib (generación EPUB)\n"
			"• Markdown (conversión de texto)\n"
			"• BeautifulSoup (procesamiento HTML)"
		)
		self.lbl_tecnologias = wx.StaticText(
			self,
			label=tecnologias
		)
		
		# Copyright
		self.lbl_copyright = wx.StaticText(
			self,
			label="© 2025 - Software de código abierto\n@hxebolax"
		)
		
		# Botón cerrar
		self.btn_cerrar = wx.Button(self, wx.ID_OK, label="&Cerrar")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del diálogo."""
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		sizer.Add(self.lbl_nombre, 0, wx.ALL | wx.ALIGN_CENTER, 15)
		sizer.Add(self.lbl_version, 0, wx.BOTTOM | wx.ALIGN_CENTER, 15)
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
		sizer.Add(self.lbl_descripcion, 0, wx.ALL | wx.ALIGN_CENTER, 15)
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
		sizer.Add(self.lbl_tecnologias, 0, wx.ALL, 15)
		sizer.Add(self.lbl_copyright, 0, wx.ALL | wx.ALIGN_CENTER, 10)
		sizer.Add(self.btn_cerrar, 0, wx.ALL | wx.ALIGN_CENTER, 10)
		
		self.SetSizer(sizer)
		self.btn_cerrar.SetFocus()
