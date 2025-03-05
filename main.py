from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mokiniai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Mokinys(db.Model):
    __tablename__ = 'mokinys'
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column(db.String)
    pavarde = db.Column(db.String)
    klase = db.Column(db.Integer)
    sukurimo_data = db.Column(db.DateTime, default=datetime.datetime.now)

    @property
    def sekanti_klase(self):
        return self.klase + 1

    def __init__(self,vardas,pavarde,klase):
        self.vardas = vardas
        self.pavarde=pavarde
        self.klase=klase
    def __repr__(self):
        return f'{self.id} {self.vardas} {self.pavarde} {self.klase} {self.sukurimo_data}'


with app.app_context():
    db.create_all()

    # prideti = Mokinys('Marius','Mar', 12)
    # db.session.add(prideti)
    # db.session.commit()

# @app.route('/')
# def home():
#     all_rows = Mokinys.query.all()
#     return render_template('index.html', mokinys_rows=all_rows)
@app.route('/')
def home():
    search_text = request.args.get('searchlaukelis')
    if search_text:
        filtered_rows = Mokinys.query.filter(Mokinys.vardas.ilike(f'%{search_text}%'))
        return render_template('index.html', mokinys_rows=filtered_rows)
    else:
        all_rows = Mokinys.query.all()
        return render_template('index.html', mokinys_rows=all_rows)

@app.route('/prideti-mokini', methods=['GET', 'POST'])
def prideti_mokini():
    if request.method == 'GET':
        return render_template('ivedimo_forma.html')
    elif request.method == 'POST':
        vardas = request.form.get('laukelisvardas')
        pavarde = request.form.get('laukelispavarde')
        try:
            klase = float(request.form.get('laukelisklase'))
        except:
            raise ('Klase should be float')
        if vardas and pavarde and klase:
            new_mokinys_row = Mokinys(vardas, pavarde, klase)
            db.session.add(new_mokinys_row)
            db.session.commit()
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
