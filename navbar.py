# navbar.py
from tkinter import Frame, Label, Button, LEFT, RIGHT, FLAT
# Importar constantes
from constants import *

class TopNavbar:
    """Clase que representa y construye la barra de navegación superior."""
    def __init__(self, master, username, logout_command, fravega_logo, user_icon):
        self.frame = Frame(master, height=50, bg=COLOR_NAVBAR_BG)
        self.frame.grid(row=0, column=0, sticky="ew")
        self.fravega_logo = fravega_logo
        self.user_icon = user_icon
        self.username = username
        self.logout_command = logout_command

        self.frame.grid_columnconfigure(0, weight=1) 
        self.frame.grid_columnconfigure(1, weight=1) 
        self.frame.grid_columnconfigure(2, weight=0) 

        self.create_widgets()

    def create_widgets(self):
        if self.fravega_logo:
            Label(self.frame, image=self.fravega_logo, bg=COLOR_NAVBAR_BG).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        else:
            Label(self.frame, text="[Fravega Logo]", bg=COLOR_NAVBAR_BG, fg=COLOR_TEXT_HEADING, font=FONT_MAIN).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        Label(self.frame, text="Gerencia | Admin", bg=COLOR_NAVBAR_BG, fg=COLOR_TEXT_HEADING, 
              font=('Segoe UI', 16, 'bold')).grid(row=0, column=1, sticky="nswe", pady=10)

        user_controls_frame = Frame(self.frame, bg=COLOR_NAVBAR_BG)
        user_controls_frame.grid(row=0, column=2, sticky="e", padx=10)

        logout_btn = Button(user_controls_frame, text="🚪 Cerrar Sesión", bg=COLOR_NAVBAR_BG, fg=COLOR_TEXT_NORMAL, font=('Segoe UI', 10), relief=FLAT, activebackground='#d0d0d0', activeforeground=COLOR_ACCENT, command=self.logout_command)
        logout_btn.pack(side=RIGHT, padx=(5, 0))
        
        Label(user_controls_frame, text=self.username, bg=COLOR_NAVBAR_BG, fg=COLOR_TEXT_HEADING, 
              font=('Segoe UI', 10, 'bold')).pack(side=RIGHT, padx=(10, 5))

        if self.user_icon:
            Label(user_controls_frame, image=self.user_icon, bg=COLOR_NAVBAR_BG).pack(side=RIGHT, pady=5)
        else:
            Label(user_controls_frame, text="👤", bg=COLOR_NAVBAR_BG, fg=COLOR_TEXT_HEADING, font=('Segoe UI', 16)).pack(side=RIGHT, pady=5)