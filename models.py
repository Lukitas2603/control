from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tarjeta = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    cuotas = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)

    def get_installments(self):
        return [{'month': (self.date + timedelta(days=30 * i)).strftime("%Y-%m"), 'amount': self.monto / self.cuotas, 'installment': i + 1} for i in range(self.cuotas)]
