import customtkinter as ctk
import os
import psutil
import threading
import tkinter as tk
import ctypes
import platform
import wmi
import GPUtil
import webbrowser
import time
from datetime import datetime, timedelta
from tkinter import messagebox
from send2trash import send2trash

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

        # --- Cleaning Targets ---
        self.clean_targets = {
            "User Temp": os.environ.get('TEMP'),
            "System Temp": os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'),
            "Prefetch": os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch'),
            "Recycle Bin": "C:\\$Recycle.Bin"
        }

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
        self.btn_dashboard = self.create_nav_button("Dashboard", 1, "dashboard")
        self.btn_cleaner = self.create_nav_button("Disk Cleaner", 2, "cleaner")
        self.btn_tools = self.create_nav_button("System Tools", 3, "tools")

        # Appearance Switcher at the bottom
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # --- Author Section ---
        self.author_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.author_frame.grid(row=7, column=0, padx=20, pady=(20, 20), sticky="ew")
        
        self.author_label = ctk.CTkLabel(
            self.author_frame, 
            text="Author: Gansputra", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        self.author_label.pack(anchor="w")

        self.github_btn = ctk.CTkButton(
            self.author_frame, text="GitHub", 
            height=24, font=ctk.CTkFont(size=11),
            fg_color="gray30", hover_color="gray20",
            command=lambda: webbrowser.open("https://github.com/Gansputra/")
        )
        self.github_btn.pack(fill="x", pady=(5, 2))

        self.insta_btn = ctk.CTkButton(
            self.author_frame, text="Instagram", 
            height=24, font=ctk.CTkFont(size=11),
            fg_color="#E1306C", hover_color="#C13584",
            command=lambda: webbrowser.open("https://instagram.com/gans.putra_")
        )
        self.insta_btn.pack(fill="x", pady=2)

        # --- Main Content UI ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=(40, 40), pady=(40, 40), sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # 1. Dashboard Frame
        self.dashboard_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        
        self.header_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, text="System Overview", 
            font=ctk.CTkFont(family="Inter", size=32, weight="bold")
        )
        self.title_label.pack(side="left")

        self.status_badge = ctk.CTkLabel(
            self.header_frame, text="● SYSTEM SECURE",
            text_color="#2ecc71", font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#dbf9e1", "#1e3a24"), padx=10, pady=5, corner_radius=10
        )
        self.status_badge.pack(side="right")

        self.stats_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1, pad=20)

        self.card_total = self.create_stat_card(self.stats_frame, "Total Capacity", "...", "#3498db", 0, 0)
        self.card_used = self.create_stat_card(self.stats_frame, "Used Space", "...", "#e74c3c", 1, 0)
        self.card_free = self.create_stat_card(self.stats_frame, "Free Space", "...", "#2ecc71", 2, 0)

        # CPU Card in new row
        cpu_name = platform.processor()
        # Clean up CPU name for Windows if possible
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            cpu_name = winreg.QueryValueEx(key, "ProcessorNameString")[0]
        except:
            pass
            
        self.card_cpu = self.create_stat_card(self.stats_frame, "CPU Metrics", "0%", "#9b59b6", 0, 1, subtitle=cpu_name)

        # GPU Card
        gpu_name = "Unknown GPU"
        try:
            w = wmi.WMI()
            for gpu in w.Win32_VideoController():
                gpu_name = gpu.Name
                break
        except:
            pass
            
        self.card_gpu = self.create_stat_card(self.stats_frame, "GPU Metrics", "0%", "#f1c40f", 0, 2, subtitle=gpu_name)
        
        # System Info Card
        os_info = f"{platform.system()} {platform.release()} (Build {platform.version()})"
        self.card_system = self.create_stat_card(self.stats_frame, "System Information", "...", "#2980b9", 0, 3, subtitle=os_info)

        # Start recurring updates for CPU, GPU & Uptime
        self.update_system_stats()

        # 2. Disk Cleaner Frame
        self.cleaner_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.cleaner_frame.grid_columnconfigure(0, weight=1)
        self.cleaner_frame.grid_rowconfigure(0, weight=1)

        self.work_area = ctk.CTkFrame(self.cleaner_frame, corner_radius=20, fg_color=("#f2f2f2", "#2b2b2b"))
        self.work_area.grid(row=0, column=0, sticky="nsew")
        self.work_area.grid_columnconfigure(0, weight=1)
        self.work_area.grid_rowconfigure(3, weight=1)

        self.actions_frame = ctk.CTkFrame(self.work_area, fg_color="transparent")
        self.actions_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        self.btn_analyze = ctk.CTkButton(
            self.actions_frame, text="Scan", width=150, height=40, 
            font=ctk.CTkFont(weight="bold"), command=self.start_analysis_thread
        )
        self.btn_analyze.pack(side="left", padx=(0, 10))

        self.btn_clean = ctk.CTkButton(
            self.actions_frame, text="Start Cleaning", fg_color="#e74c3c", 
            hover_color="#c0392b", width=150, height=40, font=ctk.CTkFont(weight="bold"),
            command=self.start_cleaning_thread
        )
        self.btn_clean.pack(side="left", padx=10)

        self.btn_refresh = ctk.CTkButton(
            self.actions_frame, text="Refresh", width=100, height=40, 
            fg_color="gray40", command=self.update_disk_info
        )
        self.btn_refresh.pack(side="right")

        self.progress_frame = ctk.CTkFrame(self.work_area, fg_color="transparent")
        self.progress_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=(0, 10))
        self.progress_frame.grid_columnconfigure(0, weight=1)

        self.status_text_var = ctk.StringVar(value="System Ready")
        self.status_label = ctk.CTkLabel(
            self.progress_frame, textvariable=self.status_text_var,
            font=ctk.CTkFont(size=12, slant="italic"), text_color="gray"
        )
        self.status_label.grid(row=0, column=0, sticky="w")

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, height=8, progress_color="#3498db")
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(5, 15))
        self.progress_bar.set(0)

        self.log_label = ctk.CTkLabel(self.work_area, text="Activity Log", font=ctk.CTkFont(size=14, weight="bold"))
        self.log_label.grid(row=2, column=0, sticky="nw", padx=25)

        self.log_textbox = ctk.CTkTextbox(
            self.work_area, corner_radius=10, font=ctk.CTkFont(family="Consolas", size=12),
            border_width=2, border_color=("#d1d1d1", "#3d3d3d")
        )
        self.log_textbox.grid(row=3, column=0, sticky="nsew", padx=20, pady=(5, 20))
        self.log_textbox.insert("0.0", "Welcome to CleanerC Engine v1.0\nReady for operation.\n" + "-"*30 + "\n")
        self.log_textbox.configure(state="disabled")

        # 3. System Tools Frame (Placeholder)
        self.tools_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.tools_label = ctk.CTkLabel(
            self.tools_frame, text="System Tools Coming Soon", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.tools_label.pack(expand=True)

        # Initialize navigation
        self.select_frame_by_name("dashboard")
        self.update_disk_info()

    def create_stat_card(self, parent, title, value, color, column, row=0, subtitle=None):
        card = ctk.CTkFrame(parent, height=120, corner_radius=15)
        card.grid(row=row, column=column, columnspan=3 if row > 0 else 1, sticky="ew", padx=5, pady=5)
        
        title_lbl = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13, weight="normal"), text_color="gray")
        title_lbl.pack(pady=(15, 0), padx=20, anchor="nw")
        
        if subtitle:
            sub_lbl = ctk.CTkLabel(card, text=subtitle, font=ctk.CTkFont(size=11, weight="normal"), text_color="gray60")
            sub_lbl.pack(padx=20, anchor="nw")

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

    def update_system_stats(self):
        try:
            # CPU Update
            cpu_usage = psutil.cpu_percent()
            self.card_cpu.value_label.configure(text=f"{cpu_usage}%")
            
            # Change color based on load
            if cpu_usage > 80:
                self.card_cpu.value_label.configure(text_color="#e74c3c")
            elif cpu_usage > 50:
                self.card_cpu.value_label.configure(text_color="#f39c12")
            else:
                self.card_cpu.value_label.configure(text_color="#9b59b6")

            # GPU Update
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_usage = gpus[0].load * 100
                self.card_gpu.value_label.configure(text=f"{gpu_usage:.1f}%")
                
                # Change color based on load
                if gpu_usage > 80:
                    self.card_gpu.value_label.configure(text_color="#e74c3c")
                elif gpu_usage > 50:
                    self.card_gpu.value_label.configure(text_color="#f39c12")
                else:
                    self.card_gpu.value_label.configure(text_color="#f1c40f")
            else:
                self.card_gpu.value_label.configure(text="N/A", text_color="gray")

            # Uptime Update
            boot_time_timestamp = psutil.boot_time()
            uptime_seconds = time.time() - boot_time_timestamp
            uptime_str = str(timedelta(seconds=int(uptime_seconds)))
            self.card_system.value_label.configure(text=f"Uptime: {uptime_str}")

        except Exception:
            pass
            
        # Schedule next update in 1 second
        self.after(1000, self.update_system_stats)

    def get_folder_size(self, folder_path):
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    # Skip if it is a symbolic link
                    if not os.path.islink(fp):
                        try:
                            total_size += os.path.getsize(fp)
                        except (OSError, PermissionError):
                            # Skip files that are currently in use or protected
                            continue
        except Exception as e:
            self.log_message(f"Error scanning {folder_path}: {str(e)}")
        return total_size

    def format_size(self, size_bytes):
        if size_bytes == 0: return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def start_analysis_thread(self):
        # Run scan in a separate thread
        analysis_thread = threading.Thread(target=self.run_analysis)
        analysis_thread.daemon = True
        analysis_thread.start()

    def run_analysis(self):
        self.btn_analyze.configure(state="disabled", text="Scanning...")
        self.btn_clean.configure(state="disabled")
        self.progress_bar.set(0)
        
        self.log_message("INITIALIZING SCAN...")
        self.log_message("-" * 40)
        self.total_junk_found = 0
        targets = list(self.clean_targets.items())
        total_targets = len(targets)
        
        for i, (name, path) in enumerate(targets):
            progress = (i + 1) / total_targets
            self.status_text_var.set(f"Analyzing: {name}...")
            self.progress_bar.set(progress)
            
            try:
                if path and os.path.exists(path):
                    self.log_message(f"Scanning: {name}")
                    size = self.get_folder_size(path)
                    self.total_junk_found += size
                    self.log_message(f" > Content Size: {self.format_size(size)}")
                else:
                    self.log_message(f"Skipped: {name} (Directory not found)")
            except Exception as e:
                self.log_message(f"Error checking {name}: {str(e)}")
        
        self.log_message("-" * 40)
        self.log_message(f"TOTAL RECLAIMABLE SPACE: {self.format_size(self.total_junk_found)}")
        self.log_message("Scan complete. System ready for optimization.")
        
        self.status_text_var.set("Scan Complete")
        self.btn_analyze.configure(state="normal", text="Scan")
        self.btn_clean.configure(state="normal")

        # Update status badge based on results
        if self.total_junk_found > 1024 * 1024 * 100: # > 100 MB
            self.status_badge.configure(text="● ACTION RECOMMENDED", text_color="#e67e22", fg_color=("#fef5e7", "#3e2723"))
        elif self.total_junk_found > 0:
            self.status_badge.configure(text="● OPTIMIZABLE", text_color="#3498db", fg_color=("#ebf5fb", "#1a3a5a"))

    def start_cleaning_thread(self):
        # Check if scan has been run
        if not hasattr(self, 'total_junk_found') or self.total_junk_found == 0:
            messagebox.showinfo("No Junk Found", "Please run a 'Scan' first or no junk files were detected.")
            return

        # Ask for confirmation before cleaning
        confirm = messagebox.askyesno(
            "Confirm Optimization", 
            f"Are you sure you want to move approximately {self.format_size(self.total_junk_found)} of junk files to the Recycle Bin?\n\n"
            "This will help reclaim storage space safely."
        )
        
        if confirm:
            # Run cleaning in a separate thread to keep UI responsive
            cleaning_thread = threading.Thread(target=self.run_cleaning)
            cleaning_thread.daemon = True
            cleaning_thread.start()

    def run_cleaning(self):
        self.log_message("STARTING CLEANING PROCESS...")
        self.log_message("-" * 40)
        
        items_cleaned = 0
        errors = 0
        
        # Disable buttons during cleaning
        self.btn_clean.configure(state="disabled", text="Cleaning...")
        self.btn_analyze.configure(state="disabled")
        self.progress_bar.set(0)

        targets = list(self.clean_targets.items())
        total_targets = len(targets)

        for i, (name, path) in enumerate(targets):
            progress = (i + 1) / total_targets
            self.status_text_var.set(f"Cleaning: {name}...")
            self.progress_bar.set(progress)
            
            try:
                if not path or not os.path.exists(path):
                    continue
                
                # Special case for Recycle Bin: empty it using Windows Shell API
                if name == "Recycle Bin":
                    self.log_message(f"Emptying {name}...")
                    # 1: SHERB_NOCONFIRMATION, 2: SHERB_NOPROGRESSUI, 4: SHERB_NOSOUND
                    result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1 | 2 | 4)
                    if result == 0:
                        self.log_message(f" > {name} successfully emptied.")
                        items_cleaned += 1
                    else:
                        self.log_message(f" > Failed to empty {name} (Error code: {result})")
                    continue

                self.log_message(f"Cleaning: {name}...")
                
                # List items in the folder and send them to trash
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    try:
                        send2trash(item_path)
                        items_cleaned += 1
                    except Exception:
                        # Files in use are common in Temp folders
                        errors += 1
                        continue
                self.log_message(f" > Finished cleaning {name}")
            except Exception as e:
                self.log_message(f" > Error processing {name}: {str(e)}")

        self.log_message("-" * 40)
        self.log_message(f"CLEANING COMPLETE: {items_cleaned} items moved to Recycle Bin.")
        if errors > 0:
            self.log_message(f"Note: {errors} items were skipped (likely in use).")
        
        self.status_text_var.set("Cleaning Complete")
        # Reset buttons and update UI
        self.btn_clean.configure(state="normal", text="Start Cleaning")
        self.btn_analyze.configure(state="normal")
        self.update_disk_info()

        # Show success message
        messagebox.showinfo(
            "System Cleaned", 
            f"Optimization successful!\n\n"
            f"Moved {items_cleaned} items to Recycle Bin.\n"
            f"{errors} items were skipped (currently in use)."
        )

        # Reset junk count and status badge
        self.total_junk_found = 0
        self.status_badge.configure(text="● SYSTEM SECURE", text_color="#2ecc71", fg_color=("#dbf9e1", "#1e3a24"))

    def log_message(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"[{timestamp}] {message}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def create_nav_button(self, text, row, name):
        button = ctk.CTkButton(
            self.sidebar_frame, 
            text=text, 
            corner_radius=10, 
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=lambda: self.select_frame_by_name(name)
        )
        button.grid(row=row, column=0, padx=20, pady=10, sticky="ew")
        return button

    def select_frame_by_name(self, name):
        # Update button colors
        self.btn_dashboard.configure(fg_color=("gray75", "gray25") if name == "dashboard" else "transparent")
        self.btn_cleaner.configure(fg_color=("gray75", "gray25") if name == "cleaner" else "transparent")
        self.btn_tools.configure(fg_color=("gray75", "gray25") if name == "tools" else "transparent")

        # Hide all frames
        self.dashboard_frame.grid_forget()
        self.cleaner_frame.grid_forget()
        self.tools_frame.grid_forget()

        # Show selected frame
        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
        elif name == "cleaner":
            self.cleaner_frame.grid(row=0, column=0, sticky="nsew")
        elif name == "tools":
            self.tools_frame.grid(row=0, column=0, sticky="nsew")

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = CleanerCApp()
    app.mainloop()

