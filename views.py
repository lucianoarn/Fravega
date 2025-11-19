# views.py
from tkinter import Frame, Label, Button, ttk, messagebox, LEFT, RIGHT, END, CENTER, FLAT, Y, BOTH, NO, YES, GROOVE, W, N, E, S
import mysql.connector # Necesario para la conexión a la base de datos

# Importar módulos y constantes
from constants import *
# Se asume que estos diálogos existen en dialogs.py (aunque solo se mostró el contenido de los dos primeros)
from dialogs import AddUserDialog, AddInventoryDialog, AddFinanceDialog, AddMarketingCampaignDialog, AddEmployeeDialog

# =================================================================
# VISTAS PRINCIPALES (Asumiendo estructura básica)
# =================================================================

class UserManagementView:
    """Vista para la gestión de usuarios."""
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.home_app = home_app 

        Label(self.frame, text="👥 Gestión de Usuarios", font=FONT_HEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).grid(row=0, column=0, sticky="w", pady=(10, 10))

        # Botón para añadir usuario
        Button(self.frame, text="➕ Nuevo Usuario", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.add_user).grid(row=0, column=0, sticky="e", padx=10)

        # Configuración del Treeview (Tabla)
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Usuario", "Sector"), show='headings')
        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Definición de encabezados
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Sector", text="Sector")
        
        # Definición de anchos de columna
        self.tree.column("ID", width=50, stretch=NO, anchor=CENTER)
        self.tree.column("Usuario", width=200, stretch=YES)
        self.tree.column("Sector", width=100, stretch=YES)
        
        self.load_user_data()

    def load_user_data(self):
        """Carga datos de la tabla 'users'."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # Consulta a la tabla users
                cursor.execute("SELECT ID, username, sector_id FROM users")
                data = cursor.fetchall()
                
                for item in data:
                    user_id, username, sector_id = item
                    # Simplificación: muestra el ID del sector o N/A
                    self.tree.insert('', END, values=(user_id, username, f"Sector {sector_id}" if sector_id else "N/A")) 

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al cargar usuarios: {err}")
            finally:
                cursor.close()

    def add_user(self):
        """Abre el diálogo para agregar un nuevo usuario."""
        def refresh():
            self.load_user_data()
            self.home_app.content_area.show_user_management_list() 

        AddUserDialog(self.frame, self.home_app.db_conn, refresh)

class InventoryManagementView:
    """Vista para la gestión de inventario, incluyendo carga de datos de BD."""
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.home_app = home_app 

        Label(self.frame, text="📦 Gestión de Inventario", font=FONT_HEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).grid(row=0, column=0, sticky="w", pady=(10, 10))

        # Contenedor de Acciones
        actions_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        Button(actions_frame, text="➕ Nuevo Producto", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.add_product).pack(side=LEFT, padx=5)

        # Configuración del Treeview (Tabla)
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Producto", "Stock"), show='headings')
        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Definición de encabezados y anchos
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Producto", text="Nombre del Producto")
        self.tree.heading("Stock", text="Stock")
        
        self.tree.column("ID", width=50, stretch=NO, anchor=CENTER)
        self.tree.column("Producto", width=250, stretch=YES)
        self.tree.column("Stock", width=100, stretch=NO, anchor=CENTER)
        
        self.load_inventory_data()

    def load_inventory_data(self):
        """Carga datos de la tabla 'inventory' en la Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # Consulta de la tabla inventory
                cursor.execute("SELECT ID, name, stock FROM inventory")
                data = cursor.fetchall()
                
                for item in data:
                    product_id, name, stock = item
                    self.tree.insert('', END, values=(product_id, name, stock)) 

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al cargar inventario: {err}\nAsegúrate de tener la tabla 'inventory' con columnas ID, name y stock.")
            finally:
                cursor.close()
                
    def add_product(self):
        """Abre el diálogo para agregar un nuevo producto."""
        def refresh():
            self.load_inventory_data()
            self.home_app.content_area.show_inventory_list() 

        AddInventoryDialog(self.frame, self.home_app.db_conn, refresh)

# =================================================================
# NUEVOS MÓDULOS INTEGRADOS (Finanzas, Marketing, RRHH) - Versión Mejorada
# =================================================================

