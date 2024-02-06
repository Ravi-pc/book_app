from sanic import Blueprint, response
from sanic.request import Request
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sqlalchemy import select
from core.model import User, Book
from core.schema import BookSchema
from core.utils import decode_token, authorize
from routes.user import async_session

book_api = Blueprint('books', url_prefix='/books')
book_api.middleware(authorize, 'request')


@book_api.post('/register/')
@openapi.definition(body={'application/json': BookSchema.model_json_schema()}, tag='Book', secured='authorization')
@validate(json=BookSchema)
async def add_book(request, body):
    try:
        # Use the actual user_id from the decoded token, not User.id
        user_id = request.ctx.user_id

        async with async_session() as session:
            user = await session.execute(select(User).filter_by(id=user_id))
            user = user.scalars().first()

            data = body.model_dump()
            data.update({'user_id': user.id})
            book_data = Book(**data)
            session.add(book_data)
            await session.commit()
            await session.refresh(book_data)

            return response.json({"message": "Book registered successfully", "book_id": book_data.id}, status=201)
    except Exception as e:
        return response.json({"message": f"Failed to register book: {str(e)}"}, status=500)


@book_api.put('/update/<book_id:int>')
@openapi.definition(body={'application/json': BookSchema.model_json_schema()}, tag='Book', secured='authorization')
@validate(json=BookSchema)
async def update_book(request, body, book_id):
    try:
        # Use the actual user_id from the decoded token, not User.id
        user_id = request.ctx.user_id

        async with async_session() as session:
            # Check if the book with the specified ID exists and is owned by the user
            book = await session.execute(select(Book).filter_by(id=book_id, user_id=user_id))
            book = book.scalars().first()

            if not book:
                return response.json({"message": "Book not found or unauthorized to update"}, status=404)

            # Update book details
            data = body.model_dump()
            for key, value in data.items():
                setattr(book, key, value)

            await session.commit()
            await session.refresh(book)

            return response.json({"message": "Book updated successfully", "book_id": book.id}, status=200)
    except Exception as e:
        return response.json({"message": f"Failed to update book: {str(e)}"}, status=500)


@book_api.get('/get_book')
@openapi.definition(tag='Book', secured='authorization')
async def get_book(request):
    try:
        async with async_session() as session:
            books = await session.execute(select(Book))
            books = books.scalars().all()

            if not books:
                return response.json({"message": "No books found"}, status=404)

            # Create a list to store information about each book
            books_info = []
            for book in books:
                book_info = {
                    "book_id": book.id,
                    "book_name": book.book_name,
                    "author": book.author,
                    "price": book.price,
                    "quantity": book.quantity
                }
                books_info.append(book_info)

            # Return information about all books
            return response.json({"books": books_info}, status=200)

    except Exception as e:
        return response.json({"message": f"Failed to retrieve books: {str(e)}"}, status=500)


@book_api.delete('/delete/<book_id:int>')
@openapi.definition(response={'application/json': BookSchema.model_json_schema()}, tag='Book', secured='authorization')
async def delete_book(request, book_id: int):
    try:
        # Use the actual user_id from the decoded token, not User.id
        user_id = request.ctx.user_id

        async with async_session() as session:
            # Check if the book with the specified ID exists and is owned by the user
            book = await session.execute(select(Book).filter_by(id=book_id, user_id=user_id))
            book = book.scalars().first()

            if not book:
                return response.json({"message": "Book not found or unauthorized to delete"}, status=404)

            # Delete the book
            # session.add(book)
            await session.delete(book)
            await session.commit()
            # await session.refresh(book)

            return response.json({"message": "Book deleted successfully"}, status=200)
    except Exception as e:
        return response.json({"message": f"Failed to delete book: {str(e)}"}, status=500)
