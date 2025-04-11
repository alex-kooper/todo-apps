from typing import Protocol

from app.domain.models import TodoItemID, TodoItemInfo, TodoListID


class TodoItemRepository(Protocol):
    def all_items(self, list_id: TodoListID) -> list[TodoItemInfo]: ...

    def items_with_status(
        self, list_id: TodoListID, is_completed: bool
    ) -> list[TodoItemInfo]: ...

    def new_item(self, list_id: TodoListID, item: TodoItemInfo) -> TodoItemID: ...

    def update_item(self, id: TodoItemID, item: TodoItemInfo) -> None: ...

    def delete_item(self, id: TodoItemID) -> None: ...
