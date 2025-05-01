from applications.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150))
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    datasets = db.relationship('Dataset', backref='owner', lazy=True)
    submissions = db.relationship('Submission', backref='user', lazy=True)

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    competitions = db.relationship('Competition', backref='dataset', lazy=True)

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    
    submissions = db.relationship('Submission', backref='competition', lazy=True)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(200))
    score = db.Column(db.Float)
    submitted_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))

def initialize_admin():
    """Initialize the admin user if it doesn't exist."""
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@miniminds.com",
            name="Administrator",
            firebase_uid="admin-uid",  # This would be replaced with actual Firebase UID
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")