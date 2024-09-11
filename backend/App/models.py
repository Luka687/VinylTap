from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_sqlalchemy import SQLAlchemy
import bcrypt

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

#### MODEL FOR RECORD #####
class Record(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
    artist: Mapped[str] = mapped_column(nullable=False)
    year_of_release: Mapped[int] = mapped_column(nullable=False)
    img_link: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[float] = mapped_column(nullable=False)
    num_of_rating: Mapped[int] = mapped_column(nullable=False)

    catalogue_items = db.relationship('CatalogueItem', back_populates='record')

#### MODEL FOR USER #####
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    

    catalogues = db.relationship('Catalogue', back_populates='user')
    catalogue_items = db.relationship('CatalogueItem', back_populates='user')

#### MODEL FOR RATINGS ####
class Rating(db.Model):
    __tablename__ = 'ratings'

    record_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[float] = mapped_column(nullable=False)


#### MODEL FOR CATALOGUE #####
class Catalogue(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
  
    catalogue_items = db.relationship('CatalogueItem', back_populates='catalogue')
    user = db.relationship('User', back_populates='catalogues')

#### MODEL FOR CATALOGUE ITEM #####
class CatalogueItem(db.Model):
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), primary_key=True)
    record_id: Mapped[int] = mapped_column(db.ForeignKey('record.id'), primary_key=True)
    catalogue_id: Mapped[int] = mapped_column(db.ForeignKey('catalogue.id'), primary_key=True)
    user_rating: Mapped[int] = mapped_column(nullable = True)

    catalogue = db.relationship('Catalogue', back_populates='catalogue_items')
    record = db.relationship('Record', back_populates='catalogue_items')
    user = db.relationship('User', back_populates='catalogue_items')