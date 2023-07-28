from mongoengine import Document
from mongoengine import DateTimeField, StringField, ReferenceField, ListField


class Ingredient(Document):

    name = StringField(max_length=20, required=True, unique=False)
    description = StringField(max_length=60, required=False, unique=False)
    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name
class Recipe(Document):
    name = StringField(max_length=20, required=True, unique=True)
    description = StringField(max_length=60, required=True, unique=True)
    version = StringField(max_length=10, required=True, unique=True)
    ingredients = ListField(ReferenceField(Ingredient))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name