from datetime import datetime
import names
from mongoengine import Document, IntField, EmbeddedDocument
from mongoengine import DateTimeField, StringField, ReferenceField, ListField, DictField, BooleanField, FloatField, EmbeddedDocumentListField


from json import JSONEncoder
from bson.json_util import default
from mongoengine import Document


class MongoEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Document):
            return o.to_mongo()
        return default(o)


class Ingredient(Document):
    meta = {'collection': 'ingredients'}
    name = StringField(required=True, unique=True)
    weight_g_per_unit = FloatField(default=1.0, required=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name




class Step(EmbeddedDocument):
    meta = {'abstract': True}

    action = StringField(required=True, default="")
    text = StringField(required=False, default="")
    ingredient = ReferenceField(Ingredient, required=False)
    amount = IntField(required=False)


class ScaleStep(Step):
    action = StringField(required=True, default="")
    text = StringField(required=False, default="")
    ingredient = ReferenceField(Ingredient, required=False)
    amount = IntField(required=False)


class Category(Document):
    meta = {'collection': 'categories'}
    name = StringField(max_length=20, required=True, unique=True)



class Recipe(Document):
    meta = {'collection': 'recipes'}
    name = StringField(max_length=20, required=True, unique=True)
    filename = StringField(required=True, unique=True)
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

    def tojson(self):
        json: dict = {'name': self.name, 'description': self.description, 'author': self.author.name, 'id': str(self.id)}
        return json






class Users(Document):
    meta = {'collection': 'users'}

    name = StringField(default=names.get_full_name())
    linked_device_id = StringField(default="", required=True, unique=True)
    date_modified = DateTimeField(default=datetime.utcnow)
    linked_recipes = ListField(ReferenceField(Recipe))
    permissions = IntField(default=0, required=True)

    firmware_version = StringField(default="0.0.0", required=False , unique=False)
    hardware_version = StringField(default="dev", required=False , unique=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name



