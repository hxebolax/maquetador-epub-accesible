# -*- coding: utf-8 -*-
"""
Funciones auxiliares de la aplicación.
Contiene utilidades comunes usadas en varios módulos.
"""

import uuid
import re
import unicodedata


def generar_uuid():
	"""
	Genera un identificador único universal.
	
	Returns:
		str: UUID en formato URN (urn:uuid:...)
	"""
	return f"urn:uuid:{uuid.uuid4()}"


def generar_id_seccion():
	"""
	Genera un identificador único para una sección.
	
	Returns:
		str: ID de sección en formato sec-XXXXXXXX
	"""
	return f"sec-{uuid.uuid4().hex[:8]}"


def generar_id_imagen():
	"""
	Genera un identificador único para una imagen.
	
	Returns:
		str: ID de imagen en formato img-XXXXXXXX
	"""
	return f"img-{uuid.uuid4().hex[:8]}"


def validar_codigo_idioma(codigo):
	"""
	Valida si un código de idioma cumple con BCP 47.
	
	Args:
		codigo: Código de idioma a validar (ej: 'es', 'es-ES', 'en-US')
	
	Returns:
		bool: True si el código es válido, False en caso contrario
	"""
	if not codigo or not isinstance(codigo, str):
		return False
	
	# Patrón BCP 47 simplificado
	# Acepta: xx, xx-XX, xx-Xxxx, xx-Xxxx-XX
	patron = r'^[a-z]{2,3}(-[A-Z][a-z]{3})?(-[A-Z]{2})?$'
	
	# También aceptar formato común xx-XX
	patron_simple = r'^[a-z]{2,3}(-[A-Z]{2})?$'
	
	return bool(re.match(patron, codigo) or re.match(patron_simple, codigo))


def sanitizar_nombre_archivo(nombre):
	"""
	Convierte un nombre a un formato seguro para usar como nombre de archivo.
	
	Args:
		nombre: Nombre original
	
	Returns:
		str: Nombre sanitizado sin caracteres especiales
	"""
	if not nombre:
		return "sin_nombre"
	
	# Normalizar caracteres Unicode
	nombre = unicodedata.normalize('NFKD', nombre)
	
	# Convertir a ASCII, ignorando caracteres no convertibles
	nombre = nombre.encode('ascii', 'ignore').decode('ascii')
	
	# Reemplazar espacios y caracteres no válidos
	nombre = re.sub(r'[^\w\s-]', '', nombre)
	nombre = re.sub(r'[\s_]+', '-', nombre)
	nombre = nombre.strip('-').lower()
	
	return nombre if nombre else "sin_nombre"


def truncar_texto(texto, longitud_max=50):
	"""
	Trunca un texto a una longitud máxima, añadiendo puntos suspensivos.
	
	Args:
		texto: Texto a truncar
		longitud_max: Longitud máxima (por defecto 50)
	
	Returns:
		str: Texto truncado si excede la longitud, o el texto original
	"""
	if not texto:
		return ""
	
	if len(texto) <= longitud_max:
		return texto
	
	return texto[:longitud_max - 3] + "..."


def es_xhtml_valido(contenido):
	"""
	Verifica si un contenido es XHTML básicamente válido.
	
	Args:
		contenido: Contenido XHTML a verificar
	
	Returns:
		bool: True si parece ser XHTML válido
	"""
	if not contenido or not isinstance(contenido, str):
		return False
	
	# Verificación básica de estructura
	contenido_limpio = contenido.strip()
	
	# Debe contener al menos una etiqueta HTML
	if not re.search(r'<[a-z][^>]*>', contenido_limpio, re.IGNORECASE):
		return False
	
	return True


def obtener_extension_archivo(ruta):
	"""
	Obtiene la extensión de un archivo en minúsculas.
	
	Args:
		ruta: Ruta del archivo
	
	Returns:
		str: Extensión sin el punto, en minúsculas
	"""
	if not ruta:
		return ""
	
	partes = str(ruta).rsplit('.', 1)
	if len(partes) > 1:
		return partes[1].lower()
	
	return ""
