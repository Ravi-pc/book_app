from sanic import response, Blueprint, Request, HTTPResponse
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi
from sanic_openapi import doc
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from core.model import User, engine
from core.schema import UserDetails, UserLogin
from core.utils import hash_password, verify_password, create_access_token, email_verification, decode_token, super_key

Base = declarative_base()

app = Blueprint('user')


async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


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
@openapi.definition(body={'application/json': UserDetails.model_json_schema()}, tag=["User"])
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
        user_super_key = user_validator['super_key']
        if user_super_key == super_key:
            print("yes")
            user_validator.update({'is_super_user': True})
        user_validator.pop('super_key')
        user = User(**user_validator)
        async with async_session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            token = create_access_token({'user_id': user.id})
            email_verification(token, user.email)
        return response.json({'message': f'User registered successfully'}, status=201)
    except Exception as e:
        return response.json({"message": "Failed to register user", "error": str(e)}, status=500)


@app.post('/login')
@openapi.definition(body={'application/json': UserLogin.model_json_schema()}, tag="User")
@validate(UserLogin)
async def login(request, body: UserLogin):

    try:
        async with async_session() as session:
            # Use session.execute() for executing queries
            user = await session.execute(select(User).filter(User.user_name == body.user_name))
            user = user.scalars().first()

            if user is None:
                # User not found
                return response.json({'message': 'Invalid credentials'}, status=401)

            # Verify the provided password against the stored hashed password
            if not verify_password(body.password, user.password):
                # Password does not match
                return response.json({'message': 'Invalid credentials'}, status=401)

            if user.is_verified is False:
                return response.json({'message': 'User Not Verified'}, status=401)

        token = create_access_token({'user_id': user.id})  # create access token
        # Successful login
        return response.json({'message': 'Login successful', 'token': token}, status=200, )

    except Exception as e:
        # Handle any exceptions that may occur during the login process
        return response.json({"message": "Failed to authenticate user", "error": str(e)}, status=500)


@app.get('/verify_user')
@openapi.definition(tag="User")
async def verify_user(request: Request) -> HTTPResponse:
    """
    Description: verify_user function is to validate the user.

    Parameter: token, get_db as a Session object.

    Return: response and status code.
    """
    try:
        token = request.args.get('token')
        if not token:
            return response.json({"message": "Token is required"}, status=400)

        decoded_token = decode_token(token)
        user_id = decoded_token.get('user_id')

        async with async_session() as session:
            user = await session.execute(select(User).filter_by(id=user_id, is_verified=False))
            user = user.scalars().first()
            if not user:
                return response.json({"message": "User already verified or not found"}, status=400)

            user.is_verified = True
            await session.commit()
            return response.json({"message": "User verified successfully", "user_id": user.id}, status=200)

    except Exception as e:
        return response.json({"message": "Failed to verify user", "error": str(e)}, status=500)
