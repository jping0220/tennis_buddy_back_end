from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, antoincrement = True)
    name = db.Column(db.String)
    tennis_level = db.Column(db.Integer)
    zip_code = db.Column(db.Integer)

    def to_dict(self):
        return {
                "id":self.user_id,
                "name":self.name,
                "tennis_level":self.tennis_level,
                "zip_code":self.zip_code
                }
    @classmethod
    def from_dict(cls,user_data):
        return cls(
            name = user_data["name"],
            tennis_level = user_data["tennis_level"],
            zip_code = user_data["zip_code"]
        )