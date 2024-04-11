from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import hashlib
import json
from flask_login import current_user
from models.login import LoginManagement, User
from models.dashboard import Dashboard
from models.product_management import ProductManagement
from models.inventory_management import InventoryManagement
from models.sale_process import SaleProcess
from models.customer_management import CustomerManagement
from models.employee_management import EmployeeManagement
from models.sales_history import SalesHistory
from models.payment_integration import PaymentIntegration
from models.expenses import ExpensesManagement
from models.setting import SettingsManagement
from models.cash_register import CashRegisterManagement


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
settings_manager = SettingsManagement()
app.config['SECRET_KEY'] = 'your_secret_key'

#Aqui manejo las sessiones
def load_settings():
    return settings_manager.get_settings()
settings = load_settings()

@app.context_processor
def inject_settings():
    settings = settings_manager.get_settings()
    return dict(settings=settings)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    log = LoginManagement()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = log.get_login(username)

        if user:
            user_id, stored_password_hash = user
            if check_password_hash(stored_password_hash, password):
                user_obj = User(user_id)
                if not user_obj.verificar_expiracion():  
                    flash('Tu suscripción ha expirado', 'error')
                    return redirect(url_for('login'))

                login_user(user_obj)
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Usuario no encontrado', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Se ha cerrado la sesión', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    log = LoginManagement()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar si el usuario ya existe
        existing_user = log.get_login(username)
        if existing_user:
            return render_template('register.html', error='El usuario ya existe')

        password_hash = generate_password_hash(password)

        log.register_user(username, password_hash)

        return redirect('/login')

    return render_template('register.html', error=None)


@app.route('/')
def inicio():
    return render_template('index.html')

#Aqui la sección de Administrador 
@app.route('/update-sales-data')
@login_required
def update_sales_data():
    period = request.args.get('period')
    if period not in ['day', 'week', 'month', 'year']:
        return jsonify({'error': 'Período no válido'}), 400

    dashboard_data = Dashboard()
    sales_data = dashboard_data.get_sales_by_period(period)

    labels = [sale[0] for sale in sales_data]
    data = [sale[1] for sale in sales_data]

    return jsonify({'labels': labels, 'data': data})

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        dashboard_data = Dashboard()
        dashboard_data.get_total_sales()
        dashboard_data.get_total_inventory()

        period = request.args.get('period', 'day') 
        if period == 'day':
            sales_data = dashboard_data.get_sales_by_period('day')
        elif period == 'week':
            sales_data = dashboard_data.get_sales_by_period('week')
        elif period == 'month':
            sales_data = dashboard_data.get_sales_by_period('month')
        elif period == 'year':
            sales_data = dashboard_data.get_sales_by_period('year')
        else:
            raise ValueError("Período no válido")

        top_products = dashboard_data.get_top_products()
        
        inventory_by_category = dashboard_data.get_inventory_by_category()

        total_sales, total_costs, total_expenses, total_profit, total_egress = dashboard_data.get_financial_reports()
        

        print(period)
        return render_template('dashboard.html',
                            sales_data=sales_data,  
                            total_sales=dashboard_data.total_sales,
                            total_inventory=dashboard_data.total_inventory,
                            top_products=top_products,
                            inventory_by_category=inventory_by_category,
                            total_costs=total_costs,
                            total_expenses=total_expenses,
                            total_profit=total_profit,
                            total_egress=total_egress)
    except Exception as e:
        error_message = f"Error al cargar el panel de control: {str(e)}"
        return render_template('error.html', error_message=error_message)


