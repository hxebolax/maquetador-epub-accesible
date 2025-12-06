# -*- coding: utf-8 -*-
"""
Script de instalación para el Maquetador de EPUB Accesibles.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
	requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
	name="maquetador-epub-accesible",
	version="1.0.1",
	author="@hxebolax",
	author_email="xebolax@gmail.com",
	description="Aplicación para crear libros EPUB 3 accesibles",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/hxebolax/maquetador-epub-accesible",
	packages=find_packages(),
	classifiers=[
		"Development Status :: 4 - Beta",
		"Environment :: Win32 (MS Windows)",
		"Environment :: X11 Applications",
		"Intended Audience :: End Users/Desktop",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: Spanish",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",
		"Programming Language :: Python :: 3.12",
		"Programming Language :: Python :: 3.13",
		"Programming Language :: Python :: 3.14",
		"Topic :: Text Processing :: Markup",
		"Topic :: Multimedia :: Graphics :: Presentation",
	],
	python_requires=">=3.8",
	install_requires=requirements,
	entry_points={
		"console_scripts": [
			"maquetador-epub=main:main",
		],
		"gui_scripts": [
			"maquetador-epub-gui=main:main",
		],
	},
	include_package_data=True,
	package_data={
		"src": ["recursos/*"],
	},
	keywords=[
		"epub",
		"ebook",
		"accessibility",
		"accesibilidad",
		"wcag",
		"epub3",
		"maquetacion",
	],
)
