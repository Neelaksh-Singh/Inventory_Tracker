from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField
from wtforms.fields.list import FieldList
from wtforms.validators import DataRequired,NumberRange

FieldList()



class addproduct(FlaskForm):
    prodname = StringField('Product Name', validators=[DataRequired()])
    prodqty = IntegerField('Quantity', validators=[NumberRange(min=5, max=1000000),DataRequired()])
    prodprice = IntegerField('Price', validators=[NumberRange(min=5, max=1000000),DataRequired()])
    prodsubmit = SubmitField('Save Changes')

class editproduct(FlaskForm):
    editname = StringField('Product Name', validators=[DataRequired()])
    editqty = IntegerField('Quantity', validators=[NumberRange(min=5, max=1000000),DataRequired()])
    editprice = IntegerField('Price', validators=[NumberRange(min=5, max=1000000),DataRequired()])
    editsubmit = SubmitField('Save Changes')
    