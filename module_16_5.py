
from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from typing import List
# from typing import Annotated
from fastapi.templating import Jinja2Templates


# ...$ python3 -m uvicorn module_16_5:app

app = FastAPI()

templates = Jinja2Templates(directory='templates')

class User(BaseModel):
    username: str
    age: int = None

# class User_test():
#     id: int
#     username: str
#     age: int = None

# user1 = User_test()
# user2 = User_test()
# user3 = User_test()
# user1.id = 0
# user1.username = 'UrbanUser'
# user1.age = 24
# user2.id = 1
# user2.username = 'UrbanTest'
# user2.age = 22
# user3.id = 2
# user3.username = 'Capybara'
# user3.age = 60
# user_db = [user1, user2, user3]
user_db = []

@app.get('/')
def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': user_db})
# Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
# TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также
# передавать в него request и список users. Ключи в словаре для передачи определите
# самостоятельно в соответствии с шаблоном.


@app.get(path='/users/{user_id}')
def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('users.html', {'request': request, 'user': user_db[user_id - 1]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')
# Функция по этому запросу теперь принимает аргумент request и user_id.
# Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
# TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
# а также передавать в него request и одного из пользователей - user.
# Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.

@app.post('/users/{username}/{age}')
def create_user(user: User, username, age) -> str:
    # Создать нового пользователя
    user.username = username
    user.age = age
    user_db.append(user)
    return f'User {username} created'


@app.put('/users/{user_id}')
def update_user(user_id: int, age: int = Body()) -> str:
    try:
        edit_user = user_db[user_id]
        edit_user.age = age
        return f'User {edit_user.username} updated'
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')

@app.delete('/users/{user_id}')
def delete_user(user_id: int) -> str:
    try:
        user_deleted = user_db.pop(user_id)
        return f'User {user_deleted.username} deleted'
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')

# @app.delete('/')
# async def kill_message_all() -> str:
#     messages_db.clear()
#     return 'All messages deleted'


# current_index = str(int(max(message_db, key=int)) + 1)