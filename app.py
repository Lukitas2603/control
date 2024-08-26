from flask import Flask, render_template, request, redirect, url_for
from models import db, Expense
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    expenses = Expense.query.all()
    
    # Obtener la lista de meses disponibles
    months = sorted(set(inst['month'] for expense in expenses for inst in expense.get_installments()))
    
    # Construir un diccionario para gastos mensuales organizados por tarjeta
    monthly_expenses = {month: {} for month in months}
    for expense in expenses:
        for inst in expense.get_installments():
            if inst['month'] not in monthly_expenses:
                monthly_expenses[inst['month']] = {}
            if expense.tarjeta not in monthly_expenses[inst['month']]:
                monthly_expenses[inst['month']][expense.tarjeta] = []
            monthly_expenses[inst['month']][expense.tarjeta].append({
                'descripcion': expense.descripcion,
                'monto': inst['amount'],
                'cuota': inst['installment'],
                'total_cuotas': expense.cuotas,
                'fecha': expense.date.strftime('%d/%m/%Y')
            })
    
    # Calcular totales por mes
    monthly_totals = {month: sum(item['monto'] for tarjeta in tarjetas.values() for item in tarjeta) for month, tarjetas in monthly_expenses.items()}
    
    return render_template('index.html', monthly_expenses=monthly_expenses, monthly_totals=monthly_totals)

@app.route('/add', methods=['POST'])
def add_expense():
    tarjeta = request.form['tarjeta']
    descripcion = request.form['descripcion']
    monto = float(request.form['monto'])
    cuotas = int(request.form['cuotas'])
    fecha = request.form['fecha']
    fecha = datetime.strptime(fecha, '%Y-%m-%d') if fecha else datetime.utcnow()
    
    new_expense = Expense(tarjeta=tarjeta, descripcion=descripcion, monto=monto, cuotas=cuotas, date=fecha)
    db.session.add(new_expense)
    db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80, debug=True)