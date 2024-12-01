#Margarita Rincon
#CS152 Programming Paradigms - Meal Plan Application
#Updated: 12/12/2020
#Upgrades: GUI, Shopping List, Recipe Organizer

import customtkinter as ctk
import json
import os
from recipe import Recipe  # Ensure this class is implemented properly

# Initialize customTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Define paths
RECIPES_FILE = "recipes.json"
MEAL_PLAN_FILE = "week_plan.json"

# Load and save recipes
def load_recipes(filename=RECIPES_FILE):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                ctk.CTkMessageBox.show_error("Error", "Invalid format in recipes.json.")
                return []
    except FileNotFoundError:
        return []

def save_recipes(recipes, filename=RECIPES_FILE):
    with open(filename, "w") as file:
        json.dump(recipes, file, indent=4)

# Load and save meal plans
def load_meal_plan():
    if os.path.exists(MEAL_PLAN_FILE):
        with open(MEAL_PLAN_FILE, "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
    return {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

def save_meal_plan():
    with open(MEAL_PLAN_FILE, "w") as file:
        json.dump(meal_plan, file, indent=4)

# Initialize data
recipes = load_recipes()
meal_plan = load_meal_plan()

# GUI Functions
def add_recipe():
    name = name_entry.get()
    ingredients = ingredients_entry.get()
    instructions = instructions_entry.get()
    category = category_entry.get()

    if not name or not ingredients or not instructions or not category:
        ctk.CTkMessageBox.show_warning("Warning", "All fields must be filled!")
        return

    new_recipe = {
        "name": name,
        "ingredients": ingredients,
        "instructions": instructions,
        "category": category
    }
    recipes.append(new_recipe)
    save_recipes(recipes)
    update_recipe_list()
    ctk.CTkMessageBox.show_info("Success", f"Recipe '{name}' added!")
    name_entry.delete(0, "end")
    ingredients_entry.delete(0, "end")
    instructions_entry.delete(0, "end")
    category_entry.delete(0, "end")

def update_recipe_list():
    for widget in recipe_listbox.winfo_children():
        widget.destroy()
    for recipe in recipes:
        recipe_label = ctk.CTkLabel(recipe_listbox, text=recipe["name"], anchor="w")
        recipe_label.pack(fill="x", padx=5, pady=2)

def assign_recipe():
    selected_day = day_var.get()
    selected_recipe = selected_recipe_var.get()
    if selected_day and selected_recipe:
        meal_plan[selected_day].append(selected_recipe)
        save_meal_plan()
        update_schedule_display()
        ctk.CTkMessageBox.show_info("Success", f"Assigned '{selected_recipe}' to {selected_day}")
    else:
        ctk.CTkMessageBox.show_warning("Warning", "Select both a day and a recipe!")

def update_schedule_display():
    schedule_text.delete("1.0", "end")
    for day, meals in meal_plan.items():
        schedule_text.insert("end", f"{day}:\n")
        for meal in meals:
            schedule_text.insert("end", f"  - {meal}\n")
        schedule_text.insert("end", "\n")

def reset_week():
    for day in meal_plan:
        meal_plan[day] = []
    save_meal_plan()
    update_schedule_display()
    ctk.CTkMessageBox.show_info("Reset", "The meal plan has been reset!")

def confirm_exit():
    if ctk.CTkMessageBox.ask_ok_cancel("Exit", "Are you sure you want to exit?"):
        root.quit()

# Create GUI
root = ctk.CTk()
root.title("Meal Pal")
root.geometry("800x600")
root.iconbitmap("favicon.ico")

content_frame = ctk.CTkFrame(root)
content_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Recipe Form
name_entry = ctk.CTkEntry(content_frame, placeholder_text="Recipe Name")
name_entry.pack(pady=5)

ingredients_entry = ctk.CTkEntry(content_frame, placeholder_text="Ingredients (comma-separated)")
ingredients_entry.pack(pady=5)

instructions_entry = ctk.CTkEntry(content_frame, placeholder_text="Instructions")
instructions_entry.pack(pady=5)

category_entry = ctk.CTkEntry(content_frame, placeholder_text="Category")
category_entry.pack(pady=5)

add_button = ctk.CTkButton(content_frame, text="Add Recipe", command=add_recipe)
add_button.pack(pady=10)

# Recipe List
recipe_listbox = ctk.CTkFrame(content_frame)
recipe_listbox.pack(fill="both", expand=True, pady=10)
update_recipe_list()

# Day and Recipe Assignment
day_var = ctk.StringVar(value="Monday")
day_menu = ctk.CTkOptionMenu(content_frame, variable=day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
day_menu.pack(pady=5)

selected_recipe_var = ctk.StringVar()
recipe_dropdown = ctk.CTkOptionMenu(content_frame, variable=selected_recipe_var, values=[r["name"] for r in recipes])
recipe_dropdown.pack(pady=5)

assign_button = ctk.CTkButton(content_frame, text="Assign Recipe", command=assign_recipe)
assign_button.pack(pady=10)

# Schedule Display
schedule_text = ctk.CTkTextbox(content_frame, height=15, width=50)
schedule_text.pack(pady=10)
update_schedule_display()

reset_button = ctk.CTkButton(content_frame, text="Reset Week", command=reset_week)
reset_button.pack(pady=10)

exit_button = ctk.CTkButton(content_frame, text="Exit", command=confirm_exit)
exit_button.pack(pady=10)

root.mainloop()
