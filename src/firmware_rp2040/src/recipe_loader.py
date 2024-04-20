import machine
import os
import time
import json

from ui import ui
import config
import helper
import example_recipes
import settings


class USER_INTERACTION_MODE:
    SCALE = 0
    CONFIRM = 1
    WAIT = 2



class recipe_loader:
    
  
    loaded_recipe = None
    current_recipe_step = None
   

    def __init__(self):
        print("recipe_loader: __init__")

        self.unload_recipe()
        self.create_initial_recipe()
        
    def get_recipe_information(self) -> (str, str):
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
    
    def is_recipe_loaded(self):
        if self.loaded_recipe is not None:
            return True
        return False
        
    def get_current_recipe_step(self) -> (USER_INTERACTION_MODE, str, str, int, int, int, bool): # (action, ingredient, current_step, max_steps, target_weight, finished)
        if self.loaded_recipe is None:
            return (None, None, None, None, None, None, True)
        steps = self.loaded_recipe['steps']
        n_steps = len(steps)
        if self.current_recipe_step is None:
            self.current_recipe_step = 0
        
        if self.current_recipe_step >= n_steps:
             return (None, None, None, None, None, None, True)
            
        step = steps[self.current_recipe_step]
        if step['action'] == 'scale':
            ingredient_name = self.loaded_recipe['ingredients'][step['ingredient']]
            return (USER_INTERACTION_MODE.SCALE, step['action'], ingredient_name, self.current_recipe_step+1, n_steps, step['amount'], False)
        elif step['action'] == 'confirm':     
            return (USER_INTERACTION_MODE.CONFIRM, step['action'], step['text'], self.current_recipe_step+1, n_steps, 0, False)
        elif step['action'] == 'wait':     
            return (USER_INTERACTION_MODE.WAIT, step['action'], step['text'], self.current_recipe_step+1, n_steps, step['amount'], False)
        else:
            return (None, None, None, None, None, None, True)
                    
    def unload_recipe(self):
        self.loaded_recipe = None
        
    def get_ingredient_list(self) -> [str]:
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
        


    def create_initial_recipe(self):
        for k in example_recipes.EXAMPLE_RECIPES_COLLECTION:
            settings.settings().write_json_file(k + ".recipe", example_recipes.EXAMPLE_RECIPES_COLLECTION[k])
            

    def list_recpies(self) -> (str, str):
        res = []
        for f in settings.settings().list_files():
            if f.endswith('.recipe'):
                # f = tequila_sunrise.recipe
                name = f.replace('.recipe', '').replace('_', ' ')
                res.append((f,name))
        return res
    
    def load_recipe(self, _filename: str) -> bool:
         
        if '.recipe' not in _filename:
            _filename = _filename + ".recipe"
            
        if _filename not in settings.settings().list_files():
            return False
        
        json_recipe = settings.settings().load_json_file(_filename)
        
        if json_recipe:
            self.loaded_recipe = json_recipe
            return True

    
    
    
