# -*- coding: utf-8 -*-
"""
Constantes de la aplicación.
Define valores constantes utilizados en toda la aplicación.
"""

# Nombres legibles de los tipos de sección
TIPOS_SECCION_NOMBRES = {
	'cover': 'Portada',
	'backmatter': 'Contraportada',
	'abstract': 'Sinopsis',
	'foreword': 'Prólogo',
	'afterword': 'Epílogo',
	'dedication': 'Dedicatoria',
	'acknowledgments': 'Agradecimientos',
	'toc': 'Índice',
	'chapter': 'Capítulo',
	'appendix': 'Anexo',
	'colophon': 'Colofón',
	'preface': 'Prefacio',
	'introduction': 'Introducción',
	'bibliography': 'Bibliografía',
	'glossary': 'Glosario'
}

# Tipos epub:type válidos para EPUB 3
EPUB_TYPES = [
	'cover',
	'frontmatter',
	'bodymatter',
	'backmatter',
	'titlepage',
	'toc',
	'foreword',
	'preface',
	'introduction',
	'prologue',
	'chapter',
	'part',
	'division',
	'afterword',
	'epilogue',
	'conclusion',
	'appendix',
	'glossary',
	'bibliography',
	'index',
	'colophon',
	'dedication',
	'acknowledgments',
	'abstract'
]

# Códigos de idioma BCP 47 comunes
CODIGOS_IDIOMA = [
	'es',
	'es-ES',
	'es-MX',
	'es-AR',
	'en',
	'en-US',
	'en-GB',
	'fr',
	'fr-FR',
	'de',
	'de-DE',
	'it',
	'it-IT',
	'pt',
	'pt-BR',
	'pt-PT',
	'ca',
	'gl',
	'eu'
]

# Características de accesibilidad EPUB
ACCESSIBILITY_FEATURES = [
	'tableOfContents',
	'structuralNavigation',
	'alternativeText',
	'longDescription',
	'readingOrder',
	'displayTransformability',
	'printPageNumbers',
	'pageBreakMarkers',
	'index',
	'ARIA'
]

# Peligros de accesibilidad EPUB
ACCESSIBILITY_HAZARDS = [
	'none',
	'flashing',
	'motionSimulation',
	'sound',
	'noFlashingHazard',
	'noMotionSimulationHazard',
	'noSoundHazard'
]

# Modos de acceso
ACCESS_MODES = [
	'textual',
	'visual',
	'auditory',
	'tactile'
]

# Niveles WCAG
WCAG_LEVELS = ['A', 'AA', 'AAA']
WCAG_VERSIONS = ['2.0', '2.1', '2.2']

# Extensiones de archivo soportadas
EXTENSIONES_IMPORTACION = {
	'txt': 'Archivos de texto (*.txt)',
	'md': 'Archivos Markdown (*.md)',
	'html': 'Archivos HTML (*.html;*.htm)'
}

# Versión del formato de proyecto
VERSION_FORMATO_PROYECTO = "1.0"

# Nombre de la aplicación
NOMBRE_APP = "Maquetador EPUB Accesible"
VERSION_APP = "1.0.1"
