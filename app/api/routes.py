from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema
        #car, ccar_schema, cars_schema
api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
        return {'yee':'haw'}


#CREATE
@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
        make = request.json['make']
        model = request.json['model']
        year = request.json['year']
        color = request.json['color']
        user_token = current_user_token.token
        
        print(f'{current_user_token.first_name} {current_user_token.token} just got a car')
        
        car = Car(make,model,year,color, user_token = user_token)
        
        db.session.add(car)
        db.session.commit()
        
        response = car_schema.dump(car)
        return jsonify(response)


# @api.route('/mycars')
# # @login_required
# # @token_required
# def my_cars(current_user_token):
#         user_cars = Car.query.filter_by(user_id=current_user_token.id).all()
#         return render_template('mycars.html', user_cars=user_cars)




# LIST OF ALL CARS
# Bearer f944d07058f1bfcc40564c223f28776d3fbe429b61a99a68
@api.route('/cars', methods = ['GET'])
# @token_required
def get_car():
        cars = db.session.query(Car, User.first_name).join(User, Car.user_token == User.token).all()
    
        cars_list = []
        for c, owner_name in cars:
                cars_list.append({
                        "id": c.id,
                        "make": c.make,
                        "model": c.model,
                        "year": c.year,
                        "color": c.color,
                        "owner": owner_name,
                })
        return jsonify(cars_list)


#SINGLE QUERY
@api.route('/cars/<car_id>', methods=['GET'])
def get_single_car(car_id):
    car = Car.query.get(car_id)
        # car_owner = (
        #     db.session.query(Car, User.first_name)
        #     .join(User, Car.user_token == User.token)
        #     .filter(Car.id == car_id).first()
        # )
    if car:
        car_data = {
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "color": car.color,
            "user_token": car.user_token  
        }
        return jsonify(car_data)
    else:
        return jsonify({"message": "Car not found"}), 404
# this works


# SELECT car.make, car.model, "user".first_name 
# FROM car
# FULL JOIN "user" ON car.user_token = "user".token;



#UPDATE
#use CAR ID
#BEARER user_token
@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_cars(current_user_token,id):
        if current_user_token is None:
                return jsonify({"message": "Authentication error: Invalid token"}), 401
        car = Car.query.get(id) 
    
        if car is None:
                return jsonify({"message": "Car not found"}), 404

        car.make = request.json['make']
        car.model = request.json['model']
        car.year = request.json['year']
        car.color = request.json['color']
        car.user_token = current_user_token.token

        db.session.commit()
        response = car_schema.dump(car)
        return jsonify(response)
# code works



#DELETE
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response, {"message": "Car deleted successfully"})
