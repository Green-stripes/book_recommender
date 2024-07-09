from flask import Flask, abort, request
from flask_basicauth import BasicAuth
from collections import defaultdict
from flask_swagger_ui import get_swaggerui_blueprint
import pymysql
import json
import math

app = Flask(__name__)
# app.config.from_file("flask_config.json", load=json.load)
# auth = BasicAuth(app)

swaggerui_blueprint = get_swaggerui_blueprint(
    base_url='/docs',
    api_url='/static/openapi.yaml',
)
app.register_blueprint(swaggerui_blueprint)

@app.route('/books')
def books():
    try:
        page = int(request.args.get('page', 0))
        MAX_PAGE_SIZE = 20
        include_details = int(request.args.get('include_details', 0))
        books_dict = defaultdict(list)
        page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
        page_size = min(page_size, MAX_PAGE_SIZE)

        db_conn = pymysql.connect(host="localhost", user="root", database="final",
                            password="drinkwater123", cursorclass=pymysql.cursors.DictCursor)

        try:
            with db_conn.cursor() as cursor:
                cursor.execute("""SELECT DISTINCT
                                B.book_id as id,
                                B.title,
                                B.author
                                FROM books B
                                ORDER BY B.book_id
                                LIMIT %s
                                OFFSET %s
                                """, (page_size, page * page_size))
                books_dict = cursor.fetchall()
                id_list = [item['id'] for item in books_dict]
                placeholder = ",".join(["%s"] * len(id_list))

            with db_conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS total FROM books")
                total = cursor.fetchone()
                last_page = math.ceil(total['total'] / page_size)

            if include_details and id_list:
                with db_conn.cursor() as cursor:
                    cursor.execute(f"""SELECT DISTINCT
                                    B.book_id,
                                    B.series,
                                    B.rating,
                                    B.description,
                                    B.pages,
                                    L.language,
                                    G.genre
                                    FROM books B
                                    JOIN book_genre BG ON B.book_id = BG.book_id
                                    JOIN genre G ON BG.genre_id = G.genre_id
                                    JOIN languages L ON B.language_id = L.language_id
                                    WHERE B.book_id IN ({placeholder})
                                    ORDER BY B.book_id
                                    """, id_list)
                    details = cursor.fetchall()
                    details_dict = defaultdict(lambda: defaultdict(list))
                    for detail in details:
                        details_dict[detail['book_id']].update(detail)
                        details_dict[detail['book_id']]['genres'].append(detail['genre'])
                        del details_dict[detail['book_id']]['genre']

                    for book in books_dict:
                        book.update(details_dict[book['id']])
                        book['genres'] = details_dict[book['id']]['genres']

        finally:
            db_conn.close()

        return {
            'books': books_dict,
            'next_page': f'/books?page={page+1}&page_size={page_size}',
            'last_page': f'/books?page={last_page}&page_size={page_size}',
        }

    except Exception as e:
        abort(500, description=str(e))


@app.route('/books/<int:book_id>')
def get_book(book_id):
    try:
        db_conn = pymysql.connect(host="localhost", user="root", database="final",
                                  password="drinkwater123", cursorclass=pymysql.cursors.DictCursor)
        try:
            with db_conn.cursor() as cursor:
                cursor.execute("""SELECT DISTINCT
                                B.book_id as id,
                                B.title,
                                B.author,
                                B.series,
                                B.rating,
                                B.description,
                                B.pages,
                                L.language
                                FROM books B
                                JOIN languages L ON B.language_id = L.language_id
                                WHERE B.book_id = %s
                                """, (book_id,))
                book = cursor.fetchone()
                if not book:
                    abort(404, description="Book not found")

                book['genres'] = []
                cursor.execute("""SELECT G.genre
                                FROM genre G
                                JOIN book_genre BG ON G.genre_id = BG.genre_id
                                WHERE BG.book_id = %s
                                """, (book_id,))
                genres = cursor.fetchall()
                book['genres'] = [genre['genre'] for genre in genres]

        finally:
            db_conn.close()

        return book

    except Exception as e:
        abort(500, description=str(e))

if __name__ == "__main__":
    app.run(debug=True)
