#!/usr/bin/python
# -*- coding: utf-8 -*-

# Librerias
import pango
from gi.repository import Gtk

# Librerias propias
from configuracion.alias_conf import *
from configuracion.functions import *
from pprint import pprint

# Mapeado y configuracion de las tablas segun la configuracion de la base de datos

# El indice de los dictionary sera el orden de aparicion del campo de la tabla en los formularios 

class usuario :

	def __init__( self ):

		self.action = { }

		self.translate = { }

		self.extras = { }
		
		self.toolbar_buttons = { }
		
		self.singular 		    = "cliente"
		self.plural 		    = "clientes"

		self.alias = alias_database("usuario")

		self.related = { 
		
			"relation" 			: None,
			"entity" 			: None,
			"field-primary-key" : "id",
			"relationship"		: {} }

		self.default = { 
			"coordX" : 202, 
			"visibility": True, 
			"options" : {},
			"get": True }

	def list( self ):

		self.title_list 	= "Clientes"

		self.form_list = { }
		self.form_list [ 0 ] = { "campo" : "id", 

			"name" : self.alias[ "id" ],
			"treview-column-properties": {

				"fixed_width" : [112],
				"min_width" : [112],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 1 ] = { "campo" : "correo", 

			"name" : self.alias[ "correo" ],
			"treview-column-properties": {

				"fixed_width" : [180],
				"min_width" : [180],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 2 ] = { "campo" : "nombre", 

			"name" : self.alias[ "nombre" ],
			"treview-column-properties": {

				"fixed_width" : [130],
				"min_width" : [130],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 3 ] = { "campo" : "apellidos", 

			"name" : self.alias[ "apellidos" ],
			"treview-column-properties": {

				"fixed_width" : [180],
				"min_width" : [180],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 4 ] = { "campo" : "dni", 

			"name" : self.alias[ "dni" ],
			"treview-column-properties": {

				"fixed_width" : [85],
				"min_width" : [85],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 5 ] = { "campo" : "codigo_postal", 

			"name" : self.alias[ "codigo_postal" ],
			"treview-column-properties": {

				"fixed_width" : [101],
				"min_width" : [101],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 6 ] = { "campo" : "direccion", 

			"name" : self.alias[ "direccion" ],
			"treview-column-properties": {

				"fixed_width" : [200],
				"min_width" : [200],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 7 ] = { "campo" : "telefono_fijo", 

			"name" : self.alias[ "telefono_fijo" ],
			"treview-column-properties": {

				"fixed_width" : [102],
				"min_width" : [102],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 8 ] = { "campo" : "telefono_movil", 

			"name" : self.alias[ "telefono_movil" ],
			"treview-column-properties": {

				"fixed_width" : [85],
				"min_width" : [85],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }

		self.toolbar_buttons = { }

	def insert( self ):

		self.title_insert 	= "Nuevo Cliente"

		self.form_insert = { }
		self.form_insert [ 0 ] = { "campo" : "correo", 

			"name" : self.alias[ "correo" ], 
			"type": "Entry",
			"data-type": str }
		self.form_insert [ 1 ] = { "campo" : "nombre", 

			"name" : self.alias[ "nombre" ], 
			"type": "Entry",
			"data-type": str }
		self.form_insert [ 2 ] = { "campo" : "apellidos", 

			"name" : self.alias[ "apellidos" ], 
			"type": "Entry",
			"data-type": str }
		self.form_insert [ 3 ] = { "campo" : "dni", 

			"name" : self.alias[ "dni" ], 
			"type": "Entry",
			"data-type": str }
		self.form_insert [ 4 ] = { "campo" : "codigo_postal", 
			"name" : self.alias[ "codigo_postal" ], 
			"type": "Entry",
			"data-type": int }
		self.form_insert [ 5 ] = { "campo" : "direccion", 

			"name" : self.alias[ "direccion" ], 
			"type": "Entry",
			"data-type": str }
		self.form_insert [ 6 ] = { "campo" : "telefono_fijo", 

			"name" : self.alias[ "telefono_fijo" ], 
			"type": "Entry",
			"data-type": int }
		self.form_insert [ 7 ] = { "campo" : "telefono_movil", 

			"name" : self.alias[ "telefono_movil" ], 
			"type": "Entry",
			"data-type": int }

	def change( self ):

		self.title_change 	= "Modificar Cliente"

		self.form_change = { }
		self.form_change [ 0 ] = { "campo" : "correo", 
			
			"name" : self.alias[ "correo" ], 
			"type": "Entry",
			"data-type": str }
		self.form_change [ 1 ] = { "campo" : "nombre", 

			"name" : self.alias[ "nombre" ], 
			"type": "Entry",
			"data-type": str }
		self.form_change [ 2 ] = { "campo" : "apellidos", 

			"name" : self.alias[ "apellidos" ], 
			"type": "Entry",
			"data-type": str }
		self.form_change [ 3 ] = { "campo" : "dni", 

			"name" : self.alias[ "dni" ], 
			"type": "Entry",
			"data-type": str }
		self.form_change [ 4 ] = { "campo" : "codigo_postal",  

			"name" : self.alias[ "codigo_postal" ], 
			"type": "Entry",
			"data-type": int }
		self.form_change [ 5 ] = { "campo" : "direccion", 

			"name" : self.alias[ "direccion" ], 
			"type": "Entry",
			"data-type": str }
		self.form_change [ 6 ] = { "campo" : "telefono_fijo", 

			"name" : self.alias[ "telefono_fijo" ], 
			"type": "Entry",
			"data-type": int }
		self.form_change [ 7 ] = { "campo" : "telefono_movil", 

			"name" : self.alias[ "telefono_movil" ], 
			"type": "Entry",
			"data-type": int }

#-------------------------------------------------------------------------------------------------------------------------------------------------

class producto :
	
	def __init__( self ):

		self.action = { }

		self.translate = { }

		self.extras = { }
		
		self.toolbar_buttons = { }
	
		self.singular 		= "neumatico"
		self.plural 		= "neumaticos"

		self.alias = alias_database("producto")

		self.related = { 
			
			"relation" 			: None,
			"entity" 			: None,
			"field-primary-key" : "id",
			"relationship"		: {} }

		self.default = { 
			"coordX" : 202, 
			"visibility": True, 
			"options" : {},
			"get": True }
	
	def list( self ):

		self.title_list 	= "Neumaticos"

		self.form_list = { }
		self.form_list [ 0 ] = { "campo" : "id", 

			"name" : self.alias[ "id" ],
			"treview-column-properties": {

				"fixed_width" : [126],
				"min_width" : [126],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 1 ] = { "campo" : "nombre", 

			"name" : self.alias[ "nombre" ],
			"treview-column-properties": {

				"fixed_width" : [360],
				"min_width" : [360],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 2 ] = { "campo" : "descripcion", 

			"name" : self.alias[ "descripcion" ],
			"treview-column-properties": {

				"fixed_width" : [450],
				"min_width" : [450],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 3 ] = { "campo" : "precio", 

			"name" : self.alias[ "precio" ],
			"treview-column-properties": {

				"fixed_width" : [61],
				"min_width" : [61],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		# self.form_list [ 4 ] = { "campo" : "stock", 

		# 	"name" : self.alias[ "stock" ],
		# 	"treview-column-properties": {

		# 		"fixed_width" : [61],
		# 		"min_width" : [61],
		# 		"max_width" : [100000],
		# 		"resizable" : [True] },
		# 	"renderer-properties": {

		# 		"wrap-mode" : pango.WRAP_WORD,
		# 		"wrap-width" : 400 },
		# 	"treview-properties": {

		# 		"level-indentation" : 2 } }
		self.form_list [ 5 ] = { "campo" : "garantia", 

			"name" : self.alias[ "garantia" ],
			"treview-column-properties": {

				"fixed_width" : [74],
				"min_width" : [74],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }

		self.toolbar_buttons = { }

	def insert( self ):

		self.title_insert 	= "Nuevo Neumatico"

		self.form_insert = { }
		self.form_insert [ 0 ] = { "campo" : "nombre", 

			"name" : self.alias[ "nombre" ], 
			"type": "Entry",
			"data-type": str }
		self.form_insert [ 1 ] = { "campo" : "descripcion", 

			"name" : self.alias[ "descripcion" ], 
			"type": "TextView",
			"data-type": str, 
			"properties": { "wrap_mode": [pango.WRAP_CHAR] }, 
			"scroll": {

				"policy": [ Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC ], 
				"size_request": [ 390, 130 ], 
				"shadow_type": [ Gtk.ShadowType.ETCHED_IN ]},
			"options": { "textArea":True } }
		self.form_insert [ 2 ] = { "campo" : "precio", 

			"name" : self.alias[ "precio" ],
			"type": "SpinButton",
			"data-type": float,
			"properties": { 

				"value": [0.00], 
				"increments": [ 0.01, 0.01 ], 
				"range": [ 0.00, 9999.99], 
				"digits": [ 2 ] } }
		# self.form_insert [ 3 ] = { "campo" : "stock",

		# 	"name" : self.alias[ "stock" ], 
		# 	"type": "SpinButton",
		# 	"data-type": int, 
		# 	"properties": { 

		# 		"value": [0], 
		# 		"increments": [ 1, 1 ], 
		# 		"range": [ 0, 9999 ] } }
		self.form_insert [ 4 ] = { "campo" : "garantia", 

			"name" : self.alias[ "garantia" ], 
			"type": "SpinButton",
			"data-type": int, 
			"properties": { 

				"value": [0], 
				"increments": [ 1, 1 ], 
				"range": [ 0, 9999 ] } }

	def change( self ):

		self.title_change 	= "Modificar Neumatico"

		self.form_change = { }
		self.form_change [ 0 ] = { "campo" : "nombre",

			"name" 			: self.alias[ "nombre" ], 
			"type"			: "Entry",
			"data-type": str }
		self.form_change [ 1 ] = { "campo" : "descripcion",

			"name" 			: self.alias[ "descripcion" ], 
			"type"			: "TextView",
			"data-type": str, 
			"properties"	: { "wrap_mode": [pango.WRAP_CHAR] },
			"scroll"		: {

				"policy"		: [ Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC ], 
				"size_request" 	: [ 390, 130 ], 
				"shadow_type" 	: [ Gtk.ShadowType.ETCHED_IN ]},
			"options"		: { "textArea":True } }
		self.form_change [ 2 ] = { "campo" : "precio", 
			"name" 				: self.alias[ "precio" ], 
			"type" 				: "SpinButton",
			"data-type": float, 
			"fist-properties"	: {  
				
				"increments" 	: [ 0.01, 0.01 ], 
				"range"			: [ 0.00, 9999.99], 
				"digits" 		: [ 2 ] } }
		# self.form_change [ 3 ] = { "campo" : "stock",

		# 	"name" 				: self.alias[ "stock" ], 
		# 	"type" 				: "SpinButton",
		# 	"data-type": int, 
		# 	"fist-properties" 	: { 

		# 		"increments" 	: [ 1, 1 ], 
		# 		"range" 		: [ 0, 9999 ] } }
		self.form_change [ 4 ] = { "campo" : "garantia", 

			"name" 				: self.alias[ "garantia" ], 
			"type" 				: "SpinButton",
			"data-type": int, 
			"fist-properties" 	: { 
				
				"increments" 	: [ 1, 1 ], 
				"range" 		: [ 0, 9999 ] } }

#-------------------------------------------------------------------------------------------------------------------------------------------------

class pedido :
	
	def __init__( self ):

		self.action = { }

		self.translate = { }

		self.extras = { }
		
		self.toolbar_buttons = { }
	
		self.singular 	= "pedido"
		self.plural 	= "pedidos"
		self.related 	= { 
		
			"relation" 			: "one-to-many",
			"entity" 			: "one",
			"table-related" 	: "detalle_pedido",
			"field-primary-key"	: "id",
			"field-foreign-key" : "pedido_id",
			"relationship" 		: {
				"pedido-detalle_pedido" : { 
					"name" 				: "pedido-detalle_pedido",
					"relation" 			: "one-to-many", 
					"entity" 			: "one",
					"table-related"		: "detalle_pedido", 
					"field-foreign-key"	: "pedido_id",
					"button" : True  },
				"pedido-usuario" : { 

					"relationship" 				: "pedido-detalle_pedido",
					"name" 						: "pedido-usuario",
					"relation" 					: "one-to-many", 
					"entity" 					: "many",
					"table-related"				: "usuario",
					"field-related-primary-key"	: "id", 
					"field-table-related" 		: "clientes_id",
					"button" : False  } } }

		self.alias_pedido = alias_database("pedido")
		self.alias_usuario = alias_database("usuario")

		self.default = { 
			"coordX" : 202, 
			"visibility": True, 
			"options" : {},
			"get": True }

	def list( self ):

		self.extras = { "view" : "windowListadoPedidos" }

		self.translate = { 

			"pagado" : { 0 : "No", 1 : "Sí" },
			"enviado" : { 0 : "No", 1 : "Sí" } }

		self.title_list 	= "Pedidos de Clientes"

		self.form_list = { }

		self.form_list [ 0 ] = { "campo" : "id", 

			"name" : self.alias_pedido[ "id" ],
			"treview-column-properties": {

				"fixed_width" : [115],
				"min_width" : [115],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 1 ] = { "campo" : "nombre", 

			"name" : self.alias_pedido[ "nombre" ],
			"treview-column-properties": {

				"fixed_width" : [360],
				"min_width" : [360],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 2 ] = { "campo" : "fecha", 

			"name" : self.alias_pedido[ "fecha" ],
			"treview-column-properties": {

				"fixed_width" : [140],
				"min_width" : [140],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 3 ] = { "campo" : "nombre", 

			"name" : self.alias_usuario[ "nombre" ],
			"treview-column-properties": {

				"fixed_width" 	: [360],
				"min_width" 	: [360],
				"max_width" 	: [100000],
				"resizable" 	: [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 },
			"related":{ 

				"table": "usuario", 
				"field-foreign-key": "clientes_id", 
				"field-primary-key": "id" } }
		self.form_list [ 4 ] = { "campo" : "total",

			"name" : self.alias_pedido[ "total" ],
			"treview-column-properties": {

				"fixed_width" : [115],
				"min_width" : [115],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 5 ] = { "campo" : "pagado",

			"name" : self.alias_pedido[ "pagado" ], 
			"treview-column-properties": {

				"fixed_width" : [65],
				"min_width" : [65],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } } 
		self.form_list [ 6 ] = { "campo" : "enviado",

			"name" : self.alias_pedido[ "enviado" ], 
			"treview-column-properties": {

				"fixed_width" : [63],
				"min_width" : [63],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }

		self.toolbar_buttons = { }

		#self.toolbar_buttons [ 0 ] = { 
		#"name": "detalle_pedido", 
		#"properties": {
		#	"icon_widget":[Gtk.Widget(Gtk.GType.LABEL,"ver pedido")],
		#	"label": ["Ver Pedido"], 
		#	"icon_name": ["contact-new"], 
		#	"tooltip_text": ["Ver Pedido"], 
		#	"use_underline": [True]}}	

	def insert( self ):

		self.action = { "before-insert" : "before_insert_pedido_auto_fecha_total" }

		self.title_insert 	= "Nuevo Pedido"

		self.form_insert = { }
		self.form_insert [ 0 ] = { "campo" : "nombre", 

			"name" 			: self.alias_pedido[ "nombre" ], 
			"type" 			: "Entry",
			"data-type": str }
		self.form_insert [ 1 ] = { "campo" : "clientes_id",

			"name" 			: self.alias_pedido[ "clientes_id" ],
			"type" 			: "ComboBox",
			"data-type" 	: int,
			"relationship" 	: "pedido-usuario",
			"view-fields" 	: { "nombre": str },
			"properties" 	: { "active": [0] } }
		self.form_insert [ 2 ] = { "campo" : "fecha", 

			"name" 			: self.alias_pedido[ "fecha" ], 
			"type" 			: "Entry",
			"data-type": str,
			"visibility" 	: False,
			"get" 			: False }
		self.form_insert [ 3 ] = { "campo" : "total", 

			"name" 			: self.alias_pedido[ "total" ], 
			"type" 			: "Entry",
			"data-type": float,
			"visibility" 	: False,
			"get" 			: False }
		self.form_insert [ 4 ] = { "campo" : "pagado", 

			"name" : self.alias_pedido[ "pagado" ], 
			"type": "CheckButton",
			"data-type": bool }
		self.form_insert [ 5 ] = { "campo" : "enviado", 

			"name" : self.alias_pedido[ "enviado" ], 
			"type": "CheckButton",
			"data-type": bool }

	def change( self ):

		self.action = { "before-change" : "before_change_pedido_auto_fecha" }

		self.title_change 	= "Modificar Pedido"

		self.form_change = { }
		self.form_change [ 0 ] = { "campo" : "nombre", 

			"name" : self.alias_pedido[ "nombre" ], 
			"type"	: "Entry",
			"data-type": str }
		self.form_change [ 1 ] = { "campo" : "clientes_id",

			"name" : self.alias_pedido[ "clientes_id" ], 
			"type" : "ComboBox",
			"data-type": int,
			"relationship" 	: "pedido-usuario",
			"view-fields" : { "nombre": str } }
		self.form_change [ 2 ] = { "campo" : "fecha", 

			"name" : self.alias_pedido[ "fecha" ], 
			"type": "Entry",
			"data-type": str,
			"visibility" 	: False,
			"get" 			: False }
		self.form_change [ 3 ] = { "campo" : "pagado", 

			"name" : self.alias_pedido[ "pagado" ], 
			"type": "CheckButton",
			"data-type": bool }
		self.form_change [ 4 ] = { "campo" : "enviado", 

			"name" : self.alias_pedido[ "enviado" ], 
			"type": "CheckButton",
			"data-type": bool }

#-------------------------------------------------------------------------------------------------------------------------------------------------

class detalle_pedido :
	
	def __init__( self ):

		self.action = { }

		self.translate = { }

		self.extras = { }
		
		self.toolbar_buttons = { }

		self.singular 		    = "producto"
		self.plural 		    = "productos"

		self.alias_detalle_pedido = alias_database("detalle_pedido")
		self.alias_producto = alias_database("producto")
		
		self.related = { 

			"relation" 			: "one-to-many",
			"entity"			: "many",
			"field-primary-key" : "id",
			"field-foreign-key" : "pedido_id",
			"relationship"                   : {

				"pedido-detalle_pedido" : { 

					"name" 				: "pedido-detalle_pedido",
					"relation" 			: "one-to-many", 
					"entity" 			: "many",
					"table-related"		: "pedido",
					"field-foreign-key"	: "pedido_id",
					"button" : False },
				"detalle_pedido-producto" : { 

					"relationship" 				: "pedido-detalle_pedido",
					"name" 						: "detalle_pedido-producto",
					"relation" 					: "one-to-one", 
					"entity" 					: "one",
					"table-related"				: "producto",
					"field-related-primary-key"	: "id", 
					"field-table-related" 		: "productos_id",
					"button" : False } } }

		self.default = { 
			"coordX" : 202, 
			"visibility": True, 
			"options" : {},
			"get": True }

	def list( self ):

		self.action = { 
			"after-delete" : "after_delete_detalle_pedido_cacl_total",
			"before-delete" : "before_delete_detalle_pedido_cacl_total" }

		self.title_list 	= "Detalle del pedido"

		self.form_list = { }
		self.form_list [ 0 ] = { "campo": "id", 

			"name" : self.alias_detalle_pedido[ "id" ],
			"treview-column-properties": {

				"fixed_width" : [54],
				"min_width" : [54],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 1 ] = { "campo" : "cantidad", 

			"name" : self.alias_detalle_pedido[ "cantidad" ],
			"treview-column-properties": {

				"fixed_width" : [68],
				"min_width" : [68],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 2 ] = { "campo" : "precio", 

			"name" : self.alias_detalle_pedido[ "precio" ],
			"treview-column-properties": {

				"fixed_width" : [60],
				"min_width" : [60],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 } }
		self.form_list [ 3 ] = { "campo" : "nombre", 

			"name" : self.alias_producto[ "nombre" ],
			"treview-column-properties": {

				"fixed_width" 		: [350],
				"min_width" 	: [350],
				"max_width" : [100000],
				"resizable" : [True] },
			"renderer-properties": {

				"wrap-mode" : pango.WRAP_WORD,
				"wrap-width" : 400 },
			"treview-properties": {

				"level-indentation" : 2 },
			"related":{ 

				"table": "producto", 
				"field-foreign-key": "productos_id", 
				"field-primary-key": "id" } }

	def insert( self ):

		self.action = { "after-insert" : "after_insert_detalle_pedido_cacl_total" }

		self.title_insert 	= "Añadir productos al Pedido"

		self.form_insert = { }
		self.form_insert [ 0 ] = { "campo"	: "productos_id",

			"name" 			: "producto",
			"type" 			: "ComboBox",
			"data-type": int,
			"relationship" 	: "detalle_pedido-producto",
			"view-fields" 	: { "nombre": str },
			"properties" 	: { "active": [0] },
			"event": { "changed" : "detalle_pedido_insert_productos_id_event_changed"} }
		self.form_insert [ 1 ] = { "campo" 	: "cantidad", 

			"name" : self.alias_detalle_pedido[ "cantidad" ], 
			"type" : "SpinButton",
			"data-type": int, 
			"properties" : { 

				"value" : [1], 
				"increments" : [ 1, 1 ], 
				"range" : [ 1, 9999 ] }, 
			"event": { "value-changed" : "detalle_pedido_insert_cantidad_event_value_changed" }}
		self.form_insert [ 2 ] = { "campo" 	: "precio", 

			"name" : self.alias_producto[ "precio" ], 
			"type" : "TextView",
			"data-type": float, 
			"properties": { 

				"wrap_mode": [ pango.WRAP_CHAR ], 
				"cursor_visible": [False]},
			"scroll": {

				"policy": [ Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC ], 
				"size_request": [ 390, 20 ]}, 
			"options": { "divisa": "€" } }
		self.form_insert [ 3 ] = { "name" 	: "SubTotal", 

			"type" : "TextView",
			"data-type": float,
			"properties": { 

				"wrap_mode": [ pango.WRAP_CHAR ], 
				"cursor_visible": [False]}, 
			"scroll": {

				"policy": [ Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC ], 
				"size_request": [ 390, 17 ]}, 
			"options": { "divisa": "€" },
			"get" : False }

	def change( self ):

		self.action = { 
			"after-change" : "after_change_detalle_pedido_cacl_total" }

		self.title_change 	= "Modificar producto dentro del Pedido"

		self.form_change = { }
		self.form_change [ 0 ] = { "campo": "productos_id",

			"name" : "producto", 
			"type" : "ComboBox",
			"data-type": int,
			"relationship" 	: "detalle_pedido-producto",
			"view-fields" : { "nombre": str },
			"event": { "changed" : "detalle_pedido_change_productos_id_event_changed"} }
		self.form_change [ 1 ] = { "campo" : "cantidad", 

			"name" : self.alias_detalle_pedido[ "cantidad" ], 
			"type" : "SpinButton",
			"data-type": int, 
			"fist-properties" : {

				"value" : [1], 
				"increments" : [ 1, 1 ], 
				"range" : [ 1, 9999 ] }, 
			"event": { "value-changed" : "detalle_pedido_change_cantidad_event_value_changed" } }
		self.form_change [ 2 ] = { "campo" : "precio", 

			"name" : self.alias_producto[ "precio" ], 
			"type" : "TextView",
			"data-type": float, 
			"properties": { 

				"wrap_mode": [ pango.WRAP_CHAR ], 
				"cursor_visible": [False] },
			"scroll": {

				"policy": [ Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC ], 
				"size_request": [ 390, 20 ] }, 
			"options": { "divisa": "€" } }
		self.form_change [ 3 ] = { "name" : "SubTotal", 

			"type" : "TextView",
			"data-type": float, 
			"result-function" : "subtotal_producto", 
			"properties": {

				"wrap_mode": [ pango.WRAP_CHAR ], 
				"cursor_visible": [False] },
			"event": { "show" : "detalle_pedido_change_subTotal_event_show" }, 
			"scroll": {

				"policy": [ Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC ], 
				"size_request": [ 390, 17 ] }, 
			"options": { "divisa": "€" },
			"get": False }

# dictionary creado para la instacion de objectos mediante string

CLASS = { }

CLASS ["usuario"]  			= usuario
CLASS ["producto"] 			= producto
CLASS ["pedido"] 			= pedido
CLASS ["detalle_pedido"] 	= detalle_pedido