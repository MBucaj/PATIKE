from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Majice(db.Model):
    __tablename__ = "majice"

    id_majica = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(150))
    ime = db.Column(db.String(150))
    materijal = db.Column(db.String(150))
    boja = db.Column(db.String(150))

    def __init__(self, marka, ime, materijal, boja):
        self.marka = marka
        self.ime = ime
        self.materijal = materijal
        self.boja = boja

def create_table():
    db.create_all()

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        marka = request.form['marka']
        ime = request.form['ime']
        materijal = request.form['materijal']
        boja = request.form['boja']

        majica = Majice(
            marka=marka,
            ime=ime,
            materijal=materijal,
            boja=boja
        )

        db.session.add(majica)
        db.session.commit()
        return redirect('/')

@app.route('/')
def RetrieveList():
    majice = Majice.query.all()
    return render_template('datalist.html', majice=majice)

@app.route('/<int:id>')
def RetrieveMajica(id):
    majica = Majice.query.get(id)
    if majica:
        return render_template('data.html', majica=majica)
    return f"Majica with id = {id} doesn't exist."

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_majica(id):
    majica = Majice.query.get(id)

    if request.method == 'POST':
        if majica:
            # Prvo brišemo postojeću tenisicu
            db.session.delete(majica)
            db.session.commit()

        marka = request.form['marka']
        ime = request.form['ime']
        materijal = request.form['materijal']
        boja = request.form['boja']

        # Zatim dodajemo ažuriranu tenisicu s istim ID-om
        majica = Majice(
            marka=marka,
            ime=ime,
            materijal=materijal,
            boja=boja
        )

        db.session.add(majica)
        db.session.commit()
        return redirect('/')
    return render_template('update.html', majica=majica)

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_majica(id):
    majica = Majice.query.get(id)
    if request.method == 'POST':
        if majica:
            db.session.delete(majica)
            db.session.commit()
            return redirect('/')
    
    return render_template('delete.html', majica=majica)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=808, debug=True)

# UPDATE I BRISANJE NE ŽELI PREKO TIPKAH, NEGO TREBA U SEARCHBAR NAPISAT /id/delete  ili /id/edit
# Ali isto je OKEJ