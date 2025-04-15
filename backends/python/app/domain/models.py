from typing import NewType

from pydantic import BaseModel

TodoItemID = NewType("TodoItemID", int)
TodoListID = NewType("TodoListID", int)
TodoItemPriority = NewType("TodoItemPriority", int)


class TodoItemCreate(BaseModel):
    list_id: TodoListID
    title: str
    is_completed: bool = False
    priority: TodoItemPriority = TodoItemPriority(0)


class TodoItemUpdate(BaseModel):
    list_id: TodoListID | None = None
    title: str | None = None
    is_completed: bool | None = None
    priority: TodoItemPriority | None = None


class TodoItem(TodoItemCreate):
    id: TodoItemID


class TodoList(BaseModel):
    id: TodoListID
    name: str
