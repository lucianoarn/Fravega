# home_gerente.py (Main App)
from tkinter import Tk, messagebox, PhotoImage
import sys
import mysql.connector
# Importar módulos de componentes
from constants import COLOR_BG_WHITE
from navbar import TopNavbar
from content_area import ContentArea

# =================================================================
# CLASE PRINCIPAL DEL HOME
# =================================================================

class GerenteHome:
    def __init__(self, master, username):
        self.master = master
        master.title(f"Panel de Control | Gerente: {username}")
        master.configure(bg=COLOR_BG_WHITE)
        self.username = username
        
        # Configuración de DB
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
        
        # Carga de imágenes
        self.fravega_logo, self.user_icon = self.load_images()

        # 1. Navbar
        # Delega la creación de la barra superior a TopNavbar
        self.navbar = TopNavbar(master, self.username, self.logout, self.fravega_logo, self.user_icon)
        
        # 2. Área de Contenido (Sidebar, Listado, Detalle)
        # Delega la creación de las 3 columnas y la lógica de navegación a ContentArea
        self.content_area = ContentArea(master, self)
        
        # Iniciar con la vista por defecto (Llamando al método dentro de ContentArea)
        self.content_area.show_dashboard_list() 

    def create_db_connection(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", 
                                 f"No se pudo conectar a MySQL.\nAsegúrate que XAMPP esté corriendo. Error: {err}")
            return None

    def load_images(self):
        fravega_logo = None
        user_icon = None
        try:
            fravega_logo = PhotoImage(file='Fravega.png').subsample(x=2, y=2)
        except Exception:
            pass
        try:
            # Asumiendo que 'user_icon.png' existe en el mismo directorio.
            user_icon = PhotoImage(file='user_icon.png').subsample(x=2, y=2) 
        except Exception:
            pass
        return fravega_logo, user_icon

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que quieres cerrar la sesión?"):
            if self.db_conn and self.db_conn.is_connected():
                self.db_conn.close()
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