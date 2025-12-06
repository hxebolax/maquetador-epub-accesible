# -*- coding: utf-8 -*-
"""
Panel de Logs.
Muestra mensajes de estado, advertencias y errores.
"""

import wx
from datetime import datetime


class PanelLogs(wx.Panel):
	"""
	Panel accesible para mostrar mensajes de log.
	
	Muestra información sobre operaciones, advertencias y errores
	de forma accesible para lectores de pantalla.
	"""
	
	def __init__(self, parent, ventana_principal):
		"""
		Inicializa el panel de logs.
		
		Args:
			parent: Widget padre
			ventana_principal: Referencia a la ventana principal
		"""
		super().__init__(parent)
		
		self.ventana_principal = ventana_principal
		
		self._crear_controles()
		self._configurar_layout()
		self._configurar_eventos()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del panel."""
		# Etiqueta
		self.etiqueta = wx.StaticText(
			self,
			label="&Mensajes:"
		)
		
		# Lista de mensajes
		self.lista = wx.ListCtrl(
			self,
			style=wx.LC_REPORT | wx.LC_SINGLE_SEL
		)
		self.lista.SetName("Panel de mensajes")
		
		# Columnas
		self.lista.InsertColumn(0, "Hora", width=80)
		self.lista.InsertColumn(1, "Tipo", width=80)
		self.lista.InsertColumn(2, "Mensaje", width=400)
		
		# Botón limpiar
		self.btn_limpiar = wx.Button(self, label="&Limpiar")
		self.btn_limpiar.SetToolTip("Limpiar todos los mensajes")
		
		# Botón copiar
		self.btn_copiar = wx.Button(self, label="C&opiar")
		self.btn_copiar.SetToolTip("Copiar mensajes al portapapeles")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del panel."""
		# Sizer para botones
		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)
		sizer_botones.Add(self.btn_limpiar, 0, wx.RIGHT, 5)
		sizer_botones.Add(self.btn_copiar, 0)
		
		# Sizer principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.etiqueta, 0, wx.ALL, 5)
		sizer.Add(self.lista, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		sizer.Add(sizer_botones, 0, wx.ALL, 5)
		
		self.SetSizer(sizer)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del panel."""
		self.btn_limpiar.Bind(wx.EVT_BUTTON, self.on_limpiar)
		self.btn_copiar.Bind(wx.EVT_BUTTON, self.on_copiar)
	
	def agregar_mensaje(self, mensaje: str, tipo: str = "info") -> None:
		"""
		Agrega un mensaje al panel de logs.
		
		Args:
			mensaje: Texto del mensaje
			tipo: Tipo de mensaje (info, advertencia, error)
		"""
		# Obtener hora actual
		hora = datetime.now().strftime("%H:%M:%S")
		
		# Mapear tipo a texto legible
		tipos_texto = {
			"info": "Info",
			"advertencia": "Aviso",
			"error": "Error"
		}
		tipo_texto = tipos_texto.get(tipo, "Info")
		
		# Agregar al inicio de la lista
		indice = self.lista.InsertItem(0, hora)
		self.lista.SetItem(indice, 1, tipo_texto)
		self.lista.SetItem(indice, 2, mensaje)
		
		# Colorear según tipo
		if tipo == "error":
			self.lista.SetItemTextColour(indice, wx.RED)
		elif tipo == "advertencia":
			self.lista.SetItemTextColour(indice, wx.Colour(200, 100, 0))
		
		# Seleccionar el nuevo mensaje
		self.lista.Select(indice)
		self.lista.EnsureVisible(indice)
		
		# Limitar número de mensajes
		while self.lista.GetItemCount() > 500:
			self.lista.DeleteItem(self.lista.GetItemCount() - 1)
	
	def limpiar(self) -> None:
		"""Limpia todos los mensajes."""
		self.lista.DeleteAllItems()
	
	def obtener_mensajes(self) -> str:
		"""
		Obtiene todos los mensajes como texto.
		
		Returns:
			str: Mensajes formateados
		"""
		lineas = []
		
		for i in range(self.lista.GetItemCount()):
			hora = self.lista.GetItemText(i, 0)
			tipo = self.lista.GetItemText(i, 1)
			mensaje = self.lista.GetItemText(i, 2)
			lineas.append(f"[{hora}] [{tipo}] {mensaje}")
		
		return "\n".join(lineas)
	
	# === Eventos ===
	
	def on_limpiar(self, event) -> None:
		"""Maneja el clic en el botón Limpiar."""
		self.limpiar()
	
	def on_copiar(self, event) -> None:
		"""Maneja el clic en el botón Copiar."""
		texto = self.obtener_mensajes()
		
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(texto))
			wx.TheClipboard.Close()
			
			self.agregar_mensaje("Mensajes copiados al portapapeles")
