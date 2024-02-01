from sanic import response, Blueprint
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_openapi import doc
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from core.model import User, engine
from core.schema import UserDetails
from core.utils import hash_password

Base = declarative_base()

app = Blueprint('user')


async_session = sessionmaker(engine, class_=AsyncSession)


# Middleware to provide a database session to each request
@app.middleware('request')
async def add_session_to_request(request):
    request.ctx.db = async_session()


# Middleware to close the database session after each request
@app.middleware('response')
async def close_session(request):
    await request.ctx.db.close()


@app.route('/register_user', methods=['POST'])
@doc.summary("Add a user to the database.")
@openapi.definition(body={'application/json': UserDetails.model_json_schema()})
@validate(json=UserDetails)
async def add_user(request, body):
    """
        Description: add_user function is used to register a new user to the application.
        Parameter: request and body.
        Return: JSON Response.
    """
    print(request.body)
    try:
        user_validator = UserDetails.model_dump(body)
        user_validator['password'] = hash_password(user_validator['password'])
        user = User(**user_validator)
        async with async_session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return response.json({'message': f'User registered successfully'}, status=201)
    except Exception as e:
        return response.json({"message": "Failed to register user", "error": str(e)}, status=500)
