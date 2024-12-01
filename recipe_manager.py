import json

RECIPES_FILE = "recipes.json"

def load_recipes():
    try:
        with open(RECIPES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_recipes(recipes):
    with open(RECIPES_FILE, "w") as file:
        json.dump(recipes, file, indent=4)
