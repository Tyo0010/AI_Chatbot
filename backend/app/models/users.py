from app import db

class User(db.Model):
    id = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.String(64),
        nullable=False,
        unique=True
    )
    email = db.Column(
        db.String(64),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(255),
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime(timezone=True), 
        server_default=db.func.now()
    )
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password, 
            "created_at": self.created_at
        }
