# home_gerente.py - Versión con Separadores Verticales y Contorno Derecho
from tkinter import *
from tkinter import messagebox
from tkinter import ttk 
import sys
import os
import mysql.connector
from datetime import datetime, timedelta

# =================================================================
# CONSTANTES DE DISEÑO
# =================================================================
COLOR_ACCENT = '#57a1f8'
COLOR_BG_WHITE = '#ffffff'
COLOR_SIDEBAR = '#f0f0f0' 
COLOR_CARD_BG = '#f8f8fa' 
COLOR_NAVBAR_BG = '#e0e0e0' 
COLOR_TEXT_NORMAL = '#444444'
COLOR_TEXT_HEADING = '#333333'
COLOR_ERROR = '#e74c3c'
COLOR_BORDER_LIGHT = '#cccccc' # Color de la línea divisoria

FONT_MAIN = ('Segoe UI', 10)
FONT_HEADING = ('Segoe UI', 18, 'bold')
FONT_SUBHEADING = ('Segoe UI', 14, 'bold') 

# ... (Clases AddUserDialog y AddInventoryDialog se mantienen iguales) ...
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


# ... (Clases UserManagementView e InventoryManagementView se mantienen iguales) ...
class UserManagementView:
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5) 
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1) 
        self.home_app = home_app 
        
        header_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        Label(header_frame, text="👥 Gestión de Usuarios", font=FONT_SUBHEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(side=LEFT)
              
        Button(header_frame, text="+ Agregar Nuevo Usuario", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=('Segoe UI', 10, 'bold'), relief=FLAT,
               activebackground='#4a95e0', activeforeground=COLOR_BG_WHITE,
               command=self.open_add_user_dialog).pack(side=RIGHT)

        Label(self.frame, text=f"Listado completo de empleados activos.", font=FONT_MAIN, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.tree_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        self.tree_frame.grid(row=2, column=0, sticky="nswe")
        
        self.create_treeview_table(self.tree_frame)
        self.load_user_data()

    def create_treeview_table(self, parent_frame):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'), background='#e0e0e0', foreground=COLOR_TEXT_HEADING)
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=25)
        
        columns = ("ID", "Nombre", "Rol", "Email", "Estado")
        self.tree = ttk.Treeview(parent_frame, columns=columns, show='headings')
        
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Rol", text="Rol")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Estado", text="Estado", anchor=CENTER)

        self.tree.column("ID", width=50, anchor=CENTER, stretch=NO)
        self.tree.column("Nombre", width=150, stretch=YES)
        self.tree.column("Rol", width=100, stretch=NO)
        self.tree.column("Email", width=200, stretch=YES)
        self.tree.column("Estado", width=80, anchor=CENTER, stretch=NO)
        
        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        vsb.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        
    def load_user_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                select_query = "SELECT ID, username FROM users" 
                cursor.execute(select_query)
                users = cursor.fetchall()

                for id, username in users:
                    rol = "Gerente" if id == 1 else "Empleado" 
                    email = f"{username}@fravega.com" 
                    estado = "Activo"
                    self.tree.insert('', END, values=(id, username, rol, email, estado))
                    
            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al cargar usuarios: {err}")
            finally:
                cursor.close()
        
    def open_add_user_dialog(self):
        if not self.home_app.db_conn or not self.home_app.db_conn.is_connected():
            messagebox.showerror("Error", "No hay conexión activa a la base de datos.")
            return

        AddUserDialog(self.frame.master, self.home_app.db_conn, self.load_user_data)

