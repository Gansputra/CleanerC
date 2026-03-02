import customtkinter as ctk

def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue") 

    app = ctk.CTk()
    app.geometry("400x240")
    app.title("CleanerC - Disk Cleaner")

    label = ctk.CTkLabel(app, text="Welcome to CleanerC", font=("Inter", 20))
    label.pack(pady=40)

    button = ctk.CTkButton(app, text="Scan Disk", command=lambda: print("Scanning..."))
    button.pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    main()
