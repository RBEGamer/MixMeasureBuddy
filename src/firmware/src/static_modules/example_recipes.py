import recipe

def EXAMPLE_RECIPES_COLLECTION_TEQUILA_SUNRISE() -> recipe.recipe:
    ts: recipe.recipe = recipe.recipe("Tequila Sunrise", "A nice Tequila Sunrise Cocktail", "1.0.0", ["Tequila"])
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="White Tequila", _current_step_text="", _target_value = 10))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Orange Juice", _current_step_text="", _target_value = 80))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.CONFIRM, _ingredient_name="Ice", _current_step_text="Add Ice", _target_value = -1))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Grenadine", _current_step_text="", _target_value = 40))
    ts.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.WAIT, _ingredient_name="", _current_step_text="Wait for settle down", _target_value = 10))
    ts.valid = True
    return ts

def EXAMPLE_RECIPES_COLLECTION_STRAWBERRY_COLADA() -> recipe.recipe:
    sc: recipe.recipe = recipe.recipe("Strawberry Colada", "Fruity strawberries, coconut and cream", "1.0.0", ["Cream", "Rum"])

    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.CONFIRM, _ingredient_name="Strawberries", _current_step_text="Puree and add", _target_value = 10))
    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Coconut Juice", _current_step_text="Add", _target_value = 50))
    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Cream", _current_step_text="Add", _target_value = 30))
    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="White Rum", _current_step_text="Add", _target_value = 20))
    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Pineapple Juice", _current_step_text="Add", _target_value = 50))
    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.WAIT, _ingredient_name="", _current_step_text="Shake", _target_value = 20))
    sc.valid = True
    return sc

def EXAMPLE_RECIPES_COLLECTION_WINE() -> recipe.recipe:
    sc: recipe.recipe = recipe.recipe("Wine", "Just a glass of wine", "1.0.0", ["Wine"])

    sc.add_step(recipe.recipe_step(_action=recipe.USER_INTERACTION_MODE.SCALE, _ingredient_name="Wine", _current_step_text="Add", _target_value = 80))
    sc.valid = True
    return sc





def RECIPES_COLLECTION_MARGARITA() -> recipe.recipe:
    m: recipe.recipe = recipe.recipe("Margarita", "Classic lime and tequila cocktail", "1.0.0", ["Tequila", "Lime Juice"])
    
    m.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Tequila", "Add", 25))
    m.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Triple Sec", "Add", 25))
    m.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Lime Juice", "Add", 25))
    m.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Ice", "Add Ice", 50))
    m.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.WAIT, "", "Shake", 20))
    m.valid = True
    return m

def RECIPES_COLLECTION_MARTINI() -> recipe.recipe:
    ma: recipe.recipe = recipe.recipe("Martini", "Dry gin or vodka with vermouth", "1.0.0", ["Gin", "Vermouth"])
    
    ma.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Gin or Vodka", "Add", 30))
    ma.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Dry Vermouth", "Add", 30))
    ma.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.WAIT, "Ice", "Stir with ice", 40))
    ma.valid = True
    return ma

def RECIPES_COLLECTION_OLD_FASHIONED() -> recipe.recipe:
    of: recipe.recipe = recipe.recipe("Old Fashioned", "Classic whiskey-based cocktail", "1.0.0", ["Whiskey", "Bitters"])
    
    of.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Sugar", "Muddle", 1))
    of.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Whiskey", "Add", 40))
    of.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Angostura Bitters", "Drops", 2))
    of.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Ice", "Add Ice", 50))
    of.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Orange Peel", "Garnish", 1))
    of.valid = True
    return of

def RECIPES_COLLECTION_MOJITO() -> recipe.recipe:
    mo: recipe.recipe = recipe.recipe("Mojito", "Minty and refreshing rum cocktail", "1.0.0", ["Mint", "Rum"])
    
    mo.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Mint Leaves", "Muddle", 10))
    mo.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "White Rum", "Add", 20))
    mo.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Sugar", "Add", 15))
    mo.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Lime Juice", "Add", 10))
    mo.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Soda Water", "Add", 50))
    mo.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Ice", "Add Ice", 50))
    mo.valid = True
    return mo

