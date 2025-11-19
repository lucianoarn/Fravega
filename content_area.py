# content_area.py
from tkinter import Frame, Label, Button, LEFT, FLAT, BOTH, END, X, GROOVE
# Importar módulos
from constants import *
from views import UserManagementView, InventoryManagementView

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
        
        self.content_container.grid_columnconfigure(0, weight=0, minsize=200) 
        self.content_container.grid_columnconfigure(1, weight=0, minsize=300) 
        self.content_container.grid_columnconfigure(2, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        self._create_layout_frames()
        self._populate_main_menu()
        
    def _create_layout_frames(self):
        """Configura el área principal de contenido con separadores verticales y borde derecho final."""
        # 1. Menú Principal (Sidebar) - Borde a la derecha
        self.main_menu = Frame(self.content_container, width=200, bg=COLOR_SIDEBAR, 
                               highlightbackground=COLOR_BORDER_LIGHT, highlightcolor=COLOR_BORDER_LIGHT, 
                               highlightthickness=1) 
        self.main_menu.grid(row=0, column=0, sticky="nswe") 
        self.main_menu.pack_propagate(False) 
        
        # 2. Área de Listado (Central) - Borde a la derecha
        self.list_area = Frame(self.content_container, width=300, bg=COLOR_BG_WHITE, 
                               highlightbackground=COLOR_BORDER_LIGHT, highlightcolor=COLOR_BORDER_LIGHT, 
                               highlightthickness=1) 
        self.list_area.grid(row=0, column=1, sticky="nswe")
        self.list_area.pack_propagate(False)

        # 3. Área de Detalle (Derecha) - Borde a la derecha
        self.detail_area = Frame(self.content_container, bg=COLOR_BG_WHITE,
                                 highlightbackground=COLOR_BORDER_LIGHT, highlightcolor=COLOR_BORDER_LIGHT, 
                                 highlightthickness=1) 
        self.detail_area.grid(row=0, column=2, sticky="nswe") 
        self.detail_area.grid_columnconfigure(0, weight=1)
        self.detail_area.grid_rowconfigure(0, weight=1)

    def _populate_main_menu(self):
        """Crea los botones del menú lateral."""
        self.buttons_data = [
            ("📊 Dashboard", self.show_dashboard_list),
            ("👥 Gestión Usuarios", self.show_user_management_list),
            ("📦 Inventario", self.show_inventory_list),
            ("📝 Reportes", self.show_reports_list),
        ]
        
        for text, command in self.buttons_data:
            self._create_menu_button(text, command)
            
    def _create_menu_button(self, text, command):
        btn = Button(self.main_menu, text=text, bg=COLOR_SIDEBAR, fg=COLOR_TEXT_NORMAL, 
                     font=FONT_MAIN, relief=FLAT, anchor='w', padx=20,
                     activebackground=COLOR_ACCENT, activeforeground=COLOR_BG_WHITE,
                     command=command)
        btn.pack(fill='x', ipady=10, pady=(10, 1)) 
        
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#e0e0e0'))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_SIDEBAR))

    def switch_detail_frame(self, new_view_class):
        """Destruye el frame de detalle actual y crea una nueva vista."""
        if self.current_detail_frame is not None:
            self.current_detail_frame.destroy()
            
        # Instancia la nueva vista pasándole el frame contenedor y el controlador principal
        new_view_instance = new_view_class(self.detail_area, self.app_controller)
        self.current_detail_frame = new_view_instance.frame

    def _create_default_detail(self, module, title):
        """Crea una vista de detalle genérica para módulos no complejos."""
        if self.current_detail_frame is not None:
            self.current_detail_frame.destroy()

        self.current_detail_frame = Frame(self.detail_area, bg=COLOR_BG_WHITE, padx=30, pady=5) 
        self.current_detail_frame.grid(row=0, column=0, sticky="nswe")
        self.current_detail_frame.grid_columnconfigure(0, weight=1)
        
        Label(self.current_detail_frame, text=f"{module}: {title}", 
              font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).pack(pady=(0, 20), anchor='w')

        Label(self.current_detail_frame, text=f"Área de Detalle para {module}. Aquí se muestra la información específica de '{title}' y la funcionalidad de edición.", justify=LEFT,
              font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=10, anchor='w')

    def _create_dashboard_detail(self, title):
        """Crea la vista de detalle del Dashboard (Placeholder)."""
        if self.current_detail_frame is not None:
            self.current_detail_frame.destroy()
            
        self.current_detail_frame = Frame(self.detail_area, bg=COLOR_BG_WHITE, padx=30, pady=5) 
        self.current_detail_frame.grid(row=0, column=0, sticky="nswe")
        self.current_detail_frame.grid_columnconfigure(0, weight=1)
        self.current_detail_frame.grid_rowconfigure(1, weight=1)

        Label(self.current_detail_frame, text=f"Dashboard: {title}", 
              font=FONT_SUBHEADING, bg=COLOR_BG_WHITE, fg=COLOR_ACCENT).grid(row=0, column=0, sticky="w", pady=(0, 10))

        placeholder = Label(self.current_detail_frame, 
                            text="ÁREA DE TRABAJO DEL DASHBOARD\n\nAquí debes agregar los GRÁFICOS y MÉTICAS que necesita el Gerente (Ventas, Stock, etc.).", 
                            font=('Segoe UI', 12, 'italic'), bg=COLOR_CARD_BG, fg=COLOR_TEXT_NORMAL,
                            height=15, relief='groove')
        placeholder.grid(row=1, column=0, sticky="nswe", padx=10, pady=20)

    # =================================================================
    # VISTAS DE LISTADO (LÓGICA DEL BOTÓN)
    # =================================================================

    def clear_list_area(self):
        for widget in self.list_area.winfo_children():
            widget.destroy()

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

        Label(self.list_area, text="la lista completa de 'Gestión de Usuarios'.", font=FONT_MAIN, bg=COLOR_BG_WHITE, fg=COLOR_TEXT_NORMAL).pack(pady=20, padx=5)
            
        self.switch_detail_frame(UserManagementView)

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

        self.switch_detail_frame(InventoryManagementView)

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