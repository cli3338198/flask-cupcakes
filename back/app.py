from urllib import response
from flask import Flask, url_for, render_template, redirect, flash, jsonify, request

# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

@app.get('/api/cupcakes')
def cupcake_all():
  """Get all cupcakes. Responds with JSON:
  {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

  cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

  return jsonify(cupcakes=cupcakes)

@app.get('/api/cupcakes/<int:cupcake_id>')
def cupcake_get(cupcake_id):
  """Get a cupcake. Responds with JSON:
  {cupcake: {id, flavor, size, rating, image}}"""

  cupcake = Cupcake.query.get_or_404(cupcake_id).serialize()

  return jsonify(cupcake=cupcake)

@app.post('/api/cupcakes')
def cupcake_post():
  """Add a cupcake.
  Inputs: {"flavor": flavor, "size": size, "rating": rating, "image": image}
  Responds with JSON: {cupcake: {id, flavor, size, rating, image}}
  """

  flavor = request.json['flavor']
  size = request.json['size']
  rating = request.json['rating']
  image = request.json.get('image') or None

  cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

  db.session.add(cupcake)
  db.session.commit()

  return (jsonify(cupcake=cupcake.serialize()), 201)


@app.patch('/api/cupcakes/<int:cupcake_id>')
def cupcake_update(cupcake_id):
  """Update cupcake info. Responds with JSON:
  {cupcake: {id, flavor, size, rating, image}}"""

  cupcake = Cupcake.query.get_or_404(cupcake_id)

  cupcake.flavor = request.json.get('flavor') or cupcake.flavor
  cupcake.size = request.json.get('size') or cupcake.size
  cupcake.rating = request.json.get('rating') or cupcake.rating
  cupcake.image = request.json.get('image') or cupcake.image

  db.session.commit()

  return (jsonify(cupcake=cupcake.serialize()))


@app.delete('/api/cupcakes/<int:cupcake_id>')
def cupcake_delete(cupcake_id):
  """Delete cupcake. Responds with JSON: {deleted: [cupcake-id]}."""

  cupcake = Cupcake.query.get_or_404(cupcake_id)

  db.session.delete(cupcake)
  db.session.commit()

  return (jsonify({'deleted': cupcake_id}))


@app.get('/')
def show_homepage():
  """Displays homepage"""

  return render_template('index.html')
