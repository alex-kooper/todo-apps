from typing import NewType

from pydantic import BaseModel

TodoItemID = NewType("TodoItemID", int)
TodoListID = NewType("TodoListID", int)
TodoItemOrder = NewType("TodoItemOrder", int)


class TodoItemInfo(BaseModel):
    description: str
    order: TodoItemOrder
    is_completed: bool = False


class TodoItem(TodoItemInfo):
    id: TodoItemID
    list_id: TodoListID


class TodoList(BaseModel):
    id: TodoListID
    name: str
