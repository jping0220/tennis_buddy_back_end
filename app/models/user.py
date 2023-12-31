from app import db

class TennisUser(db.Model):
    tennis_user_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    auth_user_id = db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    tennis_level = db.Column(db.Float)
    preferences = db.Column(db.String(300))

    def to_dict(self):
        return {
            "tennis_user_id": self.tennis_user_id,
                "name":self.name,
                "email":self.email,
                "zip_code":self.zip_code,
                "tennis_level":self.tennis_level,
                "preferences":self.preferences
                }
    
    @classmethod
    def from_dict(cls,user_data):
        return cls(
            name = user_data["name"],
            email = user_data["email"],
            zip_code = user_data["zip_code"],
            tennis_level = user_data["tennis_level"],
            preferences = user_data["preferences"]
        )
