#!/usr/bin/python
# -*- coding: utf-8 -*-

# Librerias
import sys
import pango
from xhtml2pdf import pisa
from gi.repository import Gtk
from gi.repository import Gdk
from pprint import pprint

# Librerias propias
from .InterfazGlade import *
from .database import *

# Acceder a configuracion
sys.path.append("../configuracion")
from configuracion.config import *
from configuracion.windows_conf import *
from configuracion.alias_conf import *
from configuracion.functions import *

#----------------------------------------------------------------------------------------

class windowXML :

# Exception rubbish code -> parameter name and if
	def __init__( self, autoCerrado = False, name = False ):


		self.AutoCerrado 	= autoCerrado
		if name :
			self.Nombre = name
			
		else :
			self.Nombre 		= self.__class__.__name__

		# End exception rubbish code -> parameter name and if
		
		self.Interfaz 		= InterfazGlade("./vista/"+self.Nombre)
		self.Window 		= self.Interfaz.recoger(self.Nombre)

		if self.AutoCerrado:
			self.Window.connect("destroy",Gtk.main_quit)

		self.Window.show_all()

#----------------------------------------------------------------------------------------

class windowMain( windowXML ):

	def __init__( self ):

		windowXML.__init__( self, True )

		# Comprobar conexion
		try :
			
			self.conexion = DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"], CONFIG["DATABASE"]).conexion

			self.Interfaz.recoger("warning").set_text("Conectado correctamente a la base de datos MySQL")
			# Asignacion de eventos a la ventana

			# Menu
			self.btnToolClientes 	= self.Interfaz.recoger("btnToolClientes").connect( "clicked", lambda Clientes : windowListado( "usuario" ) )
			self.btnToolNeumaticos 	= self.Interfaz.recoger("btnToolNeumaticos").connect( "clicked", lambda Neumaticos : windowListado( "producto" ) )
			self.btnToolPedidos 	= self.Interfaz.recoger("btnToolPedidos").connect( "clicked", lambda Pedidos : windowListado( "pedido" ) )
			self.btnToolGrafico 	= self.Interfaz.recoger("btnToolGrafico").connect( "clicked", functions["mostrar_grafico"] )

		except Exception:

			self.Interfaz.recoger("warning").set_text("Fallo de conexion MySQL, asegurese que usted tenga el servidor activo...");

	def disableEvents( self ):

		# Menu
		if self.btnToolClientes :
			self.Interfaz.recoger("btnToolClientes").disconnect( self.btnToolClientes )
			self.Interfaz.recoger("btnToolNeumaticos").disconnect( self.btnToolNeumaticos )
			self.btnToolClientes = False

		self.Interfaz.recoger("warning").set_text("Fallo de conexion MySQL, asegurese que usted tenga el servidor activo...");

	def activeEvents( self ):

		# Menu
		self.Interfaz.recoger("btnToolClientes").connect( "clicked", lambda Clientes : windowListado( "usuario", self.clientes, "Clientes" ) )
		self.Interfaz.recoger("btnToolNeumaticos").connect( "clicked", lambda Neumaticos : windowListado( "producto", self.productos, "Productos" ) )

		self.Interfaz.recoger("warning").set_text("Conectado correctamente a la base de datos MySQL")

#----------------------------------------------------------------------------------------

