# -*- coding: utf-8 -*-
"""
Diálogo de Manual de Uso.
Muestra el manual completo de la aplicación.
"""

import wx


class DialogoManual(wx.Dialog):
	"""
	Diálogo accesible con el manual de uso de la aplicación.
	"""
	
	MANUAL = """MAQUETADOR DE EPUB ACCESIBLES - MANUAL DE USO

==============================================
1. INTRODUCCIÓN
==============================================

Esta aplicación permite crear libros EPUB 3 totalmente accesibles, cumpliendo con las pautas WCAG 2.1/2.2 y EPUB Accessibility 1.1.

La interfaz está diseñada para ser completamente usable con teclado y lectores de pantalla como NVDA, JAWS o Narrator.

==============================================
2. GESTIÓN DE PROYECTOS
==============================================

2.1 Crear un nuevo proyecto
- Use Ctrl+N o el menú Archivo > Nuevo proyecto
- Se creará un proyecto vacío con metadatos por defecto

2.2 Abrir un proyecto existente
- Use Ctrl+O o el menú Archivo > Abrir proyecto
- Seleccione un archivo con extensión .mepub

2.3 Guardar el proyecto
- Use Ctrl+S para guardar en la ubicación actual
- Use Ctrl+Shift+S para guardar con otro nombre

2.4 Exportar a EPUB
- Use Ctrl+E o el menú Archivo > Exportar EPUB
- Seleccione la ubicación y nombre del archivo EPUB
- La aplicación validará el proyecto antes de exportar

==============================================
3. ESTRUCTURA DEL LIBRO
==============================================

3.1 Panel de secciones
El panel izquierdo muestra la estructura del libro en forma de árbol.

3.2 Agregar secciones
- Use Ctrl+Shift+A o el botón "Agregar"
- Seleccione el tipo de sección (capítulo, prólogo, etc.)
- Ingrese el título de la sección

3.3 Importar contenido
- Use Ctrl+I para importar un archivo individual
- Use Ctrl+Shift+I para importar múltiples archivos
- Formatos soportados: TXT, Markdown (.md), HTML

3.4 Organizar secciones
- Use Alt+Flecha Arriba/Abajo para mover secciones
- Use F2 para renombrar una sección
- Use Delete para eliminar una sección

3.5 Tipos de sección disponibles
- Capítulo: Contenido principal del libro
- Prólogo: Texto introductorio
- Epílogo: Texto de cierre
- Introducción: Presentación del tema
- Prefacio: Notas del autor
- Dedicatoria: Dedicación del libro
- Agradecimientos: Reconocimientos
- Anexo: Material complementario
- Bibliografía: Referencias
- Glosario: Definiciones de términos
- Sinopsis: Resumen del libro
- Colofón: Información de edición

==============================================
4. EDICIÓN DE CONTENIDO
==============================================

4.1 Panel de edición
El panel derecho permite editar el contenido de la sección seleccionada.

4.2 Campos editables
- Título: Nombre de la sección
- Tipo: Tipo de sección (capítulo, prólogo, etc.)
- Nivel: Nivel de encabezado (1-6)
- Contenido: Texto en formato XHTML

4.3 Botones de formato
- H1, H2, H3: Insertar encabezados
- P: Insertar párrafo
- Lista: Insertar lista no ordenada
- Cita: Insertar cita (blockquote)

4.4 Guardar cambios
- Use el botón "Guardar cambios" o Ctrl+S

==============================================
5. METADATOS DEL LIBRO
==============================================

5.1 Metadatos Dublin Core (Ctrl+M)
- Título: Nombre del libro (obligatorio)
- Identificador: UUID único (obligatorio)
- Idioma: Código BCP 47, ej: es, es-ES (obligatorio)
- Autores: Lista de autores
- Editor: Editorial
- Fecha: Fecha de publicación (AAAA-MM-DD)
- Derechos: Información de copyright
- Descripción: Sinopsis del libro
- Temas: Palabras clave separadas por comas

5.2 Metadatos de accesibilidad (Ctrl+Shift+M)
- Nivel WCAG: Versión y nivel de conformidad
- Modos de acceso: Textual, visual, auditivo, táctil
- Características: Tabla de contenidos, navegación, etc.
- Peligros: Contenido parpadeante, sonido, etc.
- Resumen: Descripción de accesibilidad en lenguaje natural

==============================================
6. IMÁGENES Y PORTADA
==============================================

6.1 Agregar portada
- Use el menú Proyecto > Portada
- Seleccione una imagen JPG o PNG
- Ingrese el texto alternativo (obligatorio)

6.2 Imágenes en secciones
- Las imágenes requieren texto alternativo obligatorio
- Opcionalmente puede agregar descripción larga

==============================================
7. VALIDACIÓN
==============================================

7.1 Validación interna (F5)
Verifica:
- Metadatos obligatorios completos
- Todas las secciones tienen título
- Imágenes tienen texto alternativo
- Estructura de encabezados coherente

7.2 EPUBCheck
Herramienta externa para validar estructura EPUB.
Requiere Java instalado.

7.3 Ace by DAISY
Herramienta externa para validar accesibilidad.
Requiere Node.js instalado.

==============================================
8. PREFERENCIAS
==============================================

Acceda con el menú Herramientas > Preferencias:
- Directorios por defecto
- Guardado automático
- Confirmación antes de eliminar
- Mostrar panel de mensajes

==============================================
9. CONSEJOS DE ACCESIBILIDAD
==============================================

Para crear EPUB accesibles:
- Use encabezados jerárquicos (h1, h2, h3...)
- Proporcione texto alternativo a todas las imágenes
- Use listas para enumerar elementos
- Incluya tabla de contenidos
- Complete el resumen de accesibilidad
- Valide con Ace by DAISY antes de publicar

==============================================
10. SOLUCIÓN DE PROBLEMAS
==============================================

Si la exportación falla:
1. Verifique que todos los metadatos obligatorios estén completos
2. Asegúrese de que todas las secciones tengan título
3. Compruebe que las imágenes tengan texto alternativo
4. Revise el panel de mensajes para ver errores específicos

Si las herramientas de validación no funcionan:
- EPUBCheck requiere Java instalado
- Ace requiere Node.js y npm install -g @daisy/ace
"""
	
	def __init__(self, parent):
		"""
		Inicializa el diálogo.
		
		Args:
			parent: Ventana padre
		"""
		super().__init__(
			parent,
			title="Manual de uso",
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX
		)
		
		self._crear_controles()
		self._configurar_layout()
		
		self.SetSize((700, 600))
		self.Centre()
	
	def _crear_controles(self) -> None:
		"""Crea los controles del diálogo."""
		self.lbl_manual = wx.StaticText(self, label="&Manual de uso:")
		
		self.txt_manual = wx.TextCtrl(
			self,
			value=self.MANUAL,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.HSCROLL
		)
		self.txt_manual.SetName("Manual de uso de la aplicación")
		
		# Establecer fuente monoespaciada para mejor lectura
		fuente = wx.Font(
			10,
			wx.FONTFAMILY_TELETYPE,
			wx.FONTSTYLE_NORMAL,
			wx.FONTWEIGHT_NORMAL
		)
		self.txt_manual.SetFont(fuente)
		
		self.btn_cerrar = wx.Button(self, wx.ID_CLOSE, label="&Cerrar")
	
	def _configurar_layout(self) -> None:
		"""Configura el layout del diálogo."""
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.lbl_manual, 0, wx.ALL, 10)
		sizer.Add(self.txt_manual, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		sizer.Add(self.btn_cerrar, 0, wx.ALL | wx.ALIGN_CENTER, 10)
		
		self.SetSizer(sizer)
		
		self.btn_cerrar.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))
		self.txt_manual.SetFocus()
