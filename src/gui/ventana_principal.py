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
		
		# Estado
		self.proyecto: Optional[Proyecto] = None
		self.preferencias = Preferencias.cargar()
		
		# Crear interfaz
		self._crear_menu()
		self._crear_barra_herramientas()
		self._crear_paneles()
		self._crear_barra_estado()
		self._configurar_atajos()
		self._configurar_eventos()
		
		# Centrar ventana
		self.Centre()
		
		# Crear proyecto vacío inicial
		self.nuevo_proyecto()
	
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
		item_exportar = menu_archivo.Append(wx.ID_ANY, "&Exportar EPUB...\tCtrl+E", "Exportar a formato EPUB")
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
		
		# Menú Proyecto
		menu_proyecto = wx.Menu()
		
		self.item_agregar_seccion = menu_proyecto.Append(
			wx.ID_ANY, "&Agregar sección...\tCtrl+Shift+A", "Agregar nueva sección"
		)
		self.item_importar = menu_proyecto.Append(
			wx.ID_ANY, "&Importar archivo...\tCtrl+I", "Importar contenido desde archivo"
		)
		self.item_importar_multiple = menu_proyecto.Append(
			wx.ID_ANY, "Importar &múltiples archivos...\tCtrl+Shift+I", "Importar varios archivos a la vez"
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
		self.Bind(wx.EVT_MENU, self.on_exportar, item_exportar)
		self.Bind(wx.EVT_MENU, self.on_salir, item_salir)
		
		self.Bind(wx.EVT_MENU, self.on_agregar_seccion, self.item_agregar_seccion)
		self.Bind(wx.EVT_MENU, self.on_importar, self.item_importar)
		self.Bind(wx.EVT_MENU, self.on_importar_multiple, self.item_importar_multiple)
		self.Bind(wx.EVT_MENU, self.on_metadatos, self.item_metadatos)
		self.Bind(wx.EVT_MENU, self.on_accesibilidad, self.item_accesibilidad)
		self.Bind(wx.EVT_MENU, self.on_portada, self.item_portada)
		
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
		self.nuevo_proyecto()
	
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
	
	def on_exportar(self, event) -> None:
		"""Exporta el proyecto a EPUB."""
		self.exportar_epub()
	
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
		
		dialogo = DialogoPreferencias(self, self.preferencias)
		if dialogo.ShowModal() == wx.ID_OK:
			self.preferencias = dialogo.obtener_preferencias()
			self.preferencias.guardar()
			self.registrar_log("Preferencias guardadas")
		
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
	
	def nuevo_proyecto(self) -> None:
		"""Crea un nuevo proyecto vacío."""
		self.proyecto = Proyecto()
		self.panel_secciones.actualizar_arbol()
		self.panel_editor.limpiar()
		self.actualizar_titulo()
		self.actualizar_barra_estado("Nuevo proyecto creado")
		self.registrar_log("Nuevo proyecto creado")
	
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
