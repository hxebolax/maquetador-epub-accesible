# Maquetador de EPUB Accesibles

<p align="center">
  <strong>Aplicación de escritorio para crear libros EPUB 3 totalmente accesibles</strong>
</p>

<p align="center">
  <a href="#características">Características</a> •
  <a href="#instalación">Instalación</a> •
  <a href="#uso">Uso</a> •
  <a href="#accesibilidad">Accesibilidad</a> •
  <a href="#contribuir">Contribuir</a> •
  <a href="#licencia">Licencia</a>
</p>

---

## 🌟 Características

- **100% Accesible**: Diseñada para ser completamente usable con teclado y lectores de pantalla (NVDA, JAWS, Narrator)
- **EPUB 3 Compliant**: Genera archivos EPUB 3 válidos con metadatos de accesibilidad
- **WCAG 2.1/2.2**: Cumple con las pautas de accesibilidad web
- **EPUB Accessibility 1.1**: Implementa el estándar de accesibilidad para EPUB
- **Importación múltiple**: Importa archivos TXT, Markdown y HTML
- **Metadatos Dublin Core**: Gestión completa de metadatos bibliográficos
- **Validación integrada**: Soporte para EPUBCheck y Ace by DAISY

### Novedades en v1.0.2

- **🌍 Internacionalización**: Disponible en 5 idiomas (español, inglés, francés, portugués, catalán)
- **📝 Editor WYSIWYG**: Editor visual con formato en tiempo real
- **👁️ Vista previa**: Previsualiza tu libro antes de exportar (F6)
- **📚 Plantillas**: 4 plantillas predefinidas (Novela, Manual, Poemario, Ensayo)
- **🖼️ Imágenes en secciones**: Inserta imágenes con texto alternativo obligatorio
- **📄 Exportación múltiple**: Exporta a PDF, MOBI (Kindle) y HTML además de EPUB

## 📋 Requisitos

- Python 3.8 o superior
- Windows 10/11 (probado), Linux y macOS (compatibles)

## 🚀 Instalación

### Desde el código fuente

1. Clona el repositorio:
```bash
git clone https://github.com/hxebolax/maquetador-epub-accesible.git
cd maquetador-epub-accesible
```

2. Crea un entorno virtual:
```bash
python -m venv .venv
```

3. Activa el entorno virtual:

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

5. Ejecuta la aplicación:
```bash
python main.py
```

### Ejecutable (Windows)

