from app import db

class History(db.Model):
    id = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    message = db.Column(
        db.String(16000000),
        nullable=False
    )
    response = db.Column(
        db.String(16000000),
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime() 
    )
    
    user = db.relationship("User")
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "response": self.response, 
            "timestamp": self.timestamp
        }