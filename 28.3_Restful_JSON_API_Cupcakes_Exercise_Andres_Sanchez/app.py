"""Flask app for Cupcakes"""

import requests
from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

from models import Cupcake, connect_db, db

app = Flask(__name__)

app.app_context().push()

app.config['SECRET_KEY'] = 'kitties r the best!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

# debug = DebugToolbarExtension(app)


'''--------------------------ROUTES---------------------------'''


@app.route("/")
def root():
    '''Show home page'''
    return render_template("index.html")


@app.route('/api/cupcakes', methods=["GET"])
def list_all_cupcakes():
    '''Show all cupcakes in DB'''
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:cid>', methods=["GET"])
def show_one_cupcakes(cid):
    '''Show details for specific cupcake'''
    cupcake = Cupcake.query.get_or_404(cid)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def add_cupcake():
    '''Add a cupcake and its details to DB'''
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cc = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cc)
    db.session.commit()

    response_json = jsonify(cupcake=new_cc.serialize())
    return (response_json, 201)


@app.route("/api/cupcakes/<int:cid>", methods=["PATCH"])
def update_cupcake(cid):
    '''Update a cupcake'''

    cupcake = Cupcake.query.get_or_404(cid)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    # db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:cid>', methods=["DELETE"])
def delete_cupcake(cid):
    '''Delete a cupcake'''

    cupcake = Cupcake.query.get_or_404(cid)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
