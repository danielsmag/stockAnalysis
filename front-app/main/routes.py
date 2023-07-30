from main import app
from flask import render_template,redirect,url_for,flash,request,jsonify
from main.models import Item,User
from main.forms import RegisterForm
from main import db
from generalObjects.conn_postgres import ConnPostgres

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def setting_page():

    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]
    data = [
        {'name': 'John', 'age': 30, 'city': 'New York'},
        {'name': 'Jane', 'age': 28, 'city': 'Los Angeles'},
        {'name': 'Jane', 'age': 28, 'city': 'Los Angeles'},
        {'name': 'Jane', 'age': 28, 'city': 'Los Angeles'}
        # Add as many dictionaries as you need
    ]
    return render_template('settings.html', data=data,items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/update_table', methods=['POST'])
def update_table():
    data = request.get_json()  # get the data from the request
    # Your code to update the table with the data goes here.
    # The data is in the form of a list of dictionaries, each with keys 'name', 'age', and 'city'
    print(data)
    return jsonify({'status': 'success'})