Descarga el ejecutable desde la sección [Releases](https://github.com/hxebolax/maquetador-epub-accesible/releases).

## 📖 Uso

### Crear un nuevo proyecto

1. Abre la aplicación
2. Ve a **Archivo > Nuevo proyecto** (Ctrl+N)
3. Configura los metadatos en **Proyecto > Metadatos del libro** (Ctrl+M)
4. Agrega secciones con **Proyecto > Agregar sección** (Ctrl+Shift+A)

### Importar contenido

- **Archivo individual**: Ctrl+I
- **Múltiples archivos**: Ctrl+Shift+I
- Formatos soportados: `.txt`, `.md`, `.markdown`, `.html`, `.htm`

### Exportar a EPUB

1. Configura los metadatos de accesibilidad (Ctrl+Shift+M)
2. Valida el proyecto (F5)
3. Exporta con **Archivo > Exportar EPUB** (Ctrl+E)

## ⌨️ Atajos de teclado

| Acción | Atajo |
|--------|-------|
| Nuevo proyecto | Ctrl+N |
| Abrir proyecto | Ctrl+O |
| Guardar | Ctrl+S |
| Exportar EPUB | Ctrl+E |
| Vista previa | F6 |
| Agregar sección | Ctrl+Shift+A |
| Importar archivo | Ctrl+I |
| Importar múltiples | Ctrl+Alt+I |
| Insertar imagen | Ctrl+Shift+I |
| Metadatos | Ctrl+M |
| Accesibilidad | Ctrl+Shift+M |
| Validar | F5 |
| Manual de ayuda | F1 |
| Mover sección arriba | Alt+↑ |
| Mover sección abajo | Alt+↓ |
| Negrita (WYSIWYG) | Ctrl+B |
| Cursiva (WYSIWYG) | Ctrl+I |
| Subrayado (WYSIWYG) | Ctrl+U |

## ♿ Accesibilidad

Esta aplicación está diseñada siguiendo los principios de diseño universal:

- **Navegación por teclado**: Todas las funciones son accesibles sin ratón
- **Lectores de pantalla**: Compatible con NVDA, JAWS y Narrator
- **Etiquetas accesibles**: Todos los controles tienen nombres descriptivos
- **Atajos de teclado**: Acceso rápido a todas las funciones principales
- **Feedback auditivo**: Sonidos de alerta en límites de navegación

### Metadatos de accesibilidad generados

Los EPUB generados incluyen:
- `schema:accessMode` - Modos de acceso del contenido
- `schema:accessibilityFeature` - Características de accesibilidad
- `schema:accessibilityHazard` - Peligros potenciales
- `schema:accessibilitySummary` - Resumen en lenguaje natural
- Conformidad WCAG 2.1/2.2

## 🛠️ Tecnologías

- **Python 3** - Lenguaje de programación
- **wxPython** - Framework de interfaz gráfica
- **EbookLib** - Generación de archivos EPUB
- **Markdown** - Conversión de texto Markdown
- **BeautifulSoup** - Procesamiento de HTML
- **lxml** - Procesamiento XML
- **WeasyPrint** - Generación de PDF (opcional)
- **Calibre** - Conversión a MOBI (opcional, externo)

## 📁 Estructura del proyecto

```
maquetador-epub-accesible/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
├── LICENSE                # Licencia MIT
├── .gitignore            # Archivos ignorados por Git
├── src/
│   ├── modelo/           # Modelos de datos
│   │   ├── proyecto.py
│   │   ├── seccion.py
│   │   ├── metadatos.py
│   │   ├── imagen.py
│   │   ├── preferencias.py
│   │   └── plantilla.py      # Plantillas de libro
│   ├── servicios/        # Lógica de negocio
│   │   ├── servicio_epub.py
│   │   ├── servicio_xhtml.py
│   │   ├── servicio_importacion.py
│   │   ├── servicio_validacion.py
│   │   ├── servicio_persistencia.py
│   │   ├── servicio_i18n.py      # Internacionalización
│   │   └── servicio_exportacion.py  # PDF, MOBI, HTML
│   ├── gui/              # Interfaz gráfica
│   │   ├── ventana_principal.py
│   │   ├── panel_secciones.py
│   │   ├── panel_editor.py
│   │   ├── panel_editor_wysiwyg.py  # Editor visual
│   │   ├── panel_logs.py
│   │   ├── ventana_vista_previa.py  # Vista previa
│   │   └── dialogos/
│   ├── locales/          # Archivos de traducción
│   │   ├── es.json
│   │   ├── en.json
│   │   ├── fr.json
│   │   ├── pt.json
│   │   └── ca.json
│   ├── utils/            # Utilidades
│   │   ├── constantes.py
│   │   └── helpers.py
│   └── recursos/         # Recursos estáticos
│       └── estilos.css
└── scripts/              # Scripts de utilidad
    ├── crear_entorno.bat
    ├── ejecutar.bat
    └── compilar_pyinstaller.bat
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Guías de contribución

- Mantén el código accesible - todos los controles deben ser usables con teclado
- Usa español para comentarios y documentación
- Sigue el estilo de código existente (tabs para indentación)
- Añade docstrings a las funciones nuevas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- [wxPython](https://wxpython.org/) - Por el excelente framework de GUI
- [EbookLib](https://github.com/aerkalov/ebooklib) - Por la biblioteca de generación EPUB
- [DAISY Consortium](https://daisy.org/) - Por los estándares de accesibilidad

---

<p align="center">
  Hecho con ❤️ para la comunidad de personas con discapacidad visual
</p>
