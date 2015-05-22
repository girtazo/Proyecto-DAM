#!/usr/bin/python
# -*- coding: utf-8 -*-

# Alias mappeado de los campos de la tabla

def alias_database( tabla ) :

	alias = {}

	if tabla == "usuario" :
		
		alias = {
			"id"             : "Codigo Cliente",
			"correo"         : "Correo",
			"password"       : "Contraseña", 
		 	"nombre"         : "Nombre", 
		 	"apellidos"      : "Apellidos", 
		 	"dni"            : "DNI",
		 	"codigo_postal"  : "Codigo Postal",
		 	"direccion"      : "Dirección",
		 	"telefono_fijo"  : "Telefono Fijo",
		 	"telefono_movil" : "Movil",
		 	"administrador"  : "Administrador" 
		}
	elif tabla == "producto":

		alias = { 
			"id"          : "Codigo Producto",
			"nombre"      : "Nombre",
		 	"descripcion" : "Descripción", 
		 	"imagen"      : "Imagen", 
		 	"precio"      : "Precio", 
		 	"peso"        : "Peso",
		 	"stock"       : "Stock",
		 	"direccion"   : "Dirección",
		 	"garantia"    : "Garantía"
		}
	elif tabla == "pedido":
		
		alias = {
			"id"     		: "Codigo Pedido", 
			"nombre" 		: "Nombre",
			"fecha"  		: "Fecha",
		 	"total"  		: "Total", 
		 	"pagado" 		: "Pagado", 
		 	"enviado"		: "Enviado",
		 	"clientes_id" 	: "Codigo Cliente"
		}

	elif tabla == "detalle_pedido":
		
		alias = {
			"id"           : "Codigo", 
			"cantidad"     : "Cantidad",
		 	"precio"       : "Precio", 
		 	"productos_id" : "Id del producto", 
		}

	return alias
