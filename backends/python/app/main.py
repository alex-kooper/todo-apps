from fastapi import FastAPI

from app.in_memory.todo_item_service import TodoItemServiceWithInMemoryStorage
from app.in_memory.todo_list_service import TodoListServiceWithInMemoryStorage
from app.rest_api import todo_item_api, todo_list_api

app = FastAPI()

todo_item_service = TodoItemServiceWithInMemoryStorage()

todo_list_api.set_service(TodoListServiceWithInMemoryStorage(todo_item_service))
app.include_router(todo_list_api.router)

todo_item_api.set_service(todo_item_service)
app.include_router(todo_item_api.router)
