from app.domain.models import TodoItem, TodoItemID, TodoItemInfo, TodoListID


class InMemoryTodoItemRepository:
    _item_storage: dict[TodoItemID, TodoItem]
    _list_to_items: dict[TodoListID, list[TodoItemID]]

    _current_item_id: int

    def __init__(self):
        self._current_item_id = 0
        self._item_storage = {}
        self._list_to_items = {}

    def all_items(self, list_id: TodoListID) -> list[TodoItem]:
        if list_id not in self._list_to_items:
            raise KeyError(f"TodoList with ID {list_id} does not exist.")

        return [self._item_storage[item_id] for item_id in self._list_to_items[list_id]]

    def items_with_status(
        self, list_id: TodoListID, is_completed: bool
    ) -> list[TodoItemInfo]:
        return [
            item
            for item in self.all_items(list_id)
            if item.is_completed == is_completed
        ]

    def new_item(self, list_id: TodoListID, item: TodoItemInfo) -> TodoItemID:
        if list_id not in self._list_to_items:
            raise KeyError(f"TodoList with ID {list_id} does not exist.")

        id = self._next_item_id()

        item = TodoItem(id=id, list_id=list_id, **item.model_dump())
        self._item_storage[id] = item

        self._list_to_items.setdefault(list_id, []).append(id)
        return id

    def update_item(self, id: TodoItemID, item: TodoItemInfo) -> None:
        if id not in self._item_storage:
            raise KeyError(f"TodoItem with ID {id} does not exist.")

        self._item_storage[id].model_copy(update=item.model_dump())

    def move_item(self, id: TodoItemID, new_list_id: TodoListID) -> None:
        if id not in self._item_storage:
            raise KeyError(f"TodoItem with ID {id} does not exist.")

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

    def delete_item(self, id: TodoItemID) -> None:
        if id not in self._item_storage:
            raise KeyError(f"TodoItem with ID {id} does not exist.")

        item = self._item_storage[id]
        list_id = item.list_id

        # Remove from list
        self._list_to_items[list_id].remove(id)
        if not self._list_to_items[list_id]:
            del self._list_to_items[list_id]

        # Remove from storage
        del self._item_storage[id]

    def _next_item_id(self) -> TodoItemID:
        self._current_item_id += 1
        return TodoItemID(self._current_item_id)

    def _delete_list_items(self, list_id: TodoListID) -> None:
        if list_id not in self._list_to_items:
            raise KeyError(f"TodoList with ID {list_id} does not exist.")

        for item_id in self._list_to_items[list_id]:
            del self._item_storage[item_id]

        del self._list_to_items[list_id]
