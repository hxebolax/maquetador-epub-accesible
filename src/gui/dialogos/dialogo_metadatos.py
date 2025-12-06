# -*- coding: utf-8 -*-
"""
Diálogo de Metadatos Dublin Core.
Permite editar los metadatos bibliográficos del libro.
"""

import wx
from typing import List

from ...modelo.metadatos import MetadatosDC
from ...utils.constantes import CODIGOS_IDIOMA


class DialogoMetadatos(wx.Dialog):
	"""
	Diálogo accesible para edición de metadatos Dublin Core.
	"""
	
	def __init__(self, parent, metadatos: MetadatosDC):
		"""
		Inicializa el diálogo.
		
		Args:
			parent: Ventana padre
			metadatos: Metadatos actuales a editar
		"""
		super().__init__(
			parent,
			title="Metadatos del libro",
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		
		self.metadatos = MetadatosDC.from_dict(metadatos.to_dict())
		
		self._crear_controles()
		self._configurar_layout()
		self._cargar_datos()
		self._configurar_eventos()
		
		self.SetSize((500, 600))
		self.Centre()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del diálogo."""
		# Título
		self.lbl_titulo = wx.StaticText(self, label="&Título:")
		self.txt_titulo = wx.TextCtrl(self)
		self.txt_titulo.SetName("Título del libro")
		
		# Identificador
		self.lbl_id = wx.StaticText(self, label="&Identificador:")
		self.txt_id = wx.TextCtrl(self)
		self.txt_id.SetName("Identificador único")
		
		# Idioma
		self.lbl_idioma = wx.StaticText(self, label="I&dioma:")
		self.cmb_idioma = wx.ComboBox(self, choices=CODIGOS_IDIOMA)
		self.cmb_idioma.SetName("Código de idioma")
		
		# Autores
		self.lbl_autores = wx.StaticText(self, label="&Autores:")
		self.lst_autores = wx.ListBox(self)
		self.lst_autores.SetName("Lista de autores")
		
		self.btn_agregar_autor = wx.Button(self, label="A&gregar")
		self.btn_eliminar_autor = wx.Button(self, label="E&liminar")
		self.btn_subir_autor = wx.Button(self, label="&Subir")
		self.btn_bajar_autor = wx.Button(self, label="&Bajar")
		
		# Editor
		self.lbl_editor = wx.StaticText(self, label="&Editor:")
		self.txt_editor = wx.TextCtrl(self)
		self.txt_editor.SetName("Editorial")
		
		# Fecha
		self.lbl_fecha = wx.StaticText(self, label="&Fecha:")
		self.txt_fecha = wx.TextCtrl(self)
		self.txt_fecha.SetName("Fecha de publicación (AAAA-MM-DD)")
		
		# Derechos
		self.lbl_derechos = wx.StaticText(self, label="De&rechos:")
		self.txt_derechos = wx.TextCtrl(self)
		self.txt_derechos.SetName("Información de derechos de autor")
		
		# Descripción
		self.lbl_descripcion = wx.StaticText(self, label="Descripció&n:")
		self.txt_descripcion = wx.TextCtrl(
			self,
			style=wx.TE_MULTILINE,
			size=(-1, 80)
		)
		self.txt_descripcion.SetName("Descripción del libro")
		
		# Temas
		self.lbl_temas = wx.StaticText(self, label="Te&mas:")
		self.txt_temas = wx.TextCtrl(self)
		self.txt_temas.SetName("Temas separados por comas")
		
		# Botones
		self.btn_ok = wx.Button(self, wx.ID_OK, label="&Aceptar")
		self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, label="&Cancelar")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del diálogo."""
		# Sizer para autores
		sizer_autores_btns = wx.BoxSizer(wx.VERTICAL)
		sizer_autores_btns.Add(self.btn_agregar_autor, 0, wx.BOTTOM, 2)
		sizer_autores_btns.Add(self.btn_eliminar_autor, 0, wx.BOTTOM, 2)
		sizer_autores_btns.Add(self.btn_subir_autor, 0, wx.BOTTOM, 2)
		sizer_autores_btns.Add(self.btn_bajar_autor, 0)
		
		sizer_autores = wx.BoxSizer(wx.HORIZONTAL)
		sizer_autores.Add(self.lst_autores, 1, wx.EXPAND | wx.RIGHT, 5)
		sizer_autores.Add(sizer_autores_btns, 0)
		
		# Grid principal
		grid = wx.FlexGridSizer(10, 2, 5, 10)
		grid.AddGrowableCol(1)
		
		grid.Add(self.lbl_titulo, 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(self.txt_titulo, 1, wx.EXPAND)
		
		grid.Add(self.lbl_id, 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(self.txt_id, 1, wx.EXPAND)
		
		grid.Add(self.lbl_idioma, 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(self.cmb_idioma, 0)
		
		grid.Add(self.lbl_autores, 0, wx.ALIGN_TOP)
		grid.Add(sizer_autores, 1, wx.EXPAND)
		
		grid.Add(self.lbl_editor, 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(self.txt_editor, 1, wx.EXPAND)
		
		grid.Add(self.lbl_fecha, 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(self.txt_fecha, 1, wx.EXPAND)
		
		grid.Add(self.lbl_derechos, 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(self.txt_derechos, 1, wx.EXPAND)
		
		grid.Add(self.lbl_descripcion, 0, wx.ALIGN_TOP)
		grid.Add(self.txt_descripcion, 1, wx.EXPAND)
		
		grid.Add(self.lbl_temas, 0, wx.ALIGN_CENTER_VERTICAL)
		grid.Add(self.txt_temas, 1, wx.EXPAND)
		
		# Botones
		sizer_botones = wx.StdDialogButtonSizer()
		sizer_botones.AddButton(self.btn_ok)
		sizer_botones.AddButton(self.btn_cancelar)
		sizer_botones.Realize()
		
		# Sizer principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 10)
		sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		sizer.Add(sizer_botones, 0, wx.EXPAND | wx.ALL, 10)
		
		self.SetSizer(sizer)
	
	def _cargar_datos(self) -> None:
		"""Carga los datos de los metadatos en los controles."""
		self.txt_titulo.SetValue(self.metadatos.titulo)
		self.txt_id.SetValue(self.metadatos.identificador)
		self.cmb_idioma.SetValue(self.metadatos.idioma)
		
		for autor in self.metadatos.autores:
			self.lst_autores.Append(autor)
		
		self.txt_editor.SetValue(self.metadatos.editor or "")
		self.txt_fecha.SetValue(self.metadatos.fecha or "")
		self.txt_derechos.SetValue(self.metadatos.derechos or "")
		self.txt_descripcion.SetValue(self.metadatos.descripcion or "")
		self.txt_temas.SetValue(", ".join(self.metadatos.temas))
	
	def _configurar_eventos(self) -> None:
		"""Configura los eventos del diálogo."""
		self.btn_agregar_autor.Bind(wx.EVT_BUTTON, self.on_agregar_autor)
		self.btn_eliminar_autor.Bind(wx.EVT_BUTTON, self.on_eliminar_autor)
		self.btn_subir_autor.Bind(wx.EVT_BUTTON, self.on_subir_autor)
		self.btn_bajar_autor.Bind(wx.EVT_BUTTON, self.on_bajar_autor)
		self.btn_ok.Bind(wx.EVT_BUTTON, self.on_aceptar)
	
	def on_agregar_autor(self, event) -> None:
		"""Agrega un nuevo autor."""
		autor = wx.GetTextFromUser(
			"Ingrese el nombre del autor:",
			"Agregar autor"
		)
		if autor:
			self.lst_autores.Append(autor)
	
	def on_eliminar_autor(self, event) -> None:
		"""Elimina el autor seleccionado."""
		sel = self.lst_autores.GetSelection()
		if sel != wx.NOT_FOUND:
			self.lst_autores.Delete(sel)
	
	def on_subir_autor(self, event) -> None:
		"""Mueve el autor seleccionado hacia arriba."""
		sel = self.lst_autores.GetSelection()
		if sel > 0:
			autor = self.lst_autores.GetString(sel)
			self.lst_autores.Delete(sel)
			self.lst_autores.Insert(autor, sel - 1)
			self.lst_autores.SetSelection(sel - 1)
	
	def on_bajar_autor(self, event) -> None:
		"""Mueve el autor seleccionado hacia abajo."""
		sel = self.lst_autores.GetSelection()
		if sel != wx.NOT_FOUND and sel < self.lst_autores.GetCount() - 1:
			autor = self.lst_autores.GetString(sel)
			self.lst_autores.Delete(sel)
			self.lst_autores.Insert(autor, sel + 1)
			self.lst_autores.SetSelection(sel + 1)
	
	def on_aceptar(self, event) -> None:
		"""Valida y acepta los cambios."""
		# Actualizar metadatos
		self.metadatos.titulo = self.txt_titulo.GetValue()
		self.metadatos.identificador = self.txt_id.GetValue()
		self.metadatos.idioma = self.cmb_idioma.GetValue()
		
		self.metadatos.autores = [
			self.lst_autores.GetString(i)
			for i in range(self.lst_autores.GetCount())
		]
		
		self.metadatos.editor = self.txt_editor.GetValue() or None
		self.metadatos.fecha = self.txt_fecha.GetValue() or None
		self.metadatos.derechos = self.txt_derechos.GetValue() or None
		self.metadatos.descripcion = self.txt_descripcion.GetValue() or None
		
		temas_texto = self.txt_temas.GetValue()
		self.metadatos.temas = [
			t.strip() for t in temas_texto.split(",") if t.strip()
		]
		
		# Validar
		errores = self.metadatos.validar()
		if errores:
			wx.MessageBox(
				"Se encontraron los siguientes errores:\n\n" +
				"\n".join(f"• {e}" for e in errores),
				"Error de validación",
				wx.OK | wx.ICON_ERROR
			)
			return
		
		event.Skip()
	
	def obtener_metadatos(self) -> MetadatosDC:
		"""
		Obtiene los metadatos editados.
		
		Returns:
			MetadatosDC: Metadatos actualizados
		"""
		return self.metadatos
