from app.domain.models import TodoList, TodoListID
from app.domain.todo_list_repository import TodoListNotFoundError
from app.in_memory.todo_item_repository import InMemoryTodoItemRepository


class InMemoryTodoListRepository:
    """In-memory implementation of the TodoListRepository protocol."""

    _storage: dict[TodoListID, TodoList]
    _current_id: int

    def __init__(self, item_repository: InMemoryTodoItemRepository):
        self._current_id = 0
        self._storage = {}
        self._item_repository = item_repository

    async def all_lists(self) -> list[TodoList]:
        return list(self._storage.values())

    async def list_by_id(self, id: TodoListID) -> TodoList:
        if id in self._storage:
            return self._storage[id]
        else:
            raise TodoListNotFoundError(id)

    async def new_list(self, name: str) -> TodoList:
        self._current_id += 1
        id = TodoListID(self._current_id)
        new_list = TodoList(id=id, name=name)

        self._storage[id] = new_list
        await self._item_repository.new_list(id)
        return new_list

    async def update_list(self, id: TodoListID, name: str) -> TodoList:
        if id not in self._storage:
            raise TodoListNotFoundError(id)

        list = self._storage[id]
        list.name = name

        return list

    async def delete_list(self, id: TodoListID) -> None:
        if id not in self._storage:
            raise TodoListNotFoundError(id)

        await self._item_repository.delete_list_items(id)
        del self._storage[id]
