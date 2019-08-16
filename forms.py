from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired as Required


class BaseForm(FlaskForm):
    name = StringField(label='Nome', validators=[Required()])


class ContestForm(BaseForm):
    description = TextAreaField(label='Detalhes do sorteio')


class NameForm(BaseForm):
    contest_id = HiddenField(validators=[Required()])
