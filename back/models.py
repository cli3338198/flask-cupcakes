"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cupcake(db.Model):
  """Cupcake."""

  __tablename__ = "cupcakes"

  id = db.Column(
    db.Integer,
    primary_key=True,
    autoincrement=True
  )

  size = db.Column(
    db.String(50),
    nullable=False,
  )

  flavor = db.Column(
    db.String(50),
    nullable=False,
    # unique=True
    #TODO: size/flavor constraint?
  )

  rating = db.Column(
    db.Integer,
    nullable=False
  )

  image = db.Column(
    db.String(1000),
    nullable=False,
    default='https://tinyurl.com/demo-cupcake'
  )

  def __repr__(self):
    """Cupcake"""

    return f"""<Cupcake {self.id} {self.size} {self.flavor} {self.rating}>"""

  def serialize(self):

    return {
      'id': self.id,
      'flavor': self.flavor,
      'rating': self.rating,
      'size': self.size,
      'image': self.image
    }


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)