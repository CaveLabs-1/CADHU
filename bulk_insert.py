#Script para cargar información a la Base de Datos desde archivos .csv
import psycopg2

#Abrir La Conexión de la Base de Datos
def abrir_db():
    #Conexiòn a la Base de Datos
    try:
        db = psycopg2.connect("host=localhost dbname=cadhu user=cadhu password=8qX8vx1P*Xpu")
        print("CONEXIÓN EXITOSA")
        return db
    except psycopg2.Error:
        print('LA CONEXIÓN A LA BASE DE DATOS NO FUE EXITOSA')

#Eliminar Información de Tabla
def eliminar_datos(cursor, tabla):
    #Ejecutar query para eliminar la información de la tabla
    try:
        query = "DELETE FROM " + tabla + ";"
        cursor.execute(query)
        print("DELETE DATA - " + tabla)
    #En caso de no poder eliminar la información de la tabla
    except psycopg2.Error:
        print("NO SE PUDO ELIMINAR LA INFORMACIÓN DE LA TABLA " + tabla)

#COPY (BULK INSERT) de un archivo .csv a una tabla
def subir_archivo(cursor, tabla, path_archivo):
    #Abrir archivo con la Información
    try:
        with open(path_archivo, 'r') as f:
            # Saltar la primera línea (Titulo Columnas)
            next(f)
            # Insertar la información en la tabla
            try:
                cursor.copy_from(f, tabla, sep=',')
                print('COPY REALIZADO EN TABLA ' + tabla)
            except psycopg2.Error as e:
                print('NO SE PUDO AGREGAR LA INFORMACIÓN A LA TABLA ' + tabla)
                print(e.pgerror)
    #En caso de no poder abrir el archivo
    except IOError:
        print('NO SE PUDO ABRIR ' + path_archivo)

#Eliminar información de todas las tablas
def borrar_informacion(db):
    print("\n")
    cursor = db.cursor()
    #Borrar información de la Base de Datos
    eliminar_datos(cursor, 'prospectos_pago')
    eliminar_datos(cursor, 'prospectos_cliente')
    eliminar_datos(cursor, 'prospectos_actividad')
    eliminar_datos(cursor, 'prospectos_prospectogrupo')
    eliminar_datos(cursor, 'grupos_grupo')
    eliminar_datos(cursor, 'cursos_curso')
    eliminar_datos(cursor, 'prospectos_empresa')
    eliminar_datos(cursor, 'prospectos_prospecto')
    eliminar_datos(cursor, 'prospectos_lugar')
    #Guardar cambios en la Base de Datos
    db.commit()

#Cargar información a las tablas
def cargar_informacion(db):
    print("\n")
    cursor = db.cursor()
    #Cargar información de los archivos a las tablas
    subir_archivo(cursor, 'prospectos_lugar', 'data/Lugar_data.csv')
    subir_archivo(cursor, 'cursos_curso', 'data/Curso_data.csv')
    subir_archivo(cursor, 'grupos_grupo', 'data/Grupo_data.csv')
    subir_archivo(cursor, 'prospectos_empresa', 'data/Empresa_data.csv')
    subir_archivo(cursor, 'prospectos_prospecto', 'data/Prospecto_data.csv')
    #Guardar cambios en la Base de Datos
    db.commit()




# Abrir Conexion
db = abrir_db()
#borrar_informacion(db)
#cargar_informacion(db)
#Cerrar Conexión
if db.close():
    print("CONEXIÓN TERMINADA")