def RECIPES_COLLECTION_MANHATTAN() -> recipe.recipe:
    mn: recipe.recipe = recipe.recipe("Manhattan", "Whiskey-based cocktail with vermouth", "1.0.0", ["Whiskey", "Vermouth"])
    
    mn.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Whiskey", "Add", 50))
    mn.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Sweet Vermouth", "Add", 25))
    mn.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Angostura Bitters", "Add", 2))
    mn.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.WAIT, "", "Stir with ice", 30))
    mn.valid = True
    return mn

def RECIPES_COLLECTION_COSMOPOLITAN() -> recipe.recipe:
    c: recipe.recipe = recipe.recipe("Cosmopolitan", "Vodka, cranberry, and citrus mix", "1.0.0", ["Vodka", "Cranberry Juice"])
    
    c.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Vodka", "Add", 50))
    c.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Triple Sec", "Add", 15))
    c.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Cranberry Juice", "Add", 30))
    c.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Lime Juice", "Add", 10))
    c.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Ice", "Add Ice", 50))
    c.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.WAIT, "", "Shake", 20))
    c.valid = True
    return c

def RECIPES_COLLECTION_DAIQUIRI() -> recipe.recipe:
    d: recipe.recipe = recipe.recipe("Daiquiri", "Simple, lime-flavored rum cocktail", "1.0.0", ["Rum", "Lime Juice"])
    
    d.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "White Rum", "Add", 50))
    d.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Lime Juice", "Add", 25))
    d.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Sugar Syrup", "Add", 15))
    d.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Ice", "Add Ice", 50))
    d.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.WAIT, "Shake", "Shake", 20))
    d.valid = True
    return d

def RECIPES_COLLECTION_NEGRONI() -> recipe.recipe:
    n: recipe.recipe = recipe.recipe("Negroni", "Bitter and balanced aperitif cocktail", "1.0.0", ["Gin", "Campari"])
    
    n.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Gin", "Add", 30))
    n.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Campari", "Add", 30))
    n.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Sweet Vermouth", "Add", 30))
    n.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.WAIT, "", "Stir with ice", 20))
    n.valid = True
    return n

def RECIPES_COLLECTION_WHISKEY_SOUR() -> recipe.recipe:
    ws: recipe.recipe = recipe.recipe("Whiskey Sour", "Whiskey, lemon juice, sugar, and optional egg white", "1.0.0", ["Whiskey", "Lemon Juice"])
    
    ws.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Whiskey", "Add", 50))
    ws.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Lemon Juice", "Add", 25))
    ws.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Sugar Syrup", "Add", 15))
    ws.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Egg White", "Optional - Add", 1))
    ws.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.WAIT, "", "Shake", 20))
    ws.valid = True
    return ws

def RECIPES_COLLECTION_PINA_COLADA() -> recipe.recipe:
    pc: recipe.recipe = recipe.recipe("Pina Colada", "Tropical coconut and pineapple blend", "1.0.0", ["Rum", "Coconut Cream"])
    
    pc.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "White Rum", "Add", 20))
    pc.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Coconut Cream", "Add", 40))
    pc.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.SCALE, "Pineapple Juice", "Add", 80))
    pc.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.CONFIRM, "Ice", "Add", 50))
    pc.add_step(recipe.recipe_step(recipe.USER_INTERACTION_MODE.WAIT, "", "Blend", 20))
    pc.valid = True
    return pc




def GET_EXAMPLE_RECIPES_COLLECTION() -> list[recipe.recipe]:
    return [EXAMPLE_RECIPES_COLLECTION_TEQUILA_SUNRISE(), EXAMPLE_RECIPES_COLLECTION_STRAWBERRY_COLADA(), EXAMPLE_RECIPES_COLLECTION_WINE(), RECIPES_COLLECTION_MARGARITA(), RECIPES_COLLECTION_MARTINI(), RECIPES_COLLECTION_OLD_FASHIONED(), RECIPES_COLLECTION_MOJITO(), RECIPES_COLLECTION_MANHATTAN(), RECIPES_COLLECTION_COSMOPOLITAN(), RECIPES_COLLECTION_DAIQUIRI(),  RECIPES_COLLECTION_NEGRONI(), RECIPES_COLLECTION_WHISKEY_SOUR(), RECIPES_COLLECTION_PINA_COLADA()]
