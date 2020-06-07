#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__= "Alonso"
__description__ = "Aplicacion de GUI de CRUD de de datos de usuarios que se conecta una base de datos en sqlite3"
__version__ = "1.0.0"
__email__ = "ramonalonso_giron@ucol.mx"

from tkinter import *
from tkinter import messagebox
import sqlite3

#----------------------Funciones------------------------#
def conexionBBDD():
    miConexion = sqlite3.connect("Usuarios")
    
    miCursor =miConexion.cursor()
    try:
        miCursor.execute(""" 
                CREATE TABLE DATOSUSUARIOS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                NOMBRE_USUARIO VARCHAR(50),
                APELLIDO VARCHAR(20),
                PASSWORD VARCHAR(30) UNIQUE,
                DIRRECION VARCHAR(50),
                COMENTARIOS VARCHAR(100)
            )
        """)
        messagebox.showinfo("INFORMACION", "La BBDD sea creado con exito!")
    except:
        messagebox.showwarning("Advertencia", "La BBDD Usuarios ya esta creada!")  

def salirApp():
    valor = messagebox.askquestion("Salir", "Desea salir de la app?")
    
    if(valor=="yes"):
        root.destroy()

def limpiarCampos():
    miNombre.set("")
    miId.set("")
    miDirrecion.set("")
    miPass.set("")
    miApellido.set("")
    textoComentario.delete(1.0, END)

def crearDatos():
    nombre_string = miNombre.get()
    apellido_string = miApellido.get()
    pass_string = miPass.get()
    dirrec_string = miDirrecion.get()
    texto_string = textoComentario.get("1.0", END)
    
    datosUser = [nombre_string, apellido_string, pass_string, dirrec_string, texto_string]
    
    miConexion =sqlite3.connect("Usuarios")
    
    miCursor = miConexion.cursor()
    if (len(nombre_string) is not 0 and len(apellido_string) is not 0 and len(pass_string) is not 0 and len(dirrec_string) is not 0  ):
        try:
            miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES (NULL,?,?,?,?,?)", datosUser)        
            miConexion.commit()
            messagebox.showinfo("BBDD", "La informacion ha sido agregada la BD")
        except:
            messagebox.showwarning("BBDD", "Por favor introduzca otra contraseña :D")
    else:
        messagebox.showwarning("BBDD", "Por favor llene todos los recuadros menos el de ID")

def leerDatos():
    miConexion = sqlite3.connect("Usuarios")
    
    miCursor = miConexion.cursor()
    
    miCursor.execute("select * from datosusuarios where ID=" + miId.get())
    
    usuario = miCursor.fetchall()

    for i in usuario:
        miId.set(i[0])
        miNombre.set(i[1])
        miApellido.set(i[2])
        miPass.set(i[3])
        miDirrecion.set(i[4])
        textoComentario.insert("1.0", i[5])
        
    miConexion.commit()

def actualizar():

    miConexion =sqlite3.connect("Usuarios")
    
    miCursor = miConexion.cursor()
    
    datosUser = [miNombre.get(), miApellido.get(), miPass.get(), miDirrecion.get(), textoComentario.get("1.0", END)]
    
    try:
        miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO=?, APELLIDO=?, PASSWORD=?, DIRRECION=?, COMENTARIOS=?" +
         "WHERE ID=" + miId.get(), (datosUser))
        
        """miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO='" + miNombre.get() +  
            "', APELLIDO='" + miApellido.get() + 
            "', PASSWORD='" + miPass.get() + 
            "', DIRRECION='" + miDirrecion.get() + 
            "', COMENTARIOS='" + textoComentario.get("1.0", END) + 
            "'WHERE ID=" + miId.get()
        )"""
        miConexion.commit()
        messagebox.showinfo("BBDD", "La informacion ha sido actualizada con exito")
    except:
        messagebox.showwarning("BBDD", "Por favor ingrese otra contraseña")

def borrarRegistro():

    miConexion =sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()
    
    try:
        miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID=" + miId.get())
        miConexion.commit()
        messagebox.showinfo("BBDD", "Ya se ha borrado el registro")
    except:
        messagebox.showwarning("BBDD", "NO se puede borrar ese registro!")

def buttonAyuda():
    messagebox.showinfo("Information", "Utilize el campo ID solo para hacer consultas sobre un registro o borrar un registro")

