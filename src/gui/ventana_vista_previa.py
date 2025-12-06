# -*- coding: utf-8 -*-
"""
Ventana de Vista Previa del EPUB.
Muestra una representación visual del libro antes de exportar.
"""

import wx
import wx.html2
import os
from typing import Optional

from ..modelo.proyecto import Proyecto
from ..modelo.seccion import Seccion, TipoSeccion


class VentanaVistaPrevia(wx.Frame):
	"""
	Ventana de vista previa del EPUB.
	
	Muestra el contenido del libro con los estilos CSS aplicados.
	"""
	
	# CSS para la vista previa
	CSS_PREVIEW = '''
body {
	font-family: Georgia, "Times New Roman", serif;
	font-size: 14px;
	line-height: 1.6;
	margin: 20px;
	padding: 0;
	max-width: 800px;
	margin-left: auto;
	margin-right: auto;
}
h1, h2, h3, h4, h5, h6 {
	font-family: Arial, Helvetica, sans-serif;
	line-height: 1.3;
	margin-top: 1.5em;
	margin-bottom: 0.5em;
}
h1 { font-size: 1.8em; border-bottom: 1px solid #ccc; padding-bottom: 0.3em; }
h2 { font-size: 1.5em; }
h3 { font-size: 1.3em; }
p { margin: 0.5em 0; text-align: justify; }
blockquote {
	margin: 1em 2em;
	padding: 0.5em 1em;
	border-left: 3px solid #666;
	font-style: italic;
	background-color: #f9f9f9;
}
ul, ol { margin: 0.5em 0; padding-left: 2em; }
figure { margin: 1em 0; text-align: center; }
img { max-width: 100%; height: auto; }
figcaption { font-size: 0.9em; font-style: italic; margin-top: 0.5em; }
.portada { text-align: center; padding: 2em 0; }
.portada img { max-height: 80vh; }
.nav-section { padding: 1em; background: #f5f5f5; margin-bottom: 1em; }
.nav-section h3 { margin: 0 0 0.5em 0; }
.nav-section ul { list-style: none; padding: 0; margin: 0; }
.nav-section li { padding: 0.3em 0; }
.nav-section a { color: #0066cc; text-decoration: none; }
.nav-section a:hover { text-decoration: underline; }
'''
	
	def __init__(self, parent, proyecto: Proyecto):
		"""
		Inicializa la ventana de vista previa.
		
		Args:
			parent: Ventana padre
			proyecto: Proyecto a previsualizar
		"""
		super().__init__(
			parent,
			title=f"Vista previa - {proyecto.metadatos.titulo or 'Sin título'}",
			size=(900, 700),
			style=wx.DEFAULT_FRAME_STYLE
		)
		
		self.parent = parent
		self.proyecto = proyecto
		self.indice_seccion_actual = -1
		
		self._crear_controles()
		self._configurar_layout()
		self._configurar_eventos()
		self._cargar_proyecto()
		
		self.Centre()
	
	def _crear_controles(self) -> None:
		"""Crea los controles de la ventana."""
		self.panel = wx.Panel(self)
		
		# Barra de navegación
		self.btn_anterior = wx.Button(self.panel, label="◀ &Anterior")
		self.btn_anterior.SetToolTip("Sección anterior")
		
		self.lbl_seccion = wx.StaticText(
			self.panel,
			label="",
			style=wx.ALIGN_CENTER
		)
		
		self.btn_siguiente = wx.Button(self.panel, label="&Siguiente ▶")
		self.btn_siguiente.SetToolTip("Sección siguiente")
		
		self.btn_actualizar = wx.Button(self.panel, label="🔄 &Actualizar")
		self.btn_actualizar.SetToolTip("Actualizar vista previa")
		
		# Lista de secciones (índice)
		self.lbl_indice = wx.StaticText(self.panel, label="Índice:")
		self.lst_secciones = wx.ListBox(self.panel, size=(200, -1))
		self.lst_secciones.SetName("Índice del libro")
		
		# Vista previa (WebView)
		try:
			self.webview = wx.html2.WebView.New(self.panel)
			self.webview.SetName("Vista previa del contenido")
		except Exception:
			self.webview = None
		
		# Botón cerrar
		self.btn_cerrar = wx.Button(self.panel, wx.ID_CLOSE, label="&Cerrar")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout de la ventana."""
		# Barra de navegación
		sizer_nav = wx.BoxSizer(wx.HORIZONTAL)
		sizer_nav.Add(self.btn_anterior, 0, wx.RIGHT, 5)
		sizer_nav.Add(self.lbl_seccion, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 10)
		sizer_nav.Add(self.btn_siguiente, 0, wx.LEFT, 5)
		sizer_nav.Add(self.btn_actualizar, 0, wx.LEFT, 20)
		
		# Panel izquierdo (índice)
		sizer_izq = wx.BoxSizer(wx.VERTICAL)
		sizer_izq.Add(self.lbl_indice, 0, wx.BOTTOM, 5)
		sizer_izq.Add(self.lst_secciones, 1, wx.EXPAND)
		
		# Panel central (contenido)
		sizer_contenido = wx.BoxSizer(wx.HORIZONTAL)
		sizer_contenido.Add(sizer_izq, 0, wx.EXPAND | wx.RIGHT, 10)
		if self.webview:
			sizer_contenido.Add(self.webview, 1, wx.EXPAND)
		
		# Sizer principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(sizer_nav, 0, wx.EXPAND | wx.ALL, 10)
		sizer.Add(wx.StaticLine(self.panel), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		sizer.Add(sizer_contenido, 1, wx.EXPAND | wx.ALL, 10)
		sizer.Add(self.btn_cerrar, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
		
		self.panel.SetSizer(sizer)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos de la ventana."""
		self.btn_anterior.Bind(wx.EVT_BUTTON, self.on_anterior)
		self.btn_siguiente.Bind(wx.EVT_BUTTON, self.on_siguiente)
		self.btn_actualizar.Bind(wx.EVT_BUTTON, self.on_actualizar)
		self.btn_cerrar.Bind(wx.EVT_BUTTON, self.on_cerrar)
		self.lst_secciones.Bind(wx.EVT_LISTBOX, self.on_seleccionar_seccion)
		self.Bind(wx.EVT_CLOSE, self.on_cerrar)
		
		# Atajos de teclado
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
	
	def _cargar_proyecto(self) -> None:
		"""Carga el proyecto en la vista previa."""
		# Llenar lista de secciones
		self.lst_secciones.Clear()
		
		# Agregar portada si existe
		if self.proyecto.portada:
			self.lst_secciones.Append("📖 Portada")
		
		# Agregar secciones
		for seccion in self.proyecto.secciones:
			titulo = seccion.titulo or TipoSeccion.obtener_nombre_legible(seccion.tipo)
			self.lst_secciones.Append(f"  {titulo}")
		
		# Mostrar primera página
		if self.lst_secciones.GetCount() > 0:
			self.navegar_seccion(0)
	
	def navegar_seccion(self, indice: int) -> None:
		"""
		Navega a una sección específica.
		
		Args:
			indice: Índice de la sección (0 = portada si existe)
		"""
		total = self.lst_secciones.GetCount()
		if total == 0 or indice < 0 or indice >= total:
			return
		
		self.indice_seccion_actual = indice
		self.lst_secciones.SetSelection(indice)
		
		# Actualizar etiqueta
		self.lbl_seccion.SetLabel(f"Página {indice + 1} de {total}")
		
		# Actualizar botones
		self.btn_anterior.Enable(indice > 0)
		self.btn_siguiente.Enable(indice < total - 1)
		
		# Renderizar contenido
		html_contenido = self._renderizar_pagina(indice)
		if self.webview:
			self.webview.SetPage(html_contenido, "")
	
	def _renderizar_pagina(self, indice: int) -> str:
		"""
		Renderiza una página como HTML.
		
		Args:
			indice: Índice de la página
		
		Returns:
			str: HTML completo de la página
		"""
		tiene_portada = self.proyecto.portada is not None
		
		if tiene_portada and indice == 0:
			# Renderizar portada
			return self._renderizar_portada()
		
		# Ajustar índice si hay portada
		indice_seccion = indice - 1 if tiene_portada else indice
		
		if 0 <= indice_seccion < len(self.proyecto.secciones):
			seccion = self.proyecto.secciones[indice_seccion]
			return self._renderizar_seccion(seccion)
		
		return self._generar_html("<p>Contenido no disponible</p>")
	
	def _renderizar_portada(self) -> str:
		"""Renderiza la página de portada."""
		if not self.proyecto.portada:
			return self._generar_html("<p>Sin portada</p>")
		
		portada = self.proyecto.portada
		alt_text = portada.texto_alternativo or "Portada del libro"
		
		# Intentar cargar imagen como base64 o usar ruta
		if os.path.exists(portada.ruta):
			import base64
			try:
				with open(portada.ruta, 'rb') as f:
					datos = base64.b64encode(f.read()).decode('utf-8')
				mime = portada.obtener_tipo_mime()
				src = f"data:{mime};base64,{datos}"
			except Exception:
				src = portada.ruta
		else:
			src = portada.ruta
		
		contenido = f'''
<div class="portada">
	<h1>{self.proyecto.metadatos.titulo or "Sin título"}</h1>
	<img src="{src}" alt="{alt_text}"/>
	<p><em>{", ".join(self.proyecto.metadatos.autores) or "Autor desconocido"}</em></p>
</div>
'''
		return self._generar_html(contenido)
	
	def _renderizar_seccion(self, seccion: Seccion) -> str:
		"""
		Renderiza una sección como HTML.
		
		Args:
			seccion: Sección a renderizar
		
		Returns:
			str: HTML de la sección
		"""
		titulo = seccion.titulo or TipoSeccion.obtener_nombre_legible(seccion.tipo)
		nivel = seccion.nivel_encabezado
		
		contenido = f"<h{nivel}>{titulo}</h{nivel}>\n"
		contenido += seccion.contenido_xhtml or "<p><em>Sin contenido</em></p>"
		
		return self._generar_html(contenido)
	
	def _generar_html(self, contenido: str) -> str:
		"""
		Genera un documento HTML completo.
		
		Args:
			contenido: Contenido del body
		
		Returns:
			str: HTML completo
		"""
		return f'''<!DOCTYPE html>
<html lang="{self.proyecto.metadatos.idioma or 'es'}">
<head>
<meta charset="UTF-8">
<title>Vista previa</title>
<style>
{self.CSS_PREVIEW}
</style>
</head>
<body>
{contenido}
</body>
</html>'''
	
	def actualizar(self) -> None:
		"""Actualiza la vista previa con los datos actuales."""
		self._cargar_proyecto()
	
	# === Eventos ===
	
	def on_anterior(self, event) -> None:
		"""Navega a la sección anterior."""
		if self.indice_seccion_actual > 0:
			self.navegar_seccion(self.indice_seccion_actual - 1)
	
	def on_siguiente(self, event) -> None:
		"""Navega a la sección siguiente."""
		total = self.lst_secciones.GetCount()
		if self.indice_seccion_actual < total - 1:
			self.navegar_seccion(self.indice_seccion_actual + 1)
	
	def on_actualizar(self, event) -> None:
		"""Actualiza la vista previa."""
		self.actualizar()
	
	def on_seleccionar_seccion(self, event) -> None:
		"""Maneja la selección de una sección en el índice."""
		indice = self.lst_secciones.GetSelection()
		if indice != wx.NOT_FOUND:
			self.navegar_seccion(indice)
	
	def on_cerrar(self, event) -> None:
		"""Cierra la ventana y devuelve el foco."""
		if self.parent:
			self.parent.SetFocus()
		self.Destroy()
	
	def on_key_down(self, event) -> None:
		"""Maneja atajos de teclado."""
		key = event.GetKeyCode()
		
		if key == wx.WXK_ESCAPE:
			self.on_cerrar(None)
		elif key == wx.WXK_LEFT or key == wx.WXK_PAGEUP:
			self.on_anterior(None)
		elif key == wx.WXK_RIGHT or key == wx.WXK_PAGEDOWN:
			self.on_siguiente(None)
		elif key == wx.WXK_F5:
			self.on_actualizar(None)
		else:
			event.Skip()
