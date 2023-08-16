from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

all_books = []
#create the DB
# pip install -U Flask-SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
db = SQLAlchemy()
db.init_app(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)

    # def __repr__(self):
    #     return f'Title: {self.title} Author: {self.author} Rating: {self.rating}'

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title)).scalars()
        all_books = result.all()
    return render_template("index.html", books=all_books)


@app.route("/edit/",methods=["GET", "POST"])
def edit():

    book_id = request.args.get('id')
    if request.method == "POST":
        bookid = request.args.get('id')
        result = db.session.execute(db.select(Book).where(Book.id == bookid)).scalar()
        result.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    result = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    return render_template("edit.html", title=result.title, rating=result.rating, bookid=result.id)


@app.route("/delete/")
def delete():
    book_id = request.args.get('id')
    book_to_delete = db.session.execute((db.select(Book).where(Book.id == book_id))).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
            db.session.add(new_book)
            db.session.commit()

        # NOTE: You can use the redirect method from flask to redirect to another route
        # e.g. in this case to the home page after the form has been submitted.
        return redirect(url_for('home'))
    return render_template("add.html")



if __name__ == "__main__":
    app.run(debug=True)

