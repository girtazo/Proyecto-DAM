#!/usr/bin/python

from gi.repository import Gtk

class InterfazGlade :

	def __init__(self,archivo):

		self.archivo = archivo
		self.xml = Gtk.Builder()
		self.xml.add_from_file(archivo+".glade")

	def asignarsenyales(self,handler,quit=False):
		
		if(quit) :
			handler["cerrar"] = Gtk.main_quit
		self.xml.connect_signals(handler)

	def recoger(self,id):

		return self.xml.get_object(id)

	def recargar(self):

		self.xml = Gtk.Builder()
		self.xml.add_from_file(archivo+".glade")