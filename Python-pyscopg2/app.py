from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instantiation of Flask
app = Flask(__name__)

# To connect database form flask app
# Setting configuration variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mike-savy:dreamlife!@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Linking an instance of databse  sqlAlchemy to flask
# Instance of the database allows us to use SQLAlchemy
db = SQLAlchemy(app)

# Linking Migration
migrate = Migrate(app, db)


# Defining a class Person inheriting from the db.Model
# In other to creat a table in the database

class Person(db.Model):
  # By default SQLAlcemy specifies a table name for you
  # from the class name eg persons or 
  # You can specify it as below
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    # For debugging 
    # Good visualizaion of Object elements
    def __repr__(self):
        return f'<Person ID:{self.id}, Name: {self.name}>'

# To create all class model as a table
# In the database (Not needed when working with Mogration)
# db.create_all()


# Setting Decoration path
@app.route('/')

# Route handler
def index():
    person = Person.query.first()
    return 'Hello Mr ' + person.name


# To enable easy run with python3 <app_name>

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

# 'postgresql://myusername:mypassword@localhost:5432/mydatabase'
