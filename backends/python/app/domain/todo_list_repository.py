from typing import Protocol

from app.domain.models import TodoList, TodoListID


class TodoListNotFoundError(Exception):
    def __init__(self, id: TodoListID):
        self.id = id


class TodoListRepository(Protocol):
    async def lists(self) -> list[TodoList]: ...

    async def list_by_id(self, id: TodoListID) -> TodoList: ...

    async def new_list(self, name: str) -> TodoList: ...

    async def update_list(self, id: TodoListID, name: str) -> TodoList: ...

    async def delete_list(self, id: TodoListID) -> None: ...
