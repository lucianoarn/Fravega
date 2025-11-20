# content_area.py (VERSION SIN GESTIÓN DE USUARIOS)
from tkinter import Frame, Label, Button, LEFT, FLAT, BOTH, END, X, GROOVE, messagebox
# Importar módulos y constantes
from constants import *
# IMPORTACIÓN CORREGIDA: Se quita UserManagementView
from views import InventoryManagementView, FinanzasView, MarketingView, RRHHView 

class ContentArea:
    """
    Gestiona el área de contenido principal (debajo de la navbar), 
    incluyendo la barra lateral, el área de listado y el área de detalle.
    """
    def __init__(self, master, app_controller):
        self.master = master
        self.app_controller = app_controller # Referencia a GerenteHome
        self.current_detail_frame = None 
        
        self.content_container = Frame(self.master, bg=COLOR_BG_WHITE)
        self.content_container.grid(row=1, column=0, sticky="nswe")
        
        # Configuración de columnas: 
        # Col 0: Menú Lateral (Fijo)
        # Col 1: Área de Lista/Alertas/KPIs (Fijo, pequeño)
        # Col 2: Área de Detalle/Tabla (Expande)
        self.content_container.grid_columnconfigure(0, weight=0, minsize=200) 
        self.content_container.grid_columnconfigure(1, weight=0, minsize=300) 
        self.content_container.grid_columnconfigure(2, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        self._create_layout_frames()
        self._populate_main_menu()
        self.show_dashboard() # Mostrar el dashboard por defecto

    def _create_layout_frames(self):
        """Configura el área principal de contenido con separadores verticales."""
        # 1. Menú Principal (SideBar) - Columna 0
        self.sidebar_frame = Frame(self.content_container, bg=COLOR_SIDEBAR, width=200, relief=GROOVE, bd=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nswe")
        
        # 2. Área de Lista/Alertas (List Area) - Columna 1
        self.list_area = Frame(self.content_container, bg=COLOR_BG_WHITE, width=300)
        self.list_area.grid(row=0, column=1, sticky="nswe")
        
        # Separador entre Lista y Detalle
        separator = Frame(self.content_container, bg=COLOR_BORDER_LIGHT, width=1)
        separator.grid(row=0, column=2, sticky="nsw")
        
        # 3. Área de Detalle/Tabla (Detail Area) - Columna 2
        self.detail_area = Frame(self.content_container, bg=COLOR_BG_WHITE)
        self.detail_area.grid(row=0, column=2, sticky="nswe", padx=(1, 0))
        self.detail_area.grid_columnconfigure(0, weight=1)
        self.detail_area.grid_rowconfigure(0, weight=1)
        
    def _populate_main_menu(self):
        """Crea los botones de navegación del menú lateral."""
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard),
            # Se ha eliminado "👥 Gestión de Usuarios"
            ("📦 Gestión de Inventario", self.show_inventory_list),
            ("💰 Gestión de Finanzas", self.show_finance_list),
            ("📈 Gestión de Marketing", self.show_marketing_list),
            ("🧑‍💼 Gestión de RRHH", self.show_rrhh_list),
            ("📄 Reportes y Archivos", self.show_reports_list),
        ]
        
        for text, command in menu_items:
            Button(self.sidebar_frame, text=text, font=FONT_MAIN, bg=COLOR_SIDEBAR, 
                   fg=COLOR_TEXT_HEADING, relief=FLAT, anchor='w', padx=15,
                   activebackground='#e5e5e5', activeforeground=COLOR_ACCENT,
                   command=command).pack(fill=X, pady=2, ipady=5)

    def create_list_card(self, title, subtitle, note, command):
        """Crea una tarjeta de información en el área de lista."""
        card = Frame(self.list_area, bg=COLOR_CARD_BG, padx=10, pady=5, relief=GROOVE, bd=1)
        card.pack(fill=X, padx=10, pady=5)
        
        Label(card, text=title, font=FONT_MAIN, bg=COLOR_CARD_BG, fg=COLOR_TEXT_HEADING).pack(anchor='w')
        Label(card, text=subtitle, font=('Segoe UI', 9), bg=COLOR_CARD_BG, fg=COLOR_TEXT_NORMAL).pack(anchor='w')
        
        btn = Button(card, text=note, font=('Segoe UI', 8, 'bold'), bg=COLOR_ACCENT, fg=COLOR_BG_WHITE, 
                     relief=FLAT, command=command)
        btn.pack(pady=5, side=LEFT)

    def switch_detail_frame(self, ViewClass):
        """Destruye la vista actual y crea una nueva en el área de detalle."""
        if self.current_detail_frame:
            self.current_detail_frame.destroy()
            
        # El constructor de la vista debe usar self.detail_area como master_frame
        view_instance = ViewClass(self.detail_area, self.app_controller)
        self.current_detail_frame = view_instance.frame
        self.current_detail_frame.grid(row=0, column=0, sticky="nsew")

    def clear_list_area(self):
        """Limpia todos los widgets del área de lista."""
        for widget in self.list_area.winfo_children():
            widget.destroy()

    # =================================================================
    # VISTAS DE CONTENIDO (Ahora cargan la tabla/detalle directamente)
    # =================================================================

    def show_dashboard(self):
        self.clear_list_area()
        
        # Simulación de tarjetas de lista/kpis para el dashboard
        header_list_frame = Frame(self.list_area, bg=COLOR_BG_WHITE, padx=10, pady=5)
        header_list_frame.pack(fill='x')
        Label(header_list_frame, text="Resumen General", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=0, anchor='w')
        
        self.create_list_card("Cantidad de empleados", "", "Ver RRHH", self.show_rrhh_list) # Actualizado
        self.create_list_card("Cantidad de Stock", "", "Ver Alertas", self.show_inventory_list)
        self.create_list_card("Ventas", "", "Ver Ventas", self.show_finance_list)
        
        # Carga una vista de "Dashboard" por defecto en el área central
        self.switch_detail_frame(DefaultDetailView) 
        
    # **La función show_user_management_list ha sido ELIMINADA**

    def show_inventory_list(self):
        self.clear_list_area()
        
        header_list_frame = Frame(self.list_area, bg=COLOR_BG_WHITE, padx=10, pady=5)
        header_list_frame.pack(fill='x')
        Label(header_list_frame, text="Alertas de Stock", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=0, anchor='w')
        
        items = [
            ("Tv Samsung", "Stock: 10", "Pedir Reposición", lambda: self._create_default_detail("Inventario", "Pedir TV Samsung")),
        ]
        if not items:
            Label(self.list_area, text="No hay alertas de inventario.", font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=20, padx=5)

        for title, subtitle, note, command in items:
            self.create_list_card(title, subtitle, note, command)

        # Muestra la tabla de Gestión de Inventario en el centro (row=2)
        self.switch_detail_frame(InventoryManagementView)
        
    def show_finance_list(self):
        self.clear_list_area()
        
        # Información relevante para la barra lateral
        header_list_frame = Frame(self.list_area, bg=COLOR_BG_WHITE, padx=10, pady=5)
        header_list_frame.pack(fill='x')
        Label(header_list_frame, text="Resumen Finanzas", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=0, anchor='w')
        
        self.create_list_card("Margen de Ganancia", "15%", "Ver Análisis", lambda: self._create_default_detail("Finanzas", "Análisis Margen"))
        
        
        # Muestra la tabla de Gestión de Finanzas en el centro (row=2)
        self.switch_detail_frame(FinanzasView)

    def show_marketing_list(self):
        self.clear_list_area()
        
        # Información relevante para la barra lateral
        header_list_frame = Frame(self.list_area, bg=COLOR_BG_WHITE, padx=10, pady=5)
        header_list_frame.pack(fill='x')
        Label(header_list_frame, text="Resumen de Campañas", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=0, anchor='w')
        

        
        # Muestra la tabla de Gestión de Marketing en el centro (row=2)
        self.switch_detail_frame(MarketingView)

    def show_rrhh_list(self):
        self.clear_list_area()
        
        # Información relevante para la barra lateral
        header_list_frame = Frame(self.list_area, bg=COLOR_BG_WHITE, padx=10, pady=5)
        header_list_frame.pack(fill='x')
        Label(header_list_frame, text="Alertas de Personal", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=0, anchor='w')
        
        self.create_list_card("Ausencias Hoy", "2 Empleados", "Ver Lista", lambda: self._create_default_detail("RRHH", "Ausencias"))
        
        
        # Muestra la tabla de Gestión de RRHH en el centro (row=2)
        self.switch_detail_frame(RRHHView)

    def show_reports_list(self):
        self.clear_list_area()
        
        header_list_frame = Frame(self.list_area, bg=COLOR_BG_WHITE, padx=10, pady=5)
        header_list_frame.pack(fill='x')
        Label(header_list_frame, text="Archivos Recientes", font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=0, anchor='w')
        
        items = [

        ]
        if not items:
            Label(self.list_area, text="No hay archivos recientes.", font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=20, padx=5)

        for title, subtitle, note, command in items:
            self.create_list_card(title, subtitle, note, command)

        # Carga una vista de "Reportes" por defecto en el área central
        self.switch_detail_frame(DefaultDetailView) 
    
    def _create_default_detail(self, module, detail):
        """Función auxiliar para mostrar contenido de ejemplo en el área de detalle."""
        # Usa una lambda para crear la vista con argumentos dinámicos
        self.switch_detail_frame(lambda master, app: DefaultDetailView(master, app, module, detail))

class DefaultDetailView:
    """Vista de detalle por defecto/placeholder."""
    def __init__(self, master_frame, home_app, module="Bienvenido", detail="Selecciona una opción del menú"):
        self.frame = Frame(master_frame, bg=COLOR_BG_WHITE, padx=30, pady=30)
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1) # Centrar contenido
        
        content_frame = Frame(self.frame, bg=COLOR_BG_WHITE)
        # Usamos grid en el content_frame para centrar el contenido en el medio de toda la vista
        content_frame.grid(row=0, column=0, sticky="") 
        
        Label(content_frame, text=f"Módulo: {module}", font=FONT_HEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_HEADING).pack(pady=10)
        Label(content_frame, text=f"Acción: {detail}", font=FONT_SUBHEADING, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=5)
        Label(content_frame, text="El detalle de la información seleccionada aparecerá aquí.", font=FONT_MAIN, 
              bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=20)