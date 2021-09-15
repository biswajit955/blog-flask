from my_app import app
from my_app import db
from flask import request,render_template,redirect
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import math



local_server=True

with open('my_app/nilu.json', 'r') as c:
    parameter= json.load(c)["parameter"]

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['prod_uri']



# app.config.update(dict(
    # MAIL_SERVER = 'smtp.gmail.com',
    # MAIL_PORT = '465',
    # MAIL_USE_SSL = True,
    # MAIL_USERNAME = "[parameter['my_mail']",
    # MAIL_PASSWORD = "[parameter['my_emil_password']]"
# ))

# mail = Mail(app)


class Posts(db.Model):
    slno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    subtitle = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(100000),  nullable=False)
    slug = db.Column(db.String(100000),  nullable=False)
    img_file = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(120), nullable=False)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_no = db.Column(db.String(120),  nullable=False)
    mgs = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(120), nullable=False)




@app.route("/login", methods=['GET','POST'])
def login():
    if (request.method=='POST'):
        pass
    else:
        return render_template('login.html', parameter=parameter          )


@app.route("/")
def home():
    post = Posts.query.filter_by().all()[0:parameter['no_of_post']]
    return render_template('index.html', parameter=parameter, posts=post)


@app.route("/",methods=['GET','POST'])
def Pagination():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(parameter['no_of_post']))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(parameter['no_of_post']):(page-1)*int(parameter['no_of_post'])+ int(parameter['no_of_posts'])]
    if page==1:
        prev = "#"
        next = "/?page="+ str(page+1)
    elif page==last:
        prev = "/?page="+ str(page-1)
        next = "#"
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+ str(page+1)
    return render_template('index.html', parameter=parameter, posts=posts, prev=prev, next=next)



@app.route("/view_post/<string:post_slug>",methods=['GET','POST'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template("view_post.html",parameter=parameter,post=post)


@app.route("/older_post")
def older_post():
    post = Posts.query.filter_by().all()[parameter['no_of_post']:parameter['no_of_post']+parameter['no_of_post']]
    return render_template('index.html', parameter=parameter)


@app.route("/dasbord")
def dasbord():
    post = Posts.query.all()
    return render_template("dasbord.html", parameter=parameter, post=post)


@app.route("/post/<string:slno>",methods=['GET','POST'])
def post_edit(slno):
    if (request.method=='POST'):
        box_title = request.form.get('title')
        tline = request.form.get('subtitle')
        slug = request.form.get('slug')
        content = request.form.get('content')
        img_file = request.form.get('img_file')
        date = datetime.now()
        if slno=='0':
            post = Posts(title=box_title, slug=slug, content=content, subtitle=tline, img_file=img_file, date=date)
            db.session.add(post)
            db.session.commit()
            return redirect("/dasbord")
        else:
            post = Posts.query.filter_by(slno=slno).first()
            posts = Posts.query.all()
            post.title = box_title
            post.subtitle = tline
            post.slug = slug
            post.content = content
            post.img_file = img_file
            post.date = date
            db.session.commit()
            return render_template("dasbord.html", parameter=parameter, post=posts)
    post = Posts.query.filter_by(slno=slno).first()
    return render_template('edit_post.html', parameter=parameter, post=post,slno=slno)


@app.route("/delete/<string:slno>", methods=['GET','POST'])
def delete(slno):
    post = Posts.query.filter_by(slno=slno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect("/dasbord")


@app.route("/about", methods=['GET','POST'])
def about():
    return render_template("about.html",parameter=parameter)


@app.route("/contact", methods=['GET','POST'])
def contact():
    if (request.method=='POST'):
        '''add entry to the databash'''
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')

        entry = Contacts(name=name, phone_no = phone, mgs= message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        # msg = Message('Test', sender='email', recipients=[parameter['my_mail']])
        # msg.body = 'This is a test email' #Customize based on user input
        # mail.send(msg)

    return render_template("contact.html",parameter=parameter)
