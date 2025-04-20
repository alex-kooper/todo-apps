from contextlib import contextmanager
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.domain.models import (
    TodoItem,
    TodoItemCreate,
    TodoItemID,
    TodoItemUpdate,
    TodoListID,
)
from app.domain.todo_item_repository import TodoItemNotFoundError, TodoItemRepository
from app.domain.todo_list_repository import TodoListNotFoundError

router = APIRouter(
    prefix="/todo-items",
    tags=["todo-items"],
    responses={404: {"description": "TODO list or TODO item not found"}},
)

_repository: TodoItemRepository


def get_repository():
    return _repository


def repository(repository: TodoItemRepository):
    global _repository
    _repository = repository


RepositoryDep = Annotated[TodoItemRepository, Depends(get_repository)]


@contextmanager
def exception_handling():
    try:
        yield
    except TodoListNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO list with ID {e.id} does not exist.",
        ) from e
    except TodoItemNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO item with ID {e.id} does not exist.",
        ) from e


@router.get("/", response_model=list[TodoItem])
async def items(
    repo: RepositoryDep,
    list_id: TodoListID | None = Query(None, alias="list-id"),
    is_completed: bool | None = Query(None, alias="is-completed"),
):
    with exception_handling():
        return await repo.items(list_id, is_completed)


@router.get("/{item_id}", response_model=TodoItem)
async def item_by_id(repo: RepositoryDep, item_id: TodoItemID):
    with exception_handling():
        return await repo.item_by_id(item_id)


@router.post("/", response_model=TodoItem)
async def new_item(repo: RepositoryDep, item: TodoItemCreate):
    with exception_handling():
        return await repo.new_item(item)


@router.patch("/{item_id}", response_model=TodoItem)
async def update_item(repo: RepositoryDep, item_id: TodoItemID, item: TodoItemUpdate):
    with exception_handling():
        return await repo.update_item(item_id, item)


@router.delete("/{item_id}", response_model=TodoItem)
async def delete_item(repo: RepositoryDep, item_id: TodoItemID):
    with exception_handling():
        return await repo.delete_item(item_id)
