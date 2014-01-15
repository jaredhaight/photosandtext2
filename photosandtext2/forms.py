from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import ValidationError


class LoginForm(Form):
    username = TextField('username')
    password = PasswordField('password')
    submit = SubmitField('Login')

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError('Invalid user')

        if user.password != self.password.data:
            raise ValidationError('Invalid password')
