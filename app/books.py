# from flask import Blueprint, jsonify, request, abort
# from typing import Dict, Any
# import uuid
#
# books_bp = Blueprint('books', __name__)
#
# books: Dict[str, Dict[str, Any]] = {}
#
# @books_bp.route('/', methods=['POST'])
# def create_book():
#     data = request.json
#     if not data or 'title' not in data or 'author' not in data:
#         abort(400, 'Invalid book data.')
#
#     book_id = str(uuid.uuid4())
#     books[book_id] = {
#         'id': book_id,
#         'title': data['title'],
#         'author': data['author'],
#         'year': data.get('year'),
#     }
#     return jsonify(books[book_id]), 201
#
# @books_bp.route('/<book_id>', methods=['GET'])
# def get_book(book_id):
#     if book_id not in books:
#         abort(404, 'Book not found.')
#     return jsonify(books[book_id])
#
# @books_bp.route('/', methods=['GET'])
# def list_books():
#     title = request.args.get('title')
#     author = request.args.get('author')
#     page = int(request.args.get('page', 1))
#     per_page = int(request.args.get('per_page', 5))
#
#     filtered_books = filtered_books = [book for book in books.values() if
#                   (not title or title.lower() in book['title'].lower()) and
#                   (not author or author.lower() in book['author'].lower())]
#
#
#     start = (page - 1) * per_page
#     end = start + per_page
#     return jsonify(filtered_books[start:end])
#
# @books_bp.route('/<book_id>', methods=['PUT'])
# def update_book(book_id):
#     if book_id not in books:
#         abort(404, 'Book not found.')
#
#     data = request.json
#     if not data:
#         abort(400, 'Invalid book data.')
#
#     books[book_id].update({
#         'title': data.get('title', books[book_id]['title']),
#         'author': data.get('author', books[book_id]['author']),
#         'year': data.get('year', books[book_id].get('year')),
#     })
#     return jsonify(books[book_id])
#
# @books_bp.route('/<book_id>', methods=['DELETE'])
# def delete_book(book_id):
#     if book_id not in books:
#         abort(404, 'Book not found.')
#     del books[book_id]
#     return '', 204





from flask import Blueprint, jsonify, request, abort
from .models import Book
from . import db
import uuid

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['POST'])
def create_book():
    data = request.json
    if not data or 'title' not in data or 'author' not in data:
        abort(400, 'Invalid book data.')

    book_id = str(uuid.uuid4())
    new_book = Book(id=book_id, title=data['title'], author=data['author'], year=data.get('year'))
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'id': new_book.id, 'title': new_book.title, 'author': new_book.author, 'year': new_book.year}), 201




@books_bp.route('/<book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404, 'Book not found.')
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year})

@books_bp.route('/', methods=['GET'])
def list_books():
    title = request.args.get('title', '').lower()
    author = request.args.get('author', '').lower()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    query = Book.query
    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))

    paginated_books = query.paginate(page=page, per_page=per_page, error_out=False).items

    result = [{'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year} for book in paginated_books]
    return jsonify(result)

@books_bp.route('/<book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404, 'Book not found.')

    data = request.json
    if not data:
        abort(400, 'Invalid book data.')

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.year = data.get('year', book.year)
    db.session.commit()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year})

@books_bp.route('/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404, 'Book not found.')
    db.session.delete(book)
    db.session.commit()
    return '', 204
