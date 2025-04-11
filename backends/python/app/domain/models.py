from typing import NewType

from pydantic import BaseModel

TodoItemID = NewType("TodoItemID", int)
TodoListID = NewType("TodoListID", int)
TodoItemOrder = NewType("TodoItemOrder", int)


class TodoItemInfo(BaseModel):
    todo_list_id: TodoListID
    description: str
    order: TodoItemOrder
    is_completed: bool = False


class TodoItem(TodoItemInfo):
    id: TodoItemID


class TodoList(BaseModel):
    id: TodoListID
    name: str
