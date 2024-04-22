
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
    step_valid: bool = False
    action: USER_INTERACTION_MODE = USER_INTERACTION_MODE.UNKNOWN
    ingredient_name: str = ""
    current_step_text: str = "---"
    max_step: int = -1
    target_value: int = 0


    def __init__(self, _step_valid: bool = False, _action: USER_INTERACTION_MODE = USER_INTERACTION_MODE.UNKNOWN, ingredient_name: str = "", _current_step_text: str = "---", _max_step: int = -1, _target_value: int = 0):
        self.step_valid = _step_valid
        self.action = _action
        self.ingredient_name = ingredient_name
        self.current_step_text = _current_step_text
        self.max_step = _max_step
        self.target_value = _target_value

    def to_dict() -> dict:
        return {}
    
    def from_dict():
        pass


class recipe:
    
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    filename: str = ""
    steps: list[recipe_step] = []
    categories: list[str] = ["everything"]
    valid: bool = False


    def __init__(self, _name: str, _description:str = "A nice cocktail", _version: str = "1.0.0", _categories: list[str] = ["everything"]) -> None:
        self.name = _name
        self.description = _description
        self.version = _version

        self.filename = self.name.replace(" ", "_").replace(".recipe", "")
        self.filename = self.filename + ".recipe"

        self.categories = _categories
        if len(self.categories) <= 0:
            self.categories.append("everything")

       
        self.steps = []


   

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
                    self.add_step(recipe_step().from_dict(s))
        
      
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
            ret[self.filename].append(s.to_dict)

    
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
        if self.loaded_recipe is None:
            return ("invalid", "---")
        return (self.loaded_recipe['name'], self.loaded_recipe['description'])
    

    def switch_next_step(self):
        pass
                  
    def switch_prev_step(self):
        pass

    
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
        if self.loaded_recipe is None:
            return recipe_step()
        
        return recipe_step()