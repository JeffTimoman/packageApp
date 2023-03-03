from flask import Flask, render_template, request
from webdata.models import *
from flask_sqlalchemy import SQLAlchemy
from webdata.config import Config
from flask_bcrypt import Bcrypt
thisConfig = Config()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = thisConfig.DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICITION"] = False
db.init_app(app)
bcrypt = Bcrypt(app)
def main():
	print(thisConfig.DB_URL)
	db.create_all()
# def main():
# 	passwords = bcrypt.generate_password_hash('admin123').decode('utf-8')
# 	user = User(first_name="admin", last_name="admin", email="admin@admin.com", password=passwords, user_type=0)
# 	db.session.add(user)
# 	db.session.commit()
# 	print("User has been created!")
# def main():
# 	for i in range(100):
# 		package = Package(awb=f"SPXID000000{i}", owner="admin", expedition="JNE")
# 		db.session.add(package)
# 		db.session.commit()
# 		print(f"Package {i} has been created!")

		
# def main():
# 	for i in range(100):
# 		user = User(first_name=f"User{i}", last_name=f"user{i}", email=f"user{i}@gmail.com", password=bcrypt.generate_password_hash(f"user{i}").decode('utf-8'), user_type=1)
# 		db.session.add(user)
# 		db.session.commit()
# 		print(f"User {i} has been created!")

# def main():
# 	apis = open("api.txt", "r")
# 	apis = apis.read()
# 	apis = apis.splitlines()
# 	for api in apis:
# 		a, b, c = api.split(";")
# 		ins = Api(expedition=b, api=a)
# 		db.session.add(ins)
# 		db.session.commit()

# def main():
# 	pass
if __name__ == '__main__':
	# main()
	with app.app_context():
		main()