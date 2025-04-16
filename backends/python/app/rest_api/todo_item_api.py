from contextlib import contextmanager
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

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


@router.get("/todo-lists/{list_id}/items", response_model=list[TodoItem])
async def all_items(list_id: TodoListID, repo: RepositoryDep):
    with exception_handling():
        return await repo.all_items(list_id)


@router.get("/todo-items/{item_id}", response_model=TodoItem)
async def get_item_by_id(item_id: TodoItemID, repo: RepositoryDep):
    with exception_handling():
        return await repo.item_by_id(item_id)


@router.post("/todo-lists/{list_id}/items", response_model=TodoItem)
async def new_item(list_id: TodoListID, item: TodoItemCreate, repo: RepositoryDep):
    with exception_handling():
        return await repo.new_item(item)


@router.patch("/todo-items/{item_id}", response_model=TodoItem)
async def update_item(item_id: TodoItemID, item: TodoItemUpdate, repo: RepositoryDep):
    with exception_handling():
        return await repo.update_item(item_id, item)


@router.delete("/todo-items/{item_id}", response_model=TodoItem)
async def delete_item(item_id: TodoItemID, repo: RepositoryDep):
    with exception_handling():
        return await repo.delete_item(item_id)
