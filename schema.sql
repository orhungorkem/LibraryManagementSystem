DROP TABLE IF EXISTS books;

CREATE TABLE books (
  isbn INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  taker_tc INTEGER,
  due TEXT,
  FOREIGN KEY (taker_tc) REFERENCES borrowers(tc)
);

DROP TABLE IF EXISTS borrowers;

CREATE TABLE borrowers(
  tc INTEGER PRIMARY KEY,
  number_of_books INTEGER DEFAULT 0 
);

CREATE TRIGGER update_numberofbooks
   AFTER DELETE ON books
   
BEGIN
	UPDATE borrowers SET number_of_books=number_of_books-1 WHERE tc=old.taker_tc;
END;

CREATE TRIGGER update_bookdata
  AFTER DELETE ON borrowers

  BEGIN
  UPDATE books SET taker_tc=NULL, due=NULL WHERE taker_tc=old.tc;
END;