def buttonAcerca():
    messagebox.showinfo("Information", """Aplicacion de GUI de CRUD de de datos de usuarios
    que se conecta una base de datos en sqlite3""")

def buttonLicensia():
    messagebox.showwarning("License", "GNU licensed product")

#---------------------Menu superior--------------------#
root = Tk()

barraMenu = Menu(root)
root.config(menu=barraMenu, width=300, height=300)

bbddMenu = Menu(barraMenu, tearoff=0)
bbddMenu.add_command(label="Conectar", command=conexionBBDD)
bbddMenu.add_command(label="Salir", command=salirApp)

borrarMenu = Menu(barraMenu, tearoff=0)
borrarMenu.add_command(label="Borrar campos", command=limpiarCampos)

crudMenu = Menu(barraMenu, tearoff=0)
crudMenu.add_command(label="Crear", command=crearDatos)
crudMenu.add_command(label="Leer", command=leerDatos)
crudMenu.add_command(label="Actualizar", command=actualizar)
crudMenu.add_command(label="Borrar", command=borrarRegistro)

ayudaMenu =Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="Licencia", command=buttonLicensia)
ayudaMenu.add_command(label="Acerca de...", command=buttonAcerca)
ayudaMenu.add_command(label="Ayuda", command=buttonAyuda)

barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
barraMenu.add_cascade(label="Borrar", menu=borrarMenu)
barraMenu.add_cascade(label="CRUD", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

#--------------------Campos O Entrys-------------------------------#
miFrame = Frame(root)
miFrame.pack()

#varibles
miId= StringVar()
miNombre = StringVar()
miApellido = StringVar()
miPass = StringVar()
miDirrecion = StringVar()

cuadroId = Entry(miFrame, textvariable=miId)
cuadroId.grid(row=0, column=1, padx=10, pady=10)

cuadroNombre = Entry(miFrame, textvariable=miNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=10)
cuadroNombre.config(fg="red", justify="right")

cuadroApellido = Entry(miFrame, textvariable=miApellido)
cuadroApellido.grid(row=2, column=1, padx=10, pady=10)

cuadroPass = Entry(miFrame, textvariable=miPass)
cuadroPass.grid(row=3, column=1, padx=10, pady=10)
cuadroPass.config(show="*")

cuadroDic= Entry(miFrame, textvariable=miDirrecion)
cuadroDic.grid(row=4, column=1, padx=10, pady=10)

textoComentario = Text(miFrame, width=16, height=5)
textoComentario.grid(row=5, column=1, padx=10, pady=10)
scrollVert = Scrollbar(miFrame, command=textoComentario.yview)
scrollVert.grid(row=5, column=2, sticky="nsew")

textoComentario.config(yscrollcommand=scrollVert.set)

#----------------------Labels---------------------------------#
idLabel = Label(miFrame, text="ID:")
idLabel.grid(row=0, column=0 ,sticky="e", padx=10, pady=10)

nombreLabel = Label(miFrame, text="Nombre:")
nombreLabel.grid(row=1, column=0 ,sticky="e", padx=10, pady=10)

apellidoLabel = Label(miFrame, text="Apellido:")
apellidoLabel.grid(row=2, column=0 ,sticky="e", padx=10, pady=10)

passLabel = Label(miFrame, text="Password:")
passLabel.grid(row=3, column=0 ,sticky="e", padx=10, pady=10)

dirrecLabel = Label(miFrame, text="Dirreccion:")
dirrecLabel.grid(row=4, column=0 ,sticky="e", padx=10, pady=10)

comenLabel = Label(miFrame, text="Comentarios:")
comenLabel.grid(row=5, column=0 ,sticky="e", padx=10, pady=10)

#--------------------------Botones inferiores-------------------#
miFrame2 = Frame(root)
miFrame2.pack()

botonCrear = Button(miFrame2, text="Create", command=crearDatos)
botonCrear.grid(row=1, column=0, sticky="e", padx=10, pady=10)

botonLeer = Button(miFrame2, text="Read", command=leerDatos)
botonLeer.grid(row=1, column=1, sticky="e", padx=10, pady=10)

botonActualizar = Button(miFrame2, text="Update", command=actualizar)
botonActualizar.grid(row=1, column=2, sticky="e", padx=10, pady=10)

botonBorrar = Button(miFrame2, text="Delete", command=borrarRegistro)
botonBorrar.grid(row=1, column=3, sticky="e", padx=10, pady=10)

root.mainloop()
