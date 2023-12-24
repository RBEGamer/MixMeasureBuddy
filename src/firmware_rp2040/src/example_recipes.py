

EXAMPLE_RECIPES_COLLECTION: dict = {
    "example_recipe.recipe":{
        "name": "EXAMPLE_ RECIPE",
        "description": "A nice Example Cocktail",
        "version": "1.0.0",
        "ingredients": {"0": "A", "1": "B", "2": "C"},
        "steps":[
            {"action": "scale", "ingredient": "0", "amount": 10},
            {"action": "confirm", "text": "shake it"},
            {"action": "wait", "text": "wait for it", "amount": 20}
        ]
    }
}