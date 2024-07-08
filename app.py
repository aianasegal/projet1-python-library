from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


# Configuration de l'application Flask
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Change this to a secure random key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Fichier de base de données SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactiver le suivi des modifications Flask-SQLAlchemy

db = SQLAlchemy(app)

# Définition du modèle Book
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    writer = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    owner = db.Column(db.String(100), nullable=False)  # Colonne owner

    def __repr__(self):
        return f'<Book(title={self.title}, writer={self.writer}, year={self.year}, owner={self.owner})>'



#user

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user',nullable=False)

    def __repr__(self):
        return f'<User {self.username})>'

    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


# Route pour enregistrer un utilisateur régulier
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role','user')
    
    
    if not username or not password :
        return jsonify({'error': 'Username and password are required'}), 400
    # Find user by username
    if User.query.filter_by(username=username).first():
         return jsonify({'message': 'Username already exists. Please choose a different one.'}), 400

    new_user = User(username=username, role=role)  #
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify ({'message': 'Username registered succesfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    
    
    
    

# Route pour la connexion d'un utilisateur
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
   
   
    if not username or not password :
        return jsonify({'error': 'Username and password are required'}), 400
    # Find user by username
    user = User.query.filter_by(username=username).first()

    # Check if user exists and if the password is correct
    if not user or not user.check_password(password):
         return jsonify({'error': 'invalide username or password'}), 401
     
     
    access_token = create_access_token(identity= {'username': username, 'role': user.role}) #
    return jsonify({'access_token': access_token}), 200

    




@app.route('/admin', methods=['GET'])
@jwt_required()
def admin():
    current_user = get_jwt_identity()
    username = current_user.get('username')
    role = current_user.get('role')

   
    if role != 'admin' :
        return jsonify({'error': 'unauthorized access'}), 403


    return jsonify({'message': 'Admin registered successfully!'}), 200






@app.route('/test', methods=['GET'])
def test():
    return "{'test':'success'}"





# Création de toutes les tables de base de données si elles n'existent pas
with app.app_context():
    db.create_all()

# Routes de l'API CRUD pour les livres

# Ajouter un livre
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], writer=data['writer'], year=data['year'], owner=data['owner'])

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        'message': 'Livre ajouté avec succès!',
        'book': {
            'id': new_book.id,
            'title': new_book.title,
            'writer': new_book.writer,
            'year': new_book.year,
            'owner': new_book.owner
        }
    }), 201

# Lire tous les livres
@app.route('/books', methods=['GET'])

def get_books():
    books = Book.query.all()
    books_data = []
    for book in books:
        books_data.append({
            'id': book.id,
            'title': book.title,
            'writer': book.writer,
            'year': book.year,
            'owner': book.owner
        })
    return jsonify({'books': books_data})

# Lire un livre spécifique par son ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'writer': book.writer,
        'year': book.year,
        'owner': book.owner
    })

# Mettre à jour un livre par son ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    book.title = data.get('title', book.title)
    book.writer = data.get('writer', book.writer)
    book.year = data.get('year', book.year)
    book.owner = data.get('owner', book.owner)

    db.session.commit()

    return jsonify({
        'message': 'Livre mis à jour avec succès!',
        'book': {
            'id': book.id,
            'title': book.title,
            'writer': book.writer,
            'year': book.year,
            'owner': book.owner
        }
    })

# Supprimer un livre par son ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Livre supprimé avec succès!'})


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Point d'entrée principal
if __name__ == '__main__':
    app.run(debug=True)