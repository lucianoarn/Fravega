# views.py 
from tkinter import Frame, Label, Button, ttk, messagebox, LEFT, RIGHT, END, CENTER, FLAT, Y, BOTH, NO, YES, GROOVE, W, N, E, S
import mysql.connector 
# Importar módulos y constantes
from constants import *
# Se IMPORTAN los diálogos, incluyendo los nuevos de edición
from dialogs import (
    AddInventoryDialog, AddFinanceDialog, AddMarketingCampaignDialog, AddEmployeeDialog,
    EditInventoryDialog, EditFinanceDialog, EditMarketingCampaignDialog, EditEmployeeDialog # <-- NUEVOS
)

# =================================================================
# LÓGICA DE UTILIDAD
# =================================================================

def get_selected_item_data(tree):
    """
    Obtiene todos los valores (incluyendo el ID) del elemento seleccionado en un Treeview.
    Retorna una tupla de valores o None.
    """
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Selección Requerida", "Por favor, selecciona un registro de la tabla primero.")
        return None
    
    # Retorna todos los valores del ítem seleccionado como una tupla
    item_values = tree.item(selected_item, 'values')
    return item_values


# =================================================================
# VISTAS PRINCIPALES (Inventario)
# =================================================================

class InventoryManagementView:
    """Vista para la gestión de inventario, con diseño de botones unificado."""
    def __init__(self, master_frame, home_app):
        self.home_app = home_app
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=10, pady=10)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1) # Fila del Treeview
        
        Label(self.frame, text="Gestión de Inventario", font=FONT_HEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        
        self._setup_treeview()
        self._setup_buttons()
        self.load_data() # Cargar datos iniciales

    def _setup_treeview(self):
        # Configuración del Treeview
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Nombre', 'Stock'), show='headings')
        self.tree.grid(row=1, column=0, sticky='nswe', padx=10, pady=5)
        
        # Scrollbar
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky='nsw', pady=5)
        self.tree.configure(yscrollcommand=vsb.set)

        # Encabezados
        self.tree.heading('ID', text='ID', anchor=CENTER)
        self.tree.heading('Nombre', text='Nombre', anchor=CENTER)
        self.tree.heading('Stock', text='Stock', anchor=CENTER)

        # Columnas
        self.tree.column('ID', width=50, anchor=CENTER)
        self.tree.column('Nombre', width=250, anchor=W)
        self.tree.column('Stock', width=100, anchor=CENTER)

    def _setup_buttons(self):
        button_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        button_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        
        # Botón AGREGAR
        Button(button_frame, text="➕ Agregar", command=self.agregar_item, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)

        # Botón MODIFICAR (Nuevo)
        Button(button_frame, text="✏️ Modificar", command=self.modificar_item, 
               bg='#f39c12', fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)
               
        # Botón ELIMINAR/BAJA
        Button(button_frame, text="🗑️ Eliminar", command=self.baja_item, 
               bg=COLOR_ERROR, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)

    def load_data(self):
        """Carga los datos de inventario desde la base de datos."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT ID, name, stock FROM inventory ORDER BY ID DESC")
                for row in cursor.fetchall():
                    self.tree.insert('', END, values=row)
            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al cargar datos: {err}")
            finally:
                cursor.close()

    # Lógica de AGREGAR
    def agregar_item(self):
        AddInventoryDialog(self.frame, self.home_app.db_conn, self.home_app.content_area.show_inventory_list)

    # Lógica de MODIFICAR (Implementación)
    def modificar_item(self):
        item_data = get_selected_item_data(self.tree) # Obtener todos los datos
        if not item_data:
            return

        # Abre el diálogo de Modificación
        # item_data: (ID, name, stock)
        EditInventoryDialog(
            self.frame, 
            self.home_app.db_conn, 
            self.home_app.content_area.show_inventory_list, 
            item_data
        )

    # Lógica de BAJA
    def baja_item(self):
        item_data = get_selected_item_data(self.tree)
        if not item_data:
            return
        item_id = item_data[0] # El ID es el primer elemento
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar el Item con ID {item_id}?"):
            conn = self.home_app.db_conn
            if conn and conn.is_connected():
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM inventory WHERE ID = %s", (item_id,))
                    conn.commit()
                    messagebox.showinfo("Baja Exitosa", "Item eliminado correctamente.")
                    self.home_app.content_area.show_inventory_list() # Refresca la vista
                except mysql.connector.Error as err:
                    messagebox.showerror("Error de BD", f"Error al eliminar: {err}")
                finally:
                    cursor.close()
                    
# =================================================================
# VISTAS PRINCIPALES (Finanzas)
# =================================================================

class FinanzasView:
    """Vista para la gestión de Finanzas."""
    def __init__(self, master_frame, home_app):
        self.home_app = home_app
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=10, pady=10)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        Label(self.frame, text="Gestión de Finanzas", font=FONT_HEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        
        self._setup_treeview()
        self._setup_buttons()
        self.load_data()

    def _setup_treeview(self):
        # Configuración del Treeview
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Tipo', 'Monto', 'Fecha', 'Descripción'), show='headings')
        self.tree.grid(row=1, column=0, sticky='nswe', padx=10, pady=5)
        
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky='nsw', pady=5)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.heading('ID', text='ID', anchor=CENTER)
        self.tree.heading('Tipo', text='Tipo', anchor=CENTER)
        self.tree.heading('Monto', text='Monto', anchor=CENTER)
        self.tree.heading('Fecha', text='Fecha', anchor=CENTER)
        self.tree.heading('Descripción', text='Descripción', anchor=W)

        self.tree.column('ID', width=50, anchor=CENTER)
        self.tree.column('Tipo', width=80, anchor=CENTER)
        self.tree.column('Monto', width=100, anchor=CENTER)
        self.tree.column('Fecha', width=100, anchor=CENTER)
        self.tree.column('Descripción', width=300, anchor=W)

    def _setup_buttons(self):
        button_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        button_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        
        # Botón AGREGAR
        Button(button_frame, text="➕ Agregar", command=self.agregar_registro, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)

        # Botón MODIFICAR (Nuevo)
        Button(button_frame, text="✏️ Modificar", command=self.modificar_registro, 
               bg='#f39c12', fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)
               
        # Botón ELIMINAR/BAJA
        Button(button_frame, text="🗑️ Eliminar", command=self.baja_registro, 
               bg=COLOR_ERROR, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)
        
    def load_data(self):
        """Carga los datos de transacciones financieras desde la base de datos."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                
                query = "SELECT id, type, amount, description, date FROM financial_movements" 
                cursor.execute(query)# Nota: transaction_id, type, amount, transaction_date, description
                
                for row in cursor.fetchall():
                    # Formatear el monto con 2 decimales
                    formatted_row = (row[0], row[1], f"${row[2]:.2f}", str(row[3]), row[4])
                    self.tree.insert('', END, values=formatted_row)
            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al cargar datos: {err}")
            finally:
                cursor.close()

    # Lógica de AGREGAR
    def agregar_registro(self):
        AddFinanceDialog(self.frame, self.home_app.db_conn, self.home_app.content_area.show_finance_list)
        
    # Lógica de MODIFICAR (Implementación)
    def modificar_registro(self):
        item_data = get_selected_item_data(self.tree) # Obtener todos los datos
        if not item_data:
            return

        # Abre el diálogo de Modificación
        # item_data: (transaction_id, type, amount, transaction_date, description)
        # Nota: item_data[2] viene con el símbolo '$' de la tabla, debemos pasarlo limpio
        # Reconstruimos la tupla de datos limpia para el diálogo
        clean_amount = item_data[2].replace('$', '')
        clean_data = (item_data[0], item_data[1], clean_amount, item_data[3], item_data[4])
        
        EditFinanceDialog(
            self.frame, 
            self.home_app.db_conn, 
            self.home_app.content_area.show_finance_list, 
            clean_data
        )

    # Lógica de BAJA
    def baja_registro(self):
        item_data = get_selected_item_data(self.tree)
        if not item_data:
            return
        item_id = item_data[0] # El ID es el primer elemento
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar la Transacción con ID {item_id}?"):
            conn = self.home_app.db_conn
            if conn and conn.is_connected():
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM financial_transactions WHERE transaction_id = %s", (item_id,))
                    conn.commit()
                    messagebox.showinfo("Baja Exitosa", "Transacción eliminada correctamente.")
                    self.home_app.content_area.show_finance_list() # Refresca la vista
                except mysql.connector.Error as err:
                    messagebox.showerror("Error de BD", f"Error al eliminar: {err}")
                finally:
                    cursor.close()

