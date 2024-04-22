
class USER_INTERACTION_MODE:
    UNKNOWN = -1
    SCALE = 0
    CONFIRM = 1
    WAIT = 2

class ingredient:

    name: str = ""
    amount: int = -1
    id: int = 0

    def __init__(self, _name: str, _amount: int = -1, _id: int = 0):
        self.name = _name
        self.amount = _amount
        self.id = _id
class recipe_step:

    action: USER_INTERACTION_MODE = USER_INTERACTION_MODE.UNKNOWN
    ingredient_name: str = ""
    current_step_text: str = "---"
    target_value: int = 0


    def __init__(self, _action: USER_INTERACTION_MODE = USER_INTERACTION_MODE.UNKNOWN, _ingredient_name: str = "", _current_step_text: str = "---", _target_value: int = 0):
        self.action = _action
        self.ingredient_name = _ingredient_name
        self.current_step_text = _current_step_text
        self.target_value = _target_value

    def to_dict(self) -> dict:
        return {
            'action': self.action,
            'ingredient' : self.ingredient_name,
            'amount': self.target_value,
            'text': self.current_step_text
            }
    
    def from_dict(self, _step_dict: dict):
        if 'action' in _step_dict:
            self.action = _step_dict['action']
        if 'ingredient' in _step_dict:
            self.ingredient_name = _step_dict['ingredient']
        if 'amount' in _step_dict:
            self.target_value = _step_dict['amount']
        if 'text' in _step_dict:
            self.current_step_text = _step_dict['text']


class recipe:
    
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    filename: str = ""
    steps: list[recipe_step] = []
    categories: list[str] = ["everything"]
    valid: bool = False

    current_step_index: int = -1

    def __init__(self, _name: str = "Recipe", _description:str = "A nice cocktail", _version: str = "1.0.0", _categories: list[str] = ["everything"]) -> None:
        self.name = _name
        self.description = _description
        self.version = _version

        self.filename = self.name.replace(" ", "_").replace(".recipe", "")
        self.filename = self.filename + ".recipe"

        self.categories = _categories
        if len(self.categories) <= 0:
            self.categories.append("everything")

       
        self.steps = []
        self.reset_steps()

   

    def add_step(self, _step: recipe_step):
        self.steps.append(_step)
           

    
    def from_dict(self, _json_dict: dict) -> bool:
        if 'name' in _json_dict:
            self.name = _json_dict['name']
        if 'description' in _json_dict:
            self.description = _json_dict['description']
        if 'version' in _json_dict:
            self.version = _json_dict['version']

        if 'steps' in _json_dict:
            steps = _json_dict['steps']
            self.steps = []
            if len(steps) > 0:
                for s in steps:
                    step: recipe_step = recipe_step()
                    step.from_dict(s)
                    self.add_step(step)
        
      
        self.filename = self.name.replace(" ", "_").replace(".recipe", "")
        self.filename = self.filename + ".recipe"
        self.valid = True
        
    def to_dict(self, _add_filename_as_root_key: bool = False) -> dict:
        ret: dict = {}
        ret[self.filename] = {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'filename': self.filename
        }
        # ADD STEPS
        ret[self.filename]['steps'] = []
        for s in self.steps:
            ret[self.filename]['steps'].append(s.to_dict())

    
        if _add_filename_as_root_key:
            return ret

        return ret[self.filename]


    def is_valid(self) -> bool:
        return self.valid


    def get_description(self) -> str:
        return self.description

    def get_categories(self) -> list[str]:
        return self.categories

    


    def get_recipe_information(self) -> tuple[str, str]:
        return (self.name, self.description)
    

    def switch_next_step(self):
        if len(self.steps) < 0:
            self.current_step_index = -1
            return
        self.current_step_index = (self.current_step_index + 1) % len(self.steps)
                  
    def switch_prev_step(self):
        if len(self.steps) < 0:
            self.current_step_index = -1
            return
        self.current_step_index = (self.current_step_index - 1) % len(self.steps)

    def reset_steps(self):
        if len(self.steps) < 0:
            self.current_step_index = -1
            return
        self.current_step_index = 0
    
    def get_ingredients(self) -> list[ingredient]:
        for s in self.steps:
            pass
        # GET SUMMED UP AMOUNTS OF ALL INGREDIENTS
    
    def get_ingredients_as_names_list(self) -> list[str]:
        rt: list[str] = []
        for i in self.get_ingredients():
            rt.append("{} - {}".format(i.amount, i.name))
    
        return rt


    def get_current_recipe_step(self) -> recipe_step: # (action, ingredient, current_step, max_steps, target_weight, finished)
        if len(self.steps) <= 0 or self.current_step_index < 0:
            return None
        
        return self.steps[self.current_step_index]
        
    






if __name__ == "__main__":
    import example_recipes

    r = example_recipes.EXAMPLE_RECIPES_COLLECTION_STRAWBERRY_COLADA()
    c = r.get_categories()
    n = r.get_description()
    i1, i2 = r.get_recipe_information()



    js = r.to_dict()

    r1 = recipe()
    r1.from_dict(js)
    i3, i4 = r1.get_recipe_information()
    t = 0

    