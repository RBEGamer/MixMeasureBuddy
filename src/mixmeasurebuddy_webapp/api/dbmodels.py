from datetime import datetime
import names
from mongoengine import Document, IntField, EmbeddedDocument
from mongoengine import DateTimeField, StringField, ReferenceField, ListField, DictField, BooleanField, FloatField, EmbeddedDocumentListField


class Ingredient(Document):
    name = StringField(required=True, unique=True)
    weight_g_per_unit = FloatField(default=1.0, required=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name


    meta = {'collection': 'ingredients'}

class Step(EmbeddedDocument):
    action = StringField(required=True)
    text = StringField(required=False)
    ingredient = ReferenceField(Ingredient, default=None)
    amount = IntField(required=False)




class Category(Document):
    name = StringField(max_length=20, required=True, unique=True)

    meta = {'collection': 'categories'}

class Recipe(Document):
    name = StringField(max_length=20, required=True, unique=True)
    description = StringField(default="A nice new Cocktail", required=True)
    version = StringField(default="1.0.0", required=True, unique=False)
    ingredients = ListField(ReferenceField(Ingredient), unique=False)
    steps = EmbeddedDocumentListField(Step, required=False)
    author = ReferenceField("Users", required=False, unique=False)
    default_recipe = BooleanField(default=False, unique=False)
    category = ListField(ReferenceField(Category), unique=False, default=[])
    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    meta = {'collection': 'recipes'}




class Users(Document):
    name = StringField(default=names.get_full_name())
    linked_device_id = StringField(default="", required=True, unique=True)
    date_modified = DateTimeField(default=datetime.utcnow)
    linked_recipes = ListField(ReferenceField(Recipe))
    permissions = IntField(default=0, required=True)


    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    meta = {'collection': 'users'}