@app.route('/product_management', methods=['GET', 'POST'])
def product_management():
    product_manager = ProductManagement()
    products = product_manager.get_products()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_product':
            name = request.form.get('name').title()
            category = request.form.get('category')
            price = request.form.get('price')
            cost = request.form.get('cost')
            quantity = request.form.get('quantity')
            product_manager.add_product(name, category, price, cost,quantity)
            print(f"Added product: {name}, Price: {price}, Quantity: {quantity}")

        elif action == 'update_product':
            product_id = request.form.get('product_id')
            name = request.form.get('name').title()
            price = request.form.get('price')
            quantity = request.form.get('quantity')
            product_manager.update_product(product_id, name, price, quantity)
            print(f"Updated product with ID {product_id}: New Name: {name}, Price: {price}, Quantity: {quantity}")

        elif action == 'delete_product':
            product_id = request.form.get('product_id')
            product_manager.delete_product(product_id)
            print(f"Deleted product with ID {product_id}")

        return redirect(url_for('product_management'))

    return render_template('product_management.html', products=products)


@app.route('/food_management', methods=['GET', 'POST'])
def food_management():
    product_manager = ProductManagement()
    foods = product_manager.get_foods()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_food':
            name = request.form.get('name').title()
            price = request.form.get('price')
            product_manager.add_food(name, price)
            print(f"Added food: {name}, Price: {price}")

        elif action == 'update_food':
            food_id = request.form.get('food_id')
            name = request.form.get('name').title()
            price = request.form.get('price')
            product_manager.update_food(food_id, name, price)
            print(f"Updated food with ID {food_id}: New Name: {name}, Price: {price}")

        elif action == 'delete_food':
            food_id = request.form.get('food_id')
            product_manager.delete_product(food_id) 
            print(f"Deleted food with ID {food_id}")

        return redirect(url_for('food_management'))

    return render_template('food_management.html', foods=foods)


@app.route('/inventory_management', methods=['GET', 'POST'])
def inventory_management():
    inventory_manager = InventoryManagement()
    inventory = inventory_manager.get_inventory()
    return render_template('inventory.html', inventory=inventory)

@app.route('/sales_history')
def sales_history():
    sales_history_manager = SalesHistory()
    sales = sales_history_manager.get_sales_history()
    return render_template('sales_history.html', sales=sales)

@app.route('/customer_management', methods=['GET', 'POST'])
def customer_management():
    customer_manager = CustomerManagement()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_customer':
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            customer_manager.add_customer(name, email, phone)
            print(f"Added customer: {name}, Email: {email}, Phone: {phone}")

        elif action == 'update_customer':
            customer_id = request.form.get('customer_id')
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            customer_manager.update_customer(customer_id, name, email, phone)
            print(f"Updated customer with ID {customer_id}: New Name: {name}, Email: {email}, Phone: {phone}")

        elif action == 'delete_customer':
            customer_id = request.form.get('customer_id')
            customer_manager.delete_customer(customer_id)
            print(f"Deleted customer with ID {customer_id}")

        return redirect(url_for('customer_management'))

    customers = customer_manager.get_customers()
    return render_template('customer_management.html', customers=customers)

@app.route('/employee_management', methods=['GET', 'POST'])
def employee_management():
    employee_manager = EmployeeManagement()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_employee':
            name = request.form.get('name')
            position = request.form.get('position')
            email = request.form.get('email')
            phone = request.form.get('phone')
            employee_manager.add_employee(name, position, email, phone)
            print(f"Added employee: {name}, Position: {position}, Email: {email}, Phone: {phone}")

        elif action == 'update_employee':
            employee_id = request.form.get('employee_id')
            name = request.form.get('name')
            position = request.form.get('position')
            email = request.form.get('email')
            phone = request.form.get('phone')
            employee_manager.update_employee(employee_id, name, position, email, phone)
            print(f"Updated employee with ID {employee_id}: New Name: {name}, Position: {position}, Email: {email}, Phone: {phone}")

        elif action == 'delete_employee':
            employee_id = request.form.get('employee_id')
            employee_manager.delete_employee(employee_id)
            print(f"Deleted employee with ID {employee_id}")

        return redirect(url_for('employee_management'))

    employees = employee_manager.get_employees()
    return render_template('employee_management.html', employees=employees)

