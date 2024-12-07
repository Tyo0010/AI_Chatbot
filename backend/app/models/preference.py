from app import db

class Preference(db.Model):
    id = db.Column(
        db.Integer(),
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey("user.id"),
        nullable=False
    )
    theme = db.Column(
        db.String(32),
        nullable=False,
        default="light"
    )
    language = db.Column(
        db.String(32),
        nullable=False,
        default='en'
    )
    noticfication = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )
    updated_time = db.Column(
        db.DateTime(timezone=True), 
        server_default=db.func.now()
    )
    
    user=db.relationship("User")
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "theme": self.theme,
            "language": self.language,
            "notification": self.noticfication,
            "updated_time": self.updated_time
        }