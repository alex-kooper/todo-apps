from typing import Dict

from app.domain.models import TodoList, TodoListID


class InMemoryTodoListRepository:
    """In-memory implementation of the TodoListRepository protocol."""

    _storage: Dict[TodoListID, TodoList]
    _current_id: int

    def __init__(self):
        self._current_id = 0
        self._storage = {}

    def all_lists(self) -> list[TodoList]:
        return list(self._storage.values())

    def list_by_id(self, id: TodoListID) -> TodoList:
        if id in self._storage:
            return self._storage[id]
        else:
            raise KeyError(f"TodoList with ID {id} does not exist.")

    def new_list(self, name: str) -> TodoListID:
        self._current_id += 1
        id = TodoListID(self._current_id)
        self._storage[id] = TodoList(id=id, name=name)
        return id

    def update_list(self, id: TodoListID, name: str) -> None:
        if id in self._storage:
            self._storage[id].name = name
        else:
            raise KeyError(f"TodoList with ID {id} does not exist.")

    def delete_list(self, id: TodoListID) -> None:
        if id in self._storage:
            del self._storage[id]
        else:
            raise KeyError(f"TodoList with ID {id} does not exist.")
