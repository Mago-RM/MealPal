#Margarita Rincon
#CS152 Programming Paradigms - Meal Plan Application
#IU TKINTER GUI
#First Version: 10/10/2021

import json
import os
from tkinter import *
from tkinter import messagebox
from recipe import Recipe  # Import the Recipe class



# Define paths for each JSON file
RECIPES_FILE = "recipes.json"
MEAL_PLAN_FILE = "week_plan.json"

# Load recipes from recipes.json
def load_recipes(filename=RECIPES_FILE):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            # Return recipes if the data is in the correct format
            if isinstance(data, list):
                return data
            else:
                messagebox.showerror("Error", "Invalid format in recipes.json.")
                return []
    except FileNotFoundError:
        # If file doesn't exist, return an empty list
        return []

# Save recipes to recipes.json
def save_recipes(recipes, filename=RECIPES_FILE):
    with open(filename, "w") as file:
        json.dump(recipes, file, indent=4)

# Load meal plan from meal_plan.json
def load_meal_plan():
    if os.path.exists(MEAL_PLAN_FILE):
        with open(MEAL_PLAN_FILE, "r") as file:
            data = json.load(file)
            # Ensure data is a dictionary in the correct format
            if isinstance(data, dict):
                return data
            else:
                return {
                    "Monday": [], "Tuesday": [], "Wednesday": [],
                    "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []
                }
    else:
        # Default meal plan structure if file is missing
        return {
            "Monday": [], "Tuesday": [], "Wednesday": [],
            "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []
        }

# Save meal plan to meal_plan.json
def save_meal_plan():
    with open(MEAL_PLAN_FILE, "w") as file:
        json.dump(meal_plan, file, indent=4)

# Initialize data
recipes = load_recipes()  # Load recipes from recipes.json
meal_plan = load_meal_plan()  # Load meal plan from meal_plan.json


# Function to assign a selected recipe to a selected day
def assign_recipe():
    selected_day = day_var.get()
    selected_recipe = recipe_listbox.get(ACTIVE)

    if selected_day and selected_recipe:
        meal_plan[selected_day].append(selected_recipe)
        save_meal_plan()  # Save updated meal plan to file
        messagebox.showinfo("Success", f"Assigned '{selected_recipe}' to {selected_day}")
        update_schedule_display()
    else:
        messagebox.showwarning("Warning", "Please select both a day and a recipe.")

# Function to update the weekly schedule display
def update_schedule_display():
    schedule_text.delete(1.0, END)  # Clear the text widget

    for day, meals in meal_plan.items():
        schedule_text.insert(END, f"{day}:\n")
        if meals:
            for meal in meals:
                schedule_text.insert(END, f"  - {meal}\n")
        else:
            schedule_text.insert(END, "  (No meals assigned)\n")
        schedule_text.insert(END, "\n")  # Blank line between days

# Function to reset the meal plan for the week
def reset_week():
    # Clear all days in the meal plan
    for day in meal_plan:
        meal_plan[day] = []
    
    save_meal_plan()  # Save the reset meal plan to file
    update_schedule_display()
    messagebox.showinfo("Reset Week", "The meal plan has been reset for the week.")

#******************************************* Tkinter GUI Setup
root = Tk()
root.title("Recipe Organizer and Meal Planner")
root.geometry("600x400")  # Set a small window size for testing

# Create a main frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

# Create a Canvas widget inside the main frame
canvas = Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add a scrollbar to the canvas
scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame inside the canvas to hold your widgets
content_frame = Frame(canvas)

# Add the content frame to a window on the canvas
canvas.create_window((0, 0), window=content_frame, anchor="nw")


my_label = Label(content_frame, text = "Let's Get Cooking", font=("Arial", 14))
my_label.pack()

# Label for Recipe Input Section
input_label = Label(content_frame, text="Add a New Recipe", font=("Arial", 12))
input_label.pack(pady=10)

# Recipe Name
name_label = Label(content_frame, text="Recipe Name:")
name_label.pack()
name_entry = Entry(content_frame, width=50)
name_entry.pack()

# Ingredients
ingredients_label = Label(content_frame, text="Ingredients (comma-separated):")
ingredients_label.pack()
ingredients_entry = Entry(content_frame, width=50)
ingredients_entry.pack()

# Instructions
instructions_label = Label(content_frame, text="Instructions:")
instructions_label.pack()
instructions_entry = Entry(content_frame, width=50)
instructions_entry.pack()

# Category (e.g., Breakfast, Lunch, Dinner)
category_label = Label(content_frame, text="Category: Breakfast, Lunch, Dinner, Snacks, Beverages")
category_label.pack()
category_entry = Entry(content_frame, width=50)
category_entry.pack()


# Button to Add Recipe
add_button = Button(content_frame, text="Add Recipe", command=lambda: add_recipe())
add_button.pack(pady=10)

