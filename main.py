import customtkinter as ctk

class CleanerCApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("CleanerC - Modern Disk Optimizer")
        self.geometry("1000x650")
        self.minsize(850, 550)

        # Set appearance to dark mode by default
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Layout Grid Configuration ---
        # Column 0: Sidebar, Column 1: Main Content
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar UI ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Push bottom items down

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="CleanerC 🧹", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40))

        # Sidebar Buttons
        self.btn_dashboard = self.create_nav_button("Dashboard", 1)
        self.btn_cleaner = self.create_nav_button("Disk Cleaner", 2)
        self.btn_tools = self.create_nav_button("System Tools", 3)

        # Appearance Switcher at the bottom
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # --- Main Content UI ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # Header Section
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="System Status: Good", 
            font=ctk.CTkFont(family="Inter", size=32, weight="bold")
        )
        self.title_label.pack(side="left")

        # Content Area
        self.content_frame = ctk.CTkFrame(self.main_container, corner_radius=20)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        
        # Center Content
        self.center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.welcome_msg = ctk.CTkLabel(
            self.center_frame, 
            text="CleanerC is ready to scan", 
            font=ctk.CTkFont(size=18)
        )
        self.welcome_msg.pack(pady=10)

        self.scan_btn = ctk.CTkButton(
            self.center_frame, 
            text="Analyze Disk", 
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=220,
            corner_radius=10
        )
        self.scan_btn.pack(pady=20)

    def create_nav_button(self, text, row):
        button = ctk.CTkButton(
            self.sidebar_frame, 
            text=text, 
            corner_radius=10, 
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
        )
        button.grid(row=row, column=0, padx=20, pady=10, sticky="ew")
        return button

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = CleanerCApp()
    app.mainloop()

