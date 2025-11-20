# dialogs.py
from tkinter import Toplevel, Frame, Label, Entry, Button, messagebox, FLAT, StringVar, OptionMenu
import mysql.connector
from datetime import datetime
# Importar constantes (Asegúrate de que constants.py existe y tiene estas variables)
from constants import COLOR_ACCENT, COLOR_BG_WHITE, FONT_MAIN, FONT_SUBHEADING, FONT_HEADING

# =================================================================
# DIÁLOGOS DE AGREGAR (Estructuras de ejemplo basadas en tus snippets)
# =================================================================

class AddUserDialog(Toplevel):
    """Diálogo para agregar un nuevo usuario (gerente/admin)."""
    def __init__(self, master, db_conn, refresh_callback=None):
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

        # Usuario
        Label(main_frame, text="Usuario:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w')
        self.user_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.user_entry.pack(fill='x', pady=2)

        # Contraseña
        Label(main_frame, text="Contraseña:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w')
        self.pass_entry = Entry(main_frame, font=FONT_MAIN, show="*", width=40)
        self.pass_entry.pack(fill='x', pady=2)
        
        # Botón
        Button(main_frame, text="Guardar Usuario", command=self.save_user, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(pady=20)

    def save_user(self):
        # Lógica de guardar usuario
        username = self.user_entry.get()
        password = self.pass_entry.get()

        if not all([username, password]):
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return
            
        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # Nota: En una app real, la contraseña debe hashearse.
                insert_query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
                # Asumimos que el usuario que se agrega es un empleado regular o con un rol específico.
                cursor.execute(insert_query, (username, password, 'employee'))
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
                if self.refresh_callback:
                    self.refresh_callback() 
                self.destroy()
            except mysql.connector.Error as err:
                # Manejar error si el usuario ya existe (usando UNIQUE INDEX)
                messagebox.showerror("Error de BD", f"Error al agregar usuario: {err}")
            finally:
                cursor.close()

# ---

class AddInventoryDialog(Toplevel):
    """Diálogo para agregar un nuevo item de inventario."""
    def __init__(self, master, db_conn, refresh_callback):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.title("Agregar Item a Inventario")
        self.geometry("400x250")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master); self.grab_set(); self.focus_force()
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Nuevo Item", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Nombre
        Label(main_frame, text="Nombre:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.name_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.name_entry.pack(fill='x', pady=2)

        # Stock
        Label(main_frame, text="Stock:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.stock_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.stock_entry.pack(fill='x', pady=2)

        # Botón
        Button(main_frame, text="Guardar Item", command=self.save_item, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(pady=20)

    def save_item(self):
        name = self.name_entry.get()
        stock_str = self.stock_entry.get()

        if not all([name, stock_str]):
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return

        try:
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Error", "El Stock debe ser un número entero válido.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                insert_query = "INSERT INTO inventory (name, stock) VALUES (%s, %s)"
                cursor.execute(insert_query, (name, stock))
                conn.commit()

                messagebox.showinfo("Éxito", "Item de inventario agregado correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al guardar: {err}")
            finally:
                cursor.close()

# ---

class AddFinanceDialog(Toplevel):
    """Diálogo para agregar una nueva transacción financiera."""
    def __init__(self, master, db_conn, refresh_callback):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.title("Agregar Transacción")
        self.geometry("500x450")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master); self.grab_set(); self.focus_force()
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Nueva Transacción", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Tipo
        Label(main_frame, text="Tipo:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.type_var = StringVar(self)
        self.type_var.set("Ingreso") 
        self.type_menu = OptionMenu(main_frame, self.type_var, "Ingreso", "Egreso")
        self.type_menu.config(bg=COLOR_BG_WHITE, font=FONT_MAIN)
        self.type_menu.pack(fill='x', pady=2)

        # Monto
        Label(main_frame, text="Monto:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.amount_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.amount_entry.pack(fill='x', pady=2)

        # Fecha (YYYY-MM-DD)
        Label(main_frame, text="Fecha (YYYY-MM-DD):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.date_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.pack(fill='x', pady=2)

        # Descripción
        Label(main_frame, text="Descripción:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.desc_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.desc_entry.pack(fill='x', pady=2)

        # Botón
        Button(main_frame, text="Guardar Transacción", command=self.save_transaction, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(pady=20)

    def save_transaction(self):
        trans_type = self.type_var.get()
        amount_str = self.amount_entry.get()
        date_str = self.date_entry.get()
        desc = self.desc_entry.get()
        
        if not all([trans_type, amount_str, date_str, desc]):
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return

        try:
            amount = float(amount_str)
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido y la fecha debe estar en formato YYYY-MM-DD.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                insert_query = "INSERT INTO financial_transactions (type, amount, transaction_date, description) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query, (trans_type, amount, date_str, desc))
                conn.commit()

                messagebox.showinfo("Éxito", "Transacción agregada correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al guardar: {err}")
            finally:
                cursor.close()

# ---

class AddMarketingCampaignDialog(Toplevel):
    """Diálogo para agregar una nueva campaña de marketing."""
    def __init__(self, master, db_conn, refresh_callback):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.title("Agregar Campaña")
        self.geometry("400x650")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master); self.grab_set(); self.focus_force()
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Nueva Campaña", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Nombre
        Label(main_frame, text="Nombre:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.name_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.name_entry.pack(fill='x', pady=2)

        # Objetivo
        Label(main_frame, text="Objetivo:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.objective_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.objective_entry.pack(fill='x', pady=2)
        
        # Fecha Inicio (YYYY-MM-DD)
        Label(main_frame, text="Fecha Inicio (YYYY-MM-DD):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.start_date_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.start_date_entry.pack(fill='x', pady=2)
        
        # Fecha Fin (YYYY-MM-DD) - Opcional
        Label(main_frame, text="Fecha Fin (YYYY-MM-DD) [Opcional]:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.end_date_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.end_date_entry.pack(fill='x', pady=2)

        # Presupuesto
        Label(main_frame, text="Presupuesto:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.budget_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.budget_entry.pack(fill='x', pady=2)

        # Estado
        Label(main_frame, text="Estado:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.status_var = StringVar(self)
        self.status_var.set("Active") # Valor inicial
        self.status_menu = OptionMenu(main_frame, self.status_var, "Active", "Completed", "Paused")
        self.status_menu.config(bg=COLOR_BG_WHITE, font=FONT_MAIN)
        self.status_menu.pack(fill='x', pady=2)

        # Botón
        Button(main_frame, text="Guardar Campaña", command=self.save_campaign, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(pady=20)


    def save_campaign(self):
        name = self.name_entry.get()
        objective = self.objective_entry.get()
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()
        budget_str = self.budget_entry.get()
        status = self.status_var.get()
        
        if not all([name, objective, start_date_str, budget_str, status]):
            messagebox.showerror("Error", "Debe completar todos los campos obligatorios.")
            return

        try:
            budget = float(budget_str)
            datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str:
                 datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "El presupuesto debe ser un número válido y las fechas deben estar en formato YYYY-MM-DD.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                insert_query = "INSERT INTO campaigns (name, objective, start_date, end_date, budget, status) VALUES (%s, %s, %s, %s, %s, %s)"
                
                # Convertir cadena vacía a None para que MySQL lo tome como NULL
                final_end_date = end_date_str if end_date_str else None
                
                cursor.execute(insert_query, (name, objective, start_date_str, final_end_date, budget, status))
                conn.commit()

                messagebox.showinfo("Éxito", "Campaña de marketing agregada correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al guardar: {err}")
            finally:
                cursor.close()

# ---

class AddEmployeeDialog(Toplevel):
    """Diálogo para agregar un nuevo empleado (RRHH)."""
    def __init__(self, master, db_conn, refresh_callback):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.title("Agregar Nuevo Empleado")
        self.geometry("400x450")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master); self.grab_set(); self.focus_force()
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Nuevo Empleado", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Nombre y Apellido
        Label(main_frame, text="Nombre:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.fname_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.fname_entry.pack(fill='x', pady=2)
        Label(main_frame, text="Apellido:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.lname_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.lname_entry.pack(fill='x', pady=2)

        # Posición
        Label(main_frame, text="Posición:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.pos_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.pos_entry.pack(fill='x', pady=2)

        # Salario
        Label(main_frame, text="Salario:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.salary_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.salary_entry.pack(fill='x', pady=2)
        
        # Fecha de Contratación
        Label(main_frame, text="Fecha de Contratación (YYYY-MM-DD):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.hire_date_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.hire_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.hire_date_entry.pack(fill='x', pady=2)

        # Botón
        Button(main_frame, text="Guardar Empleado", command=self.save_employee, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(pady=20)

    def save_employee(self):
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        position = self.pos_entry.get()
        salary_str = self.salary_entry.get()
        hire_date_str = self.hire_date_entry.get()
        
        if not all([fname, lname, position, salary_str, hire_date_str]):
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return
            
        try:
            salary = float(salary_str)
            datetime.strptime(hire_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "El salario debe ser un número válido y la fecha debe estar en formato YYYY-MM-DD.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                insert_query = "INSERT INTO employees (first_name, last_name, hire_date, salary, position, is_active) VALUES (%s, %s, %s, %s, %s, TRUE)"
                
                cursor.execute(insert_query, (fname, lname, hire_date_str, salary, position))
                conn.commit()

                messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al guardar: {err}")
            finally:
                cursor.close()

# =================================================================
# DIÁLOGOS DE MODIFICACIÓN (Nuevos/Completos para Modificar)
# =================================================================

class EditInventoryDialog(Toplevel):
    """Diálogo para modificar un item de inventario."""
    def __init__(self, master, db_conn, refresh_callback, item_data):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.item_id = item_data[0] # ID
        self.item_name = item_data[1] # Nombre
        self.item_stock = item_data[2] # Stock

        self.title(f"Modificar Item ID: {self.item_id}")
        self.geometry("400x250")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master); self.grab_set(); self.focus_force()

        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Modificar Inventario", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Nombre
        Label(main_frame, text="Nombre:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.name_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.name_entry.insert(0, self.item_name)
        self.name_entry.pack(fill='x', pady=2)

        # Stock
        Label(main_frame, text="Stock:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.stock_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.stock_entry.insert(0, self.item_stock)
        self.stock_entry.pack(fill='x', pady=2)

        # Botón
        Button(main_frame, text="Guardar Cambios", command=self.save_changes, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(pady=20)

    def save_changes(self):
        name = self.name_entry.get()
        stock_str = self.stock_entry.get()

        if not all([name, stock_str]):
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return

        try:
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Error", "El Stock debe ser un número entero válido.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                update_query = "UPDATE inventory SET name = %s, stock = %s WHERE ID = %s"
                cursor.execute(update_query, (name, stock, self.item_id))
                conn.commit()

                messagebox.showinfo("Éxito", f"Item ID {self.item_id} modificado correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al modificar: {err}")
            finally:
                cursor.close()

# ---

class EditFinanceDialog(Toplevel):
    """Diálogo para modificar un registro financiero."""
    def __init__(self, master, db_conn, refresh_callback, item_data):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        # item_data: (transaction_id, type, amount, transaction_date, description)
        self.item_id = item_data[0] 
        self.item_type = item_data[1] 
        self.item_amount = item_data[2] 
        self.item_date = item_data[3] 
        self.item_desc = item_data[4] 

        self.title(f"Modificar Transacción ID: {self.item_id}")
        self.geometry("400x350")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master); self.grab_set(); self.focus_force()

        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Modificar Transacción", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Tipo
        Label(main_frame, text="Tipo:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.type_var = StringVar(self)
        self.type_var.set(self.item_type) # Valor inicial
        self.type_menu = OptionMenu(main_frame, self.type_var, "Ingreso", "Egreso")
        self.type_menu.config(bg=COLOR_BG_WHITE, font=FONT_MAIN)
        self.type_menu.pack(fill='x', pady=2)

        # Monto
        Label(main_frame, text="Monto:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.amount_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.amount_entry.insert(0, self.item_amount)
        self.amount_entry.pack(fill='x', pady=2)

        # Fecha (YYYY-MM-DD)
        Label(main_frame, text="Fecha (YYYY-MM-DD):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.date_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.date_entry.insert(0, self.item_date)
        self.date_entry.pack(fill='x', pady=2)

        # Descripción
        Label(main_frame, text="Descripción:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.desc_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.desc_entry.insert(0, self.item_desc)
        self.desc_entry.pack(fill='x', pady=2)

        # Botón
        Button(main_frame, text="Guardar Cambios", command=self.save_changes, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(pady=20)

    def save_changes(self):
        trans_type = self.type_var.get()
        amount_str = self.amount_entry.get()
        date_str = self.date_entry.get()
        desc = self.desc_entry.get()
        
        if not all([trans_type, amount_str, date_str, desc]):
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return

        try:
            amount = float(amount_str)
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido y la fecha debe estar en formato YYYY-MM-DD.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                update_query = "UPDATE financial_transactions SET type = %s, amount = %s, transaction_date = %s, description = %s WHERE transaction_id = %s"
                cursor.execute(update_query, (trans_type, amount, date_str, desc, self.item_id))
                conn.commit()

                messagebox.showinfo("Éxito", f"Transacción ID {self.item_id} modificada correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al modificar: {err}")
            finally:
                cursor.close()

# ---

class EditMarketingCampaignDialog(Toplevel):
    """Diálogo para modificar una campaña de marketing."""
    def __init__(self, master, db_conn, refresh_callback, item_data):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        # item_data: [ID, Nombre, Objetivo, Start_Date, End_Date, Budget, Status]
        self.item_id = item_data[0] 
        self.item_name = item_data[1] 
        self.item_objective = item_data[2] 
        self.item_start = item_data[3]
        self.item_end = item_data[4]
        self.item_budget = item_data[5]
        self.item_status = item_data[6]

        self.title(f"Modificar Campaña ID: {self.item_id}")
        self.geometry("400x450")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master); self.grab_set(); self.focus_force()

        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Modificar Campaña", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Nombre
        Label(main_frame, text="Nombre:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.name_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.name_entry.insert(0, self.item_name)
        self.name_entry.pack(fill='x', pady=2)

        # Objetivo
        Label(main_frame, text="Objetivo:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.objective_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.objective_entry.insert(0, self.item_objective)
        self.objective_entry.pack(fill='x', pady=2)
        
        # Fecha Inicio (YYYY-MM-DD)
        Label(main_frame, text="Fecha Inicio (YYYY-MM-DD):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.start_date_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.start_date_entry.insert(0, self.item_start)
        self.start_date_entry.pack(fill='x', pady=2)
        
        # Fecha Fin (YYYY-MM-DD)
        Label(main_frame, text="Fecha Fin (YYYY-MM-DD) [Opcional]:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.end_date_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        # Manejar None para la fecha de fin (si es NULL en la BD)
        self.end_date_entry.insert(0, self.item_end if self.item_end else '') 
        self.end_date_entry.pack(fill='x', pady=2)

        # Presupuesto
        Label(main_frame, text="Presupuesto:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.budget_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.budget_entry.insert(0, self.item_budget)
        self.budget_entry.pack(fill='x', pady=2)

        # Estado
        Label(main_frame, text="Estado:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.status_var = StringVar(self)
        self.status_var.set(self.item_status) # Valor inicial
        self.status_menu = OptionMenu(main_frame, self.status_var, "Active", "Completed", "Paused")
        self.status_menu.config(bg=COLOR_BG_WHITE, font=FONT_MAIN)
        self.status_menu.pack(fill='x', pady=2)

        # Botón
        Button(main_frame, text="Guardar Cambios", command=self.save_changes, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(pady=20)


    def save_changes(self):
        name = self.name_entry.get()
        objective = self.objective_entry.get()
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()
        budget_str = self.budget_entry.get()
        status = self.status_var.get()
        
        if not all([name, objective, start_date_str, budget_str, status]):
            messagebox.showerror("Error", "Debe completar todos los campos obligatorios.")
            return

        try:
            budget = float(budget_str)
            datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str:
                 datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "El presupuesto debe ser un número válido y las fechas deben estar en formato YYYY-MM-DD.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                update_query = "UPDATE campaigns SET name = %s, objective = %s, start_date = %s, end_date = %s, budget = %s, status = %s WHERE campaign_id = %s"
                
                # Convertir cadena vacía a None para que MySQL lo tome como NULL
                final_end_date = end_date_str if end_date_str else None
                
                cursor.execute(update_query, (name, objective, start_date_str, final_end_date, budget, status, self.item_id)) 
                conn.commit()

                messagebox.showinfo("Éxito", f"Campaña ID {self.item_id} modificada correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al modificar: {err}")
            finally:
                cursor.close()

# ---

class EditEmployeeDialog(Toplevel):
    """Diálogo para modificar un registro de empleado (RRHH)."""
    def __init__(self, master, db_conn, refresh_callback, item_data):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        # item_data: (employee_id, first_name, last_name, hire_date, salary, position, is_active)
        self.item_id = item_data[0] 
        self.item_fname = item_data[1] 
        self.item_lname = item_data[2] 
        self.item_hire_date = item_data[3]
        self.item_salary = item_data[4]
        self.item_position = item_data[5]

        self.title(f"Modificar Empleado ID: {self.item_id}")
        self.geometry("400x450")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master); self.grab_set(); self.focus_force()

        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Modificar Empleado", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Nombre y Apellido
        Label(main_frame, text="Nombre:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.fname_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.fname_entry.insert(0, self.item_fname)
        self.fname_entry.pack(fill='x', pady=2)
        Label(main_frame, text="Apellido:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.lname_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.lname_entry.insert(0, self.item_lname)
        self.lname_entry.pack(fill='x', pady=2)

        # Posición
        Label(main_frame, text="Posición:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.pos_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.pos_entry.insert(0, self.item_position)
        self.pos_entry.pack(fill='x', pady=2)

        # Salario
        Label(main_frame, text="Salario:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.salary_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.salary_entry.insert(0, self.item_salary)
        self.salary_entry.pack(fill='x', pady=2)
        
        # Fecha de Contratación
        Label(main_frame, text="Fecha de Contratación (YYYY-MM-DD):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5, 0))
        self.hire_date_entry = Entry(main_frame, font=FONT_MAIN, width=40)
        self.hire_date_entry.insert(0, self.item_hire_date)
        self.hire_date_entry.pack(fill='x', pady=2)

        # Botón
        Button(main_frame, text="Guardar Cambios", command=self.save_changes, 
               bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, font=FONT_MAIN, relief=FLAT).pack(pady=20)


    def save_changes(self):
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        position = self.pos_entry.get()
        salary_str = self.salary_entry.get()
        hire_date_str = self.hire_date_entry.get()
        
        if not all([fname, lname, position, salary_str, hire_date_str]):
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return
            
        try:
            salary = float(salary_str)
            datetime.strptime(hire_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "El salario debe ser un número válido y la fecha debe estar en formato YYYY-MM-DD.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                update_query = "UPDATE employees SET first_name = %s, last_name = %s, hire_date = %s, salary = %s, position = %s WHERE employee_id = %s"
                
                cursor.execute(update_query, (fname, lname, hire_date_str, salary, position, self.item_id)) 
                conn.commit()

                messagebox.showinfo("Éxito", f"Empleado ID {self.item_id} modificado correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de BD", f"Error al modificar: {err}")
            finally:
                cursor.close()