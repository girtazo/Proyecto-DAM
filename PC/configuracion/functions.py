#!/usr/bin/python
# -*- coding: utf-8 -*-

# Librerias
from pprint import pprint
from gi.repository import Gtk
from xhtml2pdf import pisa
from time import gmtime, strftime
from datetime import datetime, date, time

# Librerias propias
from bibliotecas.database import *

# Acceder a configuracion
import config

# event functions
def loop_events( name, events, data ):

	for event in events:

		getattr(data.elements[name], "connect")(*[ event, lambda element : event_functions[ events[event] ]( element, data ) ])

def detalle_pedido_insert_productos_id_event_changed( element, data ):

	select = element.get_active_iter()

	model = element.get_model()
	producto_id, producto_nombre = model[select][:2]

	if producto_id != -1:

		tabla = Tabla( data.conexion, "producto" )

		precio = tabla.busquedaTuplas( "id", producto_id, ["precio"] )

		bufferTextView = data.elements[data.form[2]["name"]].get_buffer()

		data.elements[data.form[2]["name"]].get_buffer().set_text(str(precio[0][0])+"€")

		subtotal = data.elements[data.form[1]["name"]].get_value()*precio[0][0]

		data.elements[data.form[3]["name"]].get_buffer().set_text(str(subtotal)+"€")

def detalle_pedido_insert_cantidad_event_value_changed( element, data ):

	select = data.elements[data.form[0]["name"]].get_active_iter()

	model = data.elements[data.form[0]["name"]].get_model()
	producto_id, producto_nombre = model[select][:2]
		
	if producto_id != -1:
		bufferTextView 	= data.elements[data.form[2]["name"]].get_buffer()
		start 			= bufferTextView.get_start_iter()
		end 			= bufferTextView.get_end_iter()
		precio = bufferTextView.get_text(start,end,True)

		subtotal = data.elements[data.form[1]["name"]].get_value()*float(precio.rstrip('€'))

		data.elements[data.form[3]["name"]].get_buffer().set_text(str(subtotal)+"€")

def detalle_pedido_change_productos_id_event_changed( element, data ):

	select = element.get_active_iter()

	model = element.get_model()
	producto_id, producto_nombre = model[select][:2]

	if producto_id != -1:

		tabla = Tabla( data.conexion, "producto" )

		precio = tabla.busquedaTuplas( "id", producto_id, ["precio"] )

		bufferTextView = data.elements[data.form[2]["name"]].get_buffer()

		data.elements[data.form[2]["name"]].get_buffer().set_text(str(precio[0][0])+"€")

		subtotal = data.elements[data.form[1]["name"]].get_value()*precio[0][0]

		data.elements[data.form[3]["name"]].get_buffer().set_text(str(subtotal)+"€")

def detalle_pedido_change_cantidad_event_value_changed( element, data ):

	select = data.elements[data.form[0]["name"]].get_active_iter()

	model = data.elements[data.form[0]["name"]].get_model()
	producto_id, producto_nombre = model[select][:2]
		
	if producto_id != -1:
		bufferTextView 	= data.elements[data.form[2]["name"]].get_buffer()
		start 			= bufferTextView.get_start_iter()
		end 			= bufferTextView.get_end_iter()
		precio = bufferTextView.get_text(start,end,True)

		subtotal = data.elements[data.form[1]["name"]].get_value()*float(precio.rstrip('€'))

		data.elements[data.form[3]["name"]].get_buffer().set_text(str(subtotal)+"€")

def detalle_pedido_change_subTotal_event_show( element, data ):

	bufferTextView 	= data.elements[data.form[2]["name"]].get_buffer()
	start 			= bufferTextView.get_start_iter()
	end 			= bufferTextView.get_end_iter()
	precio = bufferTextView.get_text(start,end,True)

	subtotal = data.elements[data.form[1]["name"]].get_value()*float(precio.rstrip('€'))

	element.get_buffer().set_text(str(subtotal)+"€")

event_functions = { }

