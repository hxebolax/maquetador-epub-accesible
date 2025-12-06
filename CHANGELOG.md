# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

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
- Soporte para imágenes en secciones
- Editor WYSIWYG de contenido
- Vista previa del EPUB
- Plantillas de libro predefinidas
- Exportación a otros formatos
- Internacionalización (i18n)
