# -*- coding: utf-8 -*-
"""
Panel de Editor.
Editor de contenido accesible para las secciones del libro.
"""

import wx
import html
from typing import Optional

from ..modelo.seccion import Seccion, TipoSeccion
from ..modelo.imagen import Imagen


class PanelEditor(wx.Panel):
	"""
	Panel accesible para edición de contenido de secciones.
	
	Proporciona un editor de texto básico con controles de formato.
	"""
	
	def __init__(self, parent, ventana_principal):
		"""
		Inicializa el panel de editor.
		
		Args:
			parent: Widget padre
			ventana_principal: Referencia a la ventana principal
		"""
		super().__init__(parent)
		
		self.ventana_principal = ventana_principal
		self.seccion_actual: Optional[Seccion] = None
		self.contenido_modificado = False
		
		self._crear_controles()
		self._configurar_layout()
		self._configurar_eventos()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del panel."""
		# Información de la sección
		self.lbl_seccion = wx.StaticText(
			self,
			label="Ninguna sección seleccionada"
		)
		
		# Título de la sección
		self.lbl_titulo = wx.StaticText(self, label="&Título:")
		self.txt_titulo = wx.TextCtrl(self)
		self.txt_titulo.SetName("Título de la sección")
		
		# Tipo de sección
		self.lbl_tipo = wx.StaticText(self, label="T&ipo:")
		tipos = [
			TipoSeccion.obtener_nombre_legible(t) 
			for t in TipoSeccion
		]
		self.cmb_tipo = wx.ComboBox(
			self,
			choices=tipos,
			style=wx.CB_READONLY
		)
		self.cmb_tipo.SetName("Tipo de sección")
		
		# Nivel de encabezado
		self.lbl_nivel = wx.StaticText(self, label="&Nivel:")
		self.spin_nivel = wx.SpinCtrl(
			self,
			min=1,
			max=6,
			initial=1
		)
		self.spin_nivel.SetName("Nivel de encabezado")
		
		# Barra de formato
		self.btn_h1 = wx.Button(self, label="H&1", size=(40, -1))
		self.btn_h1.SetToolTip("Encabezado nivel 1")
		
		self.btn_h2 = wx.Button(self, label="H&2", size=(40, -1))
		self.btn_h2.SetToolTip("Encabezado nivel 2")
		
		self.btn_h3 = wx.Button(self, label="H&3", size=(40, -1))
		self.btn_h3.SetToolTip("Encabezado nivel 3")
		
		self.btn_parrafo = wx.Button(self, label="&P", size=(40, -1))
		self.btn_parrafo.SetToolTip("Párrafo")
		
		self.btn_lista = wx.Button(self, label="&Lista", size=(60, -1))
		self.btn_lista.SetToolTip("Lista no ordenada")
		
		self.btn_cita = wx.Button(self, label="&Cita", size=(60, -1))
		self.btn_cita.SetToolTip("Cita (blockquote)")
		
		self.btn_imagen = wx.Button(self, label="&Imagen", size=(70, -1))
		self.btn_imagen.SetToolTip("Insertar imagen (Ctrl+Shift+I)")
		
		# Editor de contenido
		self.lbl_contenido = wx.StaticText(self, label="&Contenido:")
		self.txt_contenido = wx.TextCtrl(
			self,
			style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.HSCROLL
		)
		self.txt_contenido.SetName("Contenido de la sección")
		
		# Botón guardar
		self.btn_guardar = wx.Button(self, label="&Guardar cambios")
		self.btn_guardar.SetToolTip("Guardar cambios en la sección (Ctrl+S)")
		
		# Estado inicial
		self._habilitar_controles(False)
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del panel."""
		# Sizer para información de sección
		sizer_info = wx.FlexGridSizer(3, 2, 5, 10)
		sizer_info.AddGrowableCol(1)
		
		sizer_info.Add(self.lbl_titulo, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer_info.Add(self.txt_titulo, 1, wx.EXPAND)
		
		sizer_info.Add(self.lbl_tipo, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer_info.Add(self.cmb_tipo, 0)
		
		sizer_info.Add(self.lbl_nivel, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer_info.Add(self.spin_nivel, 0)
		
		# Sizer para barra de formato
		sizer_formato = wx.BoxSizer(wx.HORIZONTAL)
		sizer_formato.Add(wx.StaticText(self, label="Formato:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
		sizer_formato.Add(self.btn_h1, 0, wx.RIGHT, 2)
		sizer_formato.Add(self.btn_h2, 0, wx.RIGHT, 2)
		sizer_formato.Add(self.btn_h3, 0, wx.RIGHT, 10)
		sizer_formato.Add(self.btn_parrafo, 0, wx.RIGHT, 2)
		sizer_formato.Add(self.btn_lista, 0, wx.RIGHT, 2)
		sizer_formato.Add(self.btn_cita, 0, wx.RIGHT, 10)
		sizer_formato.Add(self.btn_imagen, 0)
		
		# Sizer principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.lbl_seccion, 0, wx.ALL, 5)
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		sizer.Add(sizer_info, 0, wx.EXPAND | wx.ALL, 5)
		sizer.Add(sizer_formato, 0, wx.ALL, 5)
		sizer.Add(self.lbl_contenido, 0, wx.LEFT | wx.TOP, 5)
		sizer.Add(self.txt_contenido, 1, wx.EXPAND | wx.ALL, 5)
		sizer.Add(self.btn_guardar, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
		
		self.SetSizer(sizer)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del panel."""
		self.txt_titulo.Bind(wx.EVT_TEXT, self.on_cambio)
		self.cmb_tipo.Bind(wx.EVT_COMBOBOX, self.on_cambio)
		self.spin_nivel.Bind(wx.EVT_SPINCTRL, self.on_cambio)
		self.txt_contenido.Bind(wx.EVT_TEXT, self.on_cambio)
		
		self.btn_h1.Bind(wx.EVT_BUTTON, lambda e: self.insertar_encabezado(1))
		self.btn_h2.Bind(wx.EVT_BUTTON, lambda e: self.insertar_encabezado(2))
		self.btn_h3.Bind(wx.EVT_BUTTON, lambda e: self.insertar_encabezado(3))
		self.btn_parrafo.Bind(wx.EVT_BUTTON, self.on_insertar_parrafo)
		self.btn_lista.Bind(wx.EVT_BUTTON, self.on_insertar_lista)
		self.btn_cita.Bind(wx.EVT_BUTTON, self.on_insertar_cita)
		self.btn_imagen.Bind(wx.EVT_BUTTON, self.on_insertar_imagen)
		
		self.btn_guardar.Bind(wx.EVT_BUTTON, self.on_guardar)
		
		# Atajo de teclado para insertar imagen
		self.txt_contenido.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
	
	def _habilitar_controles(self, habilitar: bool) -> None:
		"""
		Habilita o deshabilita los controles de edición.
		
		Args:
			habilitar: True para habilitar, False para deshabilitar
		"""
		self.txt_titulo.Enable(habilitar)
		self.cmb_tipo.Enable(habilitar)
		self.spin_nivel.Enable(habilitar)
		self.txt_contenido.Enable(habilitar)
		self.btn_h1.Enable(habilitar)
		self.btn_h2.Enable(habilitar)
		self.btn_h3.Enable(habilitar)
		self.btn_parrafo.Enable(habilitar)
		self.btn_lista.Enable(habilitar)
		self.btn_cita.Enable(habilitar)
		self.btn_imagen.Enable(habilitar)
		self.btn_guardar.Enable(habilitar)
	
	def cargar_seccion(self, seccion: Optional[Seccion]) -> None:
		"""
		Carga una sección para editar.
		
		NO cambia el foco automáticamente - el usuario tabulará cuando quiera.
		
		Args:
			seccion: Sección a cargar (None para limpiar)
		"""
		# Guardar cambios pendientes
		if self.contenido_modificado and self.seccion_actual:
			self._guardar_cambios()
		
		self.seccion_actual = seccion
		self.contenido_modificado = False
		
		if seccion is None:
			self.limpiar()
			return
		
		# Actualizar etiqueta
		self.lbl_seccion.SetLabel(f"Editando: {seccion.obtener_nombre_legible()}")
		
		# Cargar datos
		self.txt_titulo.ChangeValue(seccion.titulo)
		
		# Seleccionar tipo
		nombre_tipo = TipoSeccion.obtener_nombre_legible(seccion.tipo)
		indice = self.cmb_tipo.FindString(nombre_tipo)
		if indice != wx.NOT_FOUND:
			self.cmb_tipo.SetSelection(indice)
		
		self.spin_nivel.SetValue(seccion.nivel_encabezado)
		
		# Cargar contenido (mostrar XHTML como texto)
		self.txt_contenido.ChangeValue(seccion.contenido_xhtml)
		
		# Habilitar controles
		self._habilitar_controles(True)
		
		# NO cambiar el foco automáticamente
		# El usuario permanece en el árbol y tabulará cuando quiera editar
	
	def limpiar(self) -> None:
		"""Limpia el editor."""
		self.seccion_actual = None
		self.contenido_modificado = False
		
		self.lbl_seccion.SetLabel("Ninguna sección seleccionada")
		self.txt_titulo.ChangeValue("")
		self.cmb_tipo.SetSelection(0)
		self.spin_nivel.SetValue(1)
		self.txt_contenido.ChangeValue("")
		
		self._habilitar_controles(False)
	
	def _guardar_cambios(self) -> None:
		"""Guarda los cambios en la sección actual."""
		if not self.seccion_actual:
			return
		
		# Actualizar sección
		self.seccion_actual.establecer_titulo(self.txt_titulo.GetValue())
		
		# Actualizar tipo
		indice_tipo = self.cmb_tipo.GetSelection()
		if indice_tipo != wx.NOT_FOUND:
			tipos = list(TipoSeccion)
			if indice_tipo < len(tipos):
				self.seccion_actual.establecer_tipo(tipos[indice_tipo])
		
		self.seccion_actual.nivel_encabezado = self.spin_nivel.GetValue()
		self.seccion_actual.establecer_contenido(self.txt_contenido.GetValue())
		
		# Notificar cambio
		self.ventana_principal.actualizar_seccion(self.seccion_actual)
		
		self.contenido_modificado = False
	
	# === Eventos ===
	
	def on_cambio(self, event) -> None:
		"""Maneja cambios en los controles."""
		self.contenido_modificado = True
		event.Skip()
	
	def on_guardar(self, event) -> None:
		"""Maneja el clic en el botón Guardar."""
		self._guardar_cambios()
		self.ventana_principal.registrar_log("Cambios guardados en la sección")
	
	def on_insertar_parrafo(self, event) -> None:
		"""Inserta etiqueta de párrafo."""
		self._insertar_etiqueta("<p>", "</p>")
	
	def on_insertar_lista(self, event) -> None:
		"""Inserta etiqueta de lista."""
		self._insertar_etiqueta("<ul>\n  <li>", "</li>\n</ul>")
	
	def on_insertar_cita(self, event) -> None:
		"""Inserta etiqueta de cita."""
		self._insertar_etiqueta("<blockquote>\n  <p>", "</p>\n</blockquote>")
	
	def insertar_encabezado(self, nivel: int) -> None:
		"""
		Inserta etiqueta de encabezado.
		
		Args:
			nivel: Nivel del encabezado (1-6)
		"""
		self._insertar_etiqueta(f"<h{nivel}>", f"</h{nivel}>")
	
	def _insertar_etiqueta(self, apertura: str, cierre: str) -> None:
		"""
		Inserta etiquetas alrededor del texto seleccionado.
		
		Args:
			apertura: Etiqueta de apertura
			cierre: Etiqueta de cierre
		"""
		seleccion = self.txt_contenido.GetStringSelection()
		
		if seleccion:
			# Envolver selección
			nuevo_texto = f"{apertura}{seleccion}{cierre}"
			self.txt_contenido.WriteText(nuevo_texto)
		else:
			# Insertar etiquetas vacías
			pos = self.txt_contenido.GetInsertionPoint()
			self.txt_contenido.WriteText(f"{apertura}{cierre}")
			# Posicionar cursor entre etiquetas
			self.txt_contenido.SetInsertionPoint(pos + len(apertura))
		
		self.contenido_modificado = True
		self.txt_contenido.SetFocus()
	
	def on_key_down(self, event) -> None:
		"""Maneja atajos de teclado en el editor."""
		# Ctrl+Shift+I para insertar imagen
		if event.ControlDown() and event.ShiftDown() and event.GetKeyCode() == ord('I'):
			self.on_insertar_imagen(None)
		else:
			event.Skip()
	
	def on_insertar_imagen(self, event) -> None:
		"""Muestra el diálogo para insertar una imagen."""
		if not self.seccion_actual:
			return
		
		from .dialogos.dialogo_insertar_imagen import DialogoInsertarImagen
		
		# Obtener directorio inicial de preferencias
		directorio = self.ventana_principal.preferencias.directorio_importacion
		
		dialogo = DialogoInsertarImagen(
			self,
			imagen_existente=None,
			directorio_inicial=directorio
		)
		
		if dialogo.ShowModal() == wx.ID_OK:
			imagen = dialogo.obtener_imagen()
			if imagen:
				self.insertar_imagen(imagen)
		
		dialogo.Destroy()
	
	def insertar_imagen(self, imagen: Imagen) -> None:
		"""
		Inserta una imagen en el contenido.
		
		Args:
			imagen: Imagen a insertar
		"""
		if not self.seccion_actual:
			return
		
		# Agregar imagen a la sección
		self.seccion_actual.agregar_imagen(imagen)
		
		# Generar XHTML para la imagen
		xhtml = self._generar_xhtml_imagen(imagen)
		
		# Insertar en el editor
		self.txt_contenido.WriteText(xhtml)
		
		self.contenido_modificado = True
		self.ventana_principal.registrar_log(f"Imagen insertada: {imagen.obtener_nombre_archivo()}")
	
	def _generar_xhtml_imagen(self, imagen: Imagen) -> str:
		"""
		Genera el XHTML para una imagen con accesibilidad.
		
		Args:
			imagen: Imagen para generar XHTML
		
		Returns:
			str: XHTML de la imagen
		"""
		alt_text = html.escape(imagen.texto_alternativo)
		# Ruta relativa para el EPUB
		src = f"../imagenes/{imagen.obtener_nombre_epub()}"
		
		if imagen.descripcion_larga:
			# Con descripción larga, usar figure
			desc_id = f"desc-{imagen.id}"
			desc_text = html.escape(imagen.descripcion_larga)
			return f'''<figure>
  <img src="{src}" alt="{alt_text}" aria-describedby="{desc_id}"/>
  <figcaption id="{desc_id}">{desc_text}</figcaption>
</figure>'''
		else:
			# Sin descripción larga, solo img
			return f'<img src="{src}" alt="{alt_text}"/>'
	
	def editar_imagen(self, imagen: Imagen) -> None:
		"""
		Abre el diálogo para editar una imagen existente.
		
		Args:
			imagen: Imagen a editar
		"""
		from .dialogos.dialogo_insertar_imagen import DialogoInsertarImagen
		
		dialogo = DialogoInsertarImagen(
			self,
			imagen_existente=imagen
		)
		
		if dialogo.ShowModal() == wx.ID_OK:
			imagen_editada = dialogo.obtener_imagen()
			if imagen_editada:
				self.contenido_modificado = True
				self.ventana_principal.registrar_log(f"Imagen editada: {imagen.obtener_nombre_archivo()}")
		
		dialogo.Destroy()
	
	def eliminar_imagen(self, imagen: Imagen) -> None:
		"""
		Elimina una imagen de la sección.
		
		Args:
			imagen: Imagen a eliminar
		"""
		if not self.seccion_actual:
			return
		
		self.seccion_actual.eliminar_imagen(imagen.id)
		self.contenido_modificado = True
		self.ventana_principal.registrar_log(f"Imagen eliminada: {imagen.obtener_nombre_archivo()}")
