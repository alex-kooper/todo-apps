from app.domain.models import (
    TodoItem,
    TodoItemCreate,
    TodoItemID,
    TodoItemUpdate,
    TodoListID,
)
from app.domain.todo_item_repository import TodoItemNotFoundError
from app.domain.todo_list_repository import TodoListNotFoundError


class InMemoryTodoItemRepository:
    _item_storage: dict[TodoItemID, TodoItem]
    _list_to_items: dict[TodoListID, list[TodoItemID]]

    _current_item_id: int

    def __init__(self):
        self._current_item_id = 0
        self._item_storage = {}
        self._list_to_items = {}

    async def items(
        self, list_id: TodoListID | None = None, is_completed: bool | None = None
    ) -> list[TodoItem]:
        if list_id is None:
            ret = list(self._item_storage.values())
        else:
            if list_id not in self._list_to_items:
                raise TodoListNotFoundError(list_id)

            ret = [
                self._item_storage[item_id] for item_id in self._list_to_items[list_id]
            ]

        if is_completed is not None:
            ret = [item for item in ret if item.is_completed == is_completed]

        return ret

    async def item_by_id(self, id: TodoItemID) -> TodoItem:
        if id in self._item_storage:
            return self._item_storage[id]
        else:
            raise TodoItemNotFoundError(id)

    async def new_item(self, item: TodoItemCreate) -> TodoItem:
        if item.list_id not in self._list_to_items:
            raise TodoListNotFoundError(item.list_id)

        id = self._next_item_id()

        new_item = TodoItem(
            id=id,
            **item.model_dump(),
        )

        self._item_storage[id] = new_item

        self._list_to_items.setdefault(item.list_id, []).append(id)
        return new_item

    async def update_item(
        self, id: TodoItemID, item_update: TodoItemUpdate
    ) -> TodoItem:
        if id not in self._item_storage:
            raise TodoItemNotFoundError(id)

        item = self._item_storage[id]
        updated_item = item.model_copy(
            update=item_update.model_dump(exclude_none=True),
        )
        self._item_storage[id] = updated_item

        if item_update.list_id is not None:
            if item_update.list_id not in self._list_to_items:
                raise TodoListNotFoundError(item_update.list_id)

            # Move item to new list
            self._move_item(id, item_update.list_id)

        return updated_item

    async def delete_item(self, id: TodoItemID) -> None:
        if id not in self._item_storage:
            raise TodoItemNotFoundError(id)

        item = self._item_storage[id]
        list_id = item.list_id

        # Remove from list
        self._list_to_items[list_id].remove(id)
        if not self._list_to_items[list_id]:
            del self._list_to_items[list_id]

        # Remove from storage
        del self._item_storage[id]

    async def new_list(self, list_id: TodoListID) -> None:
        self._list_to_items[list_id] = []

    async def delete_list(self, list_id: TodoListID) -> None:
        if list_id not in self._list_to_items:
            return

        for item_id in self._list_to_items[list_id]:
            del self._item_storage[item_id]

        del self._list_to_items[list_id]

    def _next_item_id(self) -> TodoItemID:
        self._current_item_id += 1
        return TodoItemID(self._current_item_id)

    def _move_item(self, id: TodoItemID, new_list_id: TodoListID) -> None:
        if id not in self._item_storage:
            raise TodoItemNotFoundError(id)

        if new_list_id not in self._list_to_items:
            raise KeyError(f"TodoList with ID {new_list_id} does not exist.")

        item = self._item_storage[id]
        old_list_id = item.list_id

        # Remove from old list
        self._list_to_items[old_list_id].remove(id)
        if not self._list_to_items[old_list_id]:
            del self._list_to_items[old_list_id]

        # Add to new list
        self._list_to_items.setdefault(new_list_id, []).append(id)
        item.list_id = new_list_id