# =================================================================
# VISTAS PRINCIPALES (Marketing)
# =================================================================

class MarketingView:
    """Vista para la gestión de Marketing."""
    def __init__(self, master_frame, home_app):
        self.home_app = home_app
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=10, pady=10)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        Label(self.frame, text="Gestión de Marketing", font=FONT_HEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        
        self._setup_treeview()
        self._setup_buttons()
        self.load_data()

    def _setup_treeview(self):
        # Configuración del Treeview
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Nombre', 'Objetivo', 'Inicio', 'Fin', 'Presupuesto', 'Estado'), show='headings')
        self.tree.grid(row=1, column=0, sticky='nswe', padx=10, pady=5)
        
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky='nsw', pady=5)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.heading('ID', text='ID', anchor=CENTER)
        self.tree.heading('Nombre', text='Nombre', anchor=CENTER)
        self.tree.heading('Objetivo', text='Objetivo', anchor=W)
        self.tree.heading('Inicio', text='Inicio', anchor=CENTER)
        self.tree.heading('Fin', text='Fin', anchor=CENTER)
        self.tree.heading('Presupuesto', text='Presupuesto', anchor=CENTER)
        self.tree.heading('Estado', text='Estado', anchor=CENTER)

        self.tree.column('ID', width=50, anchor=CENTER)
        self.tree.column('Nombre', width=150, anchor=W)
        self.tree.column('Objetivo', width=200, anchor=W)
        self.tree.column('Inicio', width=80, anchor=CENTER)
        self.tree.column('Fin', width=80, anchor=CENTER)
        self.tree.column('Presupuesto', width=100, anchor=CENTER)
        self.tree.column('Estado', width=100, anchor=CENTER)

    def _setup_buttons(self):
        button_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        button_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        
        # Botón AGREGAR
        Button(button_frame, text="➕ Agregar", command=self.agregar_campana, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)

        # Botón MODIFICAR (Nuevo)
        Button(button_frame, text="✏️ Modificar", command=self.modificar_campana, 
               bg='#f39c12', fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)
               
        # Botón ELIMINAR/BAJA
        Button(button_frame, text="🗑️ Eliminar", command=self.baja_campana, 
               bg=COLOR_ERROR, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)
        
    def load_data(self):
        """Carga los datos de campañas de marketing desde la base de datos."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # Nota: campaign_id, name, objective, start_date, end_date, budget, status
                cursor.execute("SELECT campaign_id, name, objective, start_date, end_date, budget, status FROM campaigns ORDER BY campaign_id DESC")
                for row in cursor.fetchall():
                    # Formatear el presupuesto y asegurarse que las fechas sean strings
                    budget = f"${row[5]:.2f}" if row[5] is not None else "$0.00"
                    start_date = str(row[3])
                    end_date = str(row[4]) if row[4] else ''
                    
                    formatted_row = (row[0], row[1], row[2], start_date, end_date, budget, row[6])
                    self.tree.insert('', END, values=formatted_row)
            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al cargar datos: {err}")
            finally:
                cursor.close()

    # Lógica de AGREGAR
    def agregar_campana(self):
        AddMarketingCampaignDialog(self.frame, self.home_app.db_conn, self.home_app.content_area.show_marketing_list)
        
    # Lógica de MODIFICAR (Implementación)
    def modificar_campana(self):
        item_data = get_selected_item_data(self.tree) # Obtener todos los datos
        if not item_data:
            return
            
        # Reconstruimos la tupla de datos limpia (quitando el '$' del presupuesto)
        clean_budget = item_data[5].replace('$', '')
        # item_data: (ID, Nombre, Objetivo, Inicio, Fin, Presupuesto, Estado)
        clean_data = (item_data[0], item_data[1], item_data[2], item_data[3], item_data[4], clean_budget, item_data[6])

        # Abre el diálogo de Modificación
        EditMarketingCampaignDialog(
            self.frame, 
            self.home_app.db_conn, 
            self.home_app.content_area.show_marketing_list, 
            clean_data
        )

    # Lógica de BAJA
    def baja_campana(self):
        item_data = get_selected_item_data(self.tree)
        if not item_data:
            return
        item_id = item_data[0] # El ID es el primer elemento
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar la Campaña con ID {item_id}?"):
            conn = self.home_app.db_conn
            if conn and conn.is_connected():
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM campaigns WHERE campaign_id = %s", (item_id,))
                    conn.commit()
                    messagebox.showinfo("Baja Exitosa", "Campaña eliminada correctamente.")
                    self.home_app.content_area.show_marketing_list() # Refresca la vista
                except mysql.connector.Error as err:
                    messagebox.showerror("Error de BD", f"Error al eliminar: {err}")
                finally:
                    cursor.close()
                    
# =================================================================
# VISTAS PRINCIPALES (RRHH)
# =================================================================

class RRHHView:
    """Vista para la gestión de Recursos Humanos."""
    def __init__(self, master_frame, home_app):
        self.home_app = home_app
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=10, pady=10)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        Label(self.frame, text="Gestión de Recursos Humanos", font=FONT_HEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        
        self._setup_treeview()
        self._setup_buttons()
        self.load_data()

    def _setup_treeview(self):
        # Configuración del Treeview
        columns = ('ID', 'Nombre', 'Apellido', 'Contratación', 'Salario', 'Posición', 'Activo')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        self.tree.grid(row=1, column=0, sticky='nswe', padx=10, pady=5)
        
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky='nsw', pady=5)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.heading('ID', text='ID', anchor=CENTER)
        self.tree.heading('Nombre', text='Nombre', anchor=W)
        self.tree.heading('Apellido', text='Apellido', anchor=W)
        self.tree.heading('Contratación', text='Contratación', anchor=CENTER)
        self.tree.heading('Salario', text='Salario', anchor=CENTER)
        self.tree.heading('Posición', text='Posición', anchor=W)
        self.tree.heading('Activo', text='Activo', anchor=CENTER)

        self.tree.column('ID', width=50, anchor=CENTER)
        self.tree.column('Nombre', width=120, anchor=W)
        self.tree.column('Apellido', width=120, anchor=W)
        self.tree.column('Contratación', width=100, anchor=CENTER)
        self.tree.column('Salario', width=100, anchor=CENTER)
        self.tree.column('Posición', width=150, anchor=W)
        self.tree.column('Activo', width=60, anchor=CENTER)


    def _setup_buttons(self):
        button_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        button_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        
        # Botón AGREGAR
        Button(button_frame, text="➕ Alta Empleado", command=self.alta_empleado, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)

        # Botón MODIFICAR (Nuevo)
        Button(button_frame, text="✏️ Modificar", command=self.modificar_empleado, 
               bg='#f39c12', fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)
               
        # Botón ELIMINAR/BAJA
        # Usamos baja para reflejar una baja lógica (is_active = FALSE) o física (DELETE)
        Button(button_frame, text="🗑️ Baja Empleado", command=self.baja_empleado, 
               bg=COLOR_ERROR, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(side=LEFT, padx=5)

    def load_data(self):
        """Carga los datos de empleados desde la base de datos."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.home_app.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # employee_id, first_name, last_name, hire_date, salary, position, is_active
                query = "SELECT employee_id, first_name, last_name, hire_date, salary, position, is_active FROM employees ORDER BY employee_id DESC"
                cursor.execute(query)
                for row in cursor.fetchall():
                    # Formatear Salario y estado Activo
                    salary = f"${row[4]:.2f}" if row[4] is not None else "$0.00"
                    is_active = "Sí" if row[6] else "No"
                    
                    formatted_row = (row[0], row[1], row[2], str(row[3]), salary, row[5], is_active)
                    self.tree.insert('', END, values=formatted_row)
            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al cargar datos: {err}")
            finally:
                cursor.close()

    # Lógica de ALTA/AGREGAR
    def alta_empleado(self):
        AddEmployeeDialog(self.frame, self.home_app.db_conn, self.home_app.content_area.show_rrhh_list)

    # Lógica de BAJA
    def baja_empleado(self):
        item_data = get_selected_item_data(self.tree)
        if not item_data:
            return
        empleado_id = item_data[0]
        
        if messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de que deseas eliminar el Empleado con ID {empleado_id}?"):
            conn = self.home_app.db_conn
            if conn and conn.is_connected():
                cursor = conn.cursor()
                try:
                    # Baja lógica (cambiar is_active a 0) es preferible a DELETE
                    # Pero basándome en tu snippet anterior que usaba DELETE, mantengo la eliminación física
                    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (empleado_id,)) 
                    conn.commit()
                    messagebox.showinfo("Baja Exitosa", "Empleado eliminado correctamente.")
                    self.home_app.content_area.show_rrhh_list() # Refresca la vista
                except mysql.connector.Error as err:
                    messagebox.showerror("Error de BD", f"Error al eliminar el empleado: {err}")
                finally:
                    cursor.close()

    # Lógica de MODIFICACIÓN (Implementación)
    def modificar_empleado(self):
        item_data = get_selected_item_data(self.tree) # Obtener todos los datos
        if not item_data:
            return

        # Reconstruimos la tupla de datos limpia (quitando el '$' del salario y estado activo)
        clean_salary = item_data[4].replace('$', '')
        
        # item_data: (ID, first_name, last_name, hire_date, salary, position, is_active_str)
        # Solo pasamos los primeros 6 elementos que se pueden editar
        clean_data = (item_data[0], item_data[1], item_data[2], item_data[3], clean_salary, item_data[5])
        
        # Abre el diálogo de Modificación.
        EditEmployeeDialog(
            self.frame, 
            self.home_app.db_conn, 
            self.home_app.content_area.show_rrhh_list, # Función para refrescar
            clean_data
        )