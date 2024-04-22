import recipe

def EXAMPLE_RECIPES_COLLECTION_TEST() -> recipe.recipe:
    ts: recipe.recipe = recipe.recipe("Test Recipe", "To test the system", "1.0.0", ["test"])
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="White Tequila", _current_step_text="", _target_value = 10))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="White Tequila", _current_step_text="", _target_value = 10))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Orange Juice", _current_step_text="", _target_value = 120))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Orange Juice", _current_step_text="", _target_value = 120))

    ts.valid = True
    return ts

def EXAMPLE_RECIPES_COLLECTION_TEQUILA_SUNRISE() -> recipe.recipe:
    ts: recipe.recipe = recipe.recipe("Tequila Sunrise", "A nice Tequila Sunrise Cocktail", "1.0.0", ["Tequila"])
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="White Tequila", _current_step_text="", _target_value = 10))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Orange Juice", _current_step_text="", _target_value = 120))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.CONFIRM, _ingredient_name="Ice", _current_step_text="Add Ice", _target_value = -1))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Grenadine", _current_step_text="", _target_value = 40))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.WAIT, _ingredient_name="", _current_step_text="Wait for settle down", _target_value = 10))
    ts.valid = True
    return ts


def EXAMPLE_RECIPES_COLLECTION_STRAWBERRY_COLADA() -> recipe.recipe:
    sc: recipe.recipe = recipe.recipe("Strawberry Colada", "Fruity strawberries, coconut and cream", "1.0.0", ["Cream", "Rum"])

    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.CONFIRM, _ingredient_name="Strawberries", _current_step_text="Puree and add", _target_value = 10))
    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Coconut Juice", _current_step_text="Add", _target_value = 80))
    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Cream", _current_step_text="Add", _target_value = 60))
    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="White Rum", _current_step_text="Add", _target_value = 50))
    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Pineapple Juice", _current_step_text="Add", _target_value = 80))
    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.WAIT, _ingredient_name="", _current_step_text="Shake", _target_value = 20))
    sc.valid = True
    return sc

def GET_EXAMPLE_RECIPES_COLLECTION() -> list[recipe.recipe]:
    return [EXAMPLE_RECIPES_COLLECTION_TEQUILA_SUNRISE(), EXAMPLE_RECIPES_COLLECTION_STRAWBERRY_COLADA()]
