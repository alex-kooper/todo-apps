from typing import Protocol

from app.domain.models import TodoListID


class TodoListRepository(Protocol):
    def new_todo_list(self, name: str) -> None: ...

    def update_todo_list(self, id: TodoListID, name: str) -> None: ...

    def delete_todo_list(self, id: TodoListID) -> None: ...
