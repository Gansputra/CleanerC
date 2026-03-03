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
import subprocess
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

        # --- Localization ---
        self.current_lang = "en"
        self.translations = {
            "en": {
                "logo": "CleanerC 🧹", "dashboard": "Dashboard", "cleaner": "Disk Cleaner", "tools": "System Tools",
                "appearance": "Appearance Mode:", "language": "Language:", "overview": "System Overview",
                "secure": "● SYSTEM SECURE", "optimizable": "● OPTIMIZABLE", "action": "● ACTION RECOMMENDED",
                "total": "Total Capacity", "used": "Used Space", "free": "Free Space", 
                "cpu_metrics": "CPU Metrics", "gpu_metrics": "GPU Metrics", "sys_info": "System Information",
                "scan": "Scan", "start_clean": "Start Cleaning", "refresh": "Refresh", "log": "Activity Log",
                "ready": "System Ready", "process": "Process Optimizer", "startup": "Startup Manager",
                "large": "Large File Finder", "cache": "Cache Cleaner", "dns": "DNS Flush",
                "back": "← Back", "run": "Run Action", "kill_proc": "Kill Process", "open": "Open Tool",
                "proc_desc": "Manage running apps & free RAM", "start_desc": "Control apps that start with Windows",
                "large_desc": "Find files over 1GB on your drive", "cache_desc": "Clean browser & application cache",
                "dns_desc": "Reset network resolver cache", "uptime": "Uptime", "sc_ready": "System Cleaner Ready",
                "coming": "System Tools Coming Soon", "author": "Author: Gansputra", "kill_msg": "Process terminated.",
                "dns_msg": "DNS Resolver Cache successfully flushed."
            },
            "id": {
                "logo": "PembersihC 🧹", "dashboard": "Dasbor", "cleaner": "Pembersih Disk", "tools": "Alat Sistem",
                "appearance": "Mode Tampilan:", "language": "Pilihan Bahasa:", "overview": "Ikhtisar Sistem",
                "secure": "● SISTEM AMAN", "optimizable": "● BISA DIOPTIMALKAN", "action": "● BUTUH TINDAKAN",
                "total": "Kapasitas Total", "used": "Ruang Terpakai", "free": "Ruang Kosong", 
                "cpu_metrics": "Metrik CPU", "gpu_metrics": "Metrik GPU", "sys_info": "Informasi Sistem",
                "scan": "Pindai", "start_clean": "Mulai Bersihkan", "refresh": "Segarkan", "log": "Log Aktivitas",
                "ready": "Sistem Siap", "process": "Pengoptimal Proses", "startup": "Manajer Startup",
                "large": "Pencari File Besar", "cache": "Pembersih Cache", "dns": "Flush DNS",
                "back": "← Kembali", "run": "Jalankan", "kill_proc": "Matikan l", "open": "Buka Alat",
                "proc_desc": "Kelola aplikasi & bebaskan RAM", "start_desc": "Atur aplikasi startup Windows",
                "large_desc": "Cari file di atas 1GB", "cache_desc": "Bersihkan cache browser & aplikasi",
                "dns_desc": "Reset cache resolver jaringan", "uptime": "Waktu Aktif", "sc_ready": "Pembersih Sistem Siap",
                "coming": "Alat Sistem Segera Hadir", "author": "Penulis: Gansputra", "kill_msg": "Proses dimatikan.",
                "dns_msg": "Cache DNS berhasil dibersihkan."
            }
        }

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
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Language Switcher
        self.language_label = ctk.CTkLabel(self.sidebar_frame, text="Language:", anchor="w")
        self.language_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.language_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["English", "Indonesia"],
            command=self.change_language
        )
        self.language_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Adjust push

        # --- Author Section ---
        self.author_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.author_frame.grid(row=9, column=0, padx=20, pady=(20, 20), sticky="ew")
        
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

        # 3. System Tools Frame
        self.tools_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.tools_frame.grid_columnconfigure(0, weight=1)
        self.tools_frame.grid_rowconfigure(0, weight=1)

        # Tools Menu (Grid of Cards)
        self.tools_menu_frame = ctk.CTkFrame(self.tools_frame, fg_color="transparent")
        self.tools_menu_frame.grid(row=0, column=0, sticky="nsew")
        self.tools_menu_frame.grid_columnconfigure((0, 1), weight=1, pad=15)

        self.create_tool_anchor("⚡ Process Optimizer", "Manage running apps & free RAM", 0, 0, lambda: self.show_tool_page("process"))
        self.create_tool_anchor("🚀 Startup Manager", "Control apps that start with Windows", 0, 1, lambda: self.show_tool_page("startup"))
        self.create_tool_anchor("📂 Large File Finder", "Find files over 1GB on your drive", 1, 0, lambda: self.show_tool_page("large_files"))
        self.create_tool_anchor("🧹 Cache Cleaner", "Clean browser & application cache", 1, 1, lambda: self.show_tool_page("cache"))
        self.create_tool_anchor("🌐 DNS Flush", "Reset network resolver cache", 2, 0, self.run_dns_flush)

        # Individual Tool Pages
        self.process_page = self.create_tool_page("Process Optimizer", self.refresh_processes)
        self.startup_page = self.create_tool_page("Startup Manager", self.load_startup_apps)
        self.large_files_page = self.create_tool_page("Large File Finder", self.start_large_file_scan)
        self.cache_page = self.create_tool_page("Cache Cleaner", self.run_cache_clean)

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
            self.card_system.value_label.configure(text=f"{t['uptime']}: {uptime_str}")

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
        self.update_status_badge(self.total_junk_found)

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
            self.show_tool_page("menu")

    def create_tool_anchor(self, title, desc, row, col, command):
        btn_frame = ctk.CTkFrame(self.tools_menu_frame, fg_color=("#ffffff", "#2b2b2b"), corner_radius=15, border_width=2, border_color=("#dcdcdc", "#3d3d3d"))
        btn_frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        # Tool Title
        ctk.CTkLabel(btn_frame, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 0), padx=20, anchor="nw")
        
        # Tool Description
        ctk.CTkLabel(btn_frame, text=desc, font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(2, 10), padx=20, anchor="nw")
        
        # Action Button
        btn = ctk.CTkButton(
            btn_frame, text="Open Tool", height=32, 
            fg_color=("#3498db", "#2980b9"), hover_color="#21618c",
            command=command
        )
        btn.pack(pady=(10, 15), padx=20, fill="x")

    def create_tool_page(self, title, refresh_command):
        page = ctk.CTkFrame(self.tools_frame, fg_color=("#f9f9f9", "#1d1d1d"), corner_radius=20)
        
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", pady=25, padx=25)
        
        page.back_btn = ctk.CTkButton(header, text="← Back", width=80, fg_color="gray40", command=lambda: self.show_tool_page("menu"))
        page.back_btn.pack(side="left")
        
        page.title_lbl = ctk.CTkLabel(header, text=title, font=ctk.CTkFont(size=24, weight="bold"))
        page.title_lbl.pack(side="left", padx=20)
        
        if refresh_command:
            page.run_btn = ctk.CTkButton(header, text="Run Action", width=120, fg_color="#2ecc71", hover_color="#27ae60", command=refresh_command)
            page.run_btn.pack(side="right")
            
        scrollable = ctk.CTkScrollableFrame(page, height=450, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        page.list_container = scrollable
        
        return page

    def show_tool_page(self, name):
        self.tools_menu_frame.grid_forget()
        self.process_page.grid_forget()
        self.startup_page.grid_forget()
        self.large_files_page.grid_forget()
        self.cache_page.grid_forget()
        
        if name == "menu":
            self.tools_menu_frame.grid(row=0, column=0, sticky="nsew")
        elif name == "process":
            self.process_page.grid(row=0, column=0, sticky="nsew")
            self.refresh_processes()
        elif name == "startup":
            self.startup_page.grid(row=0, column=0, sticky="nsew")
            self.load_startup_apps()
        elif name == "large_files":
            self.large_files_page.grid(row=0, column=0, sticky="nsew")
        elif name == "cache":
            self.cache_page.grid(row=0, column=0, sticky="nsew")

    def refresh_processes(self):
        for widget in self.process_page.list_container.winfo_children():
            widget.destroy()
        
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                procs.append(p.info)
            except: pass
            
        procs = sorted(procs, key=lambda x: x['memory_info'].rss, reverse=True)[:15]
        
        for p in procs:
            frame = ctk.CTkFrame(self.process_page.list_container, fg_color=("#ffffff", "#2b2b2b"), corner_radius=10)
            frame.pack(fill="x", pady=5, padx=5)
            
            mem = f"{p['memory_info'].rss / (1024*1024):.1f} MB"
            info_label = ctk.CTkLabel(frame, text=f"{p['name']}", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(15, 0), pady=10)
            ctk.CTkLabel(frame, text=f"PID: {p['pid']} | {mem}", text_color="gray").pack(side="left", padx=15)
            
            btn = ctk.CTkButton(frame, text="Kill Process", width=100, height=28, fg_color="#e74c3c", hover_color="#c0392b",
                               command=lambda pid=p['pid']: self.kill_process(pid))
            btn.pack(side="right", padx=15)

    def kill_process(self, pid):
        try:
            psutil.Process(pid).terminate()
            messagebox.showinfo("Success", f"Process {pid} terminated.")
            self.refresh_processes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_startup_apps(self):
        for widget in self.startup_page.list_container.winfo_children():
            widget.destroy()
            
        import winreg
        paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run")
        ]
        
        for hkey, path in paths:
            try:
                key = winreg.OpenKey(hkey, path)
                for i in range(winreg.QueryInfoKey(key)[1]):
                    name, val, _ = winreg.EnumValue(key, i)
                    item_frame = ctk.CTkFrame(self.startup_page.list_container, fg_color=("#ffffff", "#2b2b2b"), corner_radius=8)
                    item_frame.pack(fill="x", pady=3, padx=5)
                    ctk.CTkLabel(item_frame, text=f"• {name}", font=ctk.CTkFont(weight="bold"), anchor="w").pack(padx=15, pady=(5, 0), fill="x")
                    ctk.CTkLabel(item_frame, text=val, font=ctk.CTkFont(size=10), text_color="gray", anchor="w").pack(padx=15, pady=(0, 5), fill="x")
            except: pass

    def start_large_file_scan(self):
        for widget in self.large_files_page.list_container.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(self.large_files_page.list_container, text="Scanning C: drive for files > 1GB... Please wait.").pack(pady=20)
        threading.Thread(target=self.run_large_file_scan, daemon=True).start()

    def run_large_file_scan(self):
        large_files = []
        for root, dirs, files in os.walk("C:\\"):
            for f in files:
                try:
                    fp = os.path.join(root, f)
                    size = os.path.getsize(fp)
                    if size > 1024 * 1024 * 1024: # 1GB
                        large_files.append((fp, size))
                except: continue
            if len(large_files) > 20: break # Limit for safety
            
        self.after(0, lambda: self.display_large_files(large_files))

    def display_large_files(self, files):
        for widget in self.large_files_page.list_container.winfo_children():
            widget.destroy()
            
        if not files:
            ctk.CTkLabel(self.large_files_page.list_container, text="No files larger than 1GB found or access denied.").pack(pady=20)
            return

        for fp, size in files:
            card = ctk.CTkFrame(self.large_files_page.list_container, fg_color=("#ffffff", "#2b2b2b"), corner_radius=10)
            card.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(card, text=os.path.basename(fp), font=ctk.CTkFont(weight="bold"), anchor="w").pack(padx=15, pady=(10, 0), fill="x")
            ctk.CTkLabel(card, text=f"Size: {size/(1024*1024*1024):.2f} GB", text_color="#e67e22").pack(padx=15, anchor="w")
            ctk.CTkLabel(card, text=fp, font=ctk.CTkFont(size=10), text_color="gray", anchor="w").pack(padx=15, pady=(0, 10), fill="x")

    def run_cache_clean(self):
        for widget in self.cache_page.list_container.winfo_children():
            widget.destroy()
        
        paths = {
            "Chrome Cache": os.path.join(os.environ.get('LOCALAPPDATA', ''), r"Google\Chrome\User Data\Default\Cache"),
            "Edge Cache": os.path.join(os.environ.get('LOCALAPPDATA', ''), r"Microsoft\Edge\User Data\Default\Cache")
        }
        
        for name, path in paths.items():
            if os.path.exists(path):
                try:
                    size = self.get_folder_size(path)
                    send2trash(path)
                    ctk.CTkLabel(self.cache_page.list_container, text=f"SUCCESS: {name} ({self.format_size(size)}) moved to trash.").pack(pady=5)
                except Exception as e:
                    ctk.CTkLabel(self.cache_page.list_container, text=f"FAILED: {name} ({str(e)})").pack(pady=5)
            else:
                ctk.CTkLabel(self.cache_page.list_container, text=f"NOT FOUND: {name}").pack(pady=5)

    def run_dns_flush(self):
        try:
            subprocess.run(["ipconfig", "/flushdns"], shell=True, check=True)
            messagebox.showinfo("Success", "DNS Resolver Cache successfully flushed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to flush DNS: {str(e)}")

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_language(self, new_language: str):
        self.current_lang = "en" if new_language == "English" else "id"
        self.update_ui_text()

    def update_ui_text(self):
        t = self.translations[self.current_lang]
        
        # Sidebar
        self.logo_label.configure(text=t["logo"])
        self.btn_dashboard.configure(text=t["dashboard"])
        self.btn_cleaner.configure(text=t["cleaner"])
        self.btn_tools.configure(text=t["tools"])
        self.appearance_mode_label.configure(text=t["appearance"])
        self.language_label.configure(text=t["language"])
        self.author_label.configure(text=t["author"])
        
        # Dashboard
        self.title_label.configure(text=t["overview"])
        # Update badge based on current total junk (reuse existing logic but with translated keys)
        if hasattr(self, 'total_junk_found'):
            self.update_status_badge(self.total_junk_found)
        else:
            self.status_badge.configure(text=t["secure"])
            
        # Re-title cards (need to access title labels which aren't currently saved as attributes)
        # For simplicity, let's just update the ones we can easily identify
        self.card_total.winfo_children()[0].configure(text=t["total"])
        self.card_used.winfo_children()[0].configure(text=t["used"])
        self.card_free.winfo_children()[0].configure(text=t["free"])
        self.card_cpu.winfo_children()[0].configure(text=t["cpu_metrics"])
        self.card_gpu.winfo_children()[0].configure(text=t["gpu_metrics"])
        self.card_system.winfo_children()[0].configure(text=t["sys_info"])
        
        # Disk Cleaner
        self.btn_analyze.configure(text=t["scan"])
        self.btn_clean.configure(text=t["start_clean"])
        self.btn_refresh.configure(text=t["refresh"])
        self.log_label.configure(text=t["log"])
        
        # System Tools - We'll just refresh the tools menu anchors
        for i, widget in enumerate(self.tools_menu_frame.winfo_children()):
            # This is a bit hacky because we don't have direct references to the inner labels
            # But the order is known
            titles = [t["process"], t["startup"], t["large"], t["cache"], t["dns"]]
            descs = [t["proc_desc"], t["start_desc"], t["large_desc"], t["cache_desc"], t["dns_desc"]]
            if i < len(titles):
                # widget is the card frame
                widget.winfo_children()[0].configure(text=titles[i])
                widget.winfo_children()[1].configure(text=descs[i])
                widget.winfo_children()[2].configure(text=t["open"])

        # Tool Pages Header
        tool_pages = [
            (self.process_page, t["process"]),
            (self.startup_page, t["startup"]),
            (self.large_files_page, t["large"]),
            (self.cache_page, t["cache"])
        ]
        for page, title in tool_pages:
            page.back_btn.configure(text=t["back"])
            page.title_lbl.configure(text=title)
            if hasattr(page, 'run_btn'):
                page.run_btn.configure(text=t["run"])

    def update_status_badge(self, total_size):
        t = self.translations[self.current_lang]
        if total_size == 0:
            self.status_badge.configure(text=t["secure"], text_color="#2ecc71", fg_color=("#dbf9e1", "#1e3a24"))
        elif total_size < 500 * 1024 * 1024:
            self.status_badge.configure(text=t["optimizable"], text_color="#f39c12", fg_color=("#fef5e7", "#3e2723"))
        else:
            self.status_badge.configure(text=t["action"], text_color="#e74c3c", fg_color=("#fadbd8", "#442222"))

if __name__ == "__main__":
    app = CleanerCApp()
    app.mainloop()

