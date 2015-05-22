#!/usr/bin/python
# -*- coding: utf-8 -*-

# Librerias
import sys
import MySQLdb
import re
from pprint import pprint

# Acceder a configuracion
sys.path.append("../configuracion")
from configuracion.config import *

#----------------------------------------------------------------------------------------

class MySQL :

	"""Maneja el servidor MySQL"""

	def __init__( self, host, user, password ):
		
		self.host = host;
		self.user = user;
		self.password = password;
		self.conexion = MySQLdb.connect( self.host, self.user, self.password )
		self.cursor = self.conexion.cursor()

	def cerrar( self ):

		self.conexion.close()

#----------------------------------------------------------------------------------------

class DB :

	"""Maneja el servidor MySQL"""

	def __init__( self, host, user, password, database ):
		
		self.host = host
		self.user = user
		self.password = password
		self.database = database

		self.conexion = MySQLdb.connect( self.host, self.user, self.password, self.database, charset='utf8', init_command='SET NAMES UTF8' )
		self.cursor = self.conexion.cursor()

	def cerrar( self ):

		self.conexion.close()

#----------------------------------------------------------------------------------------

class Tabla :
	
	"""Maneja una tabla de una de base de datos MySQL"""

	def __init__( self, conexion, nombre ):
		
		self.nombre = nombre
		self.conexion = conexion
		self.cursor = self.conexion.cursor()
		self.campos = self.getCampos()

	def cambiarTabla( self, nombre ):

		self.__init__( self.conexion, nombre )

	def getCampos( self ):
		
		sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = \'"+self.nombre+"\' AND table_schema = \'"+CONFIG["DATABASE"]+"\'"
		self.cursor.execute(sql)
		campos = self.cursor.fetchall()
		return campos

	def insertar( self, dictCampos ):

		sql = "INSERT INTO "+self.nombre+" ("

		c = 0

		# Indicar en la sentencia los campos a mostrar
		campos = dictCampos.keys()
		for campo in campos :

			c = c + 1
			
			if c != len(campos) :

				sql = sql+str(campo).encode('utf-8')+", "
			else :
				sql = sql+str(campo).encode('utf-8')

		sql = sql+") VALUES ("

		c = 0
		valores = dictCampos.values()
		for valor in valores :

			c = c + 1
			
			if c != len(valores) :

				sql = sql+str(valor).encode('utf-8')+", "
			else :

				sql = sql+str(valor).encode('utf-8')

		sql = sql+")"

		if CONFIG["DEBUG_SQL"]:
			pprint("------------------------------------------------------------------------------")
			pprint(sql)
			pprint("------------------------------------------------------------------------------")

		self.cursor.execute(sql)
		self.conexion.commit()

	def obtenerTuplas( self, campos = False ):

		sql = "SELECT "

		if campos :

			c = 0

			# Indicar en la sentencia los campos a mostrar

			for campo in campos :

				c = c + 1
				
				if c != len(campos) :

					sql = sql+campo+", "
				else :
					sql = sql+campo

			sql = sql+" FROM "+self.nombre

		else :

			sql = sql+"* FROM "+self.nombre

		if CONFIG["DEBUG_SQL"]:
			pprint("-----------------------------------------------------------------------------")
			pprint(sql)
			pprint("-----------------------------------------------------------------------------")

		self.cursor.execute(sql)
		tuplas=self.cursor.fetchall()
		return tuplas

	def busquedaTuplas( self, whereCampo, whereValor, campos = False ):
		
		sql = "SELECT "

		if campos :

			c = 0

			# Indicar en la sentencia los campos a mostrar

			for campo in campos :

				c = c + 1
				
				if c != len(campos) :

					sql = sql+campo+", "
				else :
					sql = sql+campo

			sql = sql+" FROM "+self.nombre+" WHERE "+str(whereCampo)+"="+str(whereValor)

		else :

			sql = sql+"* FROM "+self.nombre+" WHERE "+str(whereCampo)+"="+str(whereValor)

		if CONFIG["DEBUG_SQL"]:
			pprint("------------------------------------------------------------------------------")
			pprint(sql)
			pprint("------------------------------------------------------------------------------")

		self.cursor.execute(sql)
		tuplas = self.cursor.fetchall()
		return tuplas

	def modificar( self, dictCampos, whereCampo, whereValor ):

		sql = "UPDATE "+self.nombre+" SET "

		for campo in range(1,len(dictCampos)+1):

			if campo < len(dictCampos):
				try :

					sql = sql + dictCampos[campo]["nombre"]+"="+str(dictCampos[campo]["valor"]).encode('utf-8')+", "

				except Exception:
					sql = sql + dictCampos[campo]["nombre"]+"="+dictCampos[campo]["valor"]+", "
			else :
				try :

					sql = sql + dictCampos[campo]["nombre"]+"="+str(dictCampos[campo]["valor"]).encode('utf-8')

				except Exception:
					sql = sql + dictCampos[campo]["nombre"]+"="+dictCampos[campo]["valor"]

		sql = sql + " WHERE "+whereCampo+"="+str(whereValor)

		if CONFIG["DEBUG_SQL"]:
			pprint("------------------------------------------------------------------------------")
			pprint(sql)
			pprint("------------------------------------------------------------------------------")
			
		self.cursor.execute(sql)
		self.conexion.commit()

	def borrar( self, campo, valor ):

		sql = "DELETE FROM "+self.nombre+" WHERE "+campo+"="+valor

		if CONFIG["DEBUG_SQL"]:
			pprint("------------------------------------------------------------------------------")
			pprint(sql)
			pprint("------------------------------------------------------------------------------")

		self.cursor.execute(sql)
		self.conexion.commit()

	def advancedSQL( self, select, tables, where ):

		sql = "SELECT "

		c = 0

		for campo in select :

			c = c + 1
			
			if c != len(select) :

				sql = sql+campo+", "
			else :
				sql = sql+campo

		sql = sql + " FROM "

		c = 0

		for table in tables :

			c = c + 1
			
			if c != len(tables) :

				sql = sql+table+", "
			else :
				sql = sql+table

		sql = sql + " WHERE "

		c = 0

		for condition in where :

			c = c + 1
			
			if where[condition].has_key("campo"):

				if c != len(where) :
					sql = sql+where[condition]["campo"]+where[condition]["operator"]+str(where[condition]["value"])+" and "
				else :
					sql = sql+where[condition]["campo"]+where[condition]["operator"]+str(where[condition]["value"])
			else:

				if c != len(where) :
					sql = sql+condition+where[condition]["operator"]+str(where[condition]["value"])+" and "
				else :
					sql = sql+condition+where[condition]["operator"]+str(where[condition]["value"])

		if CONFIG["DEBUG_SQL"]:
			pprint("------------------------------------------------------------------------------")
			pprint(sql)
			pprint("------------------------------------------------------------------------------")

		self.cursor.execute(sql)
		tuplas = self.cursor.fetchall()

		return tuplas

	def executeSQL( self, sql):

		if CONFIG["DEBUG_SQL"]:
			pprint("------------------------------------------------------------------------------")
			pprint(sql)
			pprint("------------------------------------------------------------------------------")

		self.cursor.execute(sql)
		tuplas = self.cursor.fetchall()

		return tuplas

	def cerrar( self ):

		self.conexion.close()

#----------------------------------------------------------------------------------------

def exec_sql_file( cursor, sql_file ):

    print "\n[INFO] Ejecutando SQL script file: '%s'" % (sql_file)
    statement = ""

    for line in open(sql_file):

        if re.match(r'--', line):  # Elimina comentarios
        	continue
        if not re.search(r'[^-;]+;', line):  # mantener añadiendo líneas que no terminan en ';'
            statement = statement + line
        else:  
            statement = statement + line
            try:
                cursor.execute(statement)
            except (OperationalError, ProgrammingError) as e:
                print "\n[WARN] MySQLError durante ejecucion de la linea \n\tArgs: '%s'" % (str(e.args))

            statement = ""

database = { }

database["exec_sql_file"] = exec_sql_file