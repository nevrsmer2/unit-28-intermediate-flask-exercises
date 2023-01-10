from app import app
from models import Pet, db

'''db.drop_all() drops all tables in the DB.  db.create_all() creates the tables in models.py.  Once seed.py is run and the tables are created and seeded, these 2 lines should be commented to prevent them from rerunning.'''

db.drop_all()
db.create_all()

'''---------Pet Seed Instances--------'''

p1 = Pet(name='Nilo', species='cat', age='12', photo_url='https://cdn.mos.cms.futurecdn.net/VSy6kJDNq2pSXsCzb6cvYF-1920-80.jpg.webp',
         notes='Friendly.  Good with kids.', available=True)

p2 = Pet(name='Pancho', species='cat', age='11', photo_url='https://www.vets4pets.com/siteassets/species/cat/close-up-of-cat-outside.jpg',
         notes='Loving.  Protective. Good with adults', available=False)

p3 = Pet(name='Samantha', species='Ferret', age='2', photo_url='https://thumbs.dreamstime.com/z/feret-street-photo-22835653.jpg',
         notes='Does not bite.  Cage trained.', available=False)

p4 = Pet(name='Bart', species='Fish', age='5', photo_url='https://cff2.earth.com/uploads/2022/10/13062530/Goldfish-2048x1365.jpg',
         notes='It\'s a godlfish, not a piranha.', available=True)

db.session.add_all([p1, p2, p3, p4])
db.session.commit()
