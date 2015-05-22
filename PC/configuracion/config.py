#!/usr/bin/python
# -*- coding: utf-8 -*-

# Configuración del servidor MySQL

CONFIG 							= {}
CONFIG["HOST"] 					= "127.0.0.1"
CONFIG["USER"] 					= "root"
CONFIG["PASSWORD"] 				= "sistemas"
CONFIG["DATABASE"] 				= "vistapress_manager"
CONFIG["FILE"] 					= "vistapress_manager.sql"
CONFIG["HOME_ROUTE"]			= "./"
CONFIG["TEMPLATES"]				= CONFIG["HOME_ROUTE"]+"templates/"
CONFIG["FACTURES"] 				= CONFIG["HOME_ROUTE"]+"factures/"

CONFIG["GRAFICO_YEAR"] 			= "2015"

CONFIG["DEBUG_SQL"]				= False