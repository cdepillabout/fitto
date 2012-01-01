from urlparse import urlparse, urljoin
from flask import request, url_for, redirect
from flaskext.wtf import Form, TextField, HiddenField, \
        PasswordField, SubmitField, validators

from .models import User

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect_next(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))

class LoginForm(RedirectForm):
    username = TextField('Username',
            [validators.Length(min=4, max=25), validators.Required()])
    password = PasswordField('Password',
            [validators.Length(min=6, max=100), validators.Required()])
    submit = SubmitField('Login')

    def validate(self):
        # regular validation
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if self.user is None:
            self.username.errors.append('unknown username or invalid password')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('unknown username or invalid password')
            return False

        self.user = user
        return True

class ChangePasswordForm(LoginForm):
    password = PasswordField('Old Password',
            [validators.Length(min=6, max=100), validators.Required()])
    new_password = PasswordField('New Password',
            [validators.Length(min=6, max=100), validators.Required()])
    confirm_password = PasswordField('New Password',
            [validators.Length(min=6, max=100), validators.Required()])


