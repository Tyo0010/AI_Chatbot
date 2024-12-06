from app import db

class Logs(db.Model):
    id = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True
    )
    level = db.Column(
        db.String(32),
        nullable=False
    )
    message = db.Column(
        db.TEXT,
        nullable=False
    )
    created_at = db.Column(
         db.DateTime() 
    )
    
    def serialize(self):
        return{
            "id": self.id,
            "level": self.level,
            "message": self.message,
            "created_at": self.created_at
        }