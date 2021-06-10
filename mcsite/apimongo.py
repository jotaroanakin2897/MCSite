from flask import request, jsonify
from mcsite import app, mongo

from bson.json_util import dumps
from bson.objectid import ObjectId


@app.route('/book', methods=['POST'])
def create_book():
  data = request.get_json()

  if not data:
    return jsonify({'message': 'Book not sent!'})
  
  try:
    collection = mongo.db.books
    collection.insert(data)
  except:
    return jsonify({'message': 'Insert error!'})
  
  return jsonify({'message': 'Book created!'})

@app.route('/book', methods=['GET'])
def get_all_books():
  books = mongo.db.books.find()
  resp = dumps(books)

  if not resp:
    return jsonify({'message': 'No books!'})
  
  return resp


@app.route('/book/<book_id>', methods=['GET'])
def get_book(book_id):
  book = mongo.db.books.find_one({'_id':ObjectId(book_id)})
  resp = dumps(book)

  if not resp:
    return jsonify({'message': 'No books!'})
  
  return resp


@app.route('/book/<book_id>', methods=['PUT'])
def update_book(book_id):
  data = request.get_json()
  title = data['title']
  author = data['author']

  if not title and not author:
    return jsonify({'message': 'No books!'})

  mongo.db.books.update_one({'_id':ObjectId(book_id)}, {'$set':{'title': title, 'author':author}})

  return jsonify({'message': 'Book Updated!'})

@app.route('/book/<book_id>', methods=['DELETE'])
def delete_book(book_id):

  mongo.db.books.delete_one({'_id':ObjectId(book_id)})

  return jsonify({'message': 'Book Deleted!'})