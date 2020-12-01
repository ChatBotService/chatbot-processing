from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    conversation_files = db.relationship("ConversationFile")

class ConversationFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    creation_date = db.Column(db.DateTime, default=datetime.now)
    data = db.Column(db.LargeBinary)
    data_size = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    models = db.relationship("TrainedModel")

class TrainedModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    creation_date = db.Column(db.DateTime, default=datetime.now)
    data = db.Column(db.LargeBinary)
    data_size = db.Column(db.Integer)
    file_id = db.Column(db.Integer, db.ForeignKey("conversation_file.id"))


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id",)

class ConversationFileSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "creation_date", "data_size", "user_id")

class TrainedModelSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "creation_date", "data_size", "file_id")

def init_db():
    user1 = User()
    db.session.add(user1)
    user2 = User()
    db.session.add(user2)
    db.session.commit()