class FinanzasView:
    """Vista para el módulo de Finanzas, adaptada al diseño Fravega."""
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.home_app = home_app # Referencia a GerenteHome
        
        # Título de la vista
        header_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        Label(header_frame, text="💰 Gestión de Finanzas", font=FONT_HEADING,
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).pack(side=LEFT)
              
        # Contenedor de Acciones (Botones de Alta/Baja/Modificar/Ver)
        actions_frame = Frame(self.frame, bg=COLOR_CARD_BG, padx=20, pady=10, relief=GROOVE, bd=1)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(10, 20))
        actions_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Botones de Finanzas
        Button(actions_frame, text="➕ Registrar Ingreso", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.alta_ingreso).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        Button(actions_frame, text="➖ Baja Ingreso/Gasto", bg=COLOR_ERROR, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.baja_ingreso_gasto).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        Button(actions_frame, text="📊 Ver Reportes", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.ver_reportes).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        Button(actions_frame, text="📈 Planificación", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.planificacion).grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # Área de Visualización 
        self.content_container = Frame(self.frame, bg=COLOR_BG_WHITE)
        self.content_container.grid(row=2, column=0, sticky="nsew")

        Label(self.content_container, text="[Aquí se mostrarán las Tablas y Gráficos de Finanzas]", 
              font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=50)

    # Métodos de Lógica
    def alta_ingreso(self):
        """Abre un diálogo para registrar un nuevo ingreso/gasto."""
        def refresh_finance_view():
            self.home_app.content_area.show_finance_list() 
        
        AddFinanceDialog(self.frame, self.home_app.db_conn, refresh_finance_view)

    def baja_ingreso_gasto(self):
        messagebox.showinfo("Finanzas", "Función 'Baja Ingreso/Gasto' migrada.")

    def ver_reportes(self):
        messagebox.showinfo("Finanzas", "Función 'Ver Reportes' migrada.")
        
    def planificacion(self):
        messagebox.showinfo("Finanzas", "Función 'Planificación' migrada.")


class MarketingView:
    """Vista para el módulo de Marketing, adaptada al diseño Fravega."""
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.home_app = home_app 
        
        header_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        Label(header_frame, text="📈 Gestión de Marketing", font=FONT_HEADING,
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).pack(side=LEFT)
              
        # Contenedor de Acciones (Gestión de Campañas)
        actions_frame = Frame(self.frame, bg=COLOR_CARD_BG, padx=20, pady=10, relief=GROOVE, bd=1)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(10, 20))
        actions_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Botones de Marketing
        Button(actions_frame, text="➕ Alta Campaña", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.alta_campana).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        Button(actions_frame, text="➖ Baja Campaña", bg=COLOR_ERROR, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.baja_campana).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        Button(actions_frame, text="⚙️ Modificar Campaña", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.modificar_campana).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        Button(actions_frame, text="📋 Ver Detalle", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.ver_detalle).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Área de Visualización 
        self.content_container = Frame(self.frame, bg=COLOR_BG_WHITE)
        self.content_container.grid(row=2, column=0, sticky="nsew")

        Label(self.content_container, text="[Aquí se mostrarán los Gráficos de Rendimiento de Campañas]", 
              font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=50)

    # Métodos de Lógica
    def alta_campana(self):
        """Abre un diálogo para registrar una nueva campaña."""
        def refresh_marketing_view():
            self.home_app.content_area.show_marketing_list() 
        
        AddMarketingCampaignDialog(self.frame, self.home_app.db_conn, refresh_marketing_view)

    def baja_campana(self):
        messagebox.showinfo("Marketing", "Función 'Baja Campaña' migrada.")

    def modificar_campana(self):
        messagebox.showinfo("Marketing", "Función 'Modificar Campaña' migrada.")

    def ver_detalle(self):
        messagebox.showinfo("Marketing", "Función 'Ver Detalle' migrada.")


class RRHHView:
    """Vista para el módulo de Recursos Humanos, adaptada al diseño Fravega."""
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.home_app = home_app 
        
        header_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        Label(header_frame, text="🧑‍💼 Gestión de Recursos Humanos", font=FONT_HEADING,
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).pack(side=LEFT)

        # Contenedor de Acciones (Gestión de Empleados)
        actions_frame = Frame(self.frame, bg=COLOR_CARD_BG, padx=20, pady=10, relief=GROOVE, bd=1)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(10, 20))
        actions_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Botones de RRHH
        Button(actions_frame, text="👥 Alta Empleado", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.alta_empleado).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        Button(actions_frame, text="➖ Baja Empleado", bg=COLOR_ERROR, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.baja_empleado).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        Button(actions_frame, text="⚙️ Modificar Empleado", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.modificar_empleado).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        Button(actions_frame, text="📄 Ver Empleados", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.ver_empleados).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Área de Visualización 
        self.content_container = Frame(self.frame, bg=COLOR_BG_WHITE)
        self.content_container.grid(row=2, column=0, sticky="nsew")

        Label(self.content_container, text="[Aquí se mostrarán las Tablas y el Panel de Reclutamiento]", 
              font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=50)

    # Métodos de Lógica
    def alta_empleado(self):
        """Abre un diálogo para registrar un nuevo empleado."""
        def refresh_rrhh_view():
            self.home_app.content_area.show_rrhh_list() 
        
        AddEmployeeDialog(self.frame, self.home_app.db_conn, refresh_rrhh_view)

    def baja_empleado(self):
        messagebox.showinfo("RRHH", "Función 'Baja Empleado' migrada.")

    def modificar_empleado(self):
        messagebox.showinfo("RRHH", "Función 'Modificar Empleado' migrada.")
        
    def ver_empleados(self):
        messagebox.showinfo("RRHH", "Función 'Ver Empleados' migrada.")