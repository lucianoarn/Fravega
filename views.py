# views.py
from tkinter import Frame, Label, Button, ttk, messagebox, LEFT, RIGHT, END, CENTER, FLAT, Y, BOTH, NO, YES
import mysql.connector
# Importar módulos
from constants import *
from dialogs import AddUserDialog, AddInventoryDialog

class UserManagementView:
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5) 
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1) 
        self.home_app = home_app # Referencia a GerenteHome
        
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
        self.home_app = home_app # Referencia a GerenteHome
        
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
            # Si es un botón creado por create_window, no está directamente en tree_frame. 
            # Esto es una limitación de Tkinter/ttk. Mantenemos el código original de limpieza
            # aunque los botones en create_window no se destruyan con winfo_children del frame.
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