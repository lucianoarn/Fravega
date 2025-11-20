# dialogs.py
from tkinter import Toplevel, Frame, Label, Entry, Button, messagebox, FLAT, StringVar, OptionMenu
import mysql.connector
from datetime import datetime
# Importar constantes
from constants import *

# =================================================================
# DIÁLOGOS DE AGREGAR (Existente)
# =================================================================

class AddUserDialog(Toplevel):
    # ... (código AddUserDialog existente) ...
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
    # ... (código AddInventoryDialog existente) ...
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

class AddFinanceDialog(Toplevel):
    # ... (código AddFinanceDialog existente) ...
    def __init__(self, master, db_conn, refresh_callback):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.title("Registrar Nuevo Ingreso/Gasto")
        self.geometry("450x400")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.create_widgets()

    

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Nuevo Movimiento Financiero", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Campo Monto
        Label(main_frame, text="Monto:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.monto_entry = Entry(main_frame, font=FONT_MAIN)
        self.monto_entry.pack(fill='x', pady=(0, 10))

        # Campo Descripción
        Label(main_frame, text="Descripción:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.desc_entry = Entry(main_frame, font=FONT_MAIN)
        self.desc_entry.pack(fill='x', pady=(0, 10))
        
        # Campo Tipo (Para simular si es Ingreso o Gasto) - Simple ejemplo
        Label(main_frame, text="Tipo:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.tipo_var = StringVar(self)
        self.tipo_var.set("Ingreso") # Opción predeterminada
        opciones_tipo = ["Ingreso", "Gasto"]
        tipo_menu = OptionMenu(main_frame, self.tipo_var, *opciones_tipo)
        tipo_menu.config(font=FONT_MAIN, bg=COLOR_BG_WHITE)
        tipo_menu.pack(fill='x', pady=(0, 10))


        Button(main_frame, text="Guardar Movimiento", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.save_movement).pack(pady=15)

    def save_movement(self):
        monto_str = self.monto_entry.get()
        descripcion = self.desc_entry.get()
        tipo = self.tipo_var.get()
        
        if not monto_str or not descripcion:
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return

        try:
            monto = float(monto_str)
            if monto <= 0: raise ValueError
            # Si es Gasto, el monto se registra como negativo
            if tipo == "Gasto":
                monto = -abs(monto) 
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número positivo.")
            return

        # -------------------------------------------------------------
        # LÓGICA DE DB ADAPTADA (similar a tu Login/dialogs)
        # -------------------------------------------------------------
        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # Nota: Necesitarás crear la tabla 'financial_movements' en user_db.sql
                insert_query = "INSERT INTO financial_movements (type, amount, description, date) VALUES (%s, %s, %s, CURDATE())"
                
                # 'tipo' se usa para la descripción, 'monto' (ya negativo si es gasto) se usa para el valor.
                cursor.execute(insert_query, (tipo, monto, descripcion)) 
                conn.commit()

                messagebox.showinfo("Éxito", f"{tipo} '{descripcion}' registrado correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al registrar: {err}\nATENCIÓN: ¿Existe la tabla 'financial_movements' en user_db?")
            finally:
                cursor.close()

class AddMarketingCampaignDialog(Toplevel):
    # ... (código AddMarketingCampaignDialog existente - Se eliminó la duplicidad) ...
    def __init__(self, master, db_conn, refresh_callback):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.title("Registrar Nueva Campaña de Marketing")
        self.geometry("500x550")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Nueva Campaña", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Nombre
        Label(main_frame, text="Nombre:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.name_entry = Entry(main_frame, font=FONT_MAIN)
        self.name_entry.pack(fill='x', pady=(0, 10))

        # Objetivo
        Label(main_frame, text="Objetivo:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.obj_entry = Entry(main_frame, font=FONT_MAIN)
        self.obj_entry.pack(fill='x', pady=(0, 10))

        # Presupuesto
        Label(main_frame, text="Presupuesto ($):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.budget_entry = Entry(main_frame, font=FONT_MAIN)
        self.budget_entry.pack(fill='x', pady=(0, 10))
        
        # Fecha de Inicio (usaremos Entry simple si tkcalendar no está)
        Label(main_frame, text="Fecha Inicio (YYYY-MM-DD):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.start_date_entry = Entry(main_frame, font=FONT_MAIN)
        self.start_date_entry.pack(fill='x', pady=(0, 10))
        
        Button(main_frame, text="Guardar Campaña", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.save_campaign).pack(pady=15)

    def save_campaign(self):
        name = self.name_entry.get()
        objective = self.obj_entry.get()
        budget_str = self.budget_entry.get()
        start_date_str = self.start_date_entry.get()
        
        if not all([name, objective, budget_str, start_date_str]):
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return

        try:
            budget = float(budget_str)
            # Validación de formato de fecha simple
            datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "El presupuesto debe ser un número válido y la fecha debe estar en formato YYYY-MM-DD.")
            return

        # -------------------------------------------------------------
        # LÓGICA DE DB: INSERT INTO campaigns
        # -------------------------------------------------------------
        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                insert_query = "INSERT INTO campaigns (name, objective, start_date, budget, status) VALUES (%s, %s, %s, %s, %s)"
                # Estado por defecto 'Active'
                cursor.execute(insert_query, (name, objective, start_date_str, budget, 'Active')) 
                conn.commit()

                messagebox.showinfo("Éxito", f"Campaña '{name}' registrada correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al registrar campaña: {err}")
            finally:
                cursor.close()

class AddEmployeeDialog(Toplevel):
    # ... (código AddEmployeeDialog existente) ...
    def __init__(self, master, db_conn, refresh_callback):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.title("Registrar Nuevo Empleado")
        self.geometry("500x600")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=10)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Alta de Empleado", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Nombre y Apellido
        Label(main_frame, text="Nombre:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.fname_entry = Entry(main_frame, font=FONT_MAIN)
        self.fname_entry.pack(fill='x', pady=(0, 10))
        
        Label(main_frame, text="Apellido:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.lname_entry = Entry(main_frame, font=FONT_MAIN)
        self.lname_entry.pack(fill='x', pady=(0, 10))

        # Posición
        Label(main_frame, text="Posición:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.pos_entry = Entry(main_frame, font=FONT_MAIN)
        self.pos_entry.pack(fill='x', pady=(0, 10))

        # Salario
        Label(main_frame, text="Salario:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.salary_entry = Entry(main_frame, font=FONT_MAIN)
        self.salary_entry.pack(fill='x', pady=(0, 10))

        # Fecha de Contratación
        Label(main_frame, text="Fecha Contratación (YYYY-MM-DD):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.hire_date_entry = Entry(main_frame, font=FONT_MAIN)
        self.hire_date_entry.pack(fill='x', pady=(0, 10))
        
        Button(main_frame, text="Registrar Empleado", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.save_employee).pack(pady=15)

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

        # -------------------------------------------------------------
        # LÓGICA DE DB: INSERT INTO employees
        # -------------------------------------------------------------
        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # Usamos sector_id=NULL por defecto si no tienes un selector de sector
                insert_query = "INSERT INTO employees (first_name, last_name, hire_date, salary, position, is_active) VALUES (%s, %s, %s, %s, %s, %s)"
                
                cursor.execute(insert_query, (fname, lname, hire_date_str, salary, position, True)) 
                conn.commit()

                messagebox.showinfo("Éxito", f"Empleado {fname} {lname} registrado correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al registrar empleado: {err}")
            finally:
                cursor.close()

# =================================================================
# DIÁLOGOS DE MODIFICAR (NUEVOS)
# =================================================================

class ModifyInventoryDialog(Toplevel):
    def __init__(self, master, db_conn, refresh_callback, item_id):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.item_id = item_id # El ID del producto a modificar
        self.title(f"Modificar Producto ID: {item_id}")
        self.geometry("400x250")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.current_data = self._fetch_current_data()
        if not self.current_data:
            messagebox.showerror("Error", "No se encontró el producto a modificar.")
            self.destroy()
            return
        self.create_widgets()

    def _fetch_current_data(self):
        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            try:
                query = "SELECT name, stock FROM inventory WHERE ID = %s"
                cursor.execute(query, (self.item_id,))
                return cursor.fetchone()
            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al cargar datos: {err}")
                return None
            finally:
                cursor.close()
        return None

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Modificar Producto", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        Label(main_frame, text="Nombre del Producto:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.name_entry = Entry(main_frame, font=FONT_MAIN)
        self.name_entry.insert(0, self.current_data['name'])
        self.name_entry.pack(fill='x', pady=(0, 10))

        Label(main_frame, text="Cantidad (Stock):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.stock_entry = Entry(main_frame, font=FONT_MAIN)
        self.stock_entry.insert(0, str(self.current_data['stock']))
        self.stock_entry.pack(fill='x', pady=(0, 10))
        
        Button(main_frame, text="Guardar Cambios", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.update_product).pack(pady=15)

    def update_product(self):
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
                update_query = "UPDATE inventory SET name = %s, stock = %s WHERE ID = %s"
                cursor.execute(update_query, (name, stock, self.item_id))
                conn.commit()

                messagebox.showinfo("Éxito", f"Producto '{name}' (ID: {self.item_id}) modificado exitosamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al modificar producto: {err}")
            finally:
                cursor.close()
        else:
            messagebox.showerror("Error", "No hay conexión activa a la base de datos.")


class ModifyFinanceDialog(Toplevel):
    def __init__(self, master, db_conn, refresh_callback, item_id):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.item_id = item_id 
        self.title(f"Modificar Movimiento Financiero ID: {item_id}")
        self.geometry("450x400")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.current_data = self._fetch_current_data()
        if not self.current_data:
            messagebox.showerror("Error", "No se encontró el movimiento a modificar.")
            self.destroy()
            return
        self.create_widgets()

    def _fetch_current_data(self):
        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            try:
                # Usamos ID como PK (asumiendo) y obtenemos tipo, monto, descripcion
                query = "SELECT ID, type, amount, description FROM financial_movements WHERE ID = %s"
                cursor.execute(query, (self.item_id,))
                return cursor.fetchone()
            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al cargar datos: {err}")
                return None
            finally:
                cursor.close()
        return None

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Modificar Movimiento", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)
        
        # El monto se muestra como positivo en el campo, el signo lo maneja la lógica
        monto_display = abs(self.current_data['amount']) 
        tipo_inicial = "Gasto" if self.current_data['amount'] < 0 else "Ingreso"

        # Campo Monto
        Label(main_frame, text="Monto:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.monto_entry = Entry(main_frame, font=FONT_MAIN)
        self.monto_entry.insert(0, str(monto_display))
        self.monto_entry.pack(fill='x', pady=(0, 10))

        # Campo Descripción
        Label(main_frame, text="Descripción:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.desc_entry = Entry(main_frame, font=FONT_MAIN)
        self.desc_entry.insert(0, self.current_data['description'])
        self.desc_entry.pack(fill='x', pady=(0, 10))
        
        # Campo Tipo 
        Label(main_frame, text="Tipo:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.tipo_var = StringVar(self)
        self.tipo_var.set(tipo_inicial) 
        opciones_tipo = ["Ingreso", "Gasto"]
        tipo_menu = OptionMenu(main_frame, self.tipo_var, *opciones_tipo)
        tipo_menu.config(font=FONT_MAIN, bg=COLOR_BG_WHITE)
        tipo_menu.pack(fill='x', pady=(0, 10))


        Button(main_frame, text="Guardar Cambios", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.update_movement).pack(pady=15)

    def update_movement(self):
        monto_str = self.monto_entry.get()
        descripcion = self.desc_entry.get()
        tipo = self.tipo_var.get()
        
        if not monto_str or not descripcion:
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return

        try:
            monto = float(monto_str)
            if monto <= 0: raise ValueError
            # Aplicar el signo para DB
            if tipo == "Gasto":
                monto = -abs(monto) 
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número positivo.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # Se actualiza el tipo (que es la descripción en la DB) y el monto.
                update_query = "UPDATE financial_movements SET type = %s, amount = %s, description = %s WHERE ID = %s"
                
                cursor.execute(update_query, (tipo, monto, descripcion, self.item_id)) 
                conn.commit()

                messagebox.showinfo("Éxito", f"Movimiento ID {self.item_id} modificado correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al modificar: {err}")
            finally:
                cursor.close()

class ModifyMarketingCampaignDialog(Toplevel):
    def __init__(self, master, db_conn, refresh_callback, item_id):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.item_id = item_id 
        self.title(f"Modificar Campaña ID: {item_id}")
        self.geometry("500x550")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.current_data = self._fetch_current_data()
        if not self.current_data:
            messagebox.showerror("Error", "No se encontró la campaña a modificar.")
            self.destroy()
            return
        self.create_widgets()

    def _fetch_current_data(self):
        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            try:
                # campaigns tiene: campaign_id, name, objective, start_date, budget, status
                query = "SELECT name, objective, start_date, budget, status FROM campaigns WHERE campaign_id = %s"
                cursor.execute(query, (self.item_id,))
                return cursor.fetchone()
            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al cargar datos: {err}")
                return None
            finally:
                cursor.close()
        return None
        
    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Modificar Campaña", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Nombre
        Label(main_frame, text="Nombre:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.name_entry = Entry(main_frame, font=FONT_MAIN)
        self.name_entry.insert(0, self.current_data['name'])
        self.name_entry.pack(fill='x', pady=(0, 10))

        # Objetivo
        Label(main_frame, text="Objetivo:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.obj_entry = Entry(main_frame, font=FONT_MAIN)
        self.obj_entry.insert(0, self.current_data['objective'])
        self.obj_entry.pack(fill='x', pady=(0, 10))

        # Presupuesto
        Label(main_frame, text="Presupuesto ($):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.budget_entry = Entry(main_frame, font=FONT_MAIN)
        self.budget_entry.insert(0, str(self.current_data['budget']))
        self.budget_entry.pack(fill='x', pady=(0, 10))
        
        # Fecha de Inicio
        Label(main_frame, text="Fecha Inicio (YYYY-MM-DD):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.start_date_entry = Entry(main_frame, font=FONT_MAIN)
        self.start_date_entry.insert(0, str(self.current_data['start_date']))
        self.start_date_entry.pack(fill='x', pady=(0, 10))
        
        # Estado
        Label(main_frame, text="Estado:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.status_var = StringVar(self)
        self.status_var.set(self.current_data['status'])
        opciones_status = ["Active", "Completed", "Paused"]
        status_menu = OptionMenu(main_frame, self.status_var, *opciones_status)
        status_menu.config(font=FONT_MAIN, bg=COLOR_BG_WHITE)
        status_menu.pack(fill='x', pady=(0, 10))
        
        Button(main_frame, text="Guardar Cambios", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.update_campaign).pack(pady=15)

    def update_campaign(self):
        name = self.name_entry.get()
        objective = self.obj_entry.get()
        budget_str = self.budget_entry.get()
        start_date_str = self.start_date_entry.get()
        status = self.status_var.get()
        
        if not all([name, objective, budget_str, start_date_str, status]):
            messagebox.showerror("Error", "Debe completar todos los campos.")
            return

        try:
            budget = float(budget_str)
            # Validación de formato de fecha simple
            datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "El presupuesto debe ser un número válido y la fecha debe estar en formato YYYY-MM-DD.")
            return

        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                update_query = "UPDATE campaigns SET name = %s, objective = %s, start_date = %s, budget = %s, status = %s WHERE campaign_id = %s"
                
                cursor.execute(update_query, (name, objective, start_date_str, budget, status, self.item_id)) 
                conn.commit()

                messagebox.showinfo("Éxito", f"Campaña ID {self.item_id} modificada correctamente.")
                self.refresh_callback()
                self.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al modificar campaña: {err}")
            finally:
                cursor.close()

class ModifyEmployeeDialog(Toplevel):
    def __init__(self, master, db_conn, refresh_callback, item_id):
        super().__init__(master)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.item_id = item_id 
        self.title(f"Modificar Empleado ID: {item_id}")
        self.geometry("500x600")
        self.configure(bg=COLOR_BG_WHITE)
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.current_data = self._fetch_current_data()
        if not self.current_data:
            messagebox.showerror("Error", "No se encontró el empleado a modificar.")
            self.destroy()
            return
        self.create_widgets()
    
    def _fetch_current_data(self):
        conn = self.db_conn
        if conn and conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            try:
                # employees tiene: employee_id, first_name, last_name, hire_date, salary, position
                query = "SELECT first_name, last_name, position, salary, hire_date FROM employees WHERE employee_id = %s"
                cursor.execute(query, (self.item_id,))
                return cursor.fetchone()
            except mysql.connector.Error as err:
                messagebox.showerror("Error de DB", f"Error al cargar datos: {err}")
                return None
            finally:
                cursor.close()
        return None

    def create_widgets(self):
        main_frame = Frame(self, bg=COLOR_BG_WHITE, padx=20, pady=10)
        main_frame.pack(fill="both", expand=True)

        Label(main_frame, text="Modificación de Empleado", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=10)

        # Nombre y Apellido
        Label(main_frame, text="Nombre:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.fname_entry = Entry(main_frame, font=FONT_MAIN)
        self.fname_entry.insert(0, self.current_data['first_name'])
        self.fname_entry.pack(fill='x', pady=(0, 10))
        
        Label(main_frame, text="Apellido:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.lname_entry = Entry(main_frame, font=FONT_MAIN)
        self.lname_entry.insert(0, self.current_data['last_name'])
        self.lname_entry.pack(fill='x', pady=(0, 10))

        # Posición
        Label(main_frame, text="Posición:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.pos_entry = Entry(main_frame, font=FONT_MAIN)
        self.pos_entry.insert(0, self.current_data['position'])
        self.pos_entry.pack(fill='x', pady=(0, 10))

        # Salario
        Label(main_frame, text="Salario:", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.salary_entry = Entry(main_frame, font=FONT_MAIN)
        self.salary_entry.insert(0, str(self.current_data['salary']))
        self.salary_entry.pack(fill='x', pady=(0, 10))

        # Fecha de Contratación
        Label(main_frame, text="Fecha Contratación (YYYY-MM-DD):", bg=COLOR_BG_WHITE, font=FONT_MAIN).pack(anchor='w', pady=(5,0))
        self.hire_date_entry = Entry(main_frame, font=FONT_MAIN)
        self.hire_date_entry.insert(0, str(self.current_data['hire_date']))
        self.hire_date_entry.pack(fill='x', pady=(0, 10))
        
        Button(main_frame, text="Guardar Cambios", bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
               font=FONT_MAIN, relief=FLAT, command=self.update_employee).pack(pady=15)

    def update_employee(self):
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
                messagebox.showerror("Error de DB", f"Error al modificar empleado: {err}")
            finally:
                cursor.close()