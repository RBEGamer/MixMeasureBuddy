EXAMPLE_RECIPES_COLLECTION: dict = {
    "example_recipe.recipe": {
        "name": "EXAMPLE_RECIPE",
        "description": "A nice Example Cocktail",
        "version": "1.0.0",
        "ingredients": {"0": "A", "1": "B", "2": "C"},
        "steps": [
            {"action": "scale", "ingredient": "0", "amount": 10},
            {"action": "confirm", "text": "shake it"},
            {"action": "wait", "text": "wait for it", "amount": 20},
        ],
    },
    "Tequila_Sunrise.recipe": {
        "name": "Tequila Sunrise",
        "description": "A nice Tequila Sunrise Cocktail",
        "version": "1.0.0",
        "ingredients": {"0": "weißer Tequila", "1": "Orangensaft", "2": "Grenadine"},
        "steps": [
            {"action": "scale", "ingredient": "0", "amount": 10},
            {"action": "scale", "ingredient": "1", "amount": 120},
            {"action": "confirm", "text": "ADD ICE"},
            {"action": "scale", "ingredient": "2", "amount": 40},
            {"action": "wait", "text": "WAIT FOR SETTLE DOWN", "amount": 10},
        ],
    },
    "Strawberry_Colada.recipe": {
        "name": "Strawberry Colada",
        "description": "A fruity strawberry cocktail with coconut",
        "version": "1.0.0",
        "ingredients": {
            "0": "10 Strawberries",
            "1": "Coconut-Juice",
            "2": "Cream",
            "3": "Pineapple-Juice",
            "4": "white Rum",
            "5": "Crushed Ice",
        },
        "steps": [
            {"action": "confirm", "text": "puree strawberries"},
            {"action": "confirm", "text": "add 1/2 crushed ice"},
            {"action": "scale", "ingredient": "1", "amount": 60},
            {"action": "scale", "ingredient": "2", "amount": 30},
            {"action": "scale", "ingredient": "3", "amount": 80},
            {"action": "scale", "ingredient": "4", "amount": 50},
            {"action": "wait", "text": "Shake", "amount": 30},
        ],
    },
}