class windowListado( windowXML ):

	def __init__( self, tabla, relationship = False, foreign_key = False ):

		# Inicializar valores
		self.buttons 			= {}
		where					= {}
		tipos 					= list()
		list_campos 			= list()
		list_tables 			= list()
		self.entidad 			= tabla
		self.relationship 		= relationship
		self.field_related 		= False
		self.foreign_key		= foreign_key
		widthWindow 			= 10
		contador 				= 0

		# Cargar configuracion window
		self.config 			= CLASS[tabla]()
		self.config.list()
		self.translate 			= self.config.translate
		self.extras 			= self.config.extras
		self.related 			= self.config.related
		self.titulo 			= self.config.title_list
		self.form 				= self.config.form_list
		self.toolbar_buttons	= self.config.toolbar_buttons
		self.action 			= self.config.action

		# Exception rubbish code -> table pedido window view
		if not self.extras.has_key("view"):

			windowXML.__init__( self, False )
		else :

			windowXML.__init__( self, False, self.extras["view"] )

			if self.extras["view"] == "windowListadoPedidos":

				self.btnToolGenerarFactura = self.Interfaz.recoger("btnToolGenerarFactura")

				self.btnToolGenerarFactura.set_sensitive(False)

			if len(self.related["relationship"]) > 0:
				
				loop_btnToolRelated( self.related["relationship"], self )
		# End exception rubbish code -> table pedido window view

		# Recoger Interfaz
		self.btnToolModificar 	= self.Interfaz.recoger("btnToolModificar")
		self.btnToolEliminar 	= self.Interfaz.recoger("btnToolEliminar")
		self.TreeView 			= self.Interfaz.recoger("Tabla")
		self.scroll 			= self.Interfaz.recoger("scrollWindow")
		self.liststore 			= Gtk.ListStore( )
		self.select 			= self.TreeView.get_selection()

		# Establecer propiedades a la interfaz
		self.Window.set_title(self.titulo)
		self.btnToolEliminar.set_sensitive(False)
		self.btnToolModificar.set_sensitive(False)
		self.Window.set_decorated(True)
		self.select.set_mode(Gtk.SelectionMode.SINGLE)

		# Establecer conexion con la base de datos
		self.conexion 	= DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"], CONFIG["DATABASE"]).conexion
		self.tabla 		= Tabla(self.conexion, self.entidad )

		# Get fields for visualize
		list_tables.append(self.tabla.nombre)
		for column in self.form:

			if self.form[column].has_key("related"):

				self.field_related = True
				list_campos.append(self.form[column]["related"]["table"]+"."+self.form[column]["campo"])
				list_tables.append(self.form[column]["related"]["table"])
				where[ self.form[column]["related"]["table"]+"."+self.form[column]["related"]["field-primary-key"] ] = { "operator" : "=", "value" : self.tabla.nombre+"."+self.form[column]["related"]["field-foreign-key"] }
			else:

				list_campos.append(self.tabla.nombre+"."+self.form[column]["campo"])
		
		# Extraer datos de la Tabla
		if self.relationship:

			# Relationship type
			if   self.related["relationship"][self.relationship]["relation"] == "one-to-many":

				campos = list()
				campos.append(self.related["field-primary-key"])

				related_table = Tabla( self.conexion, self.tabla.nombre )
				list_primary_key = related_table.busquedaTuplas( self.related["relationship"][self.relationship]["field-foreign-key"], self.foreign_key, campos )
			elif self.related["relationship"][self.relationship]["relation"] == "one-to-one":

				pass

			# Preparing query
			tuplas = list()
			for primary_key in list_primary_key:

				if len(list_tables) == 0:

					tuplas.append( self.tabla.busquedaTuplas( self.related["relationship"][self.relationship]["field-foreign-key"], str(primary_key[0]), tuple(list_campos) )[0])
				else:

					where[ self.tabla.nombre+"."+self.related["field-primary-key"] ] = { "operator" : "=", "value" 	: primary_key[0] }
					
					tuplas.append( self.tabla.advancedSQL( tuple(list_campos), tuple(list_tables), where )[0])
		elif self.field_related:

			tuplas 		= self.tabla.advancedSQL( tuple(list_campos),list_tables, where )
		else:

			tuplas 		= self.tabla.obtenerTuplas( tuple(list_campos) )
				
		# Preparing TreeView

		# Establish headers database table del TreeView
		for campo in self.form:

			renderer 	= Gtk.CellRendererText()
			
			# Attributes render
			if self.form[campo].has_key("renderer-properties"):

				for properti in self.form[campo]["renderer-properties"]:
					
					getattr( renderer, "set_property" )( *[ properti, self.form[campo]["renderer-properties"][properti] ] )

			# Preparing TreeViewColumn
			column 		= Gtk.TreeViewColumn( self.form[campo]["name"], renderer, text=contador )

			# Attributes TreeViewColumn	
			if self.form[campo].has_key("treview-column-properties"):

				for properti in self.form[campo]["treview-column-properties"]:

					getattr( column, "set_" + properti )( *self.form[campo]["treview-column-properties"][properti] )
					#pprint(getattr( column, "get" + properti )( *self.form[campo]["treview-column-properties"][properti] ))
			
			# Add column to the TreeView
			self.TreeView.append_column( column )
			
			# Establish types for ListStore
			tipos.append( str )

			# Adjust width of window 
			widthWindow = widthWindow + self.form[ campo ]["treview-column-properties"][ "fixed_width" ][0]

			contador 	= contador +1

		# Establish types to the ListStore
		self.liststore.set_column_types( tipos )

		# Assign tuplas to the ListStoree
		for tupla in tuplas:
			
			tuplal = list()

			numcampo = 0
			for valor in tupla:
				
				try :

					tuplal.append( str(self.translate[self.form[numcampo]["campo"]][valor]).encode('utf-8') )

				except Exception:

					tuplal.append( str(valor).encode('utf-8') )

				numcampo = numcampo +1

			self.liststore.append( tuplal )
		
		# Establecer el ListStore al TreeView
		if self.form.has_key("treview-properties"):

				for properti in self.form["treview-properties"]:
					
					getattr( renderer, "set_property" )( *[ properti, self.form["treview-properties"][properti] ] )
		
		self.TreeView.set_model( self.liststore )

		#Asignacion de ancho de la Window
		self.Window.resize( widthWindow, 621 );
		self.scroll.set_min_content_width( widthWindow )

		# Asignacion de eventos a la ventana
		self.select.connect("changed", lambda activaSeleccion : self.seleccion())

		# Menu
		self.Interfaz.recoger("btnToolInsertar").connect( "clicked", lambda Nuevo : windowNuevo( self.tabla.nombre, self.foreign_key ) )
		self.btnToolModificar.connect( "clicked", lambda Modificar : self.callWindowModificar() )
		self.btnToolEliminar.connect( "clicked", lambda Eliminar : self.eliminar() )
		self.Interfaz.recoger("btnToolActualizar").connect( "clicked", lambda Actualizar : self.actualizar() )
		
		if self.extras.has_key("view"):

			if self.extras["view"] == "windowListadoPedidos":

				self.btnToolGenerarFactura.connect( "clicked", lambda GenerarFactura : self.generarFactura() )
		
		# Buttons aditionals configuration
		if len(self.toolbar_buttons):

			menu = self.Interfaz.recoger("menu")


			for toolbar_button in self.toolbar_buttons :

				button = Gtk.ToolButton
				
				self.buttons[self.toolbar_buttons[toolbar_button]["name"]] = Gtk.ToolButton

				# Assing properties
				if "properties" in self.toolbar_buttons[toolbar_button].keys():


					for properti in self.toolbar_buttons[toolbar_button]["properties"]:

						getattr(self.buttons[self.toolbar_buttons[toolbar_button]["name"]], "set_" + properti)(*self.toolbar_buttons[toolbar_button]["properties"][properti])

				pprint(self.buttons[self.toolbar_buttons[toolbar_button]["name"]])

				#menu.insert(self.buttons[self.toolbar_buttons[toolbar_button]["label"]],-1)

	def callWindowModificar( self ):

		if self.posicion != None :

			primary_key = self.valores[self.posicion][0]
			windowModificar(self.tabla.nombre, primary_key )

	def callWindowListadoDependency( self, relationship ):

		for column in self.form:

			if self.form[column]["campo"] == self.related["field-primary-key"] :
				value_position = column

		if self.posicion != None :

			foreign_key = self.valores[self.posicion][value_position]

			windowListado(self.related["relationship"][relationship]["table-related"], relationship, foreign_key )

	def seleccion( self ):

		if self.TreeView.get_selection().count_selected_rows() == 0 :

			self.btnToolEliminar.set_sensitive(False)
			self.btnToolModificar.set_sensitive(False)
			
			if self.extras.has_key("view"):

				if self.extras["view"] == "windowListadoPedidos":
					
					self.btnToolGenerarFactura.set_sensitive(False)

			for relationship in self.related["relationship"]:

				if self.related["relationship"][ relationship ]["button"]:

					self.btnToolRelated[self.related["relationship"][relationship]["name"]].set_sensitive(False)
		else :

			self.btnToolEliminar.set_sensitive(True)
			self.btnToolModificar.set_sensitive(True)
			
			if self.extras.has_key("view"):

				if self.extras["view"] == "windowListadoPedidos":
					
					self.btnToolGenerarFactura.set_sensitive(True)

			for relationship in self.related["relationship"]:

				if self.related["relationship"][ relationship ]["button"]:

					self.btnToolRelated[self.related["relationship"][relationship]["name"]].set_sensitive(True)

		self.valores, self.posicion = self.select.get_selected()

	def eliminar( self ):

		primary_key = self.valores[self.posicion][0]

		# Action before delete
		if self.action.has_key("before-delete"):

			valores = action_functions[ self.action["before-delete"] ]( self, primary_key )

		self.tabla.borrar(self.related["field-primary-key"], primary_key)

		# Action after delete
		if self.action.has_key("after-delete"):

			valores = action_functions[ self.action["after-delete"] ]( self, primary_key )

	def generarFactura( self ):

		primary_key = self.valores[self.posicion][0]

		select 	= list()
		tables 	= list()
		where 	= {}

		select.append("fecha")
		select.append("nombre")
		select.append("clientes_id")
		tables.append("pedido")
		where[self.related["field-primary-key"]] = { "operator" : "=", "value" : primary_key }

		campos = self.tabla.advancedSQL(select, tables, where)

		# Action before delete
		if self.action.has_key("before-generar-factura"):

			valores = action_functions[ self.action["before-generar-factura"] ]( self, primary_key )

		documentHTML = open( CONFIG["TEMPLATES"]+"facture.html","r")
		
		resultFile = open( CONFIG["FACTURES"]+"factura_"+str(campos[0][0])+"_"+str(campos[0][1])+"_cliente_"+str(campos[0][2])+".pdf", "w+b" )

		# convert HTML to PDF
		pisaStatus = pisa.CreatePDF( documentHTML.read(), dest=resultFile)

		resultFile.close()

		# Action after delete
		if self.action.has_key("after-generar-factura"):

			valores = action_functions[ self.action["after-generar-factura"] ]( self, primary_key )

	def actualizar( self ):

		# Inicializar valores
		tipos 		= list()
		list_campos = list()
		list_tables = list()
		where		= {}
		
		# Preparar Interfaz
		self.liststore = Gtk.ListStore()

		# Recoger campos a visualizar
		list_tables.append(self.tabla.nombre)
		for column in self.form:

			if self.form[column].has_key("related"):

				list_campos.append(self.form[column]["related"]["table"]+"."+self.form[column]["campo"])
				list_tables.append(self.form[column]["related"]["table"])
				where[ self.form[column]["related"]["table"]+"."+self.form[column]["related"]["field-primary-key"] ] = { "operator" : "=", "value" : self.tabla.nombre+"."+self.form[column]["related"]["field-foreign-key"] }
			else:

				list_campos.append(self.tabla.nombre+"."+self.form[column]["campo"])

			# Establecer tipos para el ListStore
			tipos.append( str )

		# Establecer conexion con la base de datos
		self.conexion 	= DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"], CONFIG["DATABASE"]).conexion
		self.tabla 		= Tabla(self.conexion, self.entidad )

		# Extraer datos de la Tabla
		if self.relationship:

			# Relationship type
			if   self.related["relationship"][self.relationship]["relation"] == "one-to-many":

				campos = list()
				campos.append(self.related["field-primary-key"])

				related_table = Tabla( self.conexion, self.tabla.nombre )
				list_primary_key = related_table.busquedaTuplas( self.related["relationship"][self.relationship]["field-foreign-key"], self.foreign_key, campos )
			elif self.related["relationship"][self.relationship]["relation"] == "one-to-one":

				pass

			# Preparing query
			tuplas = list()
			for primary_key in list_primary_key:

				if len(list_tables) == 0:

					tuplas.append( self.tabla.busquedaTuplas( self.related["relationship"][self.relationship]["field-foreign-key"], str(primary_key[0]), tuple(list_campos) )[0])
				else:

					where[ self.tabla.nombre+"."+self.related["field-primary-key"] ] = { "operator" : "=", "value" 	: primary_key[0] }
					
					tuplas.append( self.tabla.advancedSQL( tuple(list_campos), tuple(list_tables), where )[0])
		elif self.field_related:

			tuplas 		= self.tabla.advancedSQL( tuple(list_campos),list_tables, where )
		else:

			tuplas 		= self.tabla.obtenerTuplas( tuple(list_campos) )
		
		#Establecer Tipos del ListStore
		self.liststore.set_column_types( tipos )

		# Asignar tuplas al ListStore
		for tupla in tuplas:
			
			tuplal = list()

			numcampo = 0
			for valor in tupla:
				
				try :

					tuplal.append( str(self.translate[self.form[numcampo]["campo"]][valor]).encode('utf-8') )

				except Exception:

					tuplal.append( str(valor).encode('utf-8') )

				numcampo = numcampo +1

			self.liststore.append( tuplal )

		# Establecer el ListStore al TreeView
		self.TreeView.set_model( self.liststore )

