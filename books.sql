use final;
select * from books;
CREATE TABLE IF NOT EXISTS languages (
    language_id INT AUTO_INCREMENT PRIMARY KEY,
    language VARCHAR(100) NOT NULL
);
select distinct language, count(title) from books
group by language;


UPDATE books
SET language = 'Unknown'
WHERE language IS NULL;

INSERT INTO languages (language)
SELECT DISTINCT language FROM books;

select * from languages;
select distinct language_id from languages;

ALTER TABLE books
ADD COLUMN language_id INT;
UPDATE books b
JOIN languages l ON b.language = l.language
SET b.language_id = l.language_id;

select * from books;

ALTER TABLE books
ADD CONSTRAINT fk_language
FOREIGN KEY (language_id) REFERENCES languages(language_id);

ALTER TABLE books
DROP COLUMN language;

select genres from books;

CREATE TABLE genre (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre VARCHAR(255) NOT NULL
);

INSERT INTO genre (genre)
SELECT DISTINCT genres
FROM book_genre
WHERE genres IS NOT NULL;

select * from book_genre;

ALTER TABLE book_genre
ADD CONSTRAINT fk_genre
FOREIGN KEY (genre_id) REFERENCES genre(genre_id);

ALTER TABLE book_genre
DROP COLUMN genres;

create view v_genre_summary as
select genre.genre, count(book_id) as number_of_books
from book_genre
join genre
using (genre_id)
group by genre.genre
;
 select * from v_genre_summary;
 
 -- filter query
 -- analytical function to rank books by most reviews -- window function
 -- do 5 queries
 -- where, joins, case statements
 
 SELECT
    title,
    numRatings,
    RANK() OVER (ORDER BY numRatings DESC)
FROM
    books;
 
describe books;

SELECT 
    title,
    rating,
    CASE
        WHEN rating >= 4.5 THEN 'Excellent'
        WHEN rating >= 3.5 THEN 'Good'
        WHEN rating >= 2.5 THEN 'Average'
        ELSE 'Poor'
    END AS rating_category
FROM 
    books;
    
SELECT title, author, numRatings, price
FROM books
WHERE numRatings > 1000
  AND price BETWEEN 3 AND 10
  AND title LIKE '%class%'
ORDER BY numRatings DESC;

SELECT 
    b.title,
    g.genre
FROM 
    books b
JOIN 
    book_genre bg ON b.bookId = bg.book_id
JOIN 
    genre g ON bg.genre_id = g.genre_id;
    
ALTER TABLE books
ADD COLUMN book_id INT;

SET @count = 0;
UPDATE books SET book_id = @count:=@count + 1;

ALTER TABLE books
MODIFY COLUMN book_id INT AUTO_INCREMENT PRIMARY KEY;

select * from books;
SELECT COUNT(DISTINCT genre) FROM genre;
select * from genre;
select * from book_genre;
select * from languages;

SELECT *
FROM books
WHERE genres NOT LIKE '%fiction%';

SELECT COUNT(*)
FROM (
    SELECT *
    FROM books
    WHERE genres NOT LIKE '%fiction%'
) AS filtered_books;