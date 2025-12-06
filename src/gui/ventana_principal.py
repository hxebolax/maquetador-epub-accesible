# -*- coding: utf-8 -*-
"""
Ventana Principal de la aplicación.
Contiene la interfaz principal accesible con menús y paneles.
"""

import wx
import os
from typing import Optional

from ..modelo.proyecto import Proyecto
from ..modelo.seccion import Seccion, TipoSeccion
from ..modelo.preferencias import Preferencias
from ..servicios.servicio_persistencia import ServicioPersistencia, ErrorPersistencia
from ..servicios.servicio_epub import ServicioEPUB
from ..servicios.servicio_validacion import ServicioValidacion
from ..servicios.servicio_i18n import ServicioI18n
from ..servicios.servicio_exportacion import ServicioExportacion
from ..utils.constantes import NOMBRE_APP, VERSION_APP


class VentanaPrincipal(wx.Frame):
	"""
	Ventana principal de la aplicación.
	
	Proporciona la interfaz accesible con menús, paneles y atajos de teclado.
	"""
	
	def __init__(self):
		"""Inicializa la ventana principal."""
		super().__init__(
			parent=None,
			title=f"{NOMBRE_APP} {VERSION_APP}",
			size=(1024, 768)
		)
		
		# Servicios
		self.servicio_persistencia = ServicioPersistencia()
		self.servicio_epub = ServicioEPUB()
		self.servicio_validacion = ServicioValidacion()
		self.servicio_exportacion = ServicioExportacion()
		self.servicio_i18n = ServicioI18n()
		
		# Estado
		self.proyecto: Optional[Proyecto] = None
		self.preferencias = Preferencias.cargar()
		
		# Cargar idioma desde preferencias
		self._cargar_idioma()
		
		# Crear interfaz
		self._crear_menu()
		self._crear_barra_herramientas()
		self._crear_paneles()
		self._crear_barra_estado()
		self._configurar_atajos()
		self._configurar_eventos()
		
		# Centrar ventana
		self.Centre()
		
		# Crear proyecto vacío inicial (sin diálogo)
		self.nuevo_proyecto(mostrar_dialogo=False)
	
	def _cargar_idioma(self) -> None:
		"""Carga el idioma desde las preferencias."""
		idioma = self.preferencias.idioma
		if idioma:
			self.servicio_i18n.cargar_idioma(idioma)
		else:
			# Detectar idioma del sistema
			idioma_sistema = self.servicio_i18n.detectar_idioma_sistema()
			self.servicio_i18n.cargar_idioma(idioma_sistema)
			self.preferencias.idioma = idioma_sistema
	
	def _crear_menu(self) -> None:
		"""Crea la barra de menú accesible."""
		barra_menu = wx.MenuBar()
		
		# Menú Archivo
		menu_archivo = wx.Menu()
		
		item_nuevo = menu_archivo.Append(wx.ID_NEW, "&Nuevo proyecto\tCtrl+N", "Crear un nuevo proyecto")
		item_abrir = menu_archivo.Append(wx.ID_OPEN, "&Abrir proyecto...\tCtrl+O", "Abrir un proyecto existente")
		item_guardar = menu_archivo.Append(wx.ID_SAVE, "&Guardar\tCtrl+S", "Guardar el proyecto actual")
		item_guardar_como = menu_archivo.Append(wx.ID_SAVEAS, "Guardar &como...\tCtrl+Shift+S", "Guardar con otro nombre")
		menu_archivo.AppendSeparator()
		
		# Submenú Exportar
		menu_exportar = wx.Menu()
		self.item_exportar_epub = menu_exportar.Append(wx.ID_ANY, "&EPUB...\tCtrl+E", "Exportar a formato EPUB")
		self.item_exportar_pdf = menu_exportar.Append(wx.ID_ANY, "&PDF...", "Exportar a formato PDF")
		self.item_exportar_mobi = menu_exportar.Append(wx.ID_ANY, "&MOBI (Kindle)...", "Exportar a formato MOBI")
		self.item_exportar_html = menu_exportar.Append(wx.ID_ANY, "&HTML...", "Exportar a carpeta HTML")
		menu_archivo.AppendSubMenu(menu_exportar, "E&xportar")
		
		menu_archivo.AppendSeparator()
		item_salir = menu_archivo.Append(wx.ID_EXIT, "&Salir\tAlt+F4", "Cerrar la aplicación")
		
		barra_menu.Append(menu_archivo, "&Archivo")
		
		# Menú Editar
		menu_editar = wx.Menu()
		
		self.item_deshacer = menu_editar.Append(wx.ID_UNDO, "&Deshacer\tCtrl+Z", "Deshacer última acción")
		self.item_rehacer = menu_editar.Append(wx.ID_REDO, "&Rehacer\tCtrl+Y", "Rehacer acción deshecha")
		menu_editar.AppendSeparator()
		menu_editar.Append(wx.ID_CUT, "Cor&tar\tCtrl+X", "Cortar selección")
		menu_editar.Append(wx.ID_COPY, "&Copiar\tCtrl+C", "Copiar selección")
		menu_editar.Append(wx.ID_PASTE, "&Pegar\tCtrl+V", "Pegar desde portapapeles")
		
		barra_menu.Append(menu_editar, "&Editar")
		
		# Menú Ver
		menu_ver = wx.Menu()
		
		self.item_vista_previa = menu_ver.Append(
			wx.ID_ANY, "&Vista previa\tF6", "Abrir vista previa del EPUB"
		)
		menu_ver.AppendSeparator()
		self.item_panel_logs = menu_ver.AppendCheckItem(
			wx.ID_ANY, "Panel de &mensajes", "Mostrar/ocultar panel de mensajes"
		)
		self.item_panel_logs.Check(self.preferencias.mostrar_panel_logs)
		
		barra_menu.Append(menu_ver, "&Ver")
		
		# Menú Proyecto
		menu_proyecto = wx.Menu()
		
		self.item_agregar_seccion = menu_proyecto.Append(
			wx.ID_ANY, "&Agregar sección...\tCtrl+Shift+A", "Agregar nueva sección"
		)
		self.item_importar = menu_proyecto.Append(
			wx.ID_ANY, "&Importar archivo...\tCtrl+I", "Importar contenido desde archivo"
		)
		self.item_importar_multiple = menu_proyecto.Append(
			wx.ID_ANY, "Importar &múltiples archivos...\tCtrl+Alt+I", "Importar varios archivos a la vez"
		)
		menu_proyecto.AppendSeparator()
		self.item_metadatos = menu_proyecto.Append(
			wx.ID_ANY, "&Metadatos del libro...\tCtrl+M", "Editar metadatos Dublin Core"
		)
		self.item_accesibilidad = menu_proyecto.Append(
			wx.ID_ANY, "Metadatos de &accesibilidad...\tCtrl+Shift+M", "Configurar accesibilidad"
		)
		self.item_portada = menu_proyecto.Append(
			wx.ID_ANY, "&Portada...", "Configurar imagen de portada"
		)
		menu_proyecto.AppendSeparator()
		self.item_guardar_plantilla = menu_proyecto.Append(
			wx.ID_ANY, "Guardar como &plantilla...", "Guardar estructura como plantilla"
		)
		
		barra_menu.Append(menu_proyecto, "&Proyecto")
		
		# Menú Herramientas
		menu_herramientas = wx.Menu()
		
		self.item_validar = menu_herramientas.Append(
			wx.ID_ANY, "&Validar proyecto\tF5", "Validar el proyecto actual"
		)
		self.item_epubcheck = menu_herramientas.Append(
			wx.ID_ANY, "Ejecutar &EPUBCheck...", "Validar EPUB con EPUBCheck"
		)
		self.item_ace = menu_herramientas.Append(
			wx.ID_ANY, "Ejecutar &Ace...", "Validar accesibilidad con Ace"
		)
		menu_herramientas.AppendSeparator()
		self.item_preferencias = menu_herramientas.Append(
			wx.ID_PREFERENCES, "&Preferencias...", "Configurar preferencias"
		)
		
		barra_menu.Append(menu_herramientas, "&Herramientas")
		
		# Menú Ayuda
		menu_ayuda = wx.Menu()
		
		self.item_manual = menu_ayuda.Append(wx.ID_HELP, "&Manual de uso\tF1", "Abrir manual de ayuda")
		self.item_atajos = menu_ayuda.Append(wx.ID_ANY, "&Atajos de teclado...", "Ver atajos de teclado")
		menu_ayuda.AppendSeparator()
		self.item_acerca = menu_ayuda.Append(wx.ID_ABOUT, "&Acerca de...", "Información sobre la aplicación")
		
		barra_menu.Append(menu_ayuda, "A&yuda")
		
		self.SetMenuBar(barra_menu)
		
		# Vincular eventos de menú
		self.Bind(wx.EVT_MENU, self.on_nuevo, item_nuevo)
		self.Bind(wx.EVT_MENU, self.on_abrir, item_abrir)
		self.Bind(wx.EVT_MENU, self.on_guardar, item_guardar)
		self.Bind(wx.EVT_MENU, self.on_guardar_como, item_guardar_como)
		self.Bind(wx.EVT_MENU, self.on_exportar_epub, self.item_exportar_epub)
		self.Bind(wx.EVT_MENU, self.on_exportar_pdf, self.item_exportar_pdf)
		self.Bind(wx.EVT_MENU, self.on_exportar_mobi, self.item_exportar_mobi)
		self.Bind(wx.EVT_MENU, self.on_exportar_html, self.item_exportar_html)
		self.Bind(wx.EVT_MENU, self.on_salir, item_salir)
		
		# Menú Ver
		self.Bind(wx.EVT_MENU, self.on_vista_previa, self.item_vista_previa)
		self.Bind(wx.EVT_MENU, self.on_toggle_panel_logs, self.item_panel_logs)
		
		# Menú Proyecto
		self.Bind(wx.EVT_MENU, self.on_agregar_seccion, self.item_agregar_seccion)
		self.Bind(wx.EVT_MENU, self.on_importar, self.item_importar)
		self.Bind(wx.EVT_MENU, self.on_importar_multiple, self.item_importar_multiple)
		self.Bind(wx.EVT_MENU, self.on_metadatos, self.item_metadatos)
		self.Bind(wx.EVT_MENU, self.on_accesibilidad, self.item_accesibilidad)
		self.Bind(wx.EVT_MENU, self.on_portada, self.item_portada)
		self.Bind(wx.EVT_MENU, self.on_guardar_plantilla, self.item_guardar_plantilla)
		
		self.Bind(wx.EVT_MENU, self.on_validar, self.item_validar)
		self.Bind(wx.EVT_MENU, self.on_preferencias, self.item_preferencias)
		
		# Menú Ayuda
		self.Bind(wx.EVT_MENU, self.on_manual, self.item_manual)
		self.Bind(wx.EVT_MENU, self.on_atajos, self.item_atajos)
		self.Bind(wx.EVT_MENU, self.on_acerca, self.item_acerca)
	
	def _crear_barra_herramientas(self) -> None:
		"""Crea la barra de herramientas."""
		# Por ahora no creamos barra de herramientas para mantener
		# la interfaz simple y accesible
		pass
	
	def _crear_paneles(self) -> None:
		"""Crea los paneles principales de la interfaz."""
		# Panel principal con splitter
		self.splitter_principal = wx.SplitterWindow(
			self,
			style=wx.SP_LIVE_UPDATE | wx.SP_3D
		)
		
		# Panel izquierdo: secciones
		from .panel_secciones import PanelSecciones
		self.panel_secciones = PanelSecciones(self.splitter_principal, self)
		
		# Panel derecho con splitter vertical
		self.splitter_derecho = wx.SplitterWindow(
			self.splitter_principal,
			style=wx.SP_LIVE_UPDATE | wx.SP_3D
		)
		
		# Panel editor
		from .panel_editor import PanelEditor
		self.panel_editor = PanelEditor(self.splitter_derecho, self)
		
		# Panel logs
		from .panel_logs import PanelLogs
		self.panel_logs = PanelLogs(self.splitter_derecho, self)
		
		# Configurar splitters
		self.splitter_derecho.SplitHorizontally(
			self.panel_editor,
			self.panel_logs,
			-150  # Panel de logs de 150px
		)
		
		self.splitter_principal.SplitVertically(
			self.panel_secciones,
			self.splitter_derecho,
			250  # Panel de secciones de 250px
		)
		
		# Tamaños mínimos
		self.splitter_principal.SetMinimumPaneSize(200)
		self.splitter_derecho.SetMinimumPaneSize(100)
	
	def _crear_barra_estado(self) -> None:
		"""Crea la barra de estado."""
		self.barra_estado = self.CreateStatusBar(3)
		self.barra_estado.SetStatusWidths([-2, -1, 150])
		self.actualizar_barra_estado()
	
	def _configurar_atajos(self) -> None:
		"""Configura atajos de teclado adicionales."""
		# Los atajos principales ya están en los menús
		# Aquí podemos agregar atajos adicionales si es necesario
		pass
	
	def _configurar_eventos(self) -> None:
		"""Configura eventos de la ventana."""
		self.Bind(wx.EVT_CLOSE, self.on_cerrar)
	
	def actualizar_titulo(self) -> None:
		"""Actualiza el título de la ventana."""
		titulo = f"{NOMBRE_APP} {VERSION_APP}"
		
		if self.proyecto:
			nombre = self.proyecto.metadatos.titulo or "Sin título"
			if self.proyecto.ruta_archivo:
				nombre = os.path.basename(self.proyecto.ruta_archivo)
			
			if self.proyecto.modificado:
				nombre += " *"
			
			titulo = f"{nombre} - {titulo}"
		
		self.SetTitle(titulo)
	
	def actualizar_barra_estado(self, mensaje: str = "") -> None:
		"""Actualiza la barra de estado."""
		if mensaje:
			self.barra_estado.SetStatusText(mensaje, 0)
		elif self.proyecto:
			num_secciones = len(self.proyecto.secciones)
			self.barra_estado.SetStatusText(
				f"{num_secciones} sección(es)", 0
			)
		else:
			self.barra_estado.SetStatusText("Listo", 0)
		
		# Estado de modificación
		if self.proyecto and self.proyecto.modificado:
			self.barra_estado.SetStatusText("Modificado", 1)
		else:
			self.barra_estado.SetStatusText("", 1)
		
		# Idioma
		if self.proyecto:
			self.barra_estado.SetStatusText(
				self.proyecto.metadatos.idioma.upper(), 2
			)
	
	def registrar_log(self, mensaje: str, tipo: str = "info") -> None:
		"""
		Registra un mensaje en el panel de logs.
		
		Args:
			mensaje: Mensaje a registrar
			tipo: Tipo de mensaje (info, advertencia, error)
		"""
		self.panel_logs.agregar_mensaje(mensaje, tipo)
	
	# === Acciones de menú ===
	
	def on_nuevo(self, event) -> None:
		"""Crea un nuevo proyecto."""
		if not self._confirmar_cambios_sin_guardar():
			return
		self.nuevo_proyecto(mostrar_dialogo=True)
	
	def on_abrir(self, event) -> None:
		"""Abre un proyecto existente."""
		if not self._confirmar_cambios_sin_guardar():
			return
		self.abrir_proyecto()
	
	def on_guardar(self, event) -> None:
		"""Guarda el proyecto actual."""
		self.guardar_proyecto()
	
	def on_guardar_como(self, event) -> None:
		"""Guarda el proyecto con otro nombre."""
		self.guardar_proyecto_como()
	
	def on_exportar_epub(self, event) -> None:
		"""Exporta el proyecto a EPUB."""
		self.exportar_epub()
	
	def on_exportar_pdf(self, event) -> None:
		"""Exporta el proyecto a PDF."""
		self.exportar_pdf()
	
	def on_exportar_mobi(self, event) -> None:
		"""Exporta el proyecto a MOBI."""
		self.exportar_mobi()
	
	def on_exportar_html(self, event) -> None:
		"""Exporta el proyecto a HTML."""
		self.exportar_html()
	
	def on_vista_previa(self, event) -> None:
		"""Abre la vista previa del EPUB."""
		self.mostrar_vista_previa()
	
	def on_toggle_panel_logs(self, event) -> None:
		"""Muestra/oculta el panel de logs."""
		mostrar = self.item_panel_logs.IsChecked()
		if mostrar:
			self.splitter_derecho.SplitHorizontally(
				self.panel_editor,
				self.panel_logs,
				-150
			)
		else:
			self.splitter_derecho.Unsplit(self.panel_logs)
		self.preferencias.mostrar_panel_logs = mostrar
	
	def on_guardar_plantilla(self, event) -> None:
		"""Guarda el proyecto actual como plantilla."""
		self.guardar_como_plantilla()
	
	def on_salir(self, event) -> None:
		"""Cierra la aplicación."""
		self.Close()
	
	def on_agregar_seccion(self, event) -> None:
		"""Agrega una nueva sección."""
		self.panel_secciones.agregar_seccion()
	
	def on_importar(self, event) -> None:
		"""Importa contenido desde archivo."""
		from .dialogos.dialogo_importacion import DialogoImportacion
		
		dialogo = DialogoImportacion(self)
		if dialogo.ShowModal() == wx.ID_OK:
			ruta = dialogo.obtener_ruta()
			titulo = dialogo.obtener_titulo()
			tipo = dialogo.obtener_tipo_seccion()
			
			if ruta:
				self._importar_archivo(ruta, titulo, tipo)
		
		dialogo.Destroy()
	
	def on_importar_multiple(self, event) -> None:
		"""Importa múltiples archivos a la vez."""
		from .dialogos.dialogo_importacion_multiple import DialogoImportacionMultiple
		
		dialogo = DialogoImportacionMultiple(self)
		if dialogo.ShowModal() == wx.ID_OK:
			archivos = dialogo.obtener_archivos()
			
			for ruta, titulo, tipo in archivos:
				self._importar_archivo(ruta, titulo, tipo)
			
			if archivos:
				self.registrar_log(f"{len(archivos)} archivo(s) importado(s)")
		
		dialogo.Destroy()
	
	def on_metadatos(self, event) -> None:
		"""Abre el diálogo de metadatos."""
		from .dialogos.dialogo_metadatos import DialogoMetadatos
		
		dialogo = DialogoMetadatos(self, self.proyecto.metadatos)
		if dialogo.ShowModal() == wx.ID_OK:
			self.proyecto.metadatos = dialogo.obtener_metadatos()
			self.proyecto.marcar_modificado()
			self.actualizar_titulo()
			self.actualizar_barra_estado()
			self.registrar_log("Metadatos actualizados")
		
		dialogo.Destroy()
	
	def on_accesibilidad(self, event) -> None:
		"""Abre el diálogo de accesibilidad."""
		from .dialogos.dialogo_accesibilidad import DialogoAccesibilidad
		
		dialogo = DialogoAccesibilidad(self, self.proyecto.metadatos_accesibilidad)
		if dialogo.ShowModal() == wx.ID_OK:
			self.proyecto.metadatos_accesibilidad = dialogo.obtener_metadatos()
			self.proyecto.marcar_modificado()
			self.actualizar_titulo()
			self.registrar_log("Metadatos de accesibilidad actualizados")
		
		dialogo.Destroy()
	
	def on_portada(self, event) -> None:
		"""Configura la imagen de portada."""
		from ..modelo.imagen import Imagen
		
		dialogo = wx.FileDialog(
			self,
			message="Seleccionar imagen de portada",
			wildcard="Imágenes (*.jpg;*.jpeg;*.png)|*.jpg;*.jpeg;*.png",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		)
		
		if dialogo.ShowModal() == wx.ID_OK:
			ruta = dialogo.GetPath()
			
			# Pedir texto alternativo
			texto_alt = wx.GetTextFromUser(
				"Ingrese el texto alternativo para la portada:",
				"Texto alternativo",
				"Portada del libro"
			)
			
			if texto_alt:
				imagen = Imagen(
					ruta=ruta,
					texto_alternativo=texto_alt,
					es_portada=True
				)
				self.proyecto.establecer_portada(imagen)
				self.actualizar_titulo()
				self.registrar_log(f"Portada establecida: {os.path.basename(ruta)}")
		
		dialogo.Destroy()
	
	def on_validar(self, event) -> None:
		"""Valida el proyecto actual."""
		self.validar_proyecto()
	
	def on_preferencias(self, event) -> None:
		"""Abre el diálogo de preferencias."""
		from .dialogos.dialogo_preferencias import DialogoPreferencias
		
		idioma_anterior = self.preferencias.idioma
		
		dialogo = DialogoPreferencias(self, self.preferencias)
		if dialogo.ShowModal() == wx.ID_OK:
			self.preferencias = dialogo.obtener_preferencias()
			self.preferencias.guardar()
			self.registrar_log("Preferencias guardadas")
			
			# Si cambió el idioma, avisar que requiere reinicio
			if self.preferencias.idioma != idioma_anterior:
				wx.MessageBox(
					"El cambio de idioma se aplicará la próxima vez que inicie la aplicación.",
					"Cambio de idioma",
					wx.OK | wx.ICON_INFORMATION
				)
		
		dialogo.Destroy()
	
	def on_manual(self, event) -> None:
		"""Muestra el manual de uso."""
		from .dialogos.dialogo_manual import DialogoManual
		
		dialogo = DialogoManual(self)
		dialogo.ShowModal()
		dialogo.Destroy()
	
	def on_atajos(self, event) -> None:
		"""Muestra los atajos de teclado."""
		from .dialogos.dialogo_atajos import DialogoAtajos
		
		dialogo = DialogoAtajos(self)
		dialogo.ShowModal()
		dialogo.Destroy()
	
	def on_acerca(self, event) -> None:
		"""Muestra información sobre la aplicación."""
		from .dialogos.dialogo_acerca import DialogoAcerca
		
		dialogo = DialogoAcerca(self)
		dialogo.ShowModal()
		dialogo.Destroy()
	
	def on_cerrar(self, event) -> None:
		"""Maneja el cierre de la ventana."""
		if self._confirmar_cambios_sin_guardar():
			# Guardar preferencias
			self.preferencias.guardar()
			event.Skip()
		else:
			event.Veto()
	
	# === Métodos de proyecto ===
	
	def nuevo_proyecto(self, mostrar_dialogo: bool = True) -> None:
		"""
		Crea un nuevo proyecto.
		
		Args:
			mostrar_dialogo: Si True, muestra el diálogo de selección de plantilla
		"""
		from .dialogos.dialogo_nuevo_proyecto import DialogoNuevoProyecto
		from ..modelo.plantilla import ServicioPlantillas
		
		if mostrar_dialogo:
			dialogo = DialogoNuevoProyecto(
				self,
				self.preferencias.directorio_plantillas
			)
			
			if dialogo.ShowModal() == wx.ID_OK:
				self.proyecto = Proyecto()
				
				if dialogo.usar_plantilla():
					plantilla = dialogo.obtener_plantilla_seleccionada()
					if plantilla:
						servicio = ServicioPlantillas()
						servicio.aplicar_plantilla(self.proyecto, plantilla)
						self.registrar_log(f"Proyecto creado con plantilla: {plantilla.nombre}")
					else:
						self.registrar_log("Nuevo proyecto creado")
				else:
					self.registrar_log("Nuevo proyecto en blanco creado")
				
				self.panel_secciones.actualizar_arbol()
				self.panel_editor.limpiar()
				self.actualizar_titulo()
				self.actualizar_barra_estado("Nuevo proyecto creado")
			
			dialogo.Destroy()
		else:
			# Crear proyecto vacío sin diálogo (para inicio)
			self.proyecto = Proyecto()
			self.panel_secciones.actualizar_arbol()
			self.panel_editor.limpiar()
			self.actualizar_titulo()
			self.actualizar_barra_estado("Listo")
	
	def abrir_proyecto(self, ruta: Optional[str] = None) -> bool:
		"""
		Abre un proyecto existente.
		
		Args:
			ruta: Ruta del archivo (si es None, muestra diálogo)
		
		Returns:
			bool: True si se abrió correctamente
		"""
		if ruta is None:
			dialogo = wx.FileDialog(
				self,
				message="Abrir proyecto",
				wildcard=self.servicio_persistencia.FILTRO_ARCHIVO,
				style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
			)
			
			if dialogo.ShowModal() != wx.ID_OK:
				dialogo.Destroy()
				return False
			
			ruta = dialogo.GetPath()
			dialogo.Destroy()
		
		try:
			self.proyecto = self.servicio_persistencia.cargar_proyecto(ruta)
			self.panel_secciones.actualizar_arbol()
			self.panel_editor.limpiar()
			self.actualizar_titulo()
			self.actualizar_barra_estado(f"Proyecto abierto: {os.path.basename(ruta)}")
			self.registrar_log(f"Proyecto abierto: {ruta}")
			
			# Agregar a recientes
			self.preferencias.agregar_proyecto_reciente(ruta)
			
			return True
			
		except ErrorPersistencia as e:
			wx.MessageBox(
				str(e),
				"Error al abrir proyecto",
				wx.OK | wx.ICON_ERROR
			)
			return False
	
	def guardar_proyecto(self) -> bool:
		"""
		Guarda el proyecto actual.
		
		Returns:
			bool: True si se guardó correctamente
		"""
		if not self.proyecto:
			return False
		
		if not self.proyecto.ruta_archivo:
			return self.guardar_proyecto_como()
		
		try:
			self.servicio_persistencia.guardar_proyecto(
				self.proyecto,
				self.proyecto.ruta_archivo
			)
			self.actualizar_titulo()
			self.actualizar_barra_estado("Proyecto guardado")
			self.registrar_log(f"Proyecto guardado: {self.proyecto.ruta_archivo}")
			return True
			
		except ErrorPersistencia as e:
			wx.MessageBox(
				str(e),
				"Error al guardar",
				wx.OK | wx.ICON_ERROR
			)
			return False
	
	def guardar_proyecto_como(self) -> bool:
		"""
		Guarda el proyecto con un nuevo nombre.
		
		Returns:
			bool: True si se guardó correctamente
		"""
		if not self.proyecto:
			return False
		
		# Sugerir nombre basado en título
		nombre_sugerido = self.proyecto.metadatos.titulo or "proyecto"
		nombre_sugerido = nombre_sugerido.replace(' ', '_').lower()
		
		dialogo = wx.FileDialog(
			self,
			message="Guardar proyecto como",
			defaultFile=nombre_sugerido,
			wildcard=self.servicio_persistencia.FILTRO_ARCHIVO,
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		)
		
		if dialogo.ShowModal() != wx.ID_OK:
			dialogo.Destroy()
			return False
		
		ruta = dialogo.GetPath()
		dialogo.Destroy()
		
		try:
			self.servicio_persistencia.guardar_proyecto(self.proyecto, ruta)
			self.actualizar_titulo()
			self.actualizar_barra_estado(f"Proyecto guardado: {os.path.basename(ruta)}")
			self.registrar_log(f"Proyecto guardado como: {ruta}")
			
			# Agregar a recientes
			self.preferencias.agregar_proyecto_reciente(ruta)
			
			return True
			
		except ErrorPersistencia as e:
			wx.MessageBox(
				str(e),
				"Error al guardar",
				wx.OK | wx.ICON_ERROR
			)
			return False
	
	def exportar_epub(self) -> bool:
		"""
		Exporta el proyecto a formato EPUB.
		
		Returns:
			bool: True si se exportó correctamente
		"""
		if not self.proyecto:
			return False
		
		# Validar primero
		problemas = self.servicio_validacion.validar_proyecto(self.proyecto)
		
		errores = [p for p in problemas if not p.startswith("Advertencia")]
		advertencias = [p for p in problemas if p.startswith("Advertencia")]
		
		if errores:
			mensaje = "Se encontraron los siguientes errores:\n\n"
			mensaje += "\n".join(f"• {e}" for e in errores)
			mensaje += "\n\n¿Desea continuar de todos modos?"
			
			if wx.MessageBox(
				mensaje,
				"Errores de validación",
				wx.YES_NO | wx.ICON_WARNING
			) != wx.YES:
				return False
		
		# Mostrar advertencias
		if advertencias:
			for adv in advertencias:
				self.registrar_log(adv, "advertencia")
		
		# Seleccionar destino
		nombre_sugerido = self.proyecto.metadatos.titulo or "libro"
		nombre_sugerido = nombre_sugerido.replace(' ', '_').lower() + ".epub"
		
		dialogo = wx.FileDialog(
			self,
			message="Exportar EPUB",
			defaultFile=nombre_sugerido,
			wildcard="EPUB (*.epub)|*.epub",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		)
		
		if dialogo.ShowModal() != wx.ID_OK:
			dialogo.Destroy()
			return False
		
		ruta = dialogo.GetPath()
		dialogo.Destroy()
		
		# Exportar
		self.registrar_log("Iniciando exportación EPUB...")
		
		resultado = self.servicio_epub.generar_epub(self.proyecto, ruta)
		
		if resultado.exito:
			self.registrar_log(f"EPUB exportado exitosamente: {ruta}")
			self.actualizar_barra_estado("EPUB exportado")
			
			# Mostrar archivos generados
			for archivo in resultado.archivos_generados:
				self.registrar_log(f"  Generado: {archivo}")
			
			# Preguntar si validar
			if wx.MessageBox(
				"EPUB exportado correctamente.\n\n¿Desea validar el archivo?",
				"Exportación completada",
				wx.YES_NO | wx.ICON_QUESTION
			) == wx.YES:
				self._validar_epub_externo(ruta)
			
			return True
		else:
			for error in resultado.errores:
				self.registrar_log(error, "error")
			
			wx.MessageBox(
				"Error al exportar EPUB.\nRevise el panel de logs para más detalles.",
				"Error de exportación",
				wx.OK | wx.ICON_ERROR
			)
			return False
	
	def validar_proyecto(self) -> None:
		"""Valida el proyecto actual."""
		if not self.proyecto:
			return
		
		self.registrar_log("Validando proyecto...")
		
		problemas = self.servicio_validacion.validar_proyecto(self.proyecto)
		
		if problemas:
			for problema in problemas:
				if problema.startswith("Advertencia"):
					self.registrar_log(problema, "advertencia")
				else:
					self.registrar_log(problema, "error")
			
			self.actualizar_barra_estado(f"{len(problemas)} problema(s) encontrado(s)")
		else:
			self.registrar_log("Validación completada sin problemas", "info")
			self.actualizar_barra_estado("Validación exitosa")
	
	def _validar_epub_externo(self, ruta: str) -> None:
		"""Valida un EPUB con herramientas externas."""
		# EPUBCheck
		if self.servicio_validacion.epubcheck_disponible():
			self.registrar_log("Ejecutando EPUBCheck...")
			resultado = self.servicio_validacion.ejecutar_epubcheck(ruta)
			
			if resultado.exito:
				self.registrar_log("EPUBCheck: Validación exitosa")
			else:
				for error in resultado.errores:
					self.registrar_log(f"EPUBCheck: {error}", "error")
			
			for adv in resultado.advertencias:
				self.registrar_log(f"EPUBCheck: {adv}", "advertencia")
		else:
			self.registrar_log(
				"EPUBCheck no está disponible. " +
				self.servicio_validacion.obtener_instrucciones_instalacion(),
				"advertencia"
			)
	
	def _confirmar_cambios_sin_guardar(self) -> bool:
		"""
		Confirma si hay cambios sin guardar.
		
		Returns:
			bool: True si se puede continuar, False si se canceló
		"""
		if not self.proyecto or not self.proyecto.modificado:
			return True
		
		respuesta = wx.MessageBox(
			"Hay cambios sin guardar.\n\n¿Desea guardar antes de continuar?",
			"Cambios sin guardar",
			wx.YES_NO_CANCEL | wx.ICON_QUESTION
		)
		
		if respuesta == wx.YES:
			return self.guardar_proyecto()
		elif respuesta == wx.NO:
			return True
		else:  # CANCEL
			return False
	
	def _importar_archivo(self, ruta: str, titulo: str, tipo: TipoSeccion) -> None:
		"""Importa un archivo como nueva sección."""
		from ..servicios.servicio_importacion import ServicioImportacion, ErrorImportacion
		
		servicio = ServicioImportacion()
		
		try:
			contenido = servicio.importar_archivo(ruta)
			
			# Crear sección
			seccion = self.proyecto.agregar_seccion(tipo, titulo)
			seccion.establecer_contenido(contenido)
			
			# Actualizar interfaz
			self.panel_secciones.actualizar_arbol()
			self.actualizar_titulo()
			self.actualizar_barra_estado()
			self.registrar_log(f"Archivo importado: {os.path.basename(ruta)}")
			
		except ErrorImportacion as e:
			wx.MessageBox(
				str(e),
				"Error de importación",
				wx.OK | wx.ICON_ERROR
			)
	
	# === Métodos para paneles ===
	
	def seleccionar_seccion(self, seccion: Optional[Seccion]) -> None:
		"""
		Selecciona una sección para editar.
		
		Args:
			seccion: Sección a editar (None para limpiar)
		"""
		self.panel_editor.cargar_seccion(seccion)
	
	def actualizar_seccion(self, seccion: Seccion) -> None:
		"""
		Actualiza una sección después de editar.
		
		Args:
			seccion: Sección actualizada
		"""
		self.proyecto.marcar_modificado()
		self.panel_secciones.actualizar_item_seccion(seccion)
		self.actualizar_titulo()
		self.actualizar_barra_estado()
	
	# === Métodos de exportación adicionales ===
	
	def exportar_pdf(self) -> bool:
		"""
		Exporta el proyecto a formato PDF.
		
		Returns:
			bool: True si se exportó correctamente
		"""
		if not self.proyecto:
			return False
		
		# Verificar dependencias
		disponible, mensaje = self.servicio_exportacion.verificar_dependencias('pdf')
		if not disponible:
			wx.MessageBox(
				mensaje,
				"Dependencia no disponible",
				wx.OK | wx.ICON_WARNING
			)
			return False
		
		# Seleccionar destino
		nombre_sugerido = self.proyecto.metadatos.titulo or "libro"
		nombre_sugerido = nombre_sugerido.replace(' ', '_').lower() + ".pdf"
		
		dialogo = wx.FileDialog(
			self,
			message="Exportar PDF",
			defaultFile=nombre_sugerido,
			wildcard="PDF (*.pdf)|*.pdf",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		)
		
		if dialogo.ShowModal() != wx.ID_OK:
			dialogo.Destroy()
			return False
		
		ruta = dialogo.GetPath()
		dialogo.Destroy()
		
		# Exportar
		self.registrar_log("Iniciando exportación PDF...")
		
		resultado = self.servicio_exportacion.exportar_pdf(self.proyecto, ruta)
		
		if resultado.exito:
			self.registrar_log(f"PDF exportado exitosamente: {ruta}")
			self.actualizar_barra_estado("PDF exportado")
			wx.MessageBox(
				f"PDF exportado correctamente:\n{ruta}",
				"Exportación completada",
				wx.OK | wx.ICON_INFORMATION
			)
			return True
		else:
			for error in resultado.errores:
				self.registrar_log(error, "error")
			wx.MessageBox(
				"Error al exportar PDF.\nRevise el panel de logs.",
				"Error de exportación",
				wx.OK | wx.ICON_ERROR
			)
			return False
	
	def exportar_mobi(self) -> bool:
		"""
		Exporta el proyecto a formato MOBI.
		
		Returns:
			bool: True si se exportó correctamente
		"""
		if not self.proyecto:
			return False
		
		# Verificar dependencias
		disponible, mensaje = self.servicio_exportacion.verificar_dependencias('mobi')
		if not disponible:
			wx.MessageBox(
				mensaje,
				"Dependencia no disponible",
				wx.OK | wx.ICON_WARNING
			)
			return False
		
		# Seleccionar destino
		nombre_sugerido = self.proyecto.metadatos.titulo or "libro"
		nombre_sugerido = nombre_sugerido.replace(' ', '_').lower() + ".mobi"
		
		dialogo = wx.FileDialog(
			self,
			message="Exportar MOBI",
			defaultFile=nombre_sugerido,
			wildcard="MOBI (*.mobi)|*.mobi",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		)
		
		if dialogo.ShowModal() != wx.ID_OK:
			dialogo.Destroy()
			return False
		
		ruta = dialogo.GetPath()
		dialogo.Destroy()
		
		# Exportar
		self.registrar_log("Iniciando exportación MOBI...")
		
		resultado = self.servicio_exportacion.exportar_mobi(self.proyecto, ruta)
		
		if resultado.exito:
			self.registrar_log(f"MOBI exportado exitosamente: {ruta}")
			self.actualizar_barra_estado("MOBI exportado")
			wx.MessageBox(
				f"MOBI exportado correctamente:\n{ruta}",
				"Exportación completada",
				wx.OK | wx.ICON_INFORMATION
			)
			return True
		else:
			for error in resultado.errores:
				self.registrar_log(error, "error")
			wx.MessageBox(
				"Error al exportar MOBI.\nRevise el panel de logs.",
				"Error de exportación",
				wx.OK | wx.ICON_ERROR
			)
			return False
	
	def exportar_html(self) -> bool:
		"""
		Exporta el proyecto a carpeta HTML.
		
		Returns:
			bool: True si se exportó correctamente
		"""
		if not self.proyecto:
			return False
		
		# Seleccionar carpeta destino
		dialogo = wx.DirDialog(
			self,
			message="Seleccionar carpeta para exportar HTML",
			style=wx.DD_DEFAULT_STYLE
		)
		
		if dialogo.ShowModal() != wx.ID_OK:
			dialogo.Destroy()
			return False
		
		carpeta = dialogo.GetPath()
		dialogo.Destroy()
		
		# Crear subcarpeta con nombre del libro
		nombre_libro = self.proyecto.metadatos.titulo or "libro"
		nombre_libro = nombre_libro.replace(' ', '_').lower()
		carpeta_salida = os.path.join(carpeta, nombre_libro + "_html")
		
		# Exportar
		self.registrar_log("Iniciando exportación HTML...")
		
		resultado = self.servicio_exportacion.exportar_html(self.proyecto, carpeta_salida)
		
		if resultado.exito:
			self.registrar_log(f"HTML exportado exitosamente: {carpeta_salida}")
			self.actualizar_barra_estado("HTML exportado")
			
			# Preguntar si abrir carpeta
			if wx.MessageBox(
				f"HTML exportado correctamente:\n{carpeta_salida}\n\n¿Desea abrir la carpeta?",
				"Exportación completada",
				wx.YES_NO | wx.ICON_QUESTION
			) == wx.YES:
				import subprocess
				subprocess.Popen(f'explorer "{carpeta_salida}"')
			
			return True
		else:
			for error in resultado.errores:
				self.registrar_log(error, "error")
			wx.MessageBox(
				"Error al exportar HTML.\nRevise el panel de logs.",
				"Error de exportación",
				wx.OK | wx.ICON_ERROR
			)
			return False
	
	def mostrar_vista_previa(self) -> None:
		"""Muestra la ventana de vista previa del EPUB."""
		if not self.proyecto:
			wx.MessageBox(
				"No hay proyecto abierto.",
				"Vista previa",
				wx.OK | wx.ICON_INFORMATION
			)
			return
		
		from .ventana_vista_previa import VentanaVistaPrevia
		
		ventana = VentanaVistaPrevia(self, self.proyecto)
		ventana.Show()
	
	def guardar_como_plantilla(self) -> None:
		"""Guarda el proyecto actual como plantilla personalizada."""
		if not self.proyecto:
			return
		
		from ..modelo.plantilla import ServicioPlantillas
		
		# Pedir nombre de la plantilla
		nombre = wx.GetTextFromUser(
			"Ingrese el nombre para la plantilla:",
			"Guardar como plantilla",
			self.proyecto.metadatos.titulo or "Mi plantilla"
		)
		
		if not nombre:
			return
		
		# Pedir descripción
		descripcion = wx.GetTextFromUser(
			"Ingrese una descripción para la plantilla:",
			"Descripción de la plantilla",
			f"Plantilla basada en {self.proyecto.metadatos.titulo or 'proyecto actual'}"
		)
		
		# Crear plantilla
		servicio = ServicioPlantillas()
		plantilla = servicio.crear_plantilla_desde_proyecto(
			self.proyecto,
			nombre,
			descripcion or ""
		)
		
		# Determinar directorio de plantillas
		directorio = self.preferencias.directorio_plantillas
		if not directorio:
			# Usar directorio por defecto
			if os.name == 'nt':
				base = os.environ.get('APPDATA', os.path.expanduser('~'))
			else:
				base = os.path.expanduser('~/.config')
			directorio = os.path.join(base, 'MaquetadorEPUB', 'plantillas')
			self.preferencias.directorio_plantillas = directorio
		
		# Guardar plantilla
		if servicio.guardar_plantilla_personalizada(plantilla, directorio):
			self.registrar_log(f"Plantilla guardada: {nombre}")
			wx.MessageBox(
				f"Plantilla '{nombre}' guardada correctamente.",
				"Plantilla guardada",
				wx.OK | wx.ICON_INFORMATION
			)
		else:
			wx.MessageBox(
				"Error al guardar la plantilla.",
				"Error",
				wx.OK | wx.ICON_ERROR
			)
