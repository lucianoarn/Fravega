# dialogs.py
from tkinter import Toplevel, Frame, Label, Entry, Button, messagebox, FLAT
import mysql.connector
# Importar constantes
from constants import *

class AddUserDialog(Toplevel):
    def __init__(self, master, db_conn, refresh_callback):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.title("Agregar Nuevo Usuario")
        self.geometry("400x300")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Nuevo Empleado", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        Label(main_frame, text="Usuario:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.username_entry = Entry(main_frame, font=FONT_MAIN)
        self.username_entry.pack(fill='x', pady=(0, 10))

        Label(main_frame, text="Contraseña:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.password_entry = Entry(main_frame, font=FONT_MAIN, show='*')
        self.password_entry.pack(fill='x', pady=(0, 10))
        
        Button(main_frame, text="Guardar Usuario", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.save_user).pack(pady=15)

    def save_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Debe completar ambos campos.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                check_query = "SELECT username FROM users WHERE username = %s"
                cursor.execute(check_query, (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "El nombre de usuario ya existe.")
                    return

                insert_query = "INSERT INTO users (username, password, sector_id) VALUES (%s, %s, NULL)"
                cursor.execute(insert_query, (username, password))
                conn.commit()

                messagebox.showinfo("Éxito", f"Usuario '{username}' registrado exitosamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al registrar: {err}")
            finally:
                cursor.close()
        else:
            messagebox.showerror("Error", "No hay conexión activa a la base de datos.")


class AddInventoryDialog(Toplevel):
    def __init__(self, master, db_conn, refresh_callback):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.title("Agregar Nuevo Producto")
        self.geometry("400x250")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Detalles del Producto", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        Label(main_frame, text="Nombre del Producto:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.name_entry = Entry(main_frame, font=FONT_MAIN)
        self.name_entry.pack(fill='x', pady=(0, 10))

        Label(main_frame, text="Cantidad Inicial:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.stock_entry = Entry(main_frame, font=FONT_MAIN)
        self.stock_entry.pack(fill='x', pady=(0, 10))
        
        Button(main_frame, text="Guardar Producto", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.save_product).pack(pady=15)

    def save_product(self):
        name = self.name_entry.get()
        stock_str = self.stock_entry.get()
        
        if not name or not stock_str:
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return

        try:
            stock = int(stock_str)
            if stock < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                insert_query = "INSERT INTO inventory (name, stock) VALUES (%s, %s)"
                cursor.execute(insert_query, (name, stock))
                conn.commit()

                messagebox.showinfo("Éxito", f"Producto '{name}' agregado a inventario.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al registrar producto: {err}\nAsegúrate de tener creada la tabla 'inventory' con las columnas ID, name y stock.")
            finally:
                cursor.close()
        else:
            messagebox.showerror("Error", "No hay conexión activa a la base de datos.")