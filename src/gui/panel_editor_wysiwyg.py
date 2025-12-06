# -*- coding: utf-8 -*-
"""
Panel de Editor WYSIWYG.
Editor visual de contenido con formato rico.
"""

import wx
import wx.html2
import html
from typing import Optional

from ..modelo.seccion import Seccion, TipoSeccion
from ..modelo.imagen import Imagen


class PanelEditorWYSIWYG(wx.Panel):
	"""
	Panel de editor WYSIWYG con soporte para formato rico.
	
	Permite alternar entre modo visual y modo código.
	"""
	
	# Plantilla HTML para el editor
	PLANTILLA_HTML = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{
	font-family: Georgia, "Times New Roman", serif;
	font-size: 14px;
	line-height: 1.6;
	padding: 10px;
	margin: 0;
}}
h1, h2, h3, h4, h5, h6 {{
	font-family: Arial, sans-serif;
	margin: 0.5em 0;
}}
h1 {{ font-size: 1.8em; }}
h2 {{ font-size: 1.5em; }}
h3 {{ font-size: 1.3em; }}
p {{ margin: 0.5em 0; }}
blockquote {{
	margin: 1em 2em;
	padding-left: 1em;
	border-left: 3px solid #ccc;
	font-style: italic;
}}
ul, ol {{ margin: 0.5em 0; padding-left: 2em; }}
img {{ max-width: 100%; height: auto; }}
figure {{ margin: 1em 0; text-align: center; }}
figcaption {{ font-size: 0.9em; font-style: italic; }}
</style>
</head>
<body contenteditable="true">
{contenido}
</body>
</html>'''
	
	def __init__(self, parent, ventana_principal):
		"""
		Inicializa el panel de editor WYSIWYG.
		
		Args:
			parent: Widget padre
			ventana_principal: Referencia a la ventana principal
		"""
		super().__init__(parent)
		
		self.ventana_principal = ventana_principal
		self.seccion_actual: Optional[Seccion] = None
		self.contenido_modificado = False
		self.modo_visual = True
		
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
		tipos = [TipoSeccion.obtener_nombre_legible(t) for t in TipoSeccion]
		self.cmb_tipo = wx.ComboBox(self, choices=tipos, style=wx.CB_READONLY)
		self.cmb_tipo.SetName("Tipo de sección")
		
		# Nivel de encabezado
		self.lbl_nivel = wx.StaticText(self, label="&Nivel:")
		self.spin_nivel = wx.SpinCtrl(self, min=1, max=6, initial=1)
		self.spin_nivel.SetName("Nivel de encabezado")
		
		# Barra de formato
		self.btn_negrita = wx.Button(self, label="&B", size=(35, -1))
		self.btn_negrita.SetToolTip("Negrita (Ctrl+B)")
		self.btn_negrita.SetFont(wx.Font(wx.FontInfo().Bold()))
		
		self.btn_cursiva = wx.Button(self, label="&I", size=(35, -1))
		self.btn_cursiva.SetToolTip("Cursiva (Ctrl+I)")
		self.btn_cursiva.SetFont(wx.Font(wx.FontInfo().Italic()))
		
		self.btn_subrayado = wx.Button(self, label="&U", size=(35, -1))
		self.btn_subrayado.SetToolTip("Subrayado (Ctrl+U)")
		
		# Separador
		self.sep1 = wx.StaticLine(self, style=wx.LI_VERTICAL)
		
		# Encabezados
		self.cmb_encabezado = wx.Choice(
			self,
			choices=["Párrafo", "H1", "H2", "H3", "H4", "H5", "H6"]
		)
		self.cmb_encabezado.SetSelection(0)
		self.cmb_encabezado.SetToolTip("Tipo de bloque")
		
		# Listas
		self.btn_lista = wx.Button(self, label="• Lista", size=(60, -1))
		self.btn_lista.SetToolTip("Lista con viñetas")
		
		self.btn_lista_num = wx.Button(self, label="1. Lista", size=(60, -1))
		self.btn_lista_num.SetToolTip("Lista numerada")
		
		self.btn_cita = wx.Button(self, label="❝ Cita", size=(60, -1))
		self.btn_cita.SetToolTip("Bloque de cita")
		
		# Separador
		self.sep2 = wx.StaticLine(self, style=wx.LI_VERTICAL)
		
		# Imagen
		self.btn_imagen = wx.Button(self, label="🖼 Imagen", size=(80, -1))
		self.btn_imagen.SetToolTip("Insertar imagen (Ctrl+Shift+I)")
		
		# Alternar modo
		self.btn_modo = wx.ToggleButton(self, label="Código")
		self.btn_modo.SetToolTip("Alternar entre modo visual y código")
		
		# Editor visual (WebView)
		try:
			self.webview = wx.html2.WebView.New(self)
			self.webview.SetName("Editor visual de contenido")
		except Exception:
			# Fallback si WebView no está disponible
			self.webview = None
		
		# Editor de código (TextCtrl)
		self.txt_codigo = wx.TextCtrl(
			self,
			style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.HSCROLL
		)
		self.txt_codigo.SetName("Editor de código XHTML")
		self.txt_codigo.Hide()
		
		# Botón guardar
		self.btn_guardar = wx.Button(self, label="&Guardar cambios")
		self.btn_guardar.SetToolTip("Guardar cambios en la sección (Ctrl+S)")
		
		# Estado inicial
		self._habilitar_controles(False)
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del panel."""
		# Info de sección
		sizer_info = wx.FlexGridSizer(3, 2, 5, 10)
		sizer_info.AddGrowableCol(1)
		sizer_info.Add(self.lbl_titulo, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer_info.Add(self.txt_titulo, 1, wx.EXPAND)
		sizer_info.Add(self.lbl_tipo, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer_info.Add(self.cmb_tipo, 0)
		sizer_info.Add(self.lbl_nivel, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer_info.Add(self.spin_nivel, 0)
		
		# Barra de formato
		sizer_formato = wx.BoxSizer(wx.HORIZONTAL)
		sizer_formato.Add(self.btn_negrita, 0, wx.RIGHT, 2)
		sizer_formato.Add(self.btn_cursiva, 0, wx.RIGHT, 2)
		sizer_formato.Add(self.btn_subrayado, 0, wx.RIGHT, 5)
		sizer_formato.Add(self.sep1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		sizer_formato.Add(self.cmb_encabezado, 0, wx.RIGHT, 5)
		sizer_formato.Add(self.btn_lista, 0, wx.RIGHT, 2)
		sizer_formato.Add(self.btn_lista_num, 0, wx.RIGHT, 2)
		sizer_formato.Add(self.btn_cita, 0, wx.RIGHT, 5)
		sizer_formato.Add(self.sep2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		sizer_formato.Add(self.btn_imagen, 0, wx.RIGHT, 10)
		sizer_formato.AddStretchSpacer()
		sizer_formato.Add(self.btn_modo, 0)
		
		# Sizer principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.lbl_seccion, 0, wx.ALL, 5)
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		sizer.Add(sizer_info, 0, wx.EXPAND | wx.ALL, 5)
		sizer.Add(sizer_formato, 0, wx.EXPAND | wx.ALL, 5)
		
		if self.webview:
			sizer.Add(self.webview, 1, wx.EXPAND | wx.ALL, 5)
		sizer.Add(self.txt_codigo, 1, wx.EXPAND | wx.ALL, 5)
		sizer.Add(self.btn_guardar, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
		
		self.SetSizer(sizer)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del panel."""
		self.txt_titulo.Bind(wx.EVT_TEXT, self.on_cambio)
		self.cmb_tipo.Bind(wx.EVT_COMBOBOX, self.on_cambio)
		self.spin_nivel.Bind(wx.EVT_SPINCTRL, self.on_cambio)
		self.txt_codigo.Bind(wx.EVT_TEXT, self.on_cambio)
		
		# Formato
		self.btn_negrita.Bind(wx.EVT_BUTTON, lambda e: self.aplicar_formato('bold'))
		self.btn_cursiva.Bind(wx.EVT_BUTTON, lambda e: self.aplicar_formato('italic'))
		self.btn_subrayado.Bind(wx.EVT_BUTTON, lambda e: self.aplicar_formato('underline'))
		self.cmb_encabezado.Bind(wx.EVT_CHOICE, self.on_cambiar_bloque)
		self.btn_lista.Bind(wx.EVT_BUTTON, lambda e: self.aplicar_formato('insertUnorderedList'))
		self.btn_lista_num.Bind(wx.EVT_BUTTON, lambda e: self.aplicar_formato('insertOrderedList'))
		self.btn_cita.Bind(wx.EVT_BUTTON, self.on_insertar_cita)
		self.btn_imagen.Bind(wx.EVT_BUTTON, self.on_insertar_imagen)
		
		# Modo
		self.btn_modo.Bind(wx.EVT_TOGGLEBUTTON, self.on_alternar_modo)
		
		# Guardar
		self.btn_guardar.Bind(wx.EVT_BUTTON, self.on_guardar)
		
		# Atajos de teclado
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
	
	def _habilitar_controles(self, habilitar: bool) -> None:
		"""Habilita o deshabilita los controles."""
		self.txt_titulo.Enable(habilitar)
		self.cmb_tipo.Enable(habilitar)
		self.spin_nivel.Enable(habilitar)
		self.btn_negrita.Enable(habilitar)
		self.btn_cursiva.Enable(habilitar)
		self.btn_subrayado.Enable(habilitar)
		self.cmb_encabezado.Enable(habilitar)
		self.btn_lista.Enable(habilitar)
		self.btn_lista_num.Enable(habilitar)
		self.btn_cita.Enable(habilitar)
		self.btn_imagen.Enable(habilitar)
		self.btn_modo.Enable(habilitar)
		self.btn_guardar.Enable(habilitar)
		if self.webview:
			self.webview.Enable(habilitar)
		self.txt_codigo.Enable(habilitar)
	
	def cargar_seccion(self, seccion: Optional[Seccion]) -> None:
		"""Carga una sección para editar."""
		if self.contenido_modificado and self.seccion_actual:
			self._guardar_cambios()
		
		self.seccion_actual = seccion
		self.contenido_modificado = False
		
		if seccion is None:
			self.limpiar()
			return
		
		self.lbl_seccion.SetLabel(f"Editando: {seccion.obtener_nombre_legible()}")
		self.txt_titulo.ChangeValue(seccion.titulo)
		
		nombre_tipo = TipoSeccion.obtener_nombre_legible(seccion.tipo)
		indice = self.cmb_tipo.FindString(nombre_tipo)
		if indice != wx.NOT_FOUND:
			self.cmb_tipo.SetSelection(indice)
		
		self.spin_nivel.SetValue(seccion.nivel_encabezado)
		self.cargar_contenido(seccion.contenido_xhtml)
		self._habilitar_controles(True)
	
	def limpiar(self) -> None:
		"""Limpia el editor."""
		self.seccion_actual = None
		self.contenido_modificado = False
		self.lbl_seccion.SetLabel("Ninguna sección seleccionada")
		self.txt_titulo.ChangeValue("")
		self.cmb_tipo.SetSelection(0)
		self.spin_nivel.SetValue(1)
		self.cargar_contenido("")
		self._habilitar_controles(False)
	
	def cargar_contenido(self, xhtml: str) -> None:
		"""Carga contenido XHTML en el editor."""
		self.txt_codigo.ChangeValue(xhtml)
		
		if self.webview and self.modo_visual:
			html_completo = self.PLANTILLA_HTML.format(contenido=xhtml or "")
			self.webview.SetPage(html_completo, "")
	
	def obtener_contenido(self) -> str:
		"""Obtiene el contenido como XHTML."""
		if self.modo_visual and self.webview:
			# Obtener contenido del WebView
			script = "document.body.innerHTML"
			self.webview.RunScript(script)
			# Por simplicidad, usamos el contenido del txt_codigo
			# ya que RunScript es asíncrono
			return self.txt_codigo.GetValue()
		return self.txt_codigo.GetValue()
	
	def aplicar_formato(self, comando: str) -> None:
		"""Aplica un comando de formato."""
		if self.modo_visual and self.webview:
			self.webview.RunScript(f"document.execCommand('{comando}', false, null)")
			self.contenido_modificado = True
		elif not self.modo_visual:
			# En modo código, insertar etiquetas
			etiquetas = {
				'bold': ('<strong>', '</strong>'),
				'italic': ('<em>', '</em>'),
				'underline': ('<u>', '</u>'),
				'insertUnorderedList': ('<ul>\n  <li>', '</li>\n</ul>'),
				'insertOrderedList': ('<ol>\n  <li>', '</li>\n</ol>')
			}
			if comando in etiquetas:
				apertura, cierre = etiquetas[comando]
				self._insertar_etiqueta(apertura, cierre)
	
	def _insertar_etiqueta(self, apertura: str, cierre: str) -> None:
		"""Inserta etiquetas en modo código."""
		seleccion = self.txt_codigo.GetStringSelection()
		if seleccion:
			self.txt_codigo.WriteText(f"{apertura}{seleccion}{cierre}")
		else:
			pos = self.txt_codigo.GetInsertionPoint()
			self.txt_codigo.WriteText(f"{apertura}{cierre}")
			self.txt_codigo.SetInsertionPoint(pos + len(apertura))
		self.contenido_modificado = True
	
	def on_cambiar_bloque(self, event) -> None:
		"""Cambia el tipo de bloque."""
		idx = self.cmb_encabezado.GetSelection()
		if idx == 0:
			tag = "p"
		else:
			tag = f"h{idx}"
		
		if self.modo_visual and self.webview:
			self.webview.RunScript(f"document.execCommand('formatBlock', false, '{tag}')")
		else:
			self._insertar_etiqueta(f"<{tag}>", f"</{tag}>")
		
		self.contenido_modificado = True
	
	def on_insertar_cita(self, event) -> None:
		"""Inserta un bloque de cita."""
		if self.modo_visual and self.webview:
			self.webview.RunScript("document.execCommand('formatBlock', false, 'blockquote')")
		else:
			self._insertar_etiqueta("<blockquote>\n  <p>", "</p>\n</blockquote>")
		self.contenido_modificado = True
	
	def on_insertar_imagen(self, event) -> None:
		"""Muestra el diálogo para insertar imagen."""
		if not self.seccion_actual:
			return
		
		from .dialogos.dialogo_insertar_imagen import DialogoInsertarImagen
		
		directorio = self.ventana_principal.preferencias.directorio_importacion
		dialogo = DialogoInsertarImagen(self, directorio_inicial=directorio)
		
		if dialogo.ShowModal() == wx.ID_OK:
			imagen = dialogo.obtener_imagen()
			if imagen:
				self.seccion_actual.agregar_imagen(imagen)
				xhtml = self._generar_xhtml_imagen(imagen)
				
				if self.modo_visual and self.webview:
					self.webview.RunScript(
						f"document.execCommand('insertHTML', false, '{xhtml}')"
					)
				else:
					self.txt_codigo.WriteText(xhtml)
				
				self.contenido_modificado = True
		
		dialogo.Destroy()
	
	def _generar_xhtml_imagen(self, imagen: Imagen) -> str:
		"""Genera XHTML para una imagen."""
		alt_text = html.escape(imagen.texto_alternativo)
		src = f"../imagenes/{imagen.obtener_nombre_epub()}"
		
		if imagen.descripcion_larga:
			desc_id = f"desc-{imagen.id}"
			desc_text = html.escape(imagen.descripcion_larga)
			return f'<figure><img src="{src}" alt="{alt_text}" aria-describedby="{desc_id}"/><figcaption id="{desc_id}">{desc_text}</figcaption></figure>'
		return f'<img src="{src}" alt="{alt_text}"/>'
	
	def on_alternar_modo(self, event) -> None:
		"""Alterna entre modo visual y código."""
		self.modo_visual = not self.btn_modo.GetValue()
		
		if self.modo_visual:
			# Cambiar a visual
			self.btn_modo.SetLabel("Código")
			if self.webview:
				contenido = self.txt_codigo.GetValue()
				html_completo = self.PLANTILLA_HTML.format(contenido=contenido)
				self.webview.SetPage(html_completo, "")
				self.webview.Show()
			self.txt_codigo.Hide()
		else:
			# Cambiar a código
			self.btn_modo.SetLabel("Visual")
			if self.webview:
				self.webview.Hide()
			self.txt_codigo.Show()
		
		self.Layout()
	
	def es_modo_visual(self) -> bool:
		"""Retorna True si está en modo visual."""
		return self.modo_visual
	
	def on_cambio(self, event) -> None:
		"""Maneja cambios en los controles."""
		self.contenido_modificado = True
		event.Skip()
	
	def on_guardar(self, event) -> None:
		"""Guarda los cambios."""
		self._guardar_cambios()
		self.ventana_principal.registrar_log("Cambios guardados en la sección")
	
	def _guardar_cambios(self) -> None:
		"""Guarda los cambios en la sección actual."""
		if not self.seccion_actual:
			return
		
		self.seccion_actual.establecer_titulo(self.txt_titulo.GetValue())
		
		indice_tipo = self.cmb_tipo.GetSelection()
		if indice_tipo != wx.NOT_FOUND:
			tipos = list(TipoSeccion)
			if indice_tipo < len(tipos):
				self.seccion_actual.establecer_tipo(tipos[indice_tipo])
		
		self.seccion_actual.nivel_encabezado = self.spin_nivel.GetValue()
		self.seccion_actual.establecer_contenido(self.obtener_contenido())
		
		self.ventana_principal.actualizar_seccion(self.seccion_actual)
		self.contenido_modificado = False
	
	def on_key_down(self, event) -> None:
		"""Maneja atajos de teclado."""
		if event.ControlDown():
			key = event.GetKeyCode()
			if key == ord('B'):
				self.aplicar_formato('bold')
				return
			elif key == ord('I') and not event.ShiftDown():
				self.aplicar_formato('italic')
				return
			elif key == ord('U'):
				self.aplicar_formato('underline')
				return
			elif key == ord('I') and event.ShiftDown():
				self.on_insertar_imagen(None)
				return
		event.Skip()