class InventoryManagementView:
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5) 
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1) 
        self.home_app = home_app 
        
        header_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        Label(header_frame, text="📦 Gestión de Inventario", font=FONT_SUBHEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(side=LEFT)
              
        Button(header_frame, text="+ Agregar Producto", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=('Segoe UI', 10, 'bold'), relief=FLAT,
               activebackground='#4a95e0', activeforeground=COLOR_BG_WHITE,
               command=self.open_add_product_dialog).pack(side=RIGHT)

        Label(self.frame, text="Listado de productos y gestión de stock.", font=FONT_MAIN, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.tree_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        self.tree_frame.grid(row=2, column=0, sticky="nswe")
        
        self.create_treeview_table(self.tree_frame)
        self.load_inventory_data()

    def create_treeview_table(self, parent_frame):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'), background='#e0e0e0', foreground=COLOR_TEXT_HEADING)
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=30)
        
        columns = ("ID", "Nombre", "Stock", "Acciones")
        self.tree = ttk.Treeview(parent_frame, columns=columns, show='headings')
        
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Nombre", text="Producto")
        self.tree.heading("Stock", text="Unidades", anchor=CENTER)
        self.tree.heading("Acciones", text="Stock +/-", anchor=CENTER)

        self.tree.column("ID", width=50, anchor=CENTER, stretch=NO)
        self.tree.column("Nombre", width=250, stretch=YES)
        self.tree.column("Stock", width=100, anchor=CENTER, stretch=NO)
        self.tree.column("Acciones", width=120, anchor=CENTER, stretch=NO)
        
        self.tree.bind('<Map>', self.draw_action_buttons)
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        vsb.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

    def load_inventory_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                select_query = "SELECT ID, name, stock FROM inventory"
                cursor.execute(select_query)
                products = cursor.fetchall()

                for id, name, stock in products:
                    self.tree.insert('', END, values=(id, name, stock, '')) 
                    
            except mysql.connector.Error as err:
                Label(self.tree_frame, text=f"Error al cargar inventario: {err}", fg=COLOR_ERROR, bg=COLOR_BG_WHITE).pack(pady=20)
            finally:
                cursor.close()
        
        self.tree.after(100, self.draw_action_buttons)

    def open_add_product_dialog(self):
        if not self.home_app.db_conn or not self.home_app.db_conn.is_connected():
            messagebox.showerror("Error", "No hay conexión activa a la base de datos.")
            return
        AddInventoryDialog(self.frame.master, self.home_app.db_conn, self.load_inventory_data)

    def update_stock(self, item_id, change):
        messagebox.showinfo("Stock Actualizado", 
                            f"Producto ID {item_id}: Stock {'aumentado' if change > 0 else 'reducido'} en {abs(change)}.\n\n*Nota: Esto actualizaría la DB.*")
        self.load_inventory_data()

    def item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.selection_remove(selected_item)

    def draw_action_buttons(self, event=None):
        for widget in self.tree_frame.winfo_children():
            if isinstance(widget, Button):
                widget.destroy()

        for item_id in self.tree.get_children():
            item_data = self.tree.item(item_id, 'values')
            if not item_data: continue

            product_db_id = item_data[0]
            
            x, y, width, height = self.tree.bbox(item_id, column='Acciones')
            
            btn_minus = Button(self.tree_frame, text="-", width=3, fg=COLOR_ERROR, 
                               command=lambda id=product_db_id: self.update_stock(id, -1), 
                               relief=FLAT, bg=COLOR_CARD_BG)
            self.tree.create_window(x + width*0.25, y + height/2, window=btn_minus, anchor=CENTER)

            btn_plus = Button(self.tree_frame, text="+", width=3, fg=COLOR_ACCENT, 
                              command=lambda id=product_db_id: self.update_stock(id, 1), 
                              relief=FLAT, bg=COLOR_CARD_BG)
            self.tree.create_window(x + width*0.75, y + height/2, window=btn_plus, anchor=CENTER)


# =================================================================
# CLASE PRINCIPAL DEL HOME
# =================================================================

class GerenteHome:
    def __init__(self, master, username):
        self.master = master
        master.title(f"Panel de Control | Gerente: {username}")
        master.configure(bg=COLOR_BG_WHITE)
        self.username = username
        self.current_detail_frame = None 
        
        self.db_config = {
            'host': 'localhost', 
            'user': 'root',       
            'password': '',       
            'database': 'user_db' 
        }
        self.db_conn = self.create_db_connection()
        master.state('zoomed') 

        master.grid_rowconfigure(0, weight=0) 
        master.grid_rowconfigure(1, weight=1) 
        master.grid_columnconfigure(0, weight=1)
        
        self.load_images()
        self.create_navbar()
        self.create_content_area() 
        self.show_dashboard_list() 

    def create_db_connection(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", 
                                 f"No se pudo conectar a MySQL.\nAsegúrate que XAMPP esté corriendo. Error: {err}")
            return None

    def load_images(self):
        try:
            self.fravega_logo = PhotoImage(file='Fravega.png').subsample(x=2, y=2)
        except Exception:
            self.fravega_logo = None
        try:
            self.user_icon = PhotoImage(file='user_icon.png').subsample(x=2, y=2) 
        except Exception:
            self.user_icon = None

    def create_navbar(self):
        self.navbar = Frame(self.master, height=50, bg=COLOR_NAVBAR_BG)
        self.navbar.grid(row=0, column=0, sticky="ew")
        
        self.navbar.grid_columnconfigure(0, weight=1) 
        self.navbar.grid_columnconfigure(1, weight=1) 
        self.navbar.grid_columnconfigure(2, weight=0) 

        if self.fravega_logo:
            Label(self.navbar, image=self.fravega_logo, bg=COLOR_NAVBAR_BG).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        else:
            Label(self.navbar, text="[Fravega Logo]", bg=COLOR_NAVBAR_BG, fg=COLOR_TEXT_HEADING, font=FONT_MAIN).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        Label(self.navbar, text="Gerencia | Admin", bg=COLOR_NAVBAR_BG, fg=COLOR_TEXT_HEADING, 
              font=('Segoe UI', 16, 'bold')).grid(row=0, column=1, sticky="nswe", pady=10)

        user_controls_frame = Frame(self.navbar, bg=COLOR_NAVBAR_BG)
        user_controls_frame.grid(row=0, column=2, sticky="e", padx=10)

        logout_btn = Button(user_controls_frame, text="🚪 Cerrar Sesión", bg=COLOR_NAVBAR_BG, fg=COLOR_TEXT_NORMAL, font=('Segoe UI', 10), relief=FLAT, activebackground='#d0d0d0', activeforeground=COLOR_ACCENT, command=self.logout)
        logout_btn.pack(side=RIGHT, padx=(5, 0))
        
        Label(user_controls_frame, text=self.username, bg=COLOR_NAVBAR_BG, fg=COLOR_TEXT_HEADING, 
              font=('Segoe UI', 10, 'bold')).pack(side=RIGHT, padx=(10, 5))

        if self.user_icon:
            Label(user_controls_frame, image=self.user_icon, bg=COLOR_NAVBAR_BG).pack(side=RIGHT, pady=5)
        else:
            Label(user_controls_frame, text="👤", bg=COLOR_NAVBAR_BG, fg=COLOR_TEXT_HEADING, font=('Segoe UI', 16)).pack(side=RIGHT, pady=5)

    def create_content_area(self):
        """Configura el área principal de contenido con separadores verticales y borde derecho final."""
        self.content_container = Frame(self.master, bg=COLOR_BG_WHITE)
        self.content_container.grid(row=1, column=0, sticky="nswe")
        
        self.content_container.grid_columnconfigure(0, weight=0, minsize=200) 
        self.content_container.grid_columnconfigure(1, weight=0, minsize=300) 
        self.content_container.grid_columnconfigure(2, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        # 1. Menú Principal (Sidebar) - Borde a la derecha
        self.main_menu = Frame(self.content_container, width=200, bg=COLOR_SIDEBAR, 
                               highlightbackground=COLOR_BORDER_LIGHT, highlightcolor=COLOR_BORDER_LIGHT, 
                               highlightthickness=1) 
        self.main_menu.grid(row=0, column=0, sticky="nswe") 
        self.main_menu.pack_propagate(False) 
        
        self.buttons_data = [
            ("📊 Dashboard", self.show_dashboard_list),
            ("👥 Gestión Usuarios", self.show_user_management_list),
            ("📦 Inventario", self.show_inventory_list),
            ("📝 Reportes", self.show_reports_list),
        ]
        
        for text, command in self.buttons_data:
            self.create_menu_button(text, command)

        # 2. Área de Listado (Central) - Borde a la derecha
        self.list_area = Frame(self.content_container, width=300, bg=COLOR_BG_WHITE, 
                               highlightbackground=COLOR_BORDER_LIGHT, highlightcolor=COLOR_BORDER_LIGHT, 
                               highlightthickness=1) 
        self.list_area.grid(row=0, column=1, sticky="nswe")
        self.list_area.pack_propagate(False)

        # 3. Área de Detalle (Derecha) - ¡Borde a la derecha añadido!
        self.detail_area = Frame(self.content_container, bg=COLOR_BG_WHITE,
                                 highlightbackground=COLOR_BORDER_LIGHT, highlightcolor=COLOR_BORDER_LIGHT, 
                                 highlightthickness=1) 
        self.detail_area.grid(row=0, column=2, sticky="nswe") 
        self.detail_area.grid_columnconfigure(0, weight=1)
        self.detail_area.grid_rowconfigure(0, weight=1)
        
    def create_menu_button(self, text, command):
        btn = Button(self.main_menu, text=text, bg=COLOR_SIDEBAR, fg=COLOR_TEXT_NORMAL, 
                     font=FONT_MAIN, relief=FLAT, anchor='w', padx=20,
                     activebackground=COLOR_ACCENT, activeforeground=COLOR_BG_WHITE,
                     command=command)
        btn.pack(fill='x', ipady=10, pady=(10, 1)) 
        
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#e0e0e0'))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_SIDEBAR))

    def switch_content_frame(self, new_frame_func):
        if self.current_detail_frame is not None:
            self.current_detail_frame.destroy()
            
        new_frame_func()

    def clear_list_area(self):
        for widget in self.list_area.winfo_children():
            widget.destroy()

    # =================================================================
    # VISTAS DE NAVEGACIÓN (LISTADO)
    # =================================================================

    def show_dashboard_list(self):
        self.clear_list_area()
        
        header_list_frame = Frame(self.list_area, bg=COLOR_BG_WHITE, padx=10, pady=5)
        header_list_frame.pack(fill='x')
        
        Label(header_list_frame, text="Métricas Rápidas", 
              font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=0, anchor='w') 
        
        Label(self.list_area, text="[ÁREA DE CARDS VACÍA]\nAgrega aquí tus métricas clave.", 
              font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=20, padx=5)

        self._create_dashboard_detail("Vista General del Sistema")

    def show_user_management_list(self):
        self.clear_list_area()
        
        header_list_frame = Frame(self.list_area, bg=COLOR_BG_WHITE, padx=10, pady=5)
        header_list_frame.pack(fill='x')
        Label(header_list_frame, text="Usuarios Recientes", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=0, anchor='w')

        Label(self.list_area, text="Ver la lista completa en el área de 'Gestión de Usuarios'.", font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=20, padx=5)
            
        self.show_detail_user_management()

    def show_inventory_list(self):
        self.clear_list_area()
        
        header_list_frame = Frame(self.list_area, bg=COLOR_BG_WHITE, padx=10, pady=5)
        header_list_frame.pack(fill='x')
        Label(header_list_frame, text="Alertas de Stock", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=0, anchor='w')
        
        items = []
        if not items:
            Label(self.list_area, text="No hay alertas de inventario.", font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=20, padx=5)

        for name, stock, note in items:
            self.create_list_card(name, stock, note, lambda n=name: self._create_default_detail("Inventario", n))

        self.show_detail_inventory_management()

    def show_reports_list(self):
        self.clear_list_area()
        
        header_list_frame = Frame(self.list_area, bg=COLOR_BG_WHITE, padx=10, pady=5)
        header_list_frame.pack(fill='x')
        Label(header_list_frame, text="Archivos Recientes", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=0, anchor='w')
        
        items = []
        if not items:
            Label(self.list_area, text="No hay reportes disponibles.", font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=20, padx=5)

        for title, date, action in items:
            self.create_list_card(title, date, action, lambda t=title: self._create_default_detail("Reportes", t))

        self._create_default_detail("Reportes", "Vista de Reportes Generales")

    def create_list_card(self, title, subtitle, detail, command_func):
        card = Frame(self.list_area, bg=COLOR_CARD_BG, padx=15, pady=10, relief=FLAT, bd=0)
        card.pack(fill='x', pady=5, padx=5)

        Label(card, text=title, font=('Segoe UI', 10, 'bold'), bg=COLOR_CARD_BG, fg=COLOR_TEXT_HEADING, anchor='w').pack(fill='x')
        Label(card, text=subtitle, font=('Segoe UI', 9), bg=COLOR_CARD_BG, fg=COLOR_TEXT_NORMAL, anchor='w').pack(fill='x')
        Label(card, text=detail, font=('Segoe UI', 8), bg=COLOR_CARD_BG, fg=COLOR_TEXT_NORMAL, anchor='w').pack(fill='x')

        card.bind("<Button-1>", lambda e: command_func())
        for widget in card.winfo_children():
            widget.bind("<Button-1>", lambda e: command_func())
        
        card.bind("<Enter>", lambda e, f=card: f.config(bg='#e0e0e0'))
        card.bind("<Leave>", lambda e, f=card: f.config(bg=COLOR_CARD_BG))


    # =================================================================
    # VISTAS DE DETALLE (DERECHA)
    # =================================================================

    def show_detail_user_management(self):
        self.switch_content_frame(lambda: UserManagementView(self.detail_area, self))
        
    def show_detail_inventory_management(self):
        self.switch_content_frame(lambda: InventoryManagementView(self.detail_area, self))

    def _create_dashboard_detail(self, title):
        self.current_detail_frame = Frame(self.detail_area, bg=COLOR_BG_WHITE, padx=30, pady=5) 
        self.current_detail_frame.grid(row=0, column=0, sticky="nswe")
        self.current_detail_frame.grid_columnconfigure(0, weight=1)
        self.current_detail_frame.grid_rowconfigure(1, weight=1)

        Label(self.current_detail_frame, text=f"Dashboard: {title}", 
              font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).grid(row=0, column=0, sticky="w", pady=(0, 10))

        placeholder = Label(self.current_detail_frame, 
                            text="ÁREA DE TRABAJO DEL DASHBOARD\n\nAquí debes agregar los GRÁFICOS y MÉTICAS que necesita el Gerente (Ventas, Stock, etc.).", 
                            font=('Segoe UI', 12, 'italic'), bg=COLOR_CARD_BG, fg=COLOR_TEXT_NORMAL,
                            height=15, relief=GROOVE)
        placeholder.grid(row=1, column=0, sticky="nswe", padx=10, pady=20)
        
        
    def _create_default_detail(self, module, title):
        self.current_detail_frame = Frame(self.detail_area, bg=COLOR_BG_WHITE, padx=30, pady=5) 
        self.current_detail_frame.grid(row=0, column=0, sticky="nswe")
        self.current_detail_frame.grid_columnconfigure(0, weight=1)
        
        Label(self.current_detail_frame, text=f"{module}: {title}", 
              font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=(0, 20), anchor='w')

        Label(self.current_detail_frame, text=f"Área de Detalle para {module}. Aquí se muestra la información específica de '{title}' y la funcionalidad de edición.", justify=LEFT,
              font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=10, anchor='w')

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que quieres cerrar la sesión?"):
            print("LOGOUT_COMPLETE") 
            self.master.destroy()
            sys.exit(0) 

# =================================================================
# INICIO DE LA APLICACIÓN
# =================================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        admin_username = sys.argv[1]
    else:
        admin_username = "GerenteDefault" 
        
    root = Tk()
    app = GerenteHome(root, admin_username)
    root.mainloop()