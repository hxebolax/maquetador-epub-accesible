# -*- coding: utf-8 -*-
"""
Panel de Secciones.
Muestra y gestiona la estructura de secciones del libro.
"""

import wx
from typing import Optional, Dict

from ..modelo.seccion import Seccion, TipoSeccion


class PanelSecciones(wx.Panel):
	"""
	Panel accesible para gestión de secciones del libro.
	
	Utiliza un TreeCtrl para mostrar la estructura jerárquica
	y proporciona controles para agregar, eliminar y reordenar.
	"""
	
	def __init__(self, parent, ventana_principal):
		"""
		Inicializa el panel de secciones.
		
		Args:
			parent: Widget padre
			ventana_principal: Referencia a la ventana principal
		"""
		super().__init__(parent)
		
		self.ventana_principal = ventana_principal
		self.secciones_items: Dict[str, wx.TreeItemId] = {}
		
		self._crear_controles()
		self._configurar_layout()
		self._configurar_eventos()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del panel."""
		# Etiqueta
		self.etiqueta = wx.StaticText(
			self,
			label="&Estructura del libro:"
		)
		
		# Árbol de secciones
		self.arbol = wx.TreeCtrl(
			self,
			style=wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT | 
			      wx.TR_SINGLE | wx.TR_EDIT_LABELS
		)
		self.arbol.SetName("Estructura del libro")
		
		# Botones de acción
		self.btn_agregar = wx.Button(self, label="&Agregar")
		self.btn_agregar.SetToolTip("Agregar nueva sección (Ctrl+Shift+A)")
		
		self.btn_eliminar = wx.Button(self, label="&Eliminar")
		self.btn_eliminar.SetToolTip("Eliminar sección seleccionada")
		
		self.btn_subir = wx.Button(self, label="S&ubir")
		self.btn_subir.SetToolTip("Mover sección hacia arriba")
		
		self.btn_bajar = wx.Button(self, label="&Bajar")
		self.btn_bajar.SetToolTip("Mover sección hacia abajo")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del panel."""
		# Sizer para botones
		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)
		sizer_botones.Add(self.btn_agregar, 0, wx.RIGHT, 5)
		sizer_botones.Add(self.btn_eliminar, 0, wx.RIGHT, 5)
		sizer_botones.Add(self.btn_subir, 0, wx.RIGHT, 5)
		sizer_botones.Add(self.btn_bajar, 0)
		
		# Sizer principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.etiqueta, 0, wx.ALL, 5)
		sizer.Add(self.arbol, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		sizer.Add(sizer_botones, 0, wx.ALL | wx.ALIGN_CENTER, 5)
		
		self.SetSizer(sizer)
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del panel."""
		self.arbol.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_seleccion_cambiada)
		self.arbol.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.on_edicion_titulo)
		self.arbol.Bind(wx.EVT_KEY_DOWN, self.on_tecla)
		
		self.btn_agregar.Bind(wx.EVT_BUTTON, self.on_agregar)
		self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
		self.btn_subir.Bind(wx.EVT_BUTTON, self.on_subir)
		self.btn_bajar.Bind(wx.EVT_BUTTON, self.on_bajar)
	
	def actualizar_arbol(self) -> None:
		"""Actualiza el árbol con las secciones del proyecto."""
		self.arbol.DeleteAllItems()
		self.secciones_items.clear()
		
		proyecto = self.ventana_principal.proyecto
		if not proyecto:
			return
		
		# Crear raíz
		raiz = self.arbol.AddRoot(
			proyecto.metadatos.titulo or "Libro sin título"
		)
		
		# Agregar secciones
		for seccion in proyecto.secciones:
			self._agregar_item_seccion(raiz, seccion)
		
		# Expandir raíz
		self.arbol.Expand(raiz)
		
		# Actualizar estado de botones
		self._actualizar_estado_botones()
	
	def _agregar_item_seccion(
		self,
		padre: wx.TreeItemId,
		seccion: Seccion
	) -> wx.TreeItemId:
		"""
		Agrega un item de sección al árbol.
		
		Args:
			padre: Item padre en el árbol
			seccion: Sección a agregar
		
		Returns:
			wx.TreeItemId: ID del item creado
		"""
		texto = seccion.obtener_nombre_legible()
		item = self.arbol.AppendItem(padre, texto)
		self.arbol.SetItemData(item, seccion.id)
		self.secciones_items[seccion.id] = item
		return item
	
	def actualizar_item_seccion(self, seccion: Seccion) -> None:
		"""
		Actualiza el texto de un item de sección.
		
		Args:
			seccion: Sección actualizada
		"""
		if seccion.id in self.secciones_items:
			item = self.secciones_items[seccion.id]
			self.arbol.SetItemText(item, seccion.obtener_nombre_legible())
	
	def obtener_seccion_seleccionada(self) -> Optional[Seccion]:
		"""
		Obtiene la sección actualmente seleccionada.
		
		Returns:
			Seccion o None si no hay selección
		"""
		item = self.arbol.GetSelection()
		if not item.IsOk():
			return None
		
		id_seccion = self.arbol.GetItemData(item)
		if not id_seccion:
			return None
		
		proyecto = self.ventana_principal.proyecto
		if proyecto:
			return proyecto.obtener_seccion_por_id(id_seccion)
		
		return None
	
	def _actualizar_estado_botones(self) -> None:
		"""Actualiza el estado habilitado/deshabilitado de los botones."""
		seccion = self.obtener_seccion_seleccionada()
		proyecto = self.ventana_principal.proyecto
		
		tiene_seleccion = seccion is not None
		self.btn_eliminar.Enable(tiene_seleccion)
		
		if tiene_seleccion and proyecto:
			indice = proyecto.secciones.index(seccion) if seccion in proyecto.secciones else -1
			self.btn_subir.Enable(indice > 0)
			self.btn_bajar.Enable(indice < len(proyecto.secciones) - 1)
		else:
			self.btn_subir.Enable(False)
			self.btn_bajar.Enable(False)
	
	# === Eventos ===
	
	def on_seleccion_cambiada(self, event) -> None:
		"""Maneja el cambio de selección en el árbol."""
		# Solo actualizar el editor, NO cambiar el foco
		# El usuario tabulará manualmente cuando quiera editar
		seccion = self.obtener_seccion_seleccionada()
		self.ventana_principal.seleccionar_seccion(seccion)
		self._actualizar_estado_botones()
		# NO hacer event.Skip() para evitar comportamientos por defecto
		# que puedan cambiar el foco
	
	def on_edicion_titulo(self, event) -> None:
		"""Maneja la edición del título de una sección."""
		if event.IsEditCancelled():
			event.Skip()
			return
		
		nuevo_titulo = event.GetLabel()
		seccion = self.obtener_seccion_seleccionada()
		
		if seccion and nuevo_titulo:
			seccion.establecer_titulo(nuevo_titulo)
			self.ventana_principal.actualizar_seccion(seccion)
		
		event.Skip()
	
	def on_tecla(self, event) -> None:
		"""Maneja eventos de teclado en el árbol."""
		codigo = event.GetKeyCode()
		
		if codigo == wx.WXK_DELETE:
			self.eliminar_seccion()
		elif codigo == wx.WXK_F2:
			# Editar título
			item = self.arbol.GetSelection()
			if item.IsOk():
				self.arbol.EditLabel(item)
		elif event.AltDown():
			if codigo == wx.WXK_UP:
				self.mover_arriba()
			elif codigo == wx.WXK_DOWN:
				self.mover_abajo()
			else:
				event.Skip()
		else:
			event.Skip()
	
	def on_agregar(self, event) -> None:
		"""Maneja el clic en el botón Agregar."""
		self.agregar_seccion()
	
	def on_eliminar(self, event) -> None:
		"""Maneja el clic en el botón Eliminar."""
		self.eliminar_seccion()
	
	def on_subir(self, event) -> None:
		"""Maneja el clic en el botón Subir."""
		self.mover_arriba()
	
	def on_bajar(self, event) -> None:
		"""Maneja el clic en el botón Bajar."""
		self.mover_abajo()
	
	# === Acciones ===
	
	def agregar_seccion(self) -> None:
		"""Muestra diálogo para agregar una nueva sección."""
		# Opciones de tipo de sección
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
			("Colofón", TipoSeccion.COLOFON),
			("Sinopsis", TipoSeccion.SINOPSIS)
		]
		
		nombres = [t[0] for t in tipos]
		
		dialogo = wx.SingleChoiceDialog(
			self,
			"Seleccione el tipo de sección:",
			"Agregar sección",
			nombres
		)
		
		if dialogo.ShowModal() != wx.ID_OK:
			dialogo.Destroy()
			return
		
		indice = dialogo.GetSelection()
		tipo = tipos[indice][1]
		dialogo.Destroy()
		
		# Pedir título
		titulo = wx.GetTextFromUser(
			"Ingrese el título de la sección:",
			"Título de sección",
			f"{tipos[indice][0]} nuevo"
		)
		
		if not titulo:
			return
		
		# Crear sección
		proyecto = self.ventana_principal.proyecto
		if proyecto:
			proyecto.agregar_seccion(tipo, titulo)
			self.actualizar_arbol()
			self.ventana_principal.actualizar_titulo()
			self.ventana_principal.actualizar_barra_estado()
			self.ventana_principal.registrar_log(f"Sección agregada: {titulo}")
	
	def eliminar_seccion(self) -> None:
		"""Elimina la sección seleccionada."""
		seccion = self.obtener_seccion_seleccionada()
		if not seccion:
			return
		
		# Confirmar eliminación
		if self.ventana_principal.preferencias.confirmar_eliminacion:
			respuesta = wx.MessageBox(
				f"¿Está seguro de eliminar la sección '{seccion.titulo}'?",
				"Confirmar eliminación",
				wx.YES_NO | wx.ICON_QUESTION
			)
			
			if respuesta != wx.YES:
				return
		
		# Eliminar
		proyecto = self.ventana_principal.proyecto
		if proyecto:
			proyecto.eliminar_seccion(seccion)
			self.actualizar_arbol()
			self.ventana_principal.seleccionar_seccion(None)
			self.ventana_principal.actualizar_titulo()
			self.ventana_principal.actualizar_barra_estado()
			self.ventana_principal.registrar_log(f"Sección eliminada: {seccion.titulo}")
	
	def mover_arriba(self) -> None:
		"""Mueve la sección seleccionada hacia arriba."""
		seccion = self.obtener_seccion_seleccionada()
		if not seccion:
			wx.Bell()  # Beep si no hay selección
			return
		
		proyecto = self.ventana_principal.proyecto
		if not proyecto:
			return
		
		# Verificar si ya está en el principio
		indice = proyecto.secciones.index(seccion) if seccion in proyecto.secciones else -1
		if indice <= 0:
			wx.Bell()  # Beep al llegar al principio
			return
		
		if proyecto.mover_seccion_arriba(seccion):
			self.actualizar_arbol()
			self._seleccionar_seccion(seccion)
			self.ventana_principal.actualizar_titulo()
			self.ventana_principal.registrar_log(f"Sección movida arriba: {seccion.titulo}")
	
	def mover_abajo(self) -> None:
		"""Mueve la sección seleccionada hacia abajo."""
		seccion = self.obtener_seccion_seleccionada()
		if not seccion:
			wx.Bell()  # Beep si no hay selección
			return
		
		proyecto = self.ventana_principal.proyecto
		if not proyecto:
			return
		
		# Verificar si ya está en el final
		indice = proyecto.secciones.index(seccion) if seccion in proyecto.secciones else -1
		if indice >= len(proyecto.secciones) - 1:
			wx.Bell()  # Beep al llegar al final
			return
		
		if proyecto.mover_seccion_abajo(seccion):
			self.actualizar_arbol()
			self._seleccionar_seccion(seccion)
			self.ventana_principal.actualizar_titulo()
			self.ventana_principal.registrar_log(f"Sección movida abajo: {seccion.titulo}")
	
	def _seleccionar_seccion(self, seccion: Seccion) -> None:
		"""
		Selecciona una sección en el árbol.
		
		Args:
			seccion: Sección a seleccionar
		"""
		if seccion.id in self.secciones_items:
			item = self.secciones_items[seccion.id]
			self.arbol.SelectItem(item)
			self.arbol.EnsureVisible(item)
