class Recipe:
    def __init__(self, name, ingredients, instructions, category, servings, picture=None):
        self.name = name
        self.ingredients = ingredients  # A list of dictionaries with ingredient details
        self.instructions = instructions
        self.category = category
        self.servings = servings
        self.picture = picture if picture else "assets/images/placeholder.jpg"

    def __str__(self):
        # Print ingredients with measurements
        ingredient_list = "\n".join(
            [f"{ing['quantity']} {ing['unit']} {ing['name']}" for ing in self.ingredients]
        )
        return (
            f"{self.name} - {self.category} (Serves: {self.servings})\n"
            f"Ingredients:\n{ingredient_list}\n"
            f"Instructions:\n{self.instructions}"
        )

    def to_dict(self):
        # Serialize the recipe object to a dictionary
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "category": self.category,
            "servings": self.servings,
            "picture": self.picture,
        }
