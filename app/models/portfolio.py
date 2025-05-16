from app.extensions import db

class Portfolio(db.Model):
    __tablename__ = 'Portfolio'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    strategy = db.Column(db.String, nullable=False)
    userId = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'[id: {self.id}, name: {self.name}, strategy={self.strategy}]'
    
    def to_dict(self): 
        return {
            "id": self.id,
            "name": self.name,
            "strategy": self.strategy
        }