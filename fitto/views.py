from . import app, db
from flask import render_template, request
from . import models
from forms import LoginForm



@app.route('/')
def index():
    print(dir(db))
    print(db)
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    #form = LoginForm()
    form = LoginForm(request.form)
    if form.validate_on_submit():
        flash('Logged In')
    else:
        for error in form.errors:
            flash("Error: %s" % error)
    form.redirect_next('index')


@app.context_processor
def inject_login_form():
    return dict(login_form=LoginForm())
