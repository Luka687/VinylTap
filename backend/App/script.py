from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3300/vinyltap"
db.init_app(app)

class Record(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)

    def add(n, g):
        record = Record(name = n, genre = g)
        db.session.add(record)
        db.session.commit()

    def remove():
        pass

    def edit(i,n,g):
        record = Record.query.filter_by(id=i).first()
        record.genre=g
        db.session.commit()

@app.route("/")
def hello_world():
    Record.add('test','test')
    Record.edit(4,'test','edited+again')
    return "<p>Hello, World!</p>"