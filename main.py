"""
@Author: Ravi Singh

@Date: 2024-01-01 12:20:30

@Last Modified by:

@Last Modified time: 2024-01-01 12:20:30

@Title : Book Library
"""
from sanic import Sanic
from routes.user import add_user, login, verify_user

app = Sanic('_name_')

app.add_route(add_user, '/register_user', methods=['Post'])
app.add_route(login, '/login', methods=['Post'])
app.add_route(verify_user, '/verify', methods=["GET"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
