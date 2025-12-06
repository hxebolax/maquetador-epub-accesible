# Política de Seguridad

## Versiones Soportadas

| Versión | Soportada          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reportar una Vulnerabilidad

Si descubres una vulnerabilidad de seguridad, por favor:

1. **No** abras un issue público
2. Envía un correo a xebolax@gmail.com con:
   - Descripción de la vulnerabilidad
   - Pasos para reproducirla
   - Impacto potencial
   - Sugerencias de solución (si las tienes)

Responderemos dentro de 48 horas y trabajaremos contigo para resolver el problema.

## Consideraciones de Seguridad

Esta aplicación:

- **No** envía datos a servidores externos
- **No** requiere conexión a internet para funcionar
- Almacena preferencias localmente en formato JSON
- Los proyectos se guardan en formato ZIP con extensión `.mepub`

### Archivos de Proyecto

Los archivos `.mepub` son archivos ZIP que contienen:
- `proyecto.json` - Metadatos y estructura del proyecto
- Imágenes referenciadas (si las hay)

No se ejecuta código arbitrario al abrir proyectos.

### Dependencias

Mantenemos las dependencias actualizadas. Si encuentras una vulnerabilidad en alguna dependencia, por favor repórtala.
