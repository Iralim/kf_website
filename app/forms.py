from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Optional, NumberRange
from flask_wtf.file import FileAllowed


class ProjectForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    square = IntegerField('Площадь (м²)', validators=[DataRequired(), NumberRange(min=0)])
    size = StringField('Площадь участка', validators=[DataRequired()])  # теперь текст
    price_base = IntegerField('Теплый контур', validators=[DataRequired(), NumberRange(min=0)])
    price_with_communications = IntegerField('Готовые коммуникации', validators=[Optional(), NumberRange(min=0)])
    price_ready = IntegerField('Заезжай и живи', validators=[Optional(), NumberRange(min=0)])
    mortgage_price_per_month = IntegerField('В ипотеку', validators=[Optional(), NumberRange(min=0)])
    img_files = MultipleFileField("Изображение", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], "Допустимы только изображения")
    ])
    submit = SubmitField('Сохранить')


