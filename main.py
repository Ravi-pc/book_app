"""
@Author: Ravi Singh

@Date: 2024-01-01 12:20:30

@Last Modified by:

@Last Modified time: 2024-01-01 12:20:30

@Title : Book Library
"""
from sanic import Sanic, response

from routes import user
from routes.book import authorize, add_book, book_api
# from routes.book import add_book, authorization
from routes.user import add_user, login, verify_user, app as user_api
# from sanic_jwt import Initialize


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
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
