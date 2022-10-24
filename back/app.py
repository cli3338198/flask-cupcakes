from flask import Flask, url_for, render_template, redirect, flash, jsonify, request

# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

@app.route('/api/cupcakes', methods=["GET"])
def cupcake_all():
  """Get all cupcakes."""

  cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

  return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["GET"])
def cupcake_get(cupcake_id):
  """Get a cupcake."""

  cupcake = Cupcake.query.get_or_404(cupcake_id).serialize()

  return jsonify(cupcake=cupcake)

@app.route('/api/cupcakes', methods=["POST"])
def cupcake_post():
  """Add a cupcake."""

  flavor = request.json['flavor']
  size = request.json['size']
  rating = request.json['rating']
  image = request.json['image']

  cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

  db.session.add(cupcake)
  db.session.commit()

  return (jsonify(cupcake=cupcake.serialize()), 201)
