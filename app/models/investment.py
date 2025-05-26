from app.extensions import db

class Investment(db.Model):
    __tablename__ = 'Investment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.Integer, nullable=False)
    ticker = db.Column(db.String, nullable = False)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __str__(self):
        return f'[id: {self.id}, portfolioId: {self.portfolio_id}, ticker: {self.ticker}, price: {self.price}, quantity: {self.quantity}]'
    
    def to_dict(self):
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "ticker": self.ticker,
            "price": self.price,
            "quantity": self.quantity,
            "date": self.date.isoformat() if self.date else None
        }
    