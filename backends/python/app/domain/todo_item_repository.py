from typing import Protocol

from app.domain.models import (
    TodoItem,
    TodoItemCreate,
    TodoItemID,
    TodoItemUpdate,
    TodoListID,
)


class TodoItemRepository(Protocol):
    def all_items(self, list_id: TodoListID) -> list[TodoItem]: ...

    def items_with_status(
        self, list_id: TodoListID, is_completed: bool
    ) -> list[TodoItem]: ...

    def item_by_id(self, id: TodoItemID) -> TodoItem: ...

    def new_item(self, item: TodoItemCreate) -> TodoItem: ...

    def update_item(self, id: TodoItemID, item: TodoItemUpdate) -> TodoItem: ...

    def delete_item(self, id: TodoItemID) -> None: ...
