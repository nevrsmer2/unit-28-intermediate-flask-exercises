from app import app
from models import Feedback, User, db

db.drop_all()
db.create_all()


'''---------User Seed Instances--------'''

u1 = User(username='username1', password='fake-password-1',
          email='user1@users.com', first_name='Adam', last_name='first_user')
u2 = User(username='username2', password='fake-password-2',
          email='user2@users.com', first_name='Eve', last_name='second_user')

'''Seeded passwords will genrate issue iwth salt since they were not passed through Bcrypt.'''

db.session.add_all([u1, u2])
db.session.commit()


'''---------Feedback Seed Instances--------'''

f1 = Feedback(title="Sunflower Kitty",
              content="You are my sunshine, my only sunsgine, you make me happy, when skies are grey", username="username1")
f2 = Feedback(title="Bad Medicine",
              content="Your love is like bad medicine, bad medicine is what I need", username="username2")

db.session.add_all([f1, f2])
db.session.commit()
