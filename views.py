# views.py (CON BAJA Y ESTRUCTURA DE MODIFICACIÓN FUNCIONAL)
from tkinter import Frame, Label, Button, ttk, messagebox, LEFT, RIGHT, END, CENTER, FLAT, Y, BOTH, NO, YES, GROOVE, W, N, E, S
import mysql.connector 
# Importar módulos y constantes
from constants import *
# Se IMPORTAN los diálogos necesarios para las vistas restantes
from dialogs import AddInventoryDialog, AddFinanceDialog, AddMarketingCampaignDialog, AddEmployeeDialog

# =================================================================
# LÓGICA DE UTILIDAD
# =================================================================

def get_selected_item_id(tree):
    """Obtiene el ID del elemento seleccionado en un Treeview."""
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Selección Requerida", "Por favor, selecciona un registro de la tabla primero.")
        return None
    
    # El primer valor en el Treeview siempre debe ser el ID
    item_values = tree.item(selected_item, 'values')
    if item_values:
        return item_values[0]
    return None

# =================================================================
# VISTAS PRINCIPALES (Inventario)
# =================================================================

class InventoryManagementView:
    """Vista para la gestión de inventario, con diseño de botones unificado."""
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1) # Fila de la tabla central
        self.home_app = home_app 

        # Título de la vista
        header_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        header_frame.grid(row=0, column=0, sticky="w", pady=(10, 10))
        Label(header_frame, text="📦 Gestión de Inventario", font=FONT_HEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).pack(side=LEFT)

        # Contenedor de Acciones (Diseño UNIFICADO)
        actions_frame = Frame(self.frame, bg=COLOR_CARD_BG, padx=20, pady=10, relief=GROOVE, bd=1)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(10, 20))
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1) # 3 Columnas

        # Botones de Inventario (UNIFICADO)
        Button(actions_frame, text="➕ Nuevo Producto", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.add_product).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
               
        Button(actions_frame, text="➖ Baja Producto", bg=COLOR_ERROR, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.baja_producto).grid(row=0, column=1, padx=5, pady=5, sticky="ew") # CAMBIADO

        Button(actions_frame, text="⚙️ Modificar Producto", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.modificar_producto).grid(row=0, column=2, padx=5, pady=5, sticky="ew") # CAMBIADO


        # Configuración del Treeview (Tabla) - En row=2
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Producto", "Stock"), show='headings')
        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Producto", text="Nombre del Producto")
        self.tree.heading("Stock", text="Stock")
        
        self.tree.column("ID", width=50, stretch=NO, anchor=CENTER)
        self.tree.column("Producto", width=250, stretch=YES)
        self.tree.column("Stock", width=100, stretch=NO, anchor=CENTER)
        
        self.load_inventory_data()

    def load_inventory_data(self):
        """Carga datos de la tabla 'inventory' en la Treeview (Consulta REAL)."""
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
            self.home_app.content_area.show_inventory_list() 

        AddInventoryDialog(self.frame, self.home_app.db_conn, refresh)

    # NUEVO: Lógica de Baja de Producto
    def baja_producto(self):
        producto_id = get_selected_item_id(self.tree)
        if not producto_id:
            return
        
        if messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de que deseas eliminar el Producto con ID {producto_id}?"):
            conn = self.home_app.db_conn
            if conn and conn.is_connected():
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM inventory WHERE ID = %s", (producto_id,))
                    conn.commit()
                    messagebox.showinfo("Baja Exitosa", "Producto eliminado correctamente.")
                    self.home_app.content_area.show_inventory_list() # Refresca la vista
                except mysql.connector.Error as err:
                    messagebox.showerror("Error de BD", f"Error al eliminar el producto: {err}")
                finally:
                    cursor.close()

    # NUEVO: Lógica de Modificación de Producto (Estructura base)
    def modificar_producto(self):
        producto_id = get_selected_item_id(self.tree)
        if not producto_id:
            return

        selected_item = self.tree.focus()
        data = self.tree.item(selected_item, 'values')
        
        # Aquí se abriría el diálogo de Modificación real
        messagebox.showinfo("Modificar Producto", f"Preparado para modificar el Producto con ID {producto_id}.\nDatos actuales: {data}")
        # ModificarInventoryDialog(self.frame, self.home_app.db_conn, refresh, data) # Esto sería el paso futuro

