import recipe

def EXAMPLE_RECIPES_COLLECTION_TEQUILA_SUNRISE() -> recipe.recipe:
    ts: recipe.recipe = recipe.recipe("Tequila Sunrise", "A nice Tequila Sunrise Cocktail", "1.0.0", ["Tequila"])
    ts.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.SCALE, "White Tequila", _current_step_text="", _target_value = 10))
    ts.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.SCALE, "Orange Juice", _current_step_text="", _target_value = 120))
    ts.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.CONFIRM, "Ice", _current_step_text="Add Ice", _target_value = -1))
    ts.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.SCALE, "Grenadine", _current_step_text="", _target_value = 40))
    ts.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.WAIT, "", _current_step_text="Wait for settle down", _target_value = 10))
    ts.valid = True
    return ts


def EXAMPLE_RECIPES_COLLECTION_STRAWBERRY_COLADA() -> recipe.recipe:
    sc: recipe.recipe = recipe.recipe("Strawberry Colada", "A fruity strawberry cocktail with coconut and cream", "1.0.0", ["Cream", "Rum"])

    sc.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.CONFIRM, "Strawberries", _current_step_text="Puree and add strawberries", _target_value = 10))
    sc.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.SCALE, "Coconut Juice", _current_step_text="", _target_value = 80))
    sc.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.SCALE, "Cream", _current_step_text="", _target_value = 60))
    sc.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.SCALE, "White Rum", _current_step_text="", _target_value = 50))
    sc.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.SCALE, "Pineapple Juice", _current_step_text="", _target_value = 80))
    sc.add_step(recipe.recipe_step(True,recipe.USER_INTERACTION_MODE.WAIT, "", _current_step_text="Skake", _target_value = 20))
    sc.valid = True
    return sc

def GET_EXAMPLE_RECIPES_COLLECTION() -> list[recipe.recipe]:
    return [EXAMPLE_RECIPES_COLLECTION_TEQUILA_SUNRISE(), EXAMPLE_RECIPES_COLLECTION_STRAWBERRY_COLADA()]
