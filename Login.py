from tkinter import *
from tkinter import messagebox
import mysql.connector
import subprocess

# =================================================================
# CONFIGURACIÓN Y CONEXIÓN A MYSQL
# =================================================================

DB_CONFIG = {
    'host': 'localhost', 
    'user': 'root',      
    'password': '',      
    'database': 'user_db' 
}

def create_db_connection():
    """Crea y retorna una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", 
                             f"No se pudo conectar a MySQL.\nAsegúrate que XAMPP esté corriendo. Error: {err}")
        return None

# =================================================================
# FUNCIONES DE LÓGICA Y NAVEGACIÓN
# =================================================================

# Variable global para el estado del "ojo"
show_password_login = False

def toggle_password_login():
    """Cambia el atributo 'show' del campo de entrada de login."""
    global show_password_login
    
    if show_password_login:
        code.config(show='*')
        btn_login_toggle.config(text="👁️ Mostrar")
        show_password_login = False
    else:
        code.config(show='')
        btn_login_toggle.config(text="🙈 Ocultar")
        show_password_login = True

def abrir_registro():
    """Cierra la ventana de Login y abre el script de Registro."""
    root.destroy()
    try:
        # Ejecuta el archivo 'registro.py'
        subprocess.Popen(['python', 'registro.py'])
    except FileNotFoundError:
        messagebox.showerror("Error", "Asegúrate de que 'registro.py' esté en la misma carpeta.")

def open_app_window(username):
    """Abre la ventana principal de la aplicación."""
    screen = Toplevel(root)
    screen.title("App Fravega")
    screen.geometry('925x500+300+200')
    screen.config(bg='white')

    Label(screen, text=f'Bienvenido/a {username} a Fravega', bg='#fff', 
          font=('Calibri(Body)', 30, 'bold')).pack(pady=100, expand=True)
    
    def logout():
        screen.destroy()
        root.deiconify() # Muestra la ventana de Login de nuevo
        
    Button(screen, text="Cerrar Sesión", command=logout).pack(pady=20)


def ingresar():
    """Valida las credenciales contra la base de datos."""
    username = user.get()
    password = code.get()

    if not (username and password):
        messagebox.showerror("Error", "Debes ingresar usuario y contraseña")
        return

    conn = create_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            select_query = "SELECT username FROM users WHERE username = %s AND password = %s"
            cursor.execute(select_query, (username, password))
            
            user_found = cursor.fetchone() 

            if user_found:
                messagebox.showinfo('Login', f'¡Bienvenido/a {username}!')
                root.withdraw()
                open_app_window(username)

            else:
                messagebox.showerror("Error", "Usuario o Contraseña incorrectos.")

        except mysql.connector.Error as err:
            messagebox.showerror('Error DB', f"Error al iniciar sesión: {err}")
            
        finally:
            cursor.close()
            conn.close()


# =================================================================
# CONFIGURACIÓN DE LA INTERFAZ (TKINTER)
# =================================================================
root=Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False,False)

# Funciones de PLACEHOLDER
def on_enter(e):
    e.widget.delete(0, 'end')

def on_leave_user(e):
    if user.get()=='':
        user.insert(0,'Usuario')

def on_leave_code(e):
    if code.get()=='':
        code.insert(0,'Contraseña')

# Diseño
try:
    img= PhotoImage(file='Fravega.png')
    Label(root, image=img ,bg='white').place(x=50,y=50)
except:
    pass 

frame=Frame(root, width=350, height=350, bg="white")
frame.place(x=480,y=70)

heading=Label(frame,text='Ingresar', fg='#57a1f8',bg='white', font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)

#----------------------------- USUARIO -----------------------------
user = Entry(frame,width=25,fg='black',border=0,bg="white", font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Usuario')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave_user)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

#------------------------------ CONTRASEÑA -------------------------
code = Entry(frame,width=20,fg='black',border=0,bg="white", font=('Microsoft YaHei UI Light',11), show='*')
code.place(x=30,y=150)
code.insert(0,'Contraseña')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave_code)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

# Botón "Ojo" para Contraseña
btn_login_toggle = Button(frame, text="👁️ Mostrar", fg='#57a1f8', bg='white', border=0, 
                          command=toggle_password_login)
btn_login_toggle.place(x=270, y=150)

# Botones Finales
Button(frame,width=39,pady=7,text="Ingrese",bg='#57a1f8',fg='white',border=0,command=ingresar).place(x=35 , y=204)
label=Label(frame,text="No tenes cuenta?",fg='black',bg='white', font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=270)

registro = Button(frame,width=10,text='Registrarse',border=0,bg='white',cursor='hand2',fg='#57a1f8', command=abrir_registro)
registro.place(x=215,y=270) 

root.mainloop()