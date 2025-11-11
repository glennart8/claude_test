from flask import Flask, render_template

app = Flask(__name__)

# Lista med böcker
books = [
    {"title": "1984", "author": "George Orwell", "year": 1949},
    {"title": "Att döda en härmtrast", "author": "Harper Lee", "year": 1960},
    {"title": "Stolthet och fördom", "author": "Jane Austen", "year": 1813},
    {"title": "Bröderna Karamazov", "author": "Fjodor Dostojevskij", "year": 1880},
    {"title": "Hundra år av ensamhet", "author": "Gabriel García Márquez", "year": 1967}
]

@app.route('/')
def index():
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
