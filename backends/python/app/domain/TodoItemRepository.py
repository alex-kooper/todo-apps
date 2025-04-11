from typing import Protocol

from app.domain.models import TodoItemID, TodoItemInfo


class TodoItemRepository(Protocol):
    def new_todo_item(self, todo: TodoItemInfo) -> TodoItemID: ...

    def update_todo_item(self, id: TodoItemID, todo: TodoItemInfo) -> None: ...

    def delete_todo_item(self, id: TodoItemID) -> None: ...