# =================================================================
# MÓDULOS DE GESTIÓN RESTANTES (Finanzas, Marketing, RRHH) 
# =================================================================

class FinanzasView:
    """Vista para el módulo de Finanzas, con tabla de transacciones central."""
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1) # Fila de la tabla central
        self.home_app = home_app 
        
        # Título de la vista
        header_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        header_frame.grid(row=0, column=0, sticky="w", pady=(10, 10))
        Label(header_frame, text="💰 Gestión de Finanzas", font=FONT_HEADING,
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).pack(side=LEFT)
              
        # Contenedor de Acciones (Diseño UNIFICADO)
        actions_frame = Frame(self.frame, bg=COLOR_CARD_BG, padx=20, pady=10, relief=GROOVE, bd=1)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(10, 20))
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1) # Ajustado a 3 columnas

        # Botones de Finanzas
        Button(actions_frame, text="➕ Registrar Ingreso", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.alta_ingreso).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        Button(actions_frame, text="➖ Baja Ingreso/Gasto", bg=COLOR_ERROR, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.baja_ingreso_gasto).grid(row=0, column=1, padx=5, pady=5, sticky="ew") # CAMBIADO
        
        Button(actions_frame, text="⚙️ Modificar Transacción", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.modificar_transaccion).grid(row=0, column=2, padx=5, pady=5, sticky="ew") # CAMBIADO

        # Área de Visualización (Tabla/Treeview) - MOVIDO A row=2
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Tipo", "Monto", "Fecha"), show='headings')
        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Definición de encabezados y anchos de columna
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Monto", text="Monto")
        self.tree.heading("Fecha", text="Fecha")
        
        self.tree.column("ID", width=50, stretch=NO, anchor=CENTER)
        self.tree.column("Tipo", width=100, stretch=YES, anchor=CENTER)
        self.tree.column("Monto", width=100, stretch=YES, anchor=CENTER)
        self.tree.column("Fecha", width=100, stretch=YES, anchor=CENTER)
        
        self.load_finance_data()

    def load_finance_data(self):
        """Carga datos de transacciones de Finanzas (Consulta REAL)."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id, type, amount, date FROM financial_movements")
                data = cursor.fetchall()
                
                for item in data:
                    self.tree.insert('', END, values=item) 

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al cargar finanzas: {err}\nAsegúrate de que la tabla 'financial_movements' exista y tenga las columnas id, type, amount, date.")
            finally:
                cursor.close()

    # Métodos de Lógica
    def alta_ingreso(self):
        """Abre un diálogo para registrar un nuevo ingreso/gasto."""
        def refresh_finance_view():
            self.home_app.content_area.show_finance_list() 
        
        AddFinanceDialog(self.frame, self.home_app.db_conn, refresh_finance_view)

    # NUEVO: Lógica de Baja de Ingreso/Gasto
    def baja_ingreso_gasto(self):
        transaccion_id = get_selected_item_id(self.tree)
        if not transaccion_id:
            return
        
        if messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de que deseas eliminar la Transacción con ID {transaccion_id}?"):
            conn = self.home_app.db_conn
            if conn and conn.is_connected():
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM financial_movements WHERE id = %s", (transaccion_id,))
                    conn.commit()
                    messagebox.showinfo("Baja Exitosa", "Transacción eliminada correctamente.")
                    self.home_app.content_area.show_finance_list() # Refresca la vista
                except mysql.connector.Error as err:
                    messagebox.showerror("Error de BD", f"Error al eliminar la transacción: {err}")
                finally:
                    cursor.close()
    
    # NUEVO: Lógica de Modificación de Transacción (Estructura base)
    def modificar_transaccion(self):
        transaccion_id = get_selected_item_id(self.tree)
        if not transaccion_id:
            return

        selected_item = self.tree.focus()
        data = self.tree.item(selected_item, 'values')
        
        # Aquí se abriría el diálogo de Modificación real
        messagebox.showinfo("Modificar Transacción", f"Preparado para modificar la Transacción con ID {transaccion_id}.\nDatos actuales: {data}")


class MarketingView:
    """Vista para el módulo de Marketing, con tabla de campañas central."""
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1) # Fila de la tabla central
        self.home_app = home_app 
        
        header_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        header_frame.grid(row=0, column=0, sticky="w", pady=(10, 10))
        Label(header_frame, text="📈 Gestión de Marketing", font=FONT_HEADING,
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).pack(side=LEFT)
              
        # Contenedor de Acciones (Diseño UNIFICADO)
        actions_frame = Frame(self.frame, bg=COLOR_CARD_BG, padx=20, pady=10, relief=GROOVE, bd=1)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(10, 20))
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1) # Ajustado a 3 columnas

        # Botones de Marketing 
        Button(actions_frame, text="➕ Alta Campaña", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.alta_campana).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        Button(actions_frame, text="➖ Baja Campaña", bg=COLOR_ERROR, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.baja_campana).grid(row=0, column=1, padx=5, pady=5, sticky="ew") # CAMBIADO

        Button(actions_frame, text="⚙️ Modificar Campaña", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.modificar_campana).grid(row=0, column=2, padx=5, pady=5, sticky="ew") # CAMBIADO
        
        # Área de Visualización (Tabla/Treeview) - MOVIDO A row=2
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Campaña", "Presupuesto", "Estado"), show='headings')
        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Definición de encabezados y anchos de columna
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Campaña", text="Nombre de Campaña")
        self.tree.heading("Presupuesto", text="Presupuesto")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("ID", width=50, stretch=NO, anchor=CENTER)
        self.tree.column("Campaña", width=250, stretch=YES)
        self.tree.column("Presupuesto", width=100, stretch=YES, anchor=CENTER)
        self.tree.column("Estado", width=100, stretch=YES, anchor=CENTER)

        self.load_marketing_data()

    def load_marketing_data(self):
        """Carga datos de campañas de Marketing (Consulta REAL)."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT campaign_id, name, budget, status FROM campaigns")
                data = cursor.fetchall()
                
                for item in data:
                    self.tree.insert('', END, values=item) 

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al cargar campañas: {err}\nAsegúrate de que la tabla 'campaigns' exista y tenga las columnas campaign_id, name, budget, status.")
            finally:
                cursor.close()

    # Métodos de Lógica
    def alta_campana(self):
        """Abre un diálogo para registrar una nueva campaña."""
        def refresh_marketing_view():
            self.home_app.content_area.show_marketing_list() 
        
        AddMarketingCampaignDialog(self.frame, self.home_app.db_conn, refresh_marketing_view)

    # NUEVO: Lógica de Baja de Campaña
    def baja_campana(self):
        campana_id = get_selected_item_id(self.tree)
        if not campana_id:
            return
        
        if messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de que deseas eliminar la Campaña con ID {campana_id}?"):
            conn = self.home_app.db_conn
            if conn and conn.is_connected():
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM campaigns WHERE campaign_id = %s", (campana_id,))
                    conn.commit()
                    messagebox.showinfo("Baja Exitosa", "Campaña eliminada correctamente.")
                    self.home_app.content_area.show_marketing_list() # Refresca la vista
                except mysql.connector.Error as err:
                    messagebox.showerror("Error de BD", f"Error al eliminar la campaña: {err}")
                finally:
                    cursor.close()

    # NUEVO: Lógica de Modificación de Campaña (Estructura base)
    def modificar_campana(self):
        campana_id = get_selected_item_id(self.tree)
        if not campana_id:
            return

        selected_item = self.tree.focus()
        data = self.tree.item(selected_item, 'values')
        
        # Aquí se abriría el diálogo de Modificación real
        messagebox.showinfo("Modificar Campaña", f"Preparado para modificar la Campaña con ID {campana_id}.\nDatos actuales: {data}")