# Function to add a recipe
def add_recipe():
    name = name_entry.get()
    ingredients = ingredients_entry.get()
    instructions = instructions_entry.get()
    category = category_entry.get()
    
    if not name or not ingredients or not instructions or not category:
        messagebox.showwarning("Warning", "All fields must be filled out!")
        return
    
    new_recipe = Recipe(name, ingredients, instructions, category)
    recipes.append(new_recipe)
    
    # Save all recipes to recipes.json
    save_recipes(recipes)

    recipe_listbox.insert(END, new_recipe.name)
    messagebox.showinfo("Success", f"Recipe '{name}' added!")

    name_entry.delete(0, END)
    ingredients_entry.delete(0, END)
    instructions_entry.delete(0, END)
    category_entry.delete(0, END)

    
    # Option 1: Directly add the new recipe name to the Listbox
    #recipe_listbox.insert(END, new_recipe.name)
    
    # Option 2: Reload all recipes from JSON and refresh the Listbox (if needed)
    # recipes = load_recipes("mealplandata.json")
    # refresh_listbox(recipes)

    # Show a success message
    messagebox.showinfo("Success", f"Recipe '{name}' added!")
    
    # Clear entry fields
    name_entry.delete(0, END)
    ingredients_entry.delete(0, END)
    instructions_entry.delete(0, END)
    category_entry.delete(0, END)


# Sidebar frame for saved recipes
sidebar_frame = Frame(content_frame)
sidebar_frame.pack(side=LEFT, fill=Y, padx=80, pady=10)

# Label for displaying saved recipes
display_label = Label(sidebar_frame, text="Saved Recipes", font=("Arial", 14))
display_label.pack(pady=5)

# Listbox to show recipes in the sidebar
recipe_listbox = Listbox(sidebar_frame, width=30, height=15)
recipe_listbox.pack()

# Button to view recipe details
view_button = Button(sidebar_frame, text="View Recipe", command=lambda: view_recipe())
view_button.pack(pady=5)

# Button to delete a selected recipe
delete_button = Button(sidebar_frame, text="Delete Recipe", command=lambda: delete_recipe())
delete_button.pack(pady=5)

def view_recipe():
    selected = recipe_listbox.curselection()
    if selected:
        recipe_name = recipe_listbox.get(selected[0])
        recipe = next((r for r in recipes if r.name == recipe_name), None)
        if recipe:
            messagebox.showinfo("Recipe Details", str(recipe))
    else:
        messagebox.showwarning("Warning", "Select a recipe to view.")

# Function to delete a selected recipe
def delete_recipe():
    selected = recipe_listbox.curselection()
    if selected:
        # Get the name of the selected recipe
        recipe_name = recipe_listbox.get(selected[0])

        # Confirm deletion
        confirm = messagebox.askyesno("Delete Recipe", f"Are you sure you want to delete '{recipe_name}'?")
        if confirm:
            # Remove the recipe from the recipes list
            global recipes
            recipes = [r for r in recipes if r.name != recipe_name]

            # Update the JSON file
            save_recipes(recipes, filename="mealplandata.json")
            
            # Remove the selected item from the Listbox
            recipe_listbox.delete(selected[0])
            
            # Show a success message
            messagebox.showinfo("Success", f"Recipe '{recipe_name}' deleted!")
    else:
        messagebox.showwarning("Warning", "Select a recipe to delete.")



# Load recipes from a JSON file
def load_recipes(filename="mealplandata.json"):
    try:
        with open(filename, "r") as file:
            recipes = json.load(file)
            return recipes
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {filename} not found.")
        return []

# Function to assign a selected recipe to a selected day
def assign_recipe():
    selected_day = day_var.get()
    selected_recipe = recipe_listbox.get(ACTIVE)

    if selected_day and selected_recipe:
        meal_plan[selected_day].append(selected_recipe)
        messagebox.showinfo("Success", f"Assigned '{selected_recipe}' to {selected_day}")
        update_schedule_display()
    else:
        messagebox.showwarning("Warning", "Please select both a day and a recipe.")

# Function to update the weekly schedule display
def update_schedule_display():
    schedule_text.delete(1.0, END)  # Clear the text widget

    for day, meals in meal_plan.items():
        schedule_text.insert(END, f"{day}:\n")
        if meals:
            for meal in meals:
                schedule_text.insert(END, f"  - {meal}\n")
        else:
            schedule_text.insert(END, "  (No meals assigned)\n")
        schedule_text.insert(END, "\n")  # Blank line between days

# Label for Meal Planning
meal_plan_label = Label(content_frame, text="Meal Planner", font=("Arial", 14))
meal_plan_label.pack(pady=10)

# Day of the week selection
day_label = Label(content_frame, text="Select a Day:")
day_label.pack()
day_var = StringVar(value="Monday")  # Default value
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_menu = OptionMenu(content_frame, day_var, *days)
day_menu.pack(pady=5)

# Recipe Listbox to select a recipe
recipe_label = Label(content_frame, text="Select a Recipe:")
recipe_label.pack(pady=5)
recipe_listbox = Listbox(content_frame, height=6)
recipe_listbox.pack(pady=5)

# Load recipes into the Listbox
recipes = load_recipes("recipes.json")
for recipe in recipes:
    recipe_listbox.insert(END, recipe)

# Button to assign the selected recipe to the selected day
assign_button = Button(content_frame, text="Assign Recipe to Day", command=assign_recipe)
assign_button.pack(pady=10)

# Reset Week Button
reset_button = Button(content_frame, text="Reset Week", command=reset_week)
reset_button.pack(pady=10)

# Display area for the weekly meal schedule
schedule_label = Label(content_frame, text="Weekly Meal Schedule:")
schedule_label.pack(pady=10)
schedule_text = Text(content_frame, height=15, width=50)
schedule_text.pack()

# Initial display of the current meal plan
update_schedule_display()


def confirm_exit():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.quit()

exit_button = Button(content_frame, text="Exit", command=confirm_exit)
exit_button.pack(pady=20)
      
root.mainloop()
