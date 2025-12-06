# Guía de Contribución

¡Gracias por tu interés en contribuir al Maquetador de EPUB Accesibles! Este documento proporciona las pautas para contribuir al proyecto.

## Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que respetes este código.

- Sé respetuoso y considerado
- Acepta críticas constructivas
- Enfócate en lo que es mejor para la comunidad
- Muestra empatía hacia otros miembros de la comunidad

## ¿Cómo puedo contribuir?

### Reportando bugs

Si encuentras un bug, por favor abre un issue con:

1. **Título descriptivo**: Resume el problema en una línea
2. **Descripción**: Explica el problema en detalle
3. **Pasos para reproducir**: Lista los pasos exactos
4. **Comportamiento esperado**: Qué debería pasar
5. **Comportamiento actual**: Qué pasa realmente
6. **Capturas de pantalla**: Si aplica
7. **Entorno**: Sistema operativo, versión de Python, etc.

### Sugiriendo mejoras

Las sugerencias de mejoras son bienvenidas. Abre un issue con:

1. **Título descriptivo**: Resume la mejora propuesta
2. **Descripción detallada**: Explica la mejora
3. **Justificación**: Por qué sería útil
4. **Ejemplos**: Si es posible, proporciona ejemplos

### Pull Requests

1. **Fork** el repositorio
2. **Clona** tu fork localmente
3. **Crea una rama** para tu cambio:
   ```bash
   git checkout -b feature/mi-nueva-funcionalidad
   ```
4. **Haz tus cambios** siguiendo las guías de estilo
5. **Prueba** tus cambios
6. **Commit** con mensajes descriptivos:
   ```bash
   git commit -m "Añade funcionalidad X para resolver Y"
   ```
7. **Push** a tu fork:
   ```bash
   git push origin feature/mi-nueva-funcionalidad
   ```
8. **Abre un Pull Request**

## Guías de Estilo

### Python

- **Indentación**: Usa tabs, no espacios
- **Idioma**: Código, comentarios y documentación en español
- **Docstrings**: Usa docstrings para todas las funciones y clases
- **Nombres**: Usa snake_case para funciones y variables, PascalCase para clases
- **Longitud de línea**: Máximo 100 caracteres

### Ejemplo de código

```python
# -*- coding: utf-8 -*-
"""
Módulo de ejemplo.
Descripción del módulo.
"""

class MiClase:
	"""
	Descripción de la clase.
	
	Attributes:
		atributo: Descripción del atributo
	"""
	
	def __init__(self, parametro: str):
		"""
		Inicializa la clase.
		
		Args:
			parametro: Descripción del parámetro
		"""
		self.atributo = parametro
	
	def mi_metodo(self, valor: int) -> bool:
		"""
		Descripción del método.
		
		Args:
			valor: Descripción del valor
		
		Returns:
			bool: Descripción del retorno
		"""
		return valor > 0
```

### Accesibilidad

**IMPORTANTE**: Este proyecto está diseñado para ser accesible. Cualquier contribución debe mantener o mejorar la accesibilidad.

- Todos los controles de interfaz deben ser accesibles por teclado
- Usa `SetName()` para dar nombres descriptivos a los controles
- Proporciona tooltips con `SetToolTip()`
- Usa aceleradores de teclado (ej: `&Archivo` para Alt+A)
- Prueba con un lector de pantalla si es posible

### Commits

- Usa mensajes en español
- Primera línea: resumen corto (máx. 50 caracteres)
- Línea en blanco
- Descripción detallada si es necesario

Ejemplo:
```
Añade validación de metadatos de accesibilidad

- Verifica que el resumen de accesibilidad no esté vacío
- Valida los modos de acceso seleccionados
- Muestra advertencias en el panel de logs
```

## Estructura del Proyecto

```
src/
├── modelo/      # Clases de datos (Proyecto, Seccion, etc.)
├── servicios/   # Lógica de negocio (EPUB, validación, etc.)
├── gui/         # Interfaz gráfica (ventanas, paneles, diálogos)
├── utils/       # Utilidades y constantes
└── recursos/    # Archivos estáticos (CSS, imágenes)
```

### Dónde añadir código nuevo

- **Nueva funcionalidad de datos**: `src/modelo/`
- **Nueva lógica de negocio**: `src/servicios/`
- **Nuevo diálogo o panel**: `src/gui/` o `src/gui/dialogos/`
- **Nuevas constantes**: `src/utils/constantes.py`
- **Nuevas funciones de utilidad**: `src/utils/helpers.py`

## Pruebas

Antes de enviar un PR:

1. Ejecuta la aplicación y prueba tu cambio
2. Verifica que no rompe funcionalidad existente
3. Prueba la navegación por teclado
4. Si es posible, prueba con un lector de pantalla

## Preguntas

Si tienes preguntas, abre un issue con la etiqueta `pregunta`.

¡Gracias por contribuir! 🎉
