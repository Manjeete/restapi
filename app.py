from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)
#init marshmallow
ma = Marshmallow(app)

#model
class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(200), unique=True)
    url = db.Column(db.String(400))
    averageAge = db.Column(db.Integer)
    description = db.Column(db.String(1000))

    def __init__(self,breed,url,averageAge,description):
        self.breed = breed
        self.url = url
        self.averageAge = averageAge
        self.description = description

class DogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'breed', 'url', 'averageAge', 'description')  
#init schema
dog_schema = DogSchema( )
dogs_schema = DogSchema(many=True)   

@app.route('/dog', methods=['POST'])
def add_dog():
    breed = request.json['breed']
    url = request.json['url']
    averageAge = request.json['averageAge']
    description = request.json['description']

    new_dog = Dog(breed, url, averageAge, description)

    db.session.add(new_dog)
    db.session.commit()

    return dog_schema.jsonify(new_dog)

# fetch all data
@app.route('/dog',methods=['GET'])
def get_dogs():
    all_dogs = Dog.query.all()
    result = dogs_schema.dump(all_dogs)
    return jsonify(result)

#fetch single dog
@app.route('/dog/<id>',methods=['GET'])
def get_dog(id):
    dog = Dog.query.get(id)
    return dog_schema.jsonify(dog)

#Update the dog's data    
@app.route('/dog/<id>', methods=['PUT'])
def update_dog(id):
    dog = Dog.query.get(id)

    breed = request.json['breed']
    url = request.json['url']
    averageAge = request.json['averageAge']
    description = request.json['description']

    dog.breed = breed
    dog.url = url
    dog.averageAge = averageAge
    dog.description = description

    db.session.commit()

    return dog_schema.jsonify(dog)

#delete dog
@app.route('/dog/<id>',methods=['DELETE'])
def delete_dog(id):
    dog = Dog.query.get(id)
    db.session.delete(dog)
    db.session.commit()
    return dog_schema.jsonify(dog)

# run server
if __name__ == '__main__':
    app.run(debug=True)
