import sqlite3

class DBManager: 
    def __init__(self, ruta):  
        self.ruta = ruta

    def consultarConSQL(self, consulta):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        self.movimientos = []
        columnas = []
        for tupla in cursor.description:
            columnas.append(tupla[0])  
        datos = cursor.fetchall()  
        for tupla in datos: 
            mov = {}
            indice = 0
            for nombre in columnas:
                mov[nombre] = tupla[indice]
                indice += 1
            self.movimientos.append(mov)
        conexion.commit()
        conexion.close()
        return self.movimientos
    
    def conectar_sqlite(self, consulta):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        conexion.close()


