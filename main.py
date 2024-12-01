import customtkinter as ctk
from gui import MealPalApp

# Initialize customTkinter appearance
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

# Start the application
if __name__ == "__main__":
    app = MealPalApp()
    app.mainloop()