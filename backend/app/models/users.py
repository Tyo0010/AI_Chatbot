from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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
    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime(timezone=True), 
        server_default=db.func.now()
    )

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def serialize(self):
        # Do not return the password hash
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at
        }
