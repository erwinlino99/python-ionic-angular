from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WebUser(db.Model):
    __tablename__ = 'web_user'
    
    # Definir las columnas según la tabla en SQL
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    pass_hash = db.Column(db.String(128), nullable=False)  # Cambio de nombre a 'pass_hash' para mejor legibilidad
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    domicile = db.Column(db.String(999), nullable=True)
    bornDate = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<WebUser {self.username}>'

    # Método para retornar los datos del usuario en formato JSON
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'surname': self.surname,
            'email': self.email,
            'phone': self.phone,
            'domicile': self.domicile,
            'bornDate': self.bornDate,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
