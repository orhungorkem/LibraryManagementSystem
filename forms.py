from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo


class BookForm(FlaskForm):   #to add book
    title=StringField('Title',validators=[DataRequired(), Length(min=2, max=50)])
    author=StringField('Author',validators=[DataRequired(), Length(min=2, max=30)])
    submit= SubmitField('Add book')

class BookFormDelete(FlaskForm):  #to delete book
    isbn=IntegerField('Isbn',validators=[DataRequired()])
    submit= SubmitField('Delete book')


class BorrowerForm(FlaskForm):    #to add borrower
    tc=IntegerField('Tc to add',validators=[DataRequired()])
    submit= SubmitField('Add borrower')

class BorrowerFormDelete(FlaskForm):   #to delete borrower
    del_tc=IntegerField('Tc to delete',validators=[DataRequired()])
    submit= SubmitField('Delete borrower')

class BorrowerForm2(FlaskForm):   #to seek my books
    tc=IntegerField('Tc',validators=[DataRequired()])
    submit= SubmitField('See borrowed books')

class BorrowForm(FlaskForm):   #to borrow book
    tc=IntegerField('Tc',validators=[DataRequired()])
    isbn=IntegerField('Isbn',validators=[DataRequired()])
    submit= SubmitField('Borrow book')

class ReturnForm(FlaskForm):  #to return book
    tcd=IntegerField('Tc',validators=[DataRequired()])
    isbnd=IntegerField('Isbn',validators=[DataRequired()])
    submit= SubmitField('Return book')


#to search boooks according to fields
class BookForm2(FlaskForm):
    isbn=IntegerField('Isbn',validators=[DataRequired()])
    submit= SubmitField('Search book with isbn')

class BookForm3(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    submit= SubmitField('Search book with title')

class BookForm4(FlaskForm):
    author=StringField('Author',validators=[DataRequired()])
    submit= SubmitField('Search book with author')