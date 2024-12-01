import json

MEAL_PLAN_FILE = "week_plan.json"

def load_meal_plan():
    try:
        with open(MEAL_PLAN_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

def save_meal_plan(meal_plan):
    with open(MEAL_PLAN_FILE, "w") as file:
        json.dump(meal_plan, file, indent=4)

def reset_meal_plan(meal_plan):
    for day in meal_plan:
        meal_plan[day] = []
