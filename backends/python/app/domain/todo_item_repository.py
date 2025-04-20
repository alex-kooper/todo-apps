from typing import Protocol

from app.domain.models import (
    TodoItem,
    TodoItemCreate,
    TodoItemID,
    TodoItemUpdate,
    TodoListID,
)


class TodoItemNotFoundError(Exception):
    def __init__(self, id: TodoItemID):
        self.id = id


class TodoItemRepository(Protocol):
    async def items(
        self, list_id: TodoListID | None = None, is_completed: bool | None = None
    ) -> list[TodoItem]: ...

    async def item_by_id(self, id: TodoItemID) -> TodoItem: ...

    async def new_item(self, item: TodoItemCreate) -> TodoItem: ...

    async def update_item(self, id: TodoItemID, item: TodoItemUpdate) -> TodoItem: ...

    async def delete_item(self, id: TodoItemID) -> None: ...