event_functions["detalle_pedido_insert_productos_id_event_changed"] 	= detalle_pedido_insert_productos_id_event_changed
event_functions["detalle_pedido_insert_cantidad_event_value_changed"] 	= detalle_pedido_insert_cantidad_event_value_changed
event_functions["detalle_pedido_change_productos_id_event_changed"] 	= detalle_pedido_change_productos_id_event_changed
event_functions["detalle_pedido_change_cantidad_event_value_changed"] 	= detalle_pedido_change_cantidad_event_value_changed
event_functions["detalle_pedido_change_subTotal_event_show"] 			= detalle_pedido_change_subTotal_event_show

# related functions
def loop_btnToolRelated( list_relationship, data ):

	data.btnToolRelated = {}

	for relationship in list_relationship:

		if data.related["relationship"][ list_relationship[relationship]["name"] ]["button"]:
		
			data.btnToolRelated[list_relationship[relationship]["name"]] = data.Interfaz.recoger("btnTool"+list_relationship[relationship]["name"])
			data.btnToolRelated[list_relationship[relationship]["name"]].set_sensitive(False)
			data.btnToolRelated[list_relationship[relationship]["name"]].connect( "clicked", lambda relatedWindow : data.callWindowListadoDependency(list_relationship[relationship]["name"]) )

# actions functions

def before_insert_pedido_auto_fecha_total( data, valores_insert ):

	valores_insert[ "total" ] = 0

	valores_insert[ "fecha" ] = "'"+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"'"

	return valores_insert

def before_change_pedido_auto_fecha( data, valores_change ):

	valores_change[3] = { "nombre" : "fecha", "valor" : "'"+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"'" }

	return valores_change

def after_insert_detalle_pedido_cacl_total( data, valores_insert ):

	valor_modified = { }
	list_campos = list()
	list_campos.append("total")

	bufferTextView = data.elements["SubTotal"].get_buffer()
	start 			= bufferTextView.get_start_iter()
	end 			= bufferTextView.get_end_iter()
	subtotal 		= bufferTextView.get_text( start, end, True).rstrip(data.form[3]["options"]["divisa"])

	data.tabla.cambiarTabla("pedido")

	total = data.tabla.busquedaTuplas( "id", data.foreign_key, list_campos)[0][0]

	total = total + float(subtotal)

	valor_modified[1] = { "nombre": "total", "valor" : total }

	data.tabla.modificar( valor_modified, "id", data.foreign_key )

	data.tabla.cambiarTabla("detalle_pedido")

def after_change_detalle_pedido_cacl_total( data, valores_change ):

	valor_modified = {}
	list_campos = list()
	list_campos.append("pedido_id")

	bufferTextView = data.elements["SubTotal"].get_buffer()
	start 			= bufferTextView.get_start_iter()
	end 			= bufferTextView.get_end_iter()
	subtotal 		= bufferTextView.get_text( start, end, True).rstrip(data.form[3]["options"]["divisa"])

	subtotal_initial = data.list_valores[1]*data.list_valores[2]

	id_pedido = data.tabla.busquedaTuplas( "id", data.primary_key, tuple(list_campos))[0][0]

	data.tabla.cambiarTabla("pedido")

	list_campos = list()
	list_campos.append("total")

	total = data.tabla.busquedaTuplas( "id", id_pedido, tuple(list_campos))[0][0]

	total = total + float(subtotal) - subtotal_initial

	valor_modified[1] = { "nombre": "total", "valor" : total }

	data.tabla.modificar( valor_modified, "id", id_pedido )

	data.tabla.cambiarTabla("detalle_pedido")

def before_delete_detalle_pedido_cacl_total( data, valor_delete ):

	list_campos = list()
	
	list_campos.append("precio")
	list_campos.append("cantidad")

	campos = data.tabla.busquedaTuplas( "id", valor_delete, list_campos)[0]

	subtotal = float(campos[0]) * float(campos[1])

	data.temp = { "subtotal" : subtotal }

	list_campos = list()

	list_campos.append("total")

	data.tabla.cambiarTabla("pedido")

	data.temp["total"] = data.tabla.busquedaTuplas( "id", data.foreign_key, list_campos)[0][0]

	data.tabla.cambiarTabla("detalle_pedido")

