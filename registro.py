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

# Variables globales para el estado del "ojo"
show_password_code = False
show_password_confirm = False

show_password_code = False
show_password_confirm = False

def toggle_password(entry_field, button, is_confirm=False):
    """Cambia el atributo 'show' del campo de entrada y el texto del botón."""
    
    # 1. Declarar las variables globales al inicio
    global show_password_code, show_password_confirm
    
    # 2. Determinar el estado actual directamente desde la variable global
    if is_confirm:
        current_state = show_password_confirm
    else:
        current_state = show_password_code
        
    # 3. Aplicar el cambio de estado
    if current_state:
        # Si se estaba mostrando, ocultar (usar '*')
        entry_field.config(show='*')
        button.config(text="👁️ Mostrar")
        new_state = False
    else:
        # Si estaba oculto, mostrar (usar '')
        entry_field.config(show='')
        button.config(text="🙈 Ocultar")
        new_state = True

    # 4. Actualizar la variable de estado global
    if is_confirm:
        show_password_confirm = new_state
    else:
        show_password_code = new_state

def abrir_login():
    """Cierra la ventana de Registro y abre el script de Login."""
    window.destroy()
    try:
        # Ejecuta el archivo 'login.py'
        subprocess.Popen(['python', 'login.py'])
    except FileNotFoundError:
        messagebox.showerror("Error", "Asegúrate de que 'login.py' esté en la misma carpeta.")


def signup():
    """Registra un nuevo usuario en la base de datos."""
    username = user.get()
    password = code.get()
    confirm_password = conform_code.get()

    if not (username and password and confirm_password):
        messagebox.showerror('Registro', "Todos los campos son obligatorios")
        return

    if password != confirm_password:
        messagebox.showerror('Inválido', "Ambas contraseñas deben coincidir")
        return

    conn = create_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, password))
            conn.commit()
            messagebox.showinfo('Registro', 'Registro exitoso')
            
            # Limpiar campos después del registro exitoso
            user.delete(0, 'end')
            code.delete(0, 'end')
            conform_code.delete(0, 'end')

        except mysql.connector.IntegrityError:
            messagebox.showerror('Registro', "El usuario ya existe. Intenta con otro.")
            
        except mysql.connector.Error as err:
            messagebox.showerror('Error DB', f"Error al registrar: {err}")
            
        finally:
            cursor.close()
            conn.close()

# =================================================================
# CONFIGURACIÓN DE LA INTERFAZ (TKINTER)
# =================================================================

window=Tk()
window.title("SignUp")
window.geometry('925x500+300+200')
window.configure(bg='#fff')
window.resizable(False,False)
window.state('zoomed')

# Funciones de PLACEHOLDER
def on_enter(e):
    e.widget.delete(0,'end')

def on_leave_user(e):
    if user.get()=='':
        user.insert(0,'Usuario')

def on_leave_code(e):
    if code.get()=='':
        code.insert(0,'Contraseña')

def on_leave_confirm(e):
    if conform_code.get()=='':
        conform_code.insert(0,'Confirmar contraseña')

# Diseño
try:
    img = PhotoImage(file='Fravega.png')
    Label(window, image=img, border=0, bg='white').place(x=50, y=90)
except:
    pass

frame=Frame(window,width=350,height=390,bg='#fff')
frame.place(x=480, y=50)

heading=Label(frame,text='Registro', fg="#57a1f8",bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)


## ------ USUARIO ------
user = Entry(frame,width=25,fg='black', border=0,bg='white',font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Usuario')
user.bind("<FocusIn>", on_enter)
user.bind("<FocusOut>", on_leave_user)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

##------------- CONTRASEÑA -------------
code = Entry(frame,width=20,fg='black', border=0,bg='white',font=('Microsoft YaHei UI Light',11), show='*')
code.place(x=30,y=150)
code.insert(0,'Contraseña')
code.bind("<FocusIn>", on_enter)
code.bind("<FocusOut>", on_leave_code)
Frame(frame,width=295,height=2,bg='black').place(x=25, y=177)

# Botón "Ojo" para Contraseña
btn_code_toggle = Button(frame, text="👁️ Mostrar", fg='#57a1f8', bg='white', border=0, 
                         command=lambda: toggle_password(code, btn_code_toggle, is_confirm=False))
btn_code_toggle.place(x=270, y=150) 


##----- CONFIRMAR CONTRASEÑA -----
conform_code = Entry(frame,width=20,fg='black', border=0,bg='white',font=('Microsoft YaHei UI Light',11), show='*')
conform_code.place(x=30,y=220)
conform_code.insert(0,'Confirmar contraseña')
conform_code.bind("<FocusIn>", on_enter)
conform_code.bind("<FocusOut>", on_leave_confirm)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)

# Botón "Ojo" para Confirmar Contraseña
btn_confirm_toggle = Button(frame, text="👁️ Mostrar", fg='#57a1f8', bg='white', border=0, 
                            command=lambda: toggle_password(conform_code, btn_confirm_toggle, is_confirm=True))
btn_confirm_toggle.place(x=270, y=220) 


##----- BOTONES FINALES -----
Button(frame,width=39,pady=7,text='Registrarse',bg='#57a1f8',fg='white',border=0, command=signup).place(x=35,y=280)

label=Label(frame,text='Ya tengo una cuenta',fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
label.place(x=90,y=340)

signin = Button(frame, width=10, text='Iniciar sesión', border=0, bg='white',cursor='hand2',fg='#57a1f8', command=abrir_login)
signin.place(x=230,y=340)
    
window.mainloop()