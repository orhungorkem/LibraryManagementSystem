import sqlite3
from sqlite3 import Error


def create_connection():   
    connection = None
    try:
        connection = sqlite3.connect("database.db")  #if there is no such path, database is created
        print("Connection to Library Database successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):   #use it with create queries
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):  
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()   
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_borrow(connection,tc,isbn):
    
    date=execute_read_query(connection,"SELECT date(datetime('now'), '+14 day')")[0][0]
    query1=f"UPDATE borrowers SET number_of_books=number_of_books+1 WHERE tc={tc} AND number_of_books<8"
    query2=f"UPDATE books SET due='{date}' WHERE isbn={isbn};"
    query3=f"UPDATE books SET taker_tc={tc} WHERE isbn={isbn};"
    cur=connection.cursor()
    cur.execute(query1)
    cur.execute(query2)
    cur.execute(query3)
    connection.commit()




con=create_connection()
cur=con.cursor()

with open('schema.sql') as f:
    con.executescript(f.read())

execute_query(con,"INSERT INTO books (title, author) VALUES ('Kuyucaklı Yusuf', 'Sabahattin Ali')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Açlık Oyunları', 'Suzanne Collins')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Kürk Mantolu Madonna', 'Sabahattin Ali')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Sefiller', 'Victor Hugo')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Yabancı', 'Albert Camus')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Memleket Hikayeleri', 'Refik Halit Karay')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Sis ve Gece', 'Ahmet Ümit')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Olasılıksız', 'Adam Fawer')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Gülün Adı', 'Umberto Eco')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Fareler ve İnsanlar', 'John Steinbeck')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Yılanların Öcü', 'Fakir Baykurt')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Hayvan Çiftliği', 'George Orwell')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Denemeler', 'Montaigne')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('Kayıp Sembol', 'Dan Brown')")
execute_query(con,"INSERT INTO books (title, author) VALUES ('İnsanlar Arasında', 'Maxim Gorki')")
execute_query(con,"INSERT INTO borrowers (tc) VALUES (1)")
execute_query(con,"INSERT INTO borrowers (tc) VALUES (2)")
execute_query(con,"INSERT INTO borrowers (tc) VALUES (3)")
execute_query(con,"INSERT INTO borrowers (tc) VALUES (4)")
execute_borrow(con,1,2)
execute_borrow(con,1,3)
execute_borrow(con,1,5)
execute_borrow(con,1,9)
execute_borrow(con,2,1)
execute_borrow(con,2,10)
execute_borrow(con,2,11)
execute_borrow(con,1,12)
execute_borrow(con,1,13)
execute_borrow(con,1,4)


con.close()