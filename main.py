"""
@Author: Ravi Singh

@Date: 2024-01-01 12:20:30

@Last Modified by:

@Last Modified time: 2024-01-01 12:20:30

@Title : Book Library
"""
from sanic import Sanic
from routes.book import book_api
from routes.cart import cart_api
from routes.user import app as user_api


app = Sanic('_name_')

app.ext.openapi.add_security_scheme(
    "authorization",
    "http",
    scheme="bearer",
    bearer_format="JWT"
)
#
# app.add_route(add_user, '/register_user', methods=['Post'])
# app.add_route(login, '/login', methods=['Post'])
# app.add_route(verify_user, '/verify', methods=["GET"])
# app.add_route(add_book, '/book/register', methods=["Post"])
app.blueprint(user_api)
app.blueprint(book_api)
app.blueprint(cart_api)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
