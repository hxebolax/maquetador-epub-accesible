# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.2] - 2025-12-06

### Añadido
- **Internacionalización (i18n)**: Soporte para 5 idiomas (español, inglés, francés, portugués, catalán)
- **Soporte para imágenes en secciones**: Insertar imágenes dentro del contenido de capítulos con texto alternativo obligatorio y descripción larga opcional (Ctrl+Shift+I)
- **Editor WYSIWYG**: Editor visual con barra de formato (negrita, cursiva, encabezados, listas, citas) y atajos Ctrl+B/I/U
- **Vista previa del EPUB**: Ventana de previsualización con navegación entre secciones (F6)
- **Plantillas de libro**: 4 plantillas predefinidas (Novela, Manual técnico, Poemario, Ensayo) y soporte para plantillas personalizadas
- **Exportación a PDF**: Generación de PDF con marcadores de navegación usando WeasyPrint
- **Exportación a MOBI**: Conversión a formato Kindle usando Calibre
- **Exportación a HTML**: Generación de carpeta con archivos HTML navegables e index.html
- Diálogo de nuevo proyecto con selección de plantilla al crear proyecto (Ctrl+N)
- Selector de idioma en preferencias (requiere reinicio)
- Menú Ver con vista previa y toggle de panel de mensajes
- Submenú Archivo > Exportar con opciones EPUB, PDF, MOBI, HTML
- Menú Proyecto > Guardar como plantilla para crear plantillas personalizadas
- Alternancia entre modo visual y código en el editor

### Mejorado
- Panel de editor con botón de insertar imagen
- Modelo de preferencias con campos para idioma y modo de editor
- Modelo de sección con métodos mejorados para gestión de imágenes
- Manual de uso actualizado con todas las nuevas funcionalidades
- Diálogo de atajos de teclado actualizado

### Cambiado
- Atajo Ctrl+Shift+I ahora es para insertar imagen (antes era importar múltiples)
- Atajo Ctrl+Alt+I ahora es para importar múltiples archivos

## [1.0.1] - 2025-12-06

### Corregido
- Corregida la visualización de la imagen de portada en el EPUB generado
- Corregidas las rutas relativas de recursos (CSS e imágenes) en los archivos XHTML
- Corregido el uso del texto alternativo de la portada (ahora usa el campo correcto `texto_alternativo`)

### Mejorado
- Añadido soporte para descripción larga accesible en la imagen de portada
- La descripción larga se incluye como `figcaption` oculto visualmente pero accesible para lectores de pantalla
- Mejorada la estructura XHTML de la portada para mejor compatibilidad con lectores EPUB

## [1.0.0] - 2025-12-06

### Añadido
- Interfaz gráfica accesible con wxPython
- Gestión de proyectos (crear, abrir, guardar)
- Exportación a formato EPUB 3
- Importación de archivos TXT, Markdown y HTML
- Importación múltiple de archivos
- Metadatos Dublin Core completos
- Metadatos de accesibilidad EPUB Accessibility 1.1
- Panel de estructura del libro con árbol de secciones
- Panel de edición de contenido XHTML
- Panel de logs con mensajes de estado
- Validación interna del proyecto
- Soporte para EPUBCheck y Ace by DAISY
- Gestión de portada con texto alternativo obligatorio
- Tipos de sección: capítulo, prólogo, epílogo, dedicatoria, etc.
- Atajos de teclado completos
- Manual de uso integrado (F1)
- Diálogo de atajos de teclado
- Diálogo "Acerca de"
- Preferencias de usuario
- Navegación completa por teclado
- Compatibilidad con lectores de pantalla (NVDA, JAWS, Narrator)
- Feedback auditivo en límites de navegación
- Documentación en español

### Características de accesibilidad
- Todos los controles tienen nombres descriptivos
- Aceleradores de teclado en menús y botones
- Tooltips informativos
- Navegación por Tab entre paneles
- Alt+Flechas para mover secciones
- F2 para renombrar secciones
- Delete para eliminar secciones
- Sonido de alerta al llegar a límites

## [Unreleased]

### Planificado
- Mejoras en el editor WYSIWYG
- Más plantillas de libro
- Soporte para notas al pie
- Exportación a más formatos
