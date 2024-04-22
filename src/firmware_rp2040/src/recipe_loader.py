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
        r: recipe.recipe
        for r in example_recipes.GET_EXAMPLE_RECIPES_COLLECTION():
            settings.settings().write_json_file(r.filename, r.to_dict())
            

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
    

    def get_recipe_file_content(self, _filename: str) -> dict:
        # CHECK FOR EXTENTION
        if not _filename.endswith('.recipe'):
            _filename = _filename + ".recipe"
        # CHECK FILE EXISTS
        if _filename not in settings.settings().list_files():
            return recipe.recipe()
        # LOAD CONTENT AS JSON
        json_recipe = settings.settings().load_json_file(_filename)
        return json_recipe
    

    def get_recipe_by_filename(self, _filename: str) -> recipe:
        # LOAD JSON CONTENT OF RECIPE FILE 
        json_recipe: dict = self.get_recipe_file_content(_filename)

        # CREATE RECIPE
        r: recipe.recipe = recipe.recipe()

        if json_recipe is None:        
            return r
        
        # PARSE JSON TO RECIPE
        return r.from_dict(json_recipe)
        

    
    