def after_delete_detalle_pedido_cacl_total( data, valor_delete ):

	valor_modified = { }

	total = data.temp["total"] - data.temp["subtotal"]

	valor_modified[1] = { "nombre": "total", "valor" : total }

	data.tabla.cambiarTabla("pedido")

	data.tabla.modificar( valor_modified, "id", data.foreign_key )

	data.tabla.cambiarTabla("detalle_pedido")

action_functions = { }

action_functions["after_insert_detalle_pedido_cacl_total"] 	= after_insert_detalle_pedido_cacl_total
action_functions["before_insert_pedido_auto_fecha_total"] 	= before_insert_pedido_auto_fecha_total
action_functions["before_change_pedido_auto_fecha"] 		= before_change_pedido_auto_fecha
action_functions["after_change_detalle_pedido_cacl_total"] 	= after_change_detalle_pedido_cacl_total
action_functions["after_delete_detalle_pedido_cacl_total"] 	= after_delete_detalle_pedido_cacl_total
action_functions["before_delete_detalle_pedido_cacl_total"] = before_delete_detalle_pedido_cacl_total

# functions

def mostrar_grafico(event):

	from matplotlib.figure import Figure
	from numpy import sin, cos, pi, linspace
	from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
	from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

	#Inicializar valores
	beneficios = list()

	win = Gtk.Window()
	win.set_default_size(900,500)
	win.set_title("Grafico de beneficios")

	figura = Figure(figsize=(0.5,0.5), dpi=100)
	grafica = figura.add_subplot(111)

	meses = ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre")

	meses = (1,2,3,4,5,6,7,8,9,10,11,12)
	conexion = DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"], CONFIG["DATABASE"]).conexion

	tabla = Tabla(conexion, "pedido")

	for mes in range(1,13):

		if len(str(mes)) == 1:

			fecha = CONFIG["GRAFICO_YEAR"]+"/"+"0" + str(mes)+"/01 00:00:00"

			if mes % 2 == 0:

				fecha_last = CONFIG["GRAFICO_YEAR"]+"/"+"0" + str(mes)+"/30 23:59:59"

			else:

				fecha_last = CONFIG["GRAFICO_YEAR"]+"/"+"0" + str(mes)+"/31 23:59:59"

		else:
			
			fecha = CONFIG["GRAFICO_YEAR"]+"/"+str(mes)+"/01 00:00:00"

			if mes % 2 == 0:

				fecha_last = CONFIG["GRAFICO_YEAR"]+"/"+ str(mes)+"/30 23:59:59"

			else:

				fecha_last = CONFIG["GRAFICO_YEAR"]+"/"+ str(mes)+"/31 23:59:59"

		fecha 		= "'"+fecha+"'"
		fecha_last 	= "'"+fecha_last+"'"

		select 	= list()
		tables 	= list()
		where 	= list()
		select.append("total")
		tables.append("pedido")
		where 	= {}

		where["fecha"] = { "operator" : ">=", "value" : fecha }
		where["fecha_2"] = { "operator" : "<=", "value" : fecha_last, "campo" : "fecha" }

		totales = tabla.advancedSQL(select, tables, where)

		total = 0
		for total_pedido in totales:
			
			total = total + total_pedido[0]

		beneficios.append(total)
	
	coswave = grafica.plot(meses, beneficios, color='green', label='beneficios', linestyle='-')

	#grafica.set_xlim(-pi,pi)
	#grafica.set_ylim(-1.2,1.2)

	#grafica.fill_between(fechas, 0, total, (total - 1) > -1, color='blue', alpha=.3)
	#grafica.fill_between(fechas, 0, total, (total - 1) < -1, color='red',  alpha=.3)

	#figura.xlabel("Meses "+CONFIG["GRAFICO_YEAR"])
	#figura.ylabel("Beneficios €")

	sw = Gtk.ScrolledWindow()
	win.add (sw)
	# A scrolled window border goes outside the scrollbars and viewport
	sw.set_border_width (10)

	canvas = FigureCanvas(figura)  # a Gtk.DrawingArea
	canvas.set_size_request(200,200)
	sw.add_with_viewport (canvas)

	win.show_all()

functions = { }

functions["mostrar_grafico"] = mostrar_grafico