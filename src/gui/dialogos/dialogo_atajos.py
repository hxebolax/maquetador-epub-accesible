# -*- coding: utf-8 -*-
"""
Diálogo de Atajos de Teclado.
Muestra todos los atajos de teclado disponibles.
"""

import wx


class DialogoAtajos(wx.Dialog):
	"""
	Diálogo accesible con la lista de atajos de teclado.
	"""
	
	ATAJOS = """ATAJOS DE TECLADO - MAQUETADOR DE EPUB ACCESIBLES v2.0

==============================================
ARCHIVO
==============================================
Ctrl+N          Nuevo proyecto (con plantillas)
Ctrl+O          Abrir proyecto
Ctrl+S          Guardar proyecto
Ctrl+Shift+S    Guardar como
Ctrl+E          Exportar EPUB
Alt+F4          Salir de la aplicación

==============================================
EXPORTACIÓN
==============================================
Ctrl+E          Exportar a EPUB
                Exportar a PDF (menú)
                Exportar a MOBI (menú)
                Exportar a HTML (menú)

==============================================
EDICIÓN
==============================================
Ctrl+Z          Deshacer
Ctrl+Y          Rehacer
Ctrl+X          Cortar
Ctrl+C          Copiar
Ctrl+V          Pegar

==============================================
EDITOR WYSIWYG
==============================================
Ctrl+B          Negrita
Ctrl+I          Cursiva
Ctrl+U          Subrayado

==============================================
PROYECTO
==============================================
Ctrl+Shift+A    Agregar sección
Ctrl+I          Importar archivo
Ctrl+Alt+I      Importar múltiples archivos
Ctrl+Shift+I    Insertar imagen en sección
Ctrl+M          Metadatos del libro
Ctrl+Shift+M    Metadatos de accesibilidad

==============================================
VER
==============================================
F6              Vista previa del EPUB

==============================================
HERRAMIENTAS
==============================================
F5              Validar proyecto

==============================================
AYUDA
==============================================
F1              Manual de uso

==============================================
PANEL DE SECCIONES
==============================================
Flechas         Navegar por el árbol
Enter           Seleccionar sección
F2              Renombrar sección
Delete          Eliminar sección
Alt+Arriba      Mover sección arriba
Alt+Abajo       Mover sección abajo

==============================================
PANEL DE EDICIÓN
==============================================
Tab             Siguiente control
Shift+Tab       Control anterior
Ctrl+S          Guardar cambios de la sección
Ctrl+Shift+I    Insertar imagen

==============================================
VISTA PREVIA
==============================================
Flecha Izq.     Sección anterior
Flecha Der.     Sección siguiente
Re Pág          Sección anterior
Av Pág          Sección siguiente
F5              Actualizar vista previa
Escape          Cerrar vista previa

==============================================
DIÁLOGOS
==============================================
Enter           Aceptar
Escape          Cancelar
Tab             Siguiente campo
Shift+Tab       Campo anterior

==============================================
NAVEGACIÓN GENERAL
==============================================
Tab             Siguiente control
Shift+Tab       Control anterior
Alt+Letra       Activar control con acelerador
F6              Vista previa / Cambiar paneles
"""
	
	def __init__(self, parent):
		"""
		Inicializa el diálogo.
		
		Args:
			parent: Ventana padre
		"""
		super().__init__(
			parent,
			title="Atajos de teclado",
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		
		self._crear_controles()
		self._configurar_layout()
		
		self.SetSize((500, 550))
		self.Centre()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del diálogo."""
		self.lbl_atajos = wx.StaticText(self, label="&Atajos de teclado:")
		
		self.txt_atajos = wx.TextCtrl(
			self,
			value=self.ATAJOS,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2
		)
		self.txt_atajos.SetName("Lista de atajos de teclado")
		
		# Establecer fuente monoespaciada
		fuente = wx.Font(
			10,
			wx.FONTFAMILY_TELETYPE,
			wx.FONTSTYLE_NORMAL,
			wx.FONTWEIGHT_NORMAL
		)
		self.txt_atajos.SetFont(fuente)
		
		self.btn_cerrar = wx.Button(self, wx.ID_CLOSE, label="&Cerrar")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del diálogo."""
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.lbl_atajos, 0, wx.ALL, 10)
		sizer.Add(self.txt_atajos, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		sizer.Add(self.btn_cerrar, 0, wx.ALL | wx.ALIGN_CENTER, 10)
		
		self.SetSizer(sizer)
		
		self.btn_cerrar.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))
		self.txt_atajos.SetFocus()
