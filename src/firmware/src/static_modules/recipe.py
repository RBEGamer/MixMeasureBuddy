
class USER_INTERACTION_MODE:
    UNKNOWN = -1
    SCALE = 0
    CONFIRM = 1
    WAIT = 2

class ingredient:

    name: str = ""
    amount: int = -1
    id: int = 0
    unit: str = ""

    def __init__(self, _name: str, _amount: int = -1, _id: int = 0, _unit: str = ""):
        self.name = _name
        self.amount = _amount
        self.id = _id
        self.unit = _unit
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

        if self.target_value is None:
            self.target_value = 0

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

        if self.target_value is None:
            self.target_value = 0
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
        res: list[ingredient] = []
        ingredient_dict: dict = {}
        # DETERM THE TOTAL INGREDIENT AMOUNT OVER ALL STEPS
        # TODO REWORK
        for s in self.steps:
            # SKIP USER ACTIONS WITH NO PHYSICAL INGREDIENTS
            if s.action == USER_INTERACTION_MODE.WAIT or s.action == USER_INTERACTION_MODE.UNKNOWN:
                continue


            if not s.ingredient_name in ingredient_dict:
                ingredient_dict[s.ingredient_name] = {'amount': 0, 'unit': ''}
                
                if s.action == USER_INTERACTION_MODE.SCALE:
                    ingredient_dict[s.ingredient_name]['unit'] = 'g'
                elif s.action == USER_INTERACTION_MODE.CONFIRM:
                    ingredient_dict[s.ingredient_name]['unit'] = 'x'

            if s.target_value > 0:
                ingredient_dict[s.ingredient_name]['amount'] = ingredient_dict[s.ingredient_name]['amount'] + s.target_value

            
        # REASSEMBLE DICT INTO ARRAY
        index: int = 0
        for k, v in ingredient_dict.items():
            res.append(ingredient(k, v['amount'], index, v['unit']))
            index = index +1

        return res
       
    
    def get_ingredients_as_names_list(self, _without_amount: bool = True) -> list[str]:
        rt: list[str] = []
        for i in self.get_ingredients():
            if i.amount is None or i.amount <= 0 or _without_amount:
                rt.append("{}".format(i.name))
            else:
                rt.append("{}{} {}".format(i.amount, i.unit, i.name))
    
        return rt


    def get_current_recipe_step(self) -> tuple[recipe_step, bool]: 
        if len(self.steps) <= 0 or self.current_step_index < 0:
            print("self.current_step_index is invalid / out of range")
            return recipe_step(), True
        try:
            #DETERM IF THIS IS THE LAST STEP
            is_endstep: bool = False
            if self.current_step_index >= len(self.steps) -1:
                is_endstep = True

            return self.steps[self.current_step_index], is_endstep
        except Exception as e:
            print(e)

        return recipe_step(), True
        
    






if __name__ == "__main__":
    import example_recipes

    r = example_recipes.EXAMPLE_RECIPES_COLLECTION_TEST()
    i = r.get_ingredients()
    l = r.get_ingredients_as_names_list()
    er = 0

    