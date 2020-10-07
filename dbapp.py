from flask import Flask, render_template, url_for, flash, redirect
from forms import BookForm, BookForm2, BookForm3, BookForm4, BookFormDelete, BorrowerForm, BorrowerFormDelete, BorrowForm, BorrowerForm2, ReturnForm
import sqlite3
from sqlite3 import Error


app = Flask(__name__)             # create an app instance
app.config["SECRET_KEY"] = "secretkey"


#layout.html keeps features same in each page

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(connection, query):  
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):   
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()   #to fetch result (examine the output) result is an array with tuples
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


#stored procedures

def search_books_isbn(con,isbn):
  query=f"SELECT * FROM books WHERE isbn={isbn};"
  return execute_read_query(con,query)

def search_borrowers_num(con,tc):
  query=f"SELECT number_of_books FROM borrowers WHERE tc={tc};"
  return execute_read_query(con,query)[0][0]


@app.route("/",methods=['GET','POST'])                
def home():                     
    form=BorrowForm()
    form2=BookForm2()
    form3=BookForm3()
    form4=BookForm4()
    form5=ReturnForm()
    conn = get_db_connection()
    if(form.validate_on_submit and form.tc.data and form.isbn.data):     #BORROW BOOK 
        if(search_books_isbn(conn,form.isbn.data)[0][3]!=None):
            flash(u'Book is already taken.','danger')   #how to flash red??? see
            return redirect(url_for('home'))  
       
        
        if(search_borrowers_num(conn,form.tc.data)<8): #update book data
            query=f"UPDATE borrowers SET number_of_books=number_of_books+1 WHERE tc={form.tc.data} AND number_of_books<8"   #number of books updated
            execute_query(conn,query)
            date=execute_read_query(conn,"SELECT date(datetime('now'), '+14 day')")[0][0]
            query=f"UPDATE books SET due='{date}' WHERE isbn={form.isbn.data};"  
            execute_query(conn,query)
            query=f"UPDATE books SET taker_tc={form.tc.data} WHERE isbn={form.isbn.data};"
            execute_query(conn,query)
            flash(f'Book (isbn: {form.isbn.data}) borrowed by: {form.tc.data}','success')
            conn.close()
            return redirect(url_for('home'))   

        else:
            flash(u'No book limit for borrower.','danger')   
            conn.close()
            return redirect(url_for('home'))  
    
    elif(form5.validate_on_submit and form5.tcd.data and form5.isbnd.data):    #RETURN BOOK
        query=f"SELECT * FROM books WHERE taker_tc={form5.tcd.data} AND isbn={form5.isbnd.data};"
        if(len(execute_read_query(conn,query))>0):   #exists such book
            query=f"UPDATE borrowers SET number_of_books=number_of_books-1 WHERE tc={form5.tcd.data}"   #number of books updated
            execute_query(conn,query)
            query=f"UPDATE books SET due=NULL, taker_tc=NULL WHERE isbn={form5.isbnd.data};"  
            execute_query(conn,query)
            flash(f'Book (isbn: {form5.isbnd.data}) returned by: {form5.tcd.data}','success')
           
        else:
            flash(f'Book (isbn: {form5.isbnd.data}) is not borrowed by {form5.tcd.data}','danger')
        
        conn.close()
        return redirect(url_for('home'))  
    
    #SEARCH QUERIES
    elif(form2.validate_on_submit and form2.isbn.data):
        query=f"SELECT * FROM books WHERE isbn={form2.isbn.data};"
        books=conn.execute(query).fetchall()
        conn.close()
        return render_template('home.html', books=books, form=form, form2=form2, form3=form3, form4=form4, form5=form5)

    elif(form3.validate_on_submit and form3.title.data):
        query=f"SELECT * FROM books WHERE title LIKE '%{form3.title.data}%';"
        books=conn.execute(query).fetchall()
        conn.close()
        return render_template('home.html', books=books, form=form, form2=form2, form3=form3, form4=form4, form5=form5)
    
    elif(form4.validate_on_submit and form4.author.data):
        query=f"SELECT * FROM books WHERE author LIKE '%{form4.author.data}%';"
        books=conn.execute(query).fetchall()
        conn.close()
        return render_template('home.html', books=books, form=form, form2=form2, form3=form3, form4=form4, form5=form5)
    
    
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('home.html',books=books,form=form, form2=form2, form3=form3, form4=form4, form5=form5)  

@app.route("/insertbook",methods=['GET','POST']) #another page                
def insert_book():                     
    form=BookForm()
    form2=BookFormDelete()
    if(form.validate_on_submit and form.title.data and form.author.data):  
        conn = get_db_connection()
        query=f"INSERT INTO books (title, author) VALUES ('{form.title.data}','{form.author.data}');"
        execute_query(conn,query)
        conn.close()
        flash(f'Book added: {form.title.data}','success')
        return redirect(url_for('home'))  

    elif(form2.validate_on_submit and form2.isbn.data):  
        conn = get_db_connection()
        tc=search_books_isbn(conn,form2.isbn.data)[0][3]
        query=f"DELETE FROM books WHERE isbn={form2.isbn.data};"
        execute_query(conn,query)
        if(tc!=None):   #bu kısmı triggerla yap!!!
            query=f"UPDATE borrowers SET number_of_books=number_of_books-1 WHERE tc={tc};"
            #execute_query(conn,query)
        conn.close()
        flash(f'Book deleted: {form2.isbn.data}','success')
        return redirect(url_for('home'))  


    return render_template('insertbook.html',title='Add book', form=form, form2=form2)

@app.route("/insertborrower",methods=['GET','POST']) #another page                
def insert_borrower():                     
    form=BorrowerForm()
    form2=BorrowerFormDelete()

    if(form.validate_on_submit and form.tc.data):  
        conn = get_db_connection()
        query=f"INSERT INTO borrowers (tc) VALUES ({form.tc.data});"
        execute_query(conn,query)
        conn.close()
        flash(f'Borrower added: {form.tc.data}','success') 
        return redirect(url_for('home'))  
    
    elif(form2.validate_on_submit and form2.del_tc.data):  
        conn = get_db_connection()
        query=f"DELETE FROM borrowers WHERE tc={form2.del_tc.data};"
        execute_query(conn,query)
        conn.close()
        flash(f'Borrower deleted: {form2.del_tc.data}','success')  
        return redirect(url_for('home'))  

    return render_template('insertborrower.html',title='Add borrower', form=form, form2=form2)


@app.route("/mybooks",methods=['GET','POST'])
def my_books():
    form=BorrowerForm2()
    books=None
    number=None
    if(form.validate_on_submit and form.tc.data):
        conn= get_db_connection()
        query=f"SELECT * FROM books WHERE taker_tc={form.tc.data}; "
        books=execute_read_query(conn,query)
        query=f"SELECT number_of_books FROM borrowers WHERE tc={form.tc.data};"
        number=execute_read_query(conn,query)[0][0]
        conn.close()
    return render_template('mybooks.html',title='My books',books=books,form=form, number=number)
        
  
  


if __name__ == '__main__':    
    app.run(debug=True)                     # run the flask app with debug mode  do not need to start server after each update






