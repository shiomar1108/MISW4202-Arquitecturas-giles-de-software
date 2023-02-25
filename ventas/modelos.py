from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import DateTime, func


db = SQLAlchemy()

class Milog(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(255))
    description =  db.Column(db.String(255))
    createdAt  =  db.Column(DateTime(timezone=True), server_default=func.now()    )
    

class LogSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Milog
         load_instance = True

