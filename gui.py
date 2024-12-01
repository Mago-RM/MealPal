import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
from recipe_manager import load_recipes, save_recipes
from recipe import Recipe


class MealPalApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Meal Pal")
        self.geometry("650x700")
        self.iconbitmap("assets/favicon.ico")

        self.recipes = load_recipes()

        # Initialize GUI
        self.create_navbar()
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.display_home()  # Default screen

    ### Navigation Bar ###
    def create_navbar(self):
        navbar = ctk.CTkFrame(self, height=50)
        navbar.pack(side="top", fill="x")

        # Navbar Title
        nav_title = ctk.CTkLabel(navbar, text="Welcome to MealPal", font=("Arial", 20, "bold"))
        nav_title.pack(side="left", padx=10)

        # Navbar Buttons
        button_frame = ctk.CTkFrame(navbar)
        button_frame.pack(side="right", padx=10)

        ctk.CTkButton(button_frame, text="Home", command=self.display_home, width=100).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Recipes", command=self.display_recipe_cards, width=100).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Meal Planner", command=self.display_meal_planner, width=100).pack(side="left", padx=5)

    ### Home Screen ###
    def display_home(self):
        self.clear_content_frame()

        title_label = ctk.CTkLabel(self.content_frame, text="Featured Recipes", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        card_container = ctk.CTkFrame(self.content_frame)
        card_container.pack(fill="both", expand=True)

        self.render_recipe_cards(card_container, self.recipes)

    ### Recipe Cards ###
    def display_recipe_cards(self):
        self.clear_content_frame()

        # Title
        title_label = ctk.CTkLabel(self.content_frame, text="Recipes", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        # Search and Filter Frame
        filter_frame = ctk.CTkFrame(self.content_frame)
        filter_frame.pack(fill="x", padx=10, pady=10)

        # Search Bar
        search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Search recipes...")
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        search_button = ctk.CTkButton(filter_frame, text="Search", command=lambda: self.filter_recipes(query=search_entry.get()))
        search_button.pack(side="left", padx=5)

        # Category Dropdown Menu
        categories = ["All"] + list({recipe["category"] for recipe in self.recipes})  # Dynamically populate categories
        category_var = ctk.StringVar(value="All")  # Default value
        category_dropdown = ctk.CTkOptionMenu(filter_frame, variable=category_var, values=categories, command=lambda c: self.filter_recipes(category=c))
        category_dropdown.pack(side="right", padx=5)
        
        # "Add Recipe" Button
        add_recipe_button = ctk.CTkButton(self.content_frame, text="Add Recipe", command=self.display_add_recipe_form)
        add_recipe_button.pack(pady=10)

        # Recipe Cards Container
        self.recipe_cards_container = ctk.CTkFrame(self.content_frame)
        self.recipe_cards_container.pack(fill="both", expand=True)

        # Display All Recipes by Default
        self.render_recipe_cards(self.recipe_cards_container, self.recipes)
    
    def display_add_recipe_form(self):
        self.clear_content_frame()

        # Title
        title_label = ctk.CTkLabel(self.content_frame, text="Add Recipe", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        # Input Fields
        name_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Recipe Name")
        name_entry.pack(pady=5)

        category_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Category")
        category_entry.pack(pady=5)

        servings_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Servings")
        servings_entry.pack(pady=5)

        instructions_entry = ctk.CTkTextbox(self.content_frame, width=600, height=100)
        instructions_entry.pack(pady=10)
        instructions_entry.insert("1.0", "Instructions...")

        # Ingredient Fields (Dynamic List)
        ingredients_frame = ctk.CTkFrame(self.content_frame)
        ingredients_frame.pack(pady=10)
        ingredient_entries = []

        def add_ingredient_field():
            entry_frame = ctk.CTkFrame(ingredients_frame)
            entry_frame.pack(fill="x", pady=5)

            ingredient_name = ctk.CTkEntry(entry_frame, placeholder_text="Ingredient Name")
            ingredient_name.pack(side="left", padx=5)
            ingredient_quantity = ctk.CTkEntry(entry_frame, placeholder_text="Quantity")
            ingredient_quantity.pack(side="left", padx=5)
            ingredient_unit = ctk.CTkEntry(entry_frame, placeholder_text="Unit (e.g., grams, cups)")
            ingredient_unit.pack(side="left", padx=5)

            ingredient_entries.append((ingredient_name, ingredient_quantity, ingredient_unit))

        add_ingredient_button = ctk.CTkButton(self.content_frame, text="Add Ingredient", command=add_ingredient_field)
        add_ingredient_button.pack(pady=10)
        
        # Submit Recipe (Save Button)
        def submit_recipe():
            name = name_entry.get()
            category = category_entry.get()
            servings = servings_entry.get()
            instructions = instructions_entry.get("1.0", "end").strip()

            # Collect Ingredients
            ingredients = []
            for name_field, quantity_field, unit_field in ingredient_entries:
                ingredient_name = name_field.get()
                quantity = quantity_field.get()
                unit = unit_field.get()
                if ingredient_name and quantity and unit:
                    ingredients.append({"name": ingredient_name, "quantity": quantity, "unit": unit})

            # Validate Inputs
            if not name_entry.get() or not category_entry.get():
                messagebox.showwarning("Warning", "Please fill out all required fields!")
                return

            # Save Recipe
            new_recipe = Recipe(name=name, category=category, servings=servings, instructions=instructions, ingredients=ingredients)
            self.recipes.append(new_recipe.to_dict())
            save_recipes(self.recipes)

            # Success Message and Redirect
            ctk.CTkMessageBox.show_info("Success", f"Recipe '{name}' added!")
            self.display_recipe_cards()

        submit_button = ctk.CTkButton(self.content_frame, text="Save Recipe", command=submit_recipe)
        submit_button.pack(pady=10)
        self.recipes = load_recipes()


        # Back Button
        back_button = ctk.CTkButton(self.content_frame, text="Back to Recipes", command=self.display_recipe_cards)
        back_button.pack(pady=10)


    def filter_recipes(self, query="", category="All"):
        query = query.lower()

        # Filter recipes by search query and category
        filtered_recipes = [
            recipe for recipe in self.recipes
            if (query in recipe["name"].lower() or not query) and (category == "All" or recipe["category"] == category)
        ]

        # Clear and re-render the recipe cards
        for widget in self.recipe_cards_container.winfo_children():
            widget.destroy()

        self.render_recipe_cards(self.recipe_cards_container, filtered_recipes)


    def render_recipe_cards(self, container, recipes):
        for i, recipe in enumerate(recipes):
            card = ctk.CTkFrame(container, width=250, height=300, corner_radius=15)
            card.grid(row=i // 3, column=i % 3, padx=10, pady=10)

            # Recipe Image
            self.add_recipe_image(card, recipe.get("picture"))

            # Recipe Name and Category
            ctk.CTkLabel(card, text=recipe["name"], font=("Arial", 16, "bold")).pack(pady=5)
            ctk.CTkLabel(card, text=recipe["category"], font=("Arial", 12)).pack(pady=5)

            # View Details Button
            ctk.CTkButton(card, text="View Details", command=lambda r=recipe: self.view_recipe(r)).pack(pady=10)

    def add_recipe_image(self, container, image_path):
        try:
            img = Image.open(image_path).resize((230, 150))
            img_tk = ImageTk.PhotoImage(img)
            image_label = ctk.CTkLabel(container, image=img_tk, text="")
            image_label.image = img_tk  # Prevent garbage collection
            image_label.pack(pady=10)
        except (FileNotFoundError, TypeError):
            ctk.CTkLabel(container, text="No Image Available").pack(pady=10)

    ### Recipe Details ###
    def view_recipe(self, recipe):
        self.clear_content_frame()

        ctk.CTkLabel(self.content_frame, text=recipe["name"], font=("Arial", 24, "bold")).pack(pady=20)

        # Recipe Image
        self.add_recipe_image(self.content_frame, recipe.get("picture"))

        # Ingredients
        ctk.CTkLabel(self.content_frame, text="Ingredients:", font=("Arial", 16, "bold")).pack(pady=5)
        ingredients_text = ctk.CTkTextbox(self.content_frame, width=600, height=100)
        ingredients_text.pack(pady=10)
        for ingredient in recipe["ingredients"]:
            ingredients_text.insert("end", f"- {ingredient['quantity']} {ingredient['unit']} {ingredient['name']}\n")
        ingredients_text.configure(state="disabled")

        # Instructions
        ctk.CTkLabel(self.content_frame, text="Instructions:", font=("Arial", 16, "bold")).pack(pady=5)
        instructions_text = ctk.CTkTextbox(self.content_frame, width=600, height=150)
        instructions_text.insert("1.0", recipe["instructions"])
        instructions_text.configure(state="disabled")
        instructions_text.pack(pady=10)

        # Button Frame
        button_frame = ctk.CTkFrame(self.content_frame)
        button_frame.pack(pady=20)

        # Delete Button (Red)
        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Recipe",
            fg_color="red",  # Set red background color
            hover_color="#cc0000",  # Darker red on hover
            command=lambda: self.confirm_delete(recipe),
        )
        delete_button.pack(side="left", padx=10)
        # Back Button
        back_button = ctk.CTkButton(button_frame, text="Back to Recipes", command=self.display_recipe_cards)
        back_button.pack(side="left", padx=10)
    
    def confirm_delete(self, recipe):
        # Confirmation dialog
        confirm_replace = messagebox.askyesno(
            "Delete Recipe",
            f"Are you sure you want to delete the recipe '{recipe['name']}'?"
        )

        # If the user confirms deletion
        if confirm_replace:
            # Remove the recipe from the list
            self.recipes = [r for r in self.recipes if r["name"] != recipe["name"]]
            save_recipes(self.recipes)  # Save the updated list to the JSON file

            # Show success message
            messagebox.showinfo("Success", f"The recipe '{recipe['name']}' has been deleted.")

            # Redirect back to the recipe list
            self.display_recipe_cards()


    ### Meal Planner ###
    def display_meal_planner(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Meal Planner", font=("Arial", 24, "bold")).pack(pady=20)

    ### Utility Methods ###
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = MealPalApp()
    app.mainloop()
