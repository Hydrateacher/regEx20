from flask import Flask, render_template, redirect, url_for, session, request
from pymongo import MongoClient
import requests
from uuid import uuid4 
# MongoDB-ga bog'lanish
client = MongoClient('mongodb+srv://doadmin:56Hx14L97FMUYv23@db-mongodb-fra1-82504-ec7e84b0.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-fra1-82504')
db = client['NEW']
collection = db['db']
users = collection.find()

app = Flask(__name__)

@app.route('/admin')
def admin():    
    return render_template('admin.html')

@app.route('/profile')
def profile():    
    return render_template('profile.html')


@app.route('/')
def index():    
    return render_template('index.html')

# Autentifikatsiya
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']         
        
        if username == "admin" and password == "Bahodir96HydraAI":
            session['username'] = username
            
            return redirect(url_for('admin'))

        
        user = collection.find_one({'username': username})
        
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('profile'))
        
        return render_template('login.html', error_message='Foydalanuvchi nomi yoki parol noto`g`ri kiritildi!!!')
    
    return render_template('login.html')



#registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = collection.find_one({'username': username})
        if user:
            return render_template('register.html', error_message='Bu foydalanuvchi nomi allaqachon mavjud')
        
        collection.insert_one({'username': username, 'password': password})
        # Foydalanuvchilarni MongoDB-dan olish
        users = collection.find()
        return redirect(url_for('profile', users=users))
    
    return render_template('register.html')  
  

if __name__ == '__main__':
    app.run(debug=True)

