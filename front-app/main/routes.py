from main import app
from flask import render_template,redirect,url_for,flash,request,jsonify
from main.models import Item,User
from main.forms import RegisterForm
from main import db
from generalObjects.conn_postgres import ConnPostgres
import requests,json


@app.route('/')
@app.route('/home')
def home_page():
    data = [
        {'name': 'Apple', 'category': 'Fruit'},
        {'name': 'Carrot', 'category': 'Vegetable'},
        {'name': 'Orange', 'category': 'Fruit'},
        {'name': 'Potato', 'category': 'Vegetable'},
        {'name': 'Potato', 'category': 'Vegetable'},
        {'name': 'Potato', 'category': 'Vegetable'},
        {'name': 'Potato', 'category': 'Vegetable'},
        {'name': 'Potato', 'category': 'Vegetable'},
        {'name': 'Potato', 'category': 'Vegetable'},
    ]
    # filter_category = request.args.get('filter_category', '')
    # if filter_category:
    #     data = [item for item in data if item['category'] == filter_category]
    return render_template('home.html', data=data)


@app.route('/settings')
def setting_page():
    url = "http://130.185.119.119:6000/googleTrends/kw/list"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        try:
            data = response.json()
            print(data)
        except ValueError:
            print(response.text)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        data =  {'kw': None}
    # data = [
    #     {'kw': 'stock'}


    return render_template('settings.html', data=data)


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
    url: str = "http://130.185.119.119:6000/googleTrends/kw/list"
    result = {"kw": [d["kw"] for d in data]}
    payload = json.dumps(result)
    print(payload)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request(method="POST", url=url, headers=headers, data=payload)
    print(response.text)
    return jsonify({'status': 'success'})


@app.route('/update_goole_trends', methods=['POST'])
def update_goole_trends():
    url: str = "http://130.185.119.119:6000/googleTrends/update-all"

    payload = {}
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request(method="POST", url=url, headers=headers, data=payload)
    print(response.text)
    return jsonify({'status': 'success'}), 200