#----------------------------------------------------------------------------------------

class windowNuevo( windowXML ) :

	def __init__( self, tabla, foreign_key = False  ):

		windowXML.__init__( self, False )

		# Inicializar valores
		ancho 				= 450
		coorY 				= 25
		coorX 				= 70
		where				= {}
		self.foreign_key 	= foreign_key

		# Cargar configuracion window
		self.config 	= CLASS[tabla]()
		self.config.insert()
		self.related 	= self.config.related
		self.translate 	= self.config.translate
		self.form 		= self.config.form_insert
		self.titulo 	= self.config.title_insert
		self.default 	= self.config.default
		self.action 	= self.config.action

		# Preparar Interfaz
		self.elements 	= {}
		self.scroll 	= {}
		layout 			= Gtk.Layout()
		encabezado 		= Gtk.Label( "Introduce los datos del "+self.config.singular+":" )
		color 			= Gdk.RGBA(255,255,255,255)

		self.Window.set_title(self.titulo)
		layout.override_background_color(Gtk.StateFlags.NORMAL,color)

		# Establecer conexion con la base de datos
		self.conexion 	= DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"], CONFIG["DATABASE"]).conexion
		self.tabla 		= Tabla(self.conexion, tabla)

		# Construccion Formulario
		layout.put( encabezado, coorX, coorY )
		coorY = coorY + 30

		# Añadir campos
		for element in self.form:

			# default data
			for default in self.default:
				if not default in self.form[element].keys():

					self.form[element][default] = self.default[default]

			# show fields 
			if self.form[element]["visibility"]:

				etiqueta = Gtk.Label( self.form[element]["name"] + ": " )

				# Posicionado label field
				layout.put( etiqueta, 75, coorY + 6 )

				# field form selector
				if   self.form[element]["type"] == "TextView":

					self.elements[self.form[element]["name"]] = Gtk.TextView()

					self.scroll[self.form[element]["name"]] = Gtk.ScrolledWindow()

					
					for properti in self.form[element]["scroll"]:

						getattr(self.scroll[self.form[element]["name"]], "set_" + properti)(*self.form[element]["scroll"][properti])

					self.scroll[self.form[element]["name"]].add(self.elements[self.form[element]["name"]])

					if self.form[element]["options"].has_key("textArea"):

						#Establecer nuevo width window
						ancho = 660

						# Posicionar Scroll

						layout.put( self.scroll[self.form[element]["name"]], self.form[element]["coordX"], coorY )
						coorY = coorY + 110
					else :

						# Posicionar Scroll
						layout.put( self.scroll[self.form[element]["name"]], 202, coorY + 6 )
				elif self.form[element]["type"] == "Entry":

					self.elements[self.form[element]["name"]] = Gtk.Entry()

					# Posicionar Entry
					layout.put( self.elements[self.form[element]["name"]], self.form[element]["coordX"], coorY )
				elif self.form[element]["type"] == "CheckButton":

					self.elements[self.form[element]["name"]] = Gtk.CheckButton()
					layout.put( self.elements[self.form[element]["name"]], self.form[element]["coordX"], coorY )
				elif self.form[element]["type"] == "SpinButton":

					self.elements[self.form[element]["name"]] = Gtk.SpinButton()
					layout.put( self.elements[self.form[element]["name"]], self.form[element]["coordX"], coorY )
				elif self.form[element]["type"] == "ComboBox":

					# Inicializar valores
					list_tables = list()
					list_campos = list()
					tipos 		= list()

					self.elements[self.form[element]["name"]] = Gtk.ComboBox()
					
					# Position ComboBox
					layout.put( self.elements[self.form[element]["name"]], self.form[element]["coordX"], coorY )

					# Tabla
					combo_table = Tabla( self.conexion, self.related["relationship"][ self.form[element]["relationship"] ]["table-related"] )

					# Recoger campos a visualizar
					if self.form[element].has_key("relationship"):

						if  self.related["relationship"][ self.form[element]["relationship"] ]["relation"] == "one-to-many" and self.related["relationship"][ self.form[element]["relationship"] ]["entity"] == "many" :

							tipos.append( int )
							list_campos.append( self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+self.related["relationship"][ self.form[element]["relationship"] ]["field-related-primary-key"] )
							
							for field in self.form[element]["view-fields"]:

								list_campos.append( self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+field )
								tipos.append( self.form[element]["view-fields"][field] )

							# Extraer datos de la Tabla
							tuplas = combo_table.obtenerTuplas(list_campos)
						elif self.related["relationship"][ self.form[element]["relationship"] ]["relation"] == "one-to-one":

								tipos.append( int )

								pre_sql = "SELECT COUNT(*)"

								pre_sql = pre_sql + " FROM "

								pre_sql = pre_sql + self.tabla.nombre

								pre_sql = pre_sql + " WHERE "

								pre_sql = pre_sql + self.related["relationship"][ self.related["relationship"][ self.form[element]["relationship"] ]["relationship"] ]["field-foreign-key"]+"="+str(self.foreign_key)

								num_result = int(combo_table.executeSQL( pre_sql )[0][0])

								if num_result > 0:

									sql = "SELECT DISTINCT "
									sql = sql+self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+self.related["relationship"][ self.form[element]["relationship"] ]["field-related-primary-key"]
									
									for field in self.form[element]["view-fields"]:

										sql = sql+", "+self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+field
										tipos.append( self.form[element]["view-fields"][field] )

									sql = sql+" FROM "

									sql = sql+self.tabla.nombre+", "+self.related["relationship"][self.form[element]["relationship"]]["table-related"]

									sql = sql+" WHERE "

									sql = sql+self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+self.related["relationship"][ self.form[element]["relationship"] ]["field-related-primary-key"]+" NOT IN("

									sql = sql+" SELECT "

									sql = sql+self.related["relationship"][self.form[element]["relationship"]]["field-table-related"]

									sql = sql+" FROM "

									sql = sql+self.tabla.nombre

									sql = sql+" WHERE "

									sql = sql+self.related["relationship"][ self.related["relationship"][ self.form[element]["relationship"] ]["relationship"] ]["field-foreign-key"]+"="+str(self.foreign_key)

									sql = sql+" ); "
								
								else:

									sql = "SELECT "
									sql = sql+self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+self.related["relationship"][ self.form[element]["relationship"] ]["field-related-primary-key"]
									
									for field in self.form[element]["view-fields"]:

										sql = sql+", "+self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+field
										tipos.append( self.form[element]["view-fields"][field] )

									sql = sql+" FROM "

									sql = sql+self.related["relationship"][self.form[element]["relationship"]]["table-related"]
								
								tuplas = combo_table.executeSQL( sql )
						elif self.related["relationship"][ self.form[element]["relationship"] ]["relation"] == "many-to-many":

							pass
					
					combo_liststore = Gtk.ListStore()

					# Assign types
					combo_liststore.set_column_types(tipos)

					# Asignar tuplas al ListStoree
					combo_liststore.append( [-1,"-----No Selected-----"] )
					for tupla in tuplas:

						tuplal = list()

						numcampo = 0
						for valor in tupla:

							if numcampo == 0:

								tuplal.append( int(valor) )
							else :
								tuplal.append( str(valor).encode('utf-8') )

							numcampo = numcampo +1

						combo_liststore.append( tuplal )

					# Assign listStore a ComboBox
					self.elements[self.form[element]["name"]].set_model(combo_liststore)
					
					# View Combo Box
					renderer_text = Gtk.CellRendererText()
					self.elements[self.form[element]["name"]].pack_start(renderer_text, True)
					self.elements[self.form[element]["name"]].add_attribute(renderer_text, "text", 1)

					ancho = ancho + 148

				# Vertical separate field form
				coorY = coorY + 35

				# Assing properties
				if "properties" in self.form[element].keys():

					for properti in self.form[element]["properties"]:

						getattr(self.elements[self.form[element]["name"]], "set_" + properti)(*self.form[element]["properties"][properti])

			# function events
			if "event" in self.form[element].keys():

				loop_events( self.form[element]["name"], self.form[element]["event"], self )

		# Añadir botones
		coorY = coorY + 15
		btnReset 	= Gtk.Button( "Limpiar" )
		layout.put( btnReset, 145, coorY )

		btnEnviar 	= Gtk.Button( "Guardar" )
		layout.put( btnEnviar, 225, coorY )

		self.Window.add( layout )

		self.Window.set_size_request( ancho , coorY + 50 )
		
		self.Window.show_all()

		# Asignacion de eventos a la ventana

		# Botones
		btnReset.connect( "clicked", lambda Reset : self.reset() )
		btnEnviar.connect( "clicked", lambda Insertar : self.insertar() )

	def insertar( self ):

		valores = {}

		for element in self.form:

			if self.form[element]["get"] :

				if   self.form[element]["type"] == "TextView":

					bufferTextView 	= self.elements[self.form[element]["name"]].get_buffer()
					start 			= bufferTextView.get_start_iter()
					end 			= bufferTextView.get_end_iter()

					if self.form[element]["options"].has_key("divisa"):
						
						valores[self.form[element]["campo"]] = bufferTextView.get_text(start,end,True).rstrip(self.form[element]["options"]["divisa"])
					else:
						
						valores[self.form[element]["campo"]] = bufferTextView.get_text(start,end,True)
				elif self.form[element]["type"] == "Entry":

					if self.form[element]["options"].has_key("divisa"):
						
						valores[self.form[element]["campo"]] = self.elements[self.form[element]["name"]].get_text().rstrip(self.form[element]["options"]["divisa"])
					else:
						
						valores[self.form[element]["campo"]] = self.elements[self.form[element]["name"]].get_text()
				elif self.form[element]["type"] == "CheckButton":

					valores[self.form[element]["campo"]] = self.elements[self.form[element]["name"]].get_active()	
				elif self.form[element]["type"] == "SpinButton":

					valores[self.form[element]["campo"]] = self.elements[self.form[element]["name"]].get_value()
				elif self.form[element]["type"] == "ComboBox":

					select = self.elements[self.form[element]["name"]].get_active_iter()

					model = self.elements[self.form[element]["name"]].get_model()
					param_id, param_nombre = model[select][:2]

					valores[self.form[element]["campo"]] = param_id

				# Convert type
				if self.form[element].has_key("campo"):

					if self.form[element]["data-type"] == str:

						valores[self.form[element]["campo"]] = "'"+str(valores[self.form[element]["campo"]]).encode('utf-8')+"'"
					else:

						valores[self.form[element]["campo"]] = str(valores[self.form[element]["campo"]]).encode('utf-8')

		# Action after insert
		if self.action.has_key("before-insert"):

			valores = action_functions[ self.action["before-insert"] ]( self, valores )

		# Relationship type
		if self.related["entity"] == "many":

			valores[self.related["field-foreign-key"]] = self.foreign_key
			self.tabla.insertar(valores)
		else: 
			
			self.tabla.insertar(valores)

		# Action after insert
		if self.action.has_key("after-insert"):

			valores = action_functions[ self.action["after-insert" ] ]( self, valores )

		self.Window.destroy()

	def reset( self ):

		for element in self.form:

			if  self.form[element]["type"] == "Entry":

				self.elements[self.form[element]["name"]].set_text("")
			elif self.form[element]["type"] == "TextView":

				self.elements[self.form[element]["name"]].get_buffer().set_text("")
			elif self.form[element]["type"] == "SpinButton":

				self.elements[self.form[element]["name"]].set_value(self.form[element]["properties"]["value"][0])
			elif self.form[element]["type"] == "CheckButton":

				self.elements[self.form[element]["name"]].set_active(False)
			elif self.form[element]["type"] == "ComboBox":

				self.elements[self.form[element]["name"]].set_active(self.form[element]["properties"]["active"][0])

