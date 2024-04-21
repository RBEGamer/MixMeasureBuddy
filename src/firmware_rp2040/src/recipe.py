
class USER_INTERACTION_MODE:
    UNKNOWN = -1
    SCALE = 0
    CONFIRM = 1
    WAIT = 2


class recipe_step:
    step_valid: bool = False
    action: USER_INTERACTION_MODE = USER_INTERACTION_MODE.UNKNOWN
    ingredient_name: str = "..."
    current_step_text: str = "---"
    max_step: int = -1
    target_value: int = 0
    recipe_finished: bool = True


    def __init__(self, _step_valid: bool = False, _action: USER_INTERACTION_MODE = USER_INTERACTION_MODE.UNKNOWN, _ingredient_name: str = "...", _current_step_text:str = "---", _max_step: int = -1, _target_value: int = 0, _recipe_finished: boo = False):
        self.step_valid = _step_valid
        self.action = _action
        self.ingredient_name = _ingredient_name
        self.current_step_text = _current_step_text
        self.max_step = _max_step
        self.target_value = _target_value
        self.recipe_finished = _recipe_finished

    # (action, ingredient, current_step, max_steps, target_weight, finished)

class recipe:
    

    def __init__(self) -> None:
        pass

    def is_valid(self) -> bool:
        return False


    def get_description(self) -> str:
        return ""

    def get_categories(self) -> list[str]:
        return []

    


    def get_recipe_information(self) -> tuple[str, str]:
        if self.loaded_recipe is None:
            return ("invalid", "---")
        
        return (self.loaded_recipe['name'], self.loaded_recipe['description'])
    
    def switch_next_step(self):
        if self.loaded_recipe is None:
            return
        if self.current_recipe_step is None:
            self.current_recipe_step = 0
        steps = self.loaded_recipe['steps']
        n_steps = len(steps)
        if self.current_recipe_step < n_steps:
            self.current_recipe_step = self.current_recipe_step + 1
                  
    def switch_prev_step(self):
        pass


    def get_ingredient_list(self) -> list[str]:
        if self.loaded_recipe is None:
            return []
        rt = []
        ing = self.loaded_recipe['ingredients']
        if ing is None:
            return []
        for k in ing:
            rt.append(ing[k])
        return rt
    
    def get_ingredient_str(self) -> str:
        rt = ""
        for item in self.get_ingredient_list():
            rt = rt + item + "\n"
        return rt


    def get_current_recipe_step(self) -> recipe_step: # (action, ingredient, current_step, max_steps, target_weight, finished)
        if self.loaded_recipe is None:
            return recipe_step()


        steps = self.loaded_recipe['steps']
        n_steps = len(steps)
        if self.current_recipe_step is None:
            self.current_recipe_step = 0
        
        # TODO JSON TO RECIPE IN RECIPE LOADER
        if self.current_recipe_step >= n_steps:
             return recipe_step(_recipe_finished = True)
            
        step = steps[self.current_recipe_step]
        if step['action'] == 'scale':
            ingredient_name = self.loaded_recipe['ingredients'][step['ingredient']]
            #return (USER_INTERACTION_MODE.SCALE, step['action'], ingredient_name, self.current_recipe_step+1, n_steps, step['amount'], False)
        elif step['action'] == 'confirm':
            pass     
            #return (USER_INTERACTION_MODE.CONFIRM, step['action'], step['text'], self.current_recipe_step+1, n_steps, 0, False)
        elif step['action'] == 'wait':     
            pass
            #return (USER_INTERACTION_MODE.WAIT, step['action'], step['text'], self.current_recipe_step+1, n_steps, step['amount'], False)
        else:
            return recipe_step()