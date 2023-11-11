from flask import Flask, render_template, request, flash, make_response, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(50))

    def __init__(self, username, password, user_id=0):
        self.user_id = user_id
        self.username = username
        self.password = password


    def __str__(self):
        return f'{self.username}'

with app.app_context():
    db.create_all()

@app.route('/add', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        return render_template('add_user.html')
    return render_template('add_user.html')

@app.route('/home')
def hello_world():
   return render_template('index.html')

def add(x,y):
    float_x = float(x)
    float_y = float(y)
    sum = float_x + float_y
    return sum

@app.route('/add/<x>/<y>')
def add_numbers(x,y):
    sum = add(x,y)
    return render_template('add.html',x=x,y=y,sum=sum)

def subtract(x,y):
    float_x = float(x)
    float_y = float(y)
    difference = float_x - float_y
    return difference

@app.route('/subtract/<x>/<y>')
def subtract_numbers(x,y):
    difference = subtract(x,y)
    return render_template('subtract.html',x=x,y=y,difference=difference)

def multiply(x,y):
    float_x = float(x)
    float_y = float(y)
    product = float_x * float_y
    return product

@app.route('/multiply/<x>/<y>')
def multiply_numbers(x,y):
    product = multiply(x,y)
    return render_template('multiply.html',x=x,y=y,product = product)

def divide(x,y):
    float_x = float(x)
    float_y = float(y)

    if float_y == 0.0:
        return 'I AM ERROR'

    quotient = float_x / float_y
    return quotient

@app.route('/divide/<x>/<y>')
def divide_numbers(x,y):
    quotient = divide(x,y)
    return render_template('divide.html',x=x,y=y,quotient = quotient)

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/welcome/<username>')
def welcome(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        username = 'NO USER'
        password='NO PASSWORD'
    else:
        username = user.username
        password = user.password
    return render_template('welcome.html', username=username, password=password)

# @app.route('/update/<username>', methods = ["GET","POST"], )
# def update(username):
#     user = User.query.filter_by(username=username).first()
#     if user == None:
#         abort(404)
#     username = user.username
#     password = user.password
#     if request.method == 'GET':
#         return render_template('update.html', username = username, password = password)
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user.username = username
#         user.password = password
#         db.session.commit()
#         flash('updated', 'success')
#         return redirect(url_for('update', username=username, password=password))

@app.route('/update/<uid>', methods = ["GET","POST"], )
def update(uid):
    user = User.query.filter_by(user_id=uid).first()
    if user == None:
        abort(404)
    username = user.username
    password = user.password
    if request.method == 'GET':
        return render_template('update.html', username = username, password = password)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user.username = username
        user.password = password
        db.session.commit()
        flash('updated', 'success')
        return redirect(url_for('users'))

@app.route('/groceries')
def groceries():
    groceries = ['carrots','apples','mangos']
    batteries = ['AA', 'AAA', 'Cells']
    return render_template('groceries.html',groceries=groceries, batteries = batteries)

@app.route('/unauthorized')
def unauthorized():
   return render_template('unauthorized.html')


# @app.route('/user/<username>')
# def user(username):
@app.route('/user')
def user():
    # do stuff to get username
    username = request.cookies.get('username')
    print(username)
    if username is None:
        return redirect(url_for('unauthorized'))
    return render_template('user.html', username = username)
    
@app.route('/signup', methods = ["GET","POST"])
def signup():
    username = ''
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('added', 'success')
        return redirect(url_for('welcome',username=username))


@app.route('/login', methods = ["GET","POST"])
def login():
    is_authenticated = False
    username = ''
    if request.method == 'GET':
        return render_template('login.html', username=username, is_authenticated=is_authenticated)
    if request.method == 'POST':
        # return is_authenticated as true if username contains word admin AND password is 1234
        # admin1 / 1234 -> We good
        # 1fddjndskgn_admin / 1234 -> also good
        # user / 1234 -> not good
        # admin / dfnjknsdlbn -> not good
        username = request.form['username']
        password = request.form['password']

        # if adminUsername(username) and authPassword(password):
        #     is_authenticated = True

        is_authenticated = auth(username, password)

        print(f'DID A POST. YOUR USERNAME IS {username} AND PASSWORD IS {password}')
        if is_authenticated:
            flash("hiiiiiii", 'success')
            response = make_response(redirect(url_for('user')))
            response.set_cookie('username', username)
            return response
        else:
            flash("INCORRECT LOGIN", 'error')
        return render_template('login.html', username=username, is_authenticated=is_authenticated)

# def adminUsername(username):
#     if 'admin' in username:
#         return True
#     return False

# def authPassword(password):
#     if password == '1234':
#         return True
#     return False

def auth(username, password):
    is_authenticated = False
    if password == '1234' and 'admin' in username:
        is_authenticated = True
    return is_authenticated

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug = False)