@app.route('/payment_integration', methods=['GET', 'POST'])
def payment_integration():
    payment_manager = PaymentIntegration()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_payment_method':
            name = request.form.get('name')
            interes = float(request.form.get('interes'))
            payment_manager.add_payment_method(name, float(interes))
            print(f"Added payment method: {name, interes}")

        elif action == 'delete_payment_method':
            payment_method_id = request.form.get('payment_method_id')
            payment_manager.delete_payment_method(payment_method_id)
            print(f"Deleted payment method with ID {payment_method_id}")

        return redirect(url_for('payment_integration'))

    payment_methods = payment_manager.get_payment_methods()
    return render_template('payment_integration.html', payment_methods=payment_methods)


@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    expenses_manager = ExpensesManagement()

    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']
        category = request.form['category']

        expenses_manager.add_expense(description, amount, date, category)
        flash('Gasto agregado con éxito', 'success')
        return redirect(url_for('expenses'))

    expenses = expenses_manager.get_all_expenses()
    return render_template('expenses.html', expenses=expenses)

@app.route('/cash_register', methods=['GET', 'POST'])
def cash_register():
    if request.method == 'POST':
        amount = request.form['amount']
        cash_register_manager = CashRegisterManagement()
        cash_register_manager.add_to_cash_register(amount)
        flash('Cantidad agregada a la caja con éxito', 'success')
        return redirect(url_for('cash_register'))
    else:
        cash_register_manager = CashRegisterManagement()
        entries = cash_register_manager.get_cash_register_entries()
        return render_template('cash_register.html', entries=entries)

@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    global settings
    settings_manager = SettingsManagement()
    if request.method == 'POST':
        company_name = request.form['company_name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        
        settings_manager.update_setting(company_name, address, phone_number)
        
        settings = load_settings()

    return render_template('settings.html', settings=settings)

#Seccion de ventas 
@app.route('/sale_process', methods=['GET', 'POST'])
def sale_process():
    success_message = None
    if 'payment_methods' not in session:  
        session['payment_methods'] = PaymentIntegration().get_payment_methods()

    customers_manager = CustomerManagement()
    customers = customers_manager.get_customers()

    if request.method == 'POST':
        total = 0
        selected_items = []
        quantities = []

        cart_items = json.loads(request.form.get('cart', '{}'))
        for item_id, item_data in cart_items.items():
            selected_items.append(item_id)
            quantities.append(item_data['quantity'])
            total += item_data['price'] * item_data['quantity']

        print("Total antes de aplicar el interés:", total)

        payment_method_id = request.form.get('payment_method')
        payment_method_name = None
        if payment_method_id and payment_method_id.strip():  
            payment_method_id = int(payment_method_id)
            payment_method = None
            for method in session['payment_methods']:
                if method[0] == payment_method_id:
                    payment_method = method
                    break
            if payment_method:
                payment_method_name = payment_method[1]
            print("Método de pago seleccionado - ID:", payment_method_id, "Nombre:", payment_method_name)

            payment_integration = PaymentIntegration()
            interest_rate = payment_integration.get_interes(payment_method_id)
            print("Tasa de interés:", interest_rate)

            total_with_interest = total * (1 + interest_rate / 100)
            total_with_interest = round(total_with_interest, 2)
            total_display = f"{total_with_interest:.2f}"
            print("Total con interés:", total_display)

            sale_processor = SaleProcess()
            sale_id = sale_processor.make_sale(selected_items, quantities, total_with_interest, payment_method_id)
            if sale_id:
                success_message = f'Venta realizada con éxito. Total: ${total_display}'
            else:
                success_message = 'Error al realizar la venta.'

    products = ProductManagement().get_products()  
    foods = ProductManagement().get_foods()  
    payment_methods = session['payment_methods']  

    return render_template('sale_process.html', products=products, foods=foods, success_message=success_message,
                        payment_methods=payment_methods, customers=customers)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
