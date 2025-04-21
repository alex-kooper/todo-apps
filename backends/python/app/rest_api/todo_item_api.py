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
from app.domain.todo_item_service import TodoItemNotFoundError, TodoItemService
from app.domain.todo_list_service import TodoListNotFoundError

router = APIRouter(
    prefix="/todo-items",
    tags=["todo-items"],
    responses={404: {"description": "TODO list or TODO item not found"}},
)

_service: TodoItemService


def get_service():
    return _service


def set_service(service: TodoItemService):
    global _service
    _service = service


ServiceDep = Annotated[TodoItemService, Depends(get_service)]


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
    service: ServiceDep,
    list_id: TodoListID | None = Query(None, alias="list-id"),
    is_completed: bool | None = Query(None, alias="is-completed"),
):
    with exception_handling():
        return await service.items(list_id, is_completed)


@router.get("/{id}", response_model=TodoItem)
async def item_by_id(service: ServiceDep, id: TodoItemID):
    with exception_handling():
        return await service.item_by_id(id)


@router.post("/", response_model=TodoItem)
async def new_item(service: ServiceDep, item: TodoItemCreate):
    with exception_handling():
        return await service.new_item(item)


@router.patch("/{id}", response_model=TodoItem)
async def update_item(service: ServiceDep, id: TodoItemID, item: TodoItemUpdate):
    with exception_handling():
        return await service.update_item(id, item)


@router.delete("/{id}", response_model=TodoItem)
async def delete_item(service: ServiceDep, id: TodoItemID):
    with exception_handling():
        return await service.delete_item(id)
