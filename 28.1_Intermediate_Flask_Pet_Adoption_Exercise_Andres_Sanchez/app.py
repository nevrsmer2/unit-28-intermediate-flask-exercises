from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

from forms import AddPetForm, EditPetForm
from models import Pet, connect_db, db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'kitties r the best!'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

'''Use db.create_all() only when not using a seed file to create the tables in models.py.  Otherwise, the code to create the tables is run in the seed file.'''
# db.create_all()

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


'''------------------------ROUTES'------------------------'''


@app.route('/')
def show_pets_list():
    '''Show all pets at adoption center.'''

    pets = Pet.query.all()
    return render_template('pets/index.html', pets=pets)


@app.route('/pets/add', methods=['GET', 'POST'])
def show_add_pet_form():
    '''1. Show form to add new pat, 2. Commit new-pet details to DB.'''

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        age = form.age.data
        photo_url = form.photo_url.data
        notes = form.notes.data

        new_pet = Pet(name=name, species=species, age=age,
                      photo_url=photo_url, notes=notes)
        db.session.add(new_pet)
        db.session.commit()

        return redirect('/')

    else:
        return render_template('pets/add.html', form=form)

    '''-------------------Code to edit a pet-------------------'''


@app.route('/pets/<int:pid>', methods=['GET', 'POST'])
def show_edit_pet_details(pid):
    '''1. Show details on a pet.  2. Show form to edit the same pet.'''

    pet = Pet.query.get_or_404(pid)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        photo_url = form.photo_url.data
        notes = form.notes.data
        available = form.available.data

        db.session.commit()
        return redirect('/')

    else:
        return render_template('pets/details-edit.html', pet=pet, form=form)
