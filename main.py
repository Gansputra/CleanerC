import customtkinter as ctk
import psutil
import os

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
        self.main_container.grid_rowconfigure(2, weight=1) # Log area expands

        # 1. Header Section
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="System Overview", 
            font=ctk.CTkFont(family="Inter", size=32, weight="bold")
        )
        self.title_label.pack(side="left")

        self.status_badge = ctk.CTkLabel(
            self.header_frame,
            text="● SYSTEM SECURE",
            text_color="#2ecc71",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#dbf9e1", "#1e3a24"),
            padx=10,
            pady=5,
            corner_radius=10
        )
        self.status_badge.pack(side="right")

        # 2. Top Section: Stats Cards
        self.stats_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1, pad=20)

        self.card_total = self.create_stat_card(self.stats_frame, "Total Capacity", "...", "#3498db", 0)
        self.card_used = self.create_stat_card(self.stats_frame, "Used Space", "...", "#e74c3c", 1)
        self.card_free = self.create_stat_card(self.stats_frame, "Free Space", "...", "#2ecc71", 2)


        # 3. Middle Section: Actions & Log Layout
        # Creating a combined frame for Buttons and Logs
        self.work_area = ctk.CTkFrame(self.main_container, corner_radius=20, fg_color=("#f2f2f2", "#2b2b2b"))
        self.work_area.grid(row=2, column=0, sticky="nsew")
        self.work_area.grid_columnconfigure(0, weight=1)
        self.work_area.grid_rowconfigure(1, weight=1)

        # Action Buttons Ribbon
        self.actions_frame = ctk.CTkFrame(self.work_area, fg_color="transparent")
        self.actions_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        self.btn_analyze = ctk.CTkButton(
            self.actions_frame, text="Quick Analysis", 
            width=150, height=40, font=ctk.CTkFont(weight="bold"),
            command=lambda: self.log_message("Starting system analysis...")
        )
        self.btn_analyze.pack(side="left", padx=(0, 10))

        self.btn_clean = ctk.CTkButton(
            self.actions_frame, text="Start Cleaning", 
            fg_color="#e74c3c", hover_color="#c0392b",
            width=150, height=40, font=ctk.CTkFont(weight="bold"),
            command=lambda: self.log_message("Warning: Cleaning logic not implemented yet.")
        )
        self.btn_clean.pack(side="left", padx=10)

        self.btn_refresh = ctk.CTkButton(
            self.actions_frame, text="Refresh", 
            width=100, height=40, fg_color="gray40",
            command=self.update_disk_info
        )
        self.btn_refresh.pack(side="right")

        # Log/Output Panel
        self.log_label = ctk.CTkLabel(self.work_area, text="Activity Log", font=ctk.CTkFont(size=14, weight="bold"))
        self.log_label.grid(row=1, column=0, sticky="nw", padx=25)

        self.log_textbox = ctk.CTkTextbox(
            self.work_area, 
            corner_radius=10,
            font=ctk.CTkFont(family="Consolas", size=12),
            border_width=2,
            border_color=("#d1d1d1", "#3d3d3d")
        )
        self.log_textbox.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 20))
        self.log_textbox.insert("0.0", "Welcome to CleanerC Engine v1.0\nReady for operation.\n" + "-"*30 + "\n")
        self.log_textbox.configure(state="disabled")

        # Update disk info on startup (UI components must be initialized first)
        self.update_disk_info()

    def create_stat_card(self, parent, title, value, color, column):
        card = ctk.CTkFrame(parent, height=120, corner_radius=15)
        card.grid(row=0, column=column, sticky="ew", padx=5)
        
        title_lbl = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13, weight="normal"), text_color="gray")
        title_lbl.pack(pady=(15, 0), padx=20, anchor="nw")
        
        value_lbl = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"), text_color=color)
        value_lbl.pack(pady=(5, 15), padx=20, anchor="nw")
        
        # Keep a reference to the label so it can be updated
        card.value_label = value_lbl
        return card

    def update_disk_info(self):
        try:
            # Get usage for C:\ on Windows
            disk = psutil.disk_usage('C:\\')
            
            # Helper to convert bytes to GB
            to_gb = lambda b: f"{b / (1024**3):.1f} GB"
            
            # Update labels
            self.card_total.value_label.configure(text=to_gb(disk.total))
            self.card_used.value_label.configure(text=to_gb(disk.used))
            self.card_free.value_label.configure(text=to_gb(disk.free))
            
            self.log_message(f"Disk C fetched: {to_gb(disk.free)} free of {to_gb(disk.total)}")
            
        except Exception as e:
            self.log_message(f"Error fetching disk info: {str(e)}")

    def log_message(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"[{type(self).__name__}] {message}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

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