#----------------------------------------------------------------------------------------

class windowModificar( windowXML ) :

	def __init__( self, tabla, primary_key ):

		windowXML.__init__( self, False )

		# Inicializar valores
		ancho 				= 450
		coorY 				= 25
		coorX 				= 70
		contador 			= 0
		list_campos 		= list()
		self.list_valores 	= {}
		self.primary_key 	= primary_key


		# Cargar configuracion window
		self.config 			= CLASS[tabla]()
		self.config.change()
		self.translate 			= self.config.translate
		self.form 				= self.config.form_change
		self.titulo 			= self.config.title_change
		self.related 			= self.config.related
		self.default 			= self.config.default
		self.action 			= self.config.action

		# Preparar interfaz
		self.elements 	= {}
		self.scroll 	= {}
		layout 			= Gtk.Layout()
		encabezado 		= Gtk.Label( "Modifica los datos del "+self.config.singular+":" )
		color 			= Gdk.RGBA(255,255,255,255)
		
		layout.override_background_color(Gtk.StateFlags.NORMAL,color)
		self.Window.set_title(self.titulo)

		# Cargar Alias
		alias 			= alias_database(tabla)

		# Establecer conexion con la base de datos
		self.conexion 	= DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"], CONFIG["DATABASE"]).conexion
		self.tabla 		= Tabla(self.conexion, tabla)

		# Recoger campos a visualizar
		for element in self.form:

			if self.form[element].has_key("campo"):
				list_campos.append(self.form[element]["campo"])

		# Extraer datos de la Tabla
		tuplas 		= self.tabla.busquedaTuplas(self.related["field-primary-key"], self.primary_key, tuple(list_campos))

		# Construccion Formulario
		layout.put( encabezado, coorX, coorY )
		coorY = coorY + 30
		
		# Recuperar valores
		for tupla in tuplas:
			
			for valor in tupla:

				self.list_valores[contador] = valor
				contador = contador +1

		# Añadir campos
		contador = 0
		for element in self.form:

			# default data
			for default in self.default:
				
				if not default in self.form[element].keys():

					self.form[element][default] = self.default[default]
			
			# show fields 
			if self.form[element]["visibility"] :

				etiqueta 	= Gtk.Label( self.form[element]["name"] + ": " )

				# Position label field
				layout.put( etiqueta, 75, coorY + 6 )

				# Create element GTK
				self.elements[self.form[element]["name"]] = getattr( Gtk, self.form[element]["type"] )()

				# Assing properties
				if "fist-properties" in self.form[element].keys():

					for properti in self.form[element]["fist-properties"]:

						getattr(self.elements[self.form[element]["name"]], "set_" + properti)(*self.form[element]["fist-properties"][properti])

				# field form selector
				if   self.form[element]["type"] == "TextView":

					self.scroll[self.form[element]["name"]] = Gtk.ScrolledWindow()

					for properti in self.form[element]["scroll"]:

						getattr(self.scroll[self.form[element]["name"]], "set_" + properti)(*self.form[element]["scroll"][properti])

					# Rellenar de valores
					if self.form[element].has_key("campo"):

						try:
							
							if self.form[element]["options"].has_key("divisa"):
								text_buffer = self.elements[self.form[element]["name"]].get_buffer().set_text(str(self.translate[self.form[element]["campo"]][self.list_valores[contador]]).encode('utf-8')+str(self.form[element]["options"]["divisa"]).encode('utf-8'))
							else:
								text_buffer = self.elements[self.form[element]["name"]].get_buffer().set_text(str(self.translate[self.form[element]["campo"]][self.list_valores[contador]]).encode('utf-8'))
						except Exception:
							
							if self.form[element]["options"].has_key("divisa"):
								text_buffer = self.elements[self.form[element]["name"]].get_buffer().set_text(str(self.list_valores[contador]).encode('utf-8')+str(self.form[element]["options"]["divisa"]).encode('utf-8'))
							else:
								text_buffer = self.elements[self.form[element]["name"]].get_buffer().set_text(str(self.list_valores[contador]).encode('utf-8'))

					self.scroll[self.form[element]["name"]].add(self.elements[self.form[element]["name"]])

					if self.form[element]["options"].has_key("textArea"):

						#Establecer nuevo width window
						ancho = 660

						# Posicionar Scroll
						layout.put( self.scroll[self.form[element]["name"]], self.form[element]["coordX"], coorY )

						coorY = coorY + 110
					else :

						# Posicionar Scroll
						layout.put( self.scroll[self.form[element]["name"]], 202, coorY+6 )
				elif self.form[element]["type"] == "Entry":

					layout.put( self.elements[self.form[element]["name"]], self.form[element]["coordX"], coorY )
					
					# Rellenar de valores
					if self.form[element].has_key("campo"):
						try:
							
							if self.form[element]["options"].has_key("divisa"):
								
								self.elements[self.form[element]["name"]].set_text(str(self.translate[self.form[element]["campo"]][self.list_valores[contador]]).encode('utf-8')+str(self.form[element]["options"]["divisa"]).encode('utf-8'))
							else:
								
								self.elements[self.form[element]["name"]].set_text(str(self.translate[self.form[element]["campo"]][self.list_valores[contador]]).encode('utf-8'))
							
						except Exception:

							if self.form[element]["options"].has_key("divisa"):

								self.elements[self.form[element]["name"]].set_text(str(self.list_valores[contador]).encode('utf-8')+str(self.form[element]["options"]["divisa"]).encode('utf-8'))
							else:

								self.elements[self.form[element]["name"]].set_text(str(self.list_valores[contador]).encode('utf-8'))
				elif self.form[element]["type"] == "CheckButton":

					layout.put( self.elements[self.form[element]["name"]], self.form[element]["coordX"], coorY )
					
					# Rellenar de valores
					if self.form[element].has_key("campo"):
						self.elements[self.form[element]["name"]].set_active(self.list_valores[contador])
				elif self.form[element]["type"] == "SpinButton":

					layout.put( self.elements[self.form[element]["name"]], self.form[element]["coordX"], coorY )
					# Rellenar de valores
					if self.form[element].has_key("campo"):
						self.elements[self.form[element]["name"]].set_value(self.list_valores[contador])			
				elif self.form[element]["type"] == "ComboBox":

					# Inicializar valores
					list_tables = list()
					list_campos = list()
					tipos 		= list()

					layout.put( self.elements[self.form[element]["name"]], self.form[element]["coordX"], coorY )

					combo_table = Tabla( self.conexion, self.related["relationship"][ self.form[element]["relationship"] ]["table-related"] )

					# Recoger campos a visualizar
					if self.form[element].has_key("relationship"):

						if   self.related["relationship"][ self.form[element]["relationship"] ]["relation"] == "one-to-many" and self.related["relationship"][ self.form[element]["relationship"] ]["entity"] == "many" :

							tipos.append( int )
							list_campos.append( self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+self.related["relationship"][ self.form[element]["relationship"] ]["field-related-primary-key"] )
							
							for field in self.form[element]["view-fields"]:

								list_campos.append( self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+field )
								tipos.append( self.form[element]["view-fields"][field] )

							# Extraer datos de la Tabla
							tuplas = combo_table.obtenerTuplas(list_campos)
						elif self.related["relationship"][ self.form[element]["relationship"] ]["relation"] == "one-to-one":

							tipos.append( int )

							sql = "SELECT DISTINCT "
							sql = sql+self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+self.related["relationship"][ self.form[element]["relationship"] ]["field-related-primary-key"]
							
							list_campos.append(self.related["relationship"][ self.form[element]["relationship"] ]["field-related-primary-key"])
							for field in self.form[element]["view-fields"]:

								sql = sql+", "+self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+field
								list_campos.append(field)
								tipos.append( self.form[element]["view-fields"][field] )

							sql = sql+" FROM "

							sql = sql+self.tabla.nombre+", "+self.related["relationship"][self.form[element]["relationship"]]["table-related"]

							sql = sql+" WHERE "

							sql = sql+self.related["relationship"][ self.form[element]["relationship"] ]["table-related"]+"."+self.related["relationship"][ self.form[element]["relationship"] ]["field-related-primary-key"]+" NOT IN("

							sql = sql+" SELECT "

							sql = sql+self.related["relationship"][self.form[element]["relationship"]]["field-table-related"]

							sql = sql+" FROM "

							sql = sql+self.tabla.nombre

							sql = sql+" ); "
							
							tuplas = combo_table.executeSQL( sql )

							# Recuperar Valor seleccionado
							select_valor = combo_table.busquedaTuplas( self.related["relationship"][ self.form[element]["relationship"] ]["field-related-primary-key"], self.list_valores[contador],list_campos)
							tuplas = select_valor + tuplas
						elif self.related["relationship"][ self.form[element]["relationship"] ]["relation"] == "many-to-many":

							pass

			
					combo_liststore = Gtk.ListStore()

					# Assign types
					combo_liststore.set_column_types(tipos)

					# Asignar tuplas al ListStoree
					combo_liststore.append( [-1,"-----No Selected-----"] )
					position = 1
					
					for tupla in tuplas:

						tuplal = list()

						numcampo = 0
						for valor in tupla:

							if numcampo == 0:

								try:

									if int(valor) == int(self.list_valores[contador]):
										
										self.active_iter = position

								except Exception:
									self.active_iter = 0

								tuplal.append( int(valor) )
							else :
								tuplal.append( str(valor).encode('utf-8') )

							numcampo = numcampo +1

						combo_liststore.append( tuplal )
						position = position +1

					self.elements[self.form[element]["name"]].set_model(combo_liststore)
					
					renderer_text = Gtk.CellRendererText()
					self.elements[self.form[element]["name"]].pack_start(renderer_text, True)
					self.elements[self.form[element]["name"]].add_attribute(renderer_text, "text", 1)

					ancho = ancho + 148

					# Rellenar de valores
					if self.form[element].has_key("campo"):

						self.elements[self.form[element]["name"]].set_active(self.active_iter)

				# Vertical separate field form
				coorY = coorY + 35

				# Assing properties
				if "properties" in self.form[element].keys():

					for properti in self.form[element]["properties"]:

						getattr(self.elements[self.form[element]["name"]], "set_" + properti)(*self.form[element]["properties"][properti])
				
			# function events
			if "event" in self.form[element].keys():

				loop_events( self.form[element]["name"], self.form[element]["event"], self )
			
			contador = contador +1

		# Añadir botones
		coorY = coorY + 15
		btnReset 	= Gtk.Button( "Limpiar" )
		layout.put( btnReset, 145, coorY )

		btnEnviar 	= Gtk.Button( "Modificar" )
		layout.put( btnEnviar, 225, coorY )

		self.Window.add( layout )
		self.Window.set_size_request( ancho , coorY + 50 )
		self.Window.show_all()

		# Asignacion de eventos a la ventana

		# Botones
		btnReset.connect( "clicked", lambda Reset : self.reset() )
		btnEnviar.connect( "clicked", lambda Insertar : self.modificar() )

	def modificar( self ):

		valores = {}
		c = 0
		
		for element in self.form:
			
			c = c + 1
			if self.form[element]["get"]:
				
				if   self.form[element]["type"] == "TextView":

					bufferTextView 	= self.elements[self.form[element]["name"]].get_buffer()
					start 			= bufferTextView.get_start_iter()
					end 			= bufferTextView.get_end_iter()

					if self.form[element]["options"].has_key("divisa") :
						
						valores[c] = { "nombre" : self.form[element]["campo"], "valor" : bufferTextView.get_text(start,end,True).rstrip(self.form[element]["options"]["divisa"]) }
					else:
						
						valores[c] = { "nombre" : self.form[element]["campo"], "valor" : bufferTextView.get_text(start,end,True) }
				elif self.form[element]["type"] == "Entry":

					if self.form[element]["options"].has_key("divisa"):
						
						valores[c] = { "nombre" : self.form[element]["campo"], "valor" : self.elements[self.form[element]["name"]].get_text().rstrip(self.form[element]["options"]["divisa"]) }
					else:

						valores[c] = { "nombre" : self.form[element]["campo"], "valor" : self.elements[self.form[element]["name"]].get_text() }
				elif self.form[element]["type"] == "CheckButton":

					valores[c] = { "nombre" : self.form[element]["campo"], "valor" : self.elements[self.form[element]["name"]].get_active() }
				elif self.form[element]["type"] == "SpinButton":

					valores[c] = { "nombre" : self.form[element]["campo"], "valor" : self.elements[self.form[element]["name"]].get_value() }
				elif self.form[element]["type"] == "ComboBox":

					select = self.elements[self.form[element]["name"]].get_active_iter()

					model = self.elements[self.form[element]["name"]].get_model()
					param_id, param_nombre = model[select][:2]

					valores[c] = { "nombre" : self.form[element]["campo"], "valor" : param_id }

				
				# Convert type
				if self.form[element].has_key("campo"):

					if self.form[element]["data-type"] == str:

						valores[c]["valor"] = "'"+str(valores[c]["valor"]).encode('utf-8')+"'"
					else:

						valores[c]["valor"] = str(valores[c]["valor"]).encode('utf-8')

		# Action before change
		if self.action.has_key("before-change"):

			valores = action_functions[ self.action["before-change"] ]( self, valores )

		self.tabla.modificar( valores,self.related["field-primary-key"], self.primary_key )

		# Action after change
		if self.action.has_key("after-change"):
			
			valores = action_functions[ self.action["after-change"] ]( self, valores )

		self.Window.destroy()

	def reset( self ):

		contador = 0

		for element in self.form:

			if self.form[element].has_key("campo"):
				
				if   self.form[element]["type"] == "Entry":

					if self.form[element]["options"].has_key("divisa"):
						
						try:

							self.elements[ self.form[element]["name"] ].set_text(str(self.translate[self.form[element]["campo"]][ str(self.list_valores[contador]) + self.form[element]["options"]["divisa"] ]).encode('utf-8'))

						except Exception:

							self.elements[ self.form[element]["name"] ].set_text(str(self.list_valores[contador] + self.form[element]["options"]["divisa"]).encode('utf-8'))
					else:

						try:

							self.elements[ self.form[element]["name"] ].set_text(str(self.translate[self.form[element]["campo"]][self.list_valores[contador]]).encode('utf-8'))

						except Exception:

							self.elements[ self.form[element]["name"] ].set_text(str(self.list_valores[contador]).encode('utf-8'))
				elif self.form[element]["type"] == "TextView":

					if self.form[element]["options"].has_key("divisa"):
						
						try:
						
							text_buffer = self.elements[ self.form[element]["name"] ].get_buffer().set_text(self.translate[ self.form[element]["campo"] ][ str(self.list_valores[contador]) + self.form[element]["options"]["divisa"] ].encode('utf-8'))

						except Exception:

							text_buffer = self.elements[ self.form[element]["name"] ].get_buffer().set_text( str( self.list_valores[contador] ).encode('utf-8') + self.form[element]["options"]["divisa"])
					else:

						try:
						
							text_buffer = self.elements[ self.form[element]["name"] ].get_buffer().set_text( self.translate[ self.form[element]["campo"] ][ self.list_valores[contador] ].encode('utf-8'))

						except Exception:

							text_buffer = self.elements[ self.form[element]["name"] ].get_buffer().set_text(str(self.list_valores[contador]).encode('utf-8'))
				elif self.form[element]["type"] == "SpinButton":

					self.elements[ self.form[element]["name"] ].set_value(self.list_valores[contador])
				elif self.form[element]["type"] == "CheckButton":

					self.elements[ self.form[element]["name"] ].set_active(self.list_valores[contador])
				elif self.form[element]["type"] == "ComboBox":

					self.elements[ self.form[element]["name"] ].set_active(self.active_iter)
			
			contador = contador +1

