from flask_sqlalchemy import SQLAlchemy
 
db =SQLAlchemy()
 
class Tenisice(db.Model):
    __tablename__ = "tenisice"

    id_tenisica = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(150))
    ime = db.Column(db.String(150))
    materijal = db.Column(db.String(150))
    boja = db.Column(db.String(150))

    def __init__(self, marka, ime, materijal, boja):
        self.marka = marka
        self.ime = ime
        self.materijal = materijal
        self.boja = boja

    def __repr__(self):
        return f"{self.marka} {self.ime}"