import machine
import os
import time
import json

from ui import ui
import config
import helper
import example_recipes
import settings
import recipe
from singleton import singleton



@singleton
class recipe_loader:
    
  
   
    def __init__(self):
        print("recipe_loader: __init__")

        self.create_initial_recipe()
        
   
     
    def create_initial_recipe(self):
        for k in example_recipes.EXAMPLE_RECIPES_COLLECTION:
            settings.settings().write_json_file(k + ".recipe", example_recipes.EXAMPLE_RECIPES_COLLECTION[k])
            

    def list_recpies(self, _include_description: bool = False) -> tuple[str, str, str]:
        res = []
        for f in settings.settings().list_files():
            if f.endswith('.recipe'):
                # f = tequila_sunrise.recipe
                name: str = f.replace('.recipe', '').replace('_', ' ')

                description: str = ""

                if _include_description:
                    r: recipe.recipe = self.get_recipe_by_filename(f)
                    description = r.get_description()
                    del r

                res.append((f,name, description))
        return res
    


    def get_recipe_by_filename(self, _filename: str) -> recipe:
         
        if '.recipe' not in _filename:
            _filename = _filename + ".recipe"
            
        if _filename not in settings.settings().list_files():
            return recipe.recipe()
        
        json_recipe = settings.settings().load_json_file(_filename)
        


        # TODO IMPLEMENT LOADER
        if json_recipe:
            pass
        
        return recipe.recipe()
    
    