class windowFacturas( windowXML ) :

	def __init__( self ):

		# Cargar configuracion window
		self.config 			= CLASS["factura"]()
		self.config.list()
		self.translate 			= self.config.translate
		self.extras 			= self.config.extras
		self.related 			= self.config.related
		self.titulo 			= self.config.title_list
		self.form 			= self.config.form

		windowXML.__init__( self, False, self.extras["view"] )

		# Inicializar valores
		where					= {}
		tipos 					= list()
		list_campos 			= list()
		list_tables 			= list()
		self.entidad 			= config.extras["tabla"]
		widthWindow 			= 10
		contador 				= 0

		# Recoger Interfaz
		self.btnToolEliminar 	= self.Interfaz.recoger("btnToolEliminar")
		self.btnToolVerFactura 	= self.Interfaz.recoger("btnToolVerFactura")
		self.TreeView 			= self.Interfaz.recoger("Tabla")
		self.scroll 			= self.Interfaz.recoger("scrollWindow")
		self.liststore 			= Gtk.ListStore( )
		self.select 			= self.TreeView.get_selection()

		# Establecer propiedades a la interfaz
		self.Window.set_title(self.titulo)
		self.btnToolEliminar.set_sensitive(False)
		self.btnToolVerFactura.set_sensitive(False)
		self.Window.set_decorated(True)
		self.select.set_mode(Gtk.SelectionMode.SINGLE)

		# Establecer conexion con la base de datos
		self.conexion 	= DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"], CONFIG["DATABASE"]).conexion
		self.tabla 		= Tabla(self.conexion, self.entidad )

		# Get fields for visualize
		list_tables.append(self.tabla.nombre)
		for column in self.form:

			list_campos.append(self.tabla.nombre+"."+self.form[column]["campo"])

		# Extraer datos de la Tabla
		tuplas 		= self.tabla.advancedSQL( list_campos )

		# Preparing TreeView

		# Establish headers database table del TreeView
		for campo in self.form:

			renderer 	= Gtk.CellRendererText()
			
			# Attributes render
			renderer.set_property( "wrap-mode", pango.WRAP_WORD )
			renderer.set_property( "wrap-width", 400 )

			# Preparing TreeViewColumn
			column 		= Gtk.TreeViewColumn( self.form[ campo ]["name"], renderer, text=contador )

			# Attributes TreeViewColumn	
			column.set_fixed_width ( self.form[ campo ][ "size" ] )
			column.set_min_width( self.form[ campo ][ "size-min" ] )
			column.set_max_width( self.form[ campo ][ "size-max" ] )
			column.set_resizable( True )
			
			# Add column to the TreeView
			self.TreeView.append_column( column )
			
			# Establish types for ListStore
			tipos.append( str )

			# Adjust width of window 
			widthWindow = widthWindow + self.form[ campo ][ "size" ]

			contador 	= contador +1

		# Establish types to the ListStore
		self.liststore.set_column_types( tipos )

		# Assign tuplas to the ListStoree
		for tupla in tuplas:
			
			tuplal = list()

			numcampo = 0
			for valor in tupla:
				
				try :

					tuplal.append( str(self.translate[self.form[numcampo]["campo"]][valor]).encode('utf-8') )

				except Exception:

					tuplal.append( str(valor).encode('utf-8') )

				numcampo = numcampo +1

			self.liststore.append( tuplal )
		
		# Establecer el ListStore al TreeView
		self.TreeView.set_property("level-indentation",2) 
		self.TreeView.set_model( self.liststore )

		#Asignacion de ancho de la Window
		self.Window.resize( widthWindow, 621 );
		self.scroll.set_min_content_width( widthWindow )

		# Asignacion de eventos a la ventana
		self.select.connect("changed", lambda activaSeleccion : self.seleccion())

	def seleccion( self ):

		if self.TreeView.get_selection().count_selected_rows() == 0 :

			self.btnToolEliminar.set_sensitive(False)
			self.btnToolVerFactura.set_sensitive(False)
		else :

			self.btnToolEliminar.set_sensitive(True)
			self.btnToolVerFactura.set_sensitive(True)

		self.valores, self.posicion = self.select.get_selected()