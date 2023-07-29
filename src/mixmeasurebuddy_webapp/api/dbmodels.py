from datetime import datetime
import names
from mongoengine import Document, IntField
from mongoengine import DateTimeField, StringField, ReferenceField, ListField, DictField, FloatField


class Ingredient(Document):
    name = StringField(required=True, unique=True)
    weight_g_per_unit = FloatField(default=1.0, required=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name


    meta = {'collection': 'ingredients'}

class Step(Document):
    action = StringField(required=True)
    text = StringField(required=False)
    ingredient = ListField[Ingredient]
    amount = IntField(required=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    meta = {'collection': 'recipes'}

class Recipe(Document):
    name = StringField(max_length=20, required=True, unique=True)
    description = StringField(default="A nice new Cocktail", required=True)
    version = StringField(default="1.0.0", required=True)
    ingredients = ListField(Ingredient, required=True)
    steps = ListField(Step, required=True)
    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    meta = {'collection': 'recipes'}




class Users(Document):
    name: StringField = StringField(default=names.get_full_name())
    linked_device_id: StringField = StringField()
    date_modified = DateTimeField(default=datetime.utcnow)
    linked_recipes: ListField(ReferenceField(Recipe))


    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    meta = {'collection': 'users'}
