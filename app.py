from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Databasmodell för Book
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='unread')  # 'unread', 'reading', 'read'
    date_read = db.Column(db.String(10), nullable=True)  # YYYY-MM-DD format
    progress = db.Column(db.Integer, default=0)  # 0-100 för pågående böcker

    def __repr__(self):
        return f'<Book {self.title}>'

# CREATE - Lägg till ny bok
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        status = request.form.get('status', 'unread')
        date_read = request.form.get('date_read', None)
        progress = request.form.get('progress', 0)

        new_book = Book(
            title=title,
            author=author,
            year=int(year),
            status=status,
            date_read=date_read if date_read else None,
            progress=int(progress) if progress else 0
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_book.html')

# READ - Visa alla böcker
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

# UPDATE - Redigera bok
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.year = int(request.form['year'])
        book.status = request.form.get('status', 'unread')
        book.date_read = request.form.get('date_read', None)
        book.progress = int(request.form.get('progress', 0))

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_book.html', book=book)

# DELETE - Ta bort bok
@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('index'))

# Initialisera databasen och lägg till exempelböcker
def init_db():
    with app.app_context():
        db.create_all()

        # Lägg till exempelböcker om databasen är tom
        if Book.query.count() == 0:
            sample_books = [
                Book(title="1984", author="George Orwell", year=1949),
                Book(title="Att döda en härmtrast", author="Harper Lee", year=1960),
                Book(title="Stolthet och fördom", author="Jane Austen", year=1813),
                Book(title="Bröderna Karamazov", author="Fjodor Dostojevskij", year=1880),
                Book(title="Hundra år av ensamhet", author="Gabriel García Márquez", year=1967)
            ]
            db.session.add_all(sample_books)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