class RRHHView:
    """Vista para el módulo de Recursos Humanos, con tabla de empleados central."""
    def __init__(self, master_frame, home_app):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=5)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1) # Fila de la tabla central
        self.home_app = home_app 
        
        header_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        header_frame.grid(row=0, column=0, sticky="w", pady=(10, 10))
        Label(header_frame, text="🧑‍💼 Gestión de Recursos Humanos", font=FONT_HEADING,
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).pack(side=LEFT)

        # Contenedor de Acciones (Diseño UNIFICADO)
        actions_frame = Frame(self.frame, bg=COLOR_CARD_BG, padx=20, pady=10, relief=GROOVE, bd=1)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(10, 20))
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1) # Ajustado a 3 columnas
        
        # Botones de RRHH
        Button(actions_frame, text="👥 Alta Empleado", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.alta_empleado).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        Button(actions_frame, text="➖ Baja Empleado", bg=COLOR_ERROR, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.baja_empleado).grid(row=0, column=1, padx=5, pady=5, sticky="ew") # CAMBIADO

        Button(actions_frame, text="⚙️ Modificar Empleado", bg=COLOR_ACCENT, 
               fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT, 
               command=self.modificar_empleado).grid(row=0, column=2, padx=5, pady=5, sticky="ew") # CAMBIADO

        # Área de Visualización (Tabla/Treeview) - MOVIDO A row=2
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Sector", "Salario"), show='headings')
        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Definición de encabezados y anchos de columna
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Nombre", text="Nombre Completo")
        self.tree.heading("Sector", text="Sector")
        self.tree.heading("Salario", text="Salario")
        
        self.tree.column("ID", width=50, stretch=NO, anchor=CENTER)
        self.tree.column("Nombre", width=200, stretch=YES)
        self.tree.column("Sector", width=100, stretch=YES, anchor=CENTER)
        self.tree.column("Salario", width=100, stretch=YES, anchor=CENTER)
        
        self.load_employee_data()

    def load_employee_data(self):
        """Carga datos de empleados de RRHH (Consulta REAL)."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # Usando CONCAT para Nombre Completo y 'position' para 'Sector'
                query = """
                SELECT 
                    employee_id, 
                    CONCAT(first_name, ' ', last_name), 
                    position, 
                    salary 
                FROM employees
                """
                cursor.execute(query)
                data = cursor.fetchall()
                
                for item in data:
                    self.tree.insert('', END, values=item) 

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al cargar empleados: {err}\nAsegúrate de que la tabla 'employees' exista y tenga las columnas correctas.")
            finally:
                cursor.close()

    # Métodos de Lógica
    def alta_empleado(self):
        """Abre un diálogo para registrar un nuevo empleado."""
        def refresh_rrhh_view():
            self.home_app.content_area.show_rrhh_list() 
        
        AddEmployeeDialog(self.frame, self.home_app.db_conn, refresh_rrhh_view)

    # NUEVO: Lógica de Baja de Empleado
    def baja_empleado(self):
        empleado_id = get_selected_item_id(self.tree)
        if not empleado_id:
            return
        
        if messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de que deseas eliminar el Empleado con ID {empleado_id}?"):
            conn = self.home_app.db_conn
            if conn and conn.is_connected():
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (empleado_id,))
                    conn.commit()
                    messagebox.showinfo("Baja Exitosa", "Empleado eliminado correctamente.")
                    self.home_app.content_area.show_rrhh_list() # Refresca la vista
                except mysql.connector.Error as err:
                    messagebox.showerror("Error de BD", f"Error al eliminar el empleado: {err}")
                finally:
                    cursor.close()

    # NUEVO: Lógica de Modificación de Empleado (Estructura base)
    def modificar_empleado(self):
        empleado_id = get_selected_item_id(self.tree)
        if not empleado_id:
            return

        selected_item = self.tree.focus()
        data = self.tree.item(selected_item, 'values')
        
        # Aquí se abriría el diálogo de Modificación real
        messagebox.showinfo("Modificar Empleado", f"Preparado para modificar el Empleado con ID {empleado_id}.\nDatos actuales: {data}")