from fastapi import FastAPI

from app.in_memory.todo_item_repository import InMemoryTodoItemRepository
from app.in_memory.todo_list_repository import InMemoryTodoListRepository
from app.rest_api import todo_list_api

app = FastAPI()

todo_list_api.repository(InMemoryTodoListRepository(InMemoryTodoItemRepository()))
app.include_router(todo_list_api.router)
