from flask import Flask


app=Flask(__name__)
db = SQLAlchemy(app)



from my_app import route