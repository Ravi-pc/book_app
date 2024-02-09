from sanic import Blueprint, response
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sqlalchemy import select
from core.model import Cart, Book, CartItems, User, async_session
from core.schema import CartItemsSchema
from core.utils import authorize

cart_api = Blueprint('cart', url_prefix='/cart')
cart_api.middleware(authorize, 'request')


# Endpoint to add a book to the cart
@cart_api.post('/add')
@openapi.definition(body={'application/json': CartItemsSchema.model_json_schema()}, tag='Cart',
                     secured="authorization")
@validate(json=CartItemsSchema)
async def add_book_to_cart(request, body):
    """
    Description: add_book_to_cart function is used to add a book to the cart.

    Parameter: Request object

    Returns: JSON response indicating the success or failure of adding a book to the cart.

    """
    try:
        async with async_session() as session:
            cart_data = await session.execute(select(Cart).filter_by(user_id=request.ctx.user_id))
            cart_data = cart_data.scalars().one_or_none()

            if cart_data is None:
                cart_data = Cart(user_id=request.ctx.user_id)
                session.add(cart_data)

            book_data = await session.execute(select(Book).filter_by(id=body.book_id))
            book_data = book_data.scalars().one_or_none()

            if book_data is None:
                raise Exception("This book is not present")

            if body.quantity > book_data.quantity:
                raise Exception(f"Oops! Only {book_data.quantity} number of books present.")

            books_price = body.quantity * book_data.price

            cart_items_data = await session.execute(select(CartItems).filter_by(book_id=body.book_id))
            cart_items_data = cart_items_data.scalars().one_or_none()

            if cart_items_data is None:
                cart_items_data = CartItems(price=books_price, quantity=body.quantity, book_id=book_data.id,
                                            cart_id=cart_data.id)
                session.add(cart_items_data)
            else:
                cart_data.total_price -= cart_items_data.price
                cart_data.total_quantity -= cart_items_data.quantity

            cart_data.total_price += books_price
            cart_data.total_quantity += body.quantity

            await session.commit()
            await session.refresh(cart_data)
            await session.refresh(cart_items_data)

            return response.json({'message': 'Book added on cart Successfully', 'status': 201})
    except Exception as ex:
        return response.json({'message': str(ex), 'status': 400})


@cart_api.get('/get/<cart_id:int>')
@openapi.definition(response={200: {'application/json': CartItemsSchema.model_json_schema()}}, tag='Cart',
                    secured="authorization")
async def get_all_cart_items_details(request, cart_id):
    """
    Description: This function to get details of all cart items.

    Parameter: Request object, cart_id (int): ID of the cart.

    Returns: JSON response containing details of all cart items.
    """
    try:
        async with async_session() as session:
            cart_data = await session.execute(select(Cart).filter_by(id=cart_id, user_id=request.ctx.user_id))
            cart_data = cart_data.scalars().one_or_none()

            if cart_data is None:
                return response.json({'message': 'Cart is empty', 'status': 400})

            card_items_data = await session.execute(select(CartItems).filter_by(cart_id=cart_id))
            card_items_data = card_items_data.scalars().all()

            serialized_card_items_data = []
            for item in card_items_data:
                serialized_item = {
                    'id': item.id,
                    'book_id': item.book_id,
                    'quantity': item.quantity,
                    'price': item.price,
                    'cart_id': item.cart_id
                }
                serialized_card_items_data.append(serialized_item)

            return response.json({'message': 'All cart items get successfully', 'status': 200,
                                  'data': serialized_card_items_data})
    except Exception as ex:
        return response.json({'message': str(ex), 'status': 400})


@cart_api.get('/confirm')
@openapi.definition(tag='Cart', secured="authorization")
async def confirm_order(request):
    """
    Description: Function to confirm the order.

    Parameters: Request object.

    Returns: JSON response indicating the success or failure of order confirmation.
    """
    try:
        async with async_session() as session:
            cart_data = await session.execute(select(Cart).filter_by(user_id=request.ctx.user_id))
            cart_data = cart_data.scalars().one_or_none()

            if cart_data is None:
                return response.json({'message': 'The Cart is Empty', 'status': 400})

            cart_items_details = await session.execute(select(CartItems).filter_by(cart_id=cart_data.id))
            cart_items_details = cart_items_details.scalars().all()

            cart_data.is_ordered = True

            user_data = await session.execute(select(User).filter_by(id=request.ctx.user_id))
            user_data = user_data.scalars().one_or_none()

            await session.commit()
            return response.json({'message': 'Order Confirmation Successfully', 'status': 200})
    except Exception as ex:
        return response.json({'message': str(ex), 'status': 400})
