from mongoengine import Document, StringField, DateField

class PanClient(Document):
    pan=StringField(required=True, unique=True)
    name=StringField(required=True)
    dob=DateField(required=True)
    father_name=StringField(required=True)