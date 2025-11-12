from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange


class HouseForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    square = IntegerField('Площадь (м²)', validators=[DataRequired(), NumberRange(min=0)])
    area = StringField('Площадь участка', validators=[DataRequired()])  # теперь текст
    price_base = IntegerField('Теплый контур', validators=[DataRequired(), NumberRange(min=0)])
    price_with_communications = IntegerField('Готовые коммуникации', validators=[Optional(), NumberRange(min=0)])
    price_ready = IntegerField('Заезжай и живи', validators=[Optional(), NumberRange(min=0)])
    mortgage_price_per_month = IntegerField('В ипотеку', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Сохранить')


