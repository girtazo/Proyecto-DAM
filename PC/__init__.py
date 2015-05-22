# -*- coding: utf-8 -*-
#!/usr/bin/python

# Librerias
import sys
import sqlite3
import time
import threading
import socket
from gi.repository import Gtk
from pprint import pprint

# Librerias propias
from bibliotecas.database import *
from bibliotecas.windows import *

# Acceder a configuracion
sys.path.append("./configuracion")
from configuracion.config import *

# Cargar codificacion
reload(sys)
sys.setdefaultencoding( "utf8" )

try :
	conexion = DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"], CONFIG["DATABASE"]).conexion
except Exception:

	try :
		database["exec_sql_file"](conexion.cursor(),CONFIG["FILE"])
	except Exception:

		try :

			conexion = MySQL(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"]).conexion
			cursor = conexion.cursor()
			cursor.execute("CREATE DATABASE "+ CONFIG["DATABASE"])
			conexion = DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"],CONFIG["DATABASE"]).conexion
			exec_sql_file(conexion.cursor(),CONFIG["FILE"]);

		except Exception:
			
			print "No connection server MySQL"
# class appPython(threading.Thread) :

# 	def __init__(self):

# 		threading.Thread.__init__(self)
mainWindow = windowMain()

	# def run(self) :
# Lanzar GTK
Gtk.main()

	# 	while True :

	# 		try :
				
	# 			conexion = DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"], CONFIG["DATABASE"]).conexion
	# 			self.mainWindow.activeEvents()
	# 			print("entra bien")
	# 		except Exception:
	# 			print("entra mal")
	# 			self.mainWindow.disableEvents()


# class ConnectMysql(threading.Thread) :

# 	def __init__(self,app):

# 		threading.Thread.__init__(self)
# 		self.app = app

# 	def run(self) :

# 		while True :
# 			try :
# 				time.sleep(1000)
# 				conexion = DB(CONFIG["HOST"], CONFIG["USER"], CONFIG["PASSWORD"], CONFIG["DATABASE"]).conexion
# 				self.app.mainWindow.activeEvents()
# 				print("entra bien")
# 			except Exception:
# 				print("entra mal")
# 				self.app.mainWindow.disableEvents()

# app = appPython()
# conexion = ConnectMysql(app)
# conexion.start()
# app.run()


# class serverListen(threading.Thread) :

# 	def __init__(self):

# 		threading.Thread.__init__(self)
# 		self.serverSocket = socket.socket()
# 		self.clientSocket = False

# 	def run(self) :

# 		try :

# 			# Establecer Socket
# 			self.serverSocket.bind(("localhost",5000))
# 			self.serverSocket.listen(10)

# 			# Escuchar peticiones
# 			print("Esperando conexion ...")
# 			self.clientSocket, (host,port) = self.serverSocket.accept()

# 			print("Conectado.")

# 		except KeyboardInterrupt:

# 			self.serverSocket.close()
# 			if self.clientSocket :
# 				self.clientSocket.close()

# 			print( "kill proceso serverListen" )

# # Establecer procesos

# server = serverListen()
# windowProgram = appPython(server)
# windowProgram.start()
# server.start()
# windowProgram.join()