from fastapi import FastAPI

from app.in_memory.todo_item_repository import InMemoryTodoItemRepository
from app.in_memory.todo_list_repository import InMemoryTodoListRepository
from app.rest_api import todo_item_api, todo_list_api

app = FastAPI()

todo_item_repository = InMemoryTodoItemRepository()

todo_list_api.repository(InMemoryTodoListRepository(todo_item_repository))
app.include_router(todo_list_api.router)

todo_item_api.repository(todo_item_repository)
app.include_router(todo_item_api.router)
