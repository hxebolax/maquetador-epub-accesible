# -*- coding: utf-8 -*-
"""
Maquetador de EPUB Accesibles
Punto de entrada principal de la aplicación.

Esta aplicación permite crear libros EPUB 3 totalmente accesibles,
cumpliendo con WCAG 2.1/2.2 y EPUB Accessibility 1.1.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def main():
	"""Función principal que inicia la aplicación."""
	try:
		import wx
	except ImportError:
		print("Error: wxPython no está instalado.")
		print("Instálelo con: pip install wxPython")
		sys.exit(1)
	
	# Importar la ventana principal
	from src.gui.ventana_principal import VentanaPrincipal
	from src.utils.constantes import NOMBRE_APP
	
	# Crear aplicación wxPython
	app = wx.App()
	
	# Configurar nombre de la aplicación
	app.SetAppName(NOMBRE_APP)
	
	# Crear y mostrar ventana principal
	ventana = VentanaPrincipal()
	ventana.Show()
	
	# Procesar argumentos de línea de comandos
	if len(sys.argv) > 1:
		ruta_proyecto = sys.argv[1]
		if os.path.exists(ruta_proyecto):
			ventana.abrir_proyecto(ruta_proyecto)
	
	# Iniciar bucle de eventos
	app.MainLoop()


if __name__ == "__main__":
	main()
