from contextlib import contextmanager
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.models import TodoList, TodoListID
from app.domain.todo_list_service import TodoListNotFoundError, TodoListService

router = APIRouter(
    prefix="/todo-lists",
    tags=["todo-lists"],
    responses={404: {"description": "TODO list not found"}},
)

_service: TodoListService


def get_service():
    return _service


def set_service(service: TodoListService):
    global _service
    _service = service


ServiceDep = Annotated[TodoListService, Depends(get_service)]


@contextmanager
def exception_handling():
    try:
        yield
    except TodoListNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TodoList with ID {e.id} does not exist.",
        ) from e


@router.get("/", response_model=list[TodoList])
async def lists(service: ServiceDep):
    return await service.lists()


@router.get("/{id}", response_model=TodoList)
async def list_by_id(id: TodoListID, service: ServiceDep):
    with exception_handling():
        return await service.list_by_id(id)


@router.post("/", response_model=TodoList)
async def new_list(name: str, service: ServiceDep):
    return await service.new_list(name)


@router.put("/{id}", response_model=TodoList)
async def update_list(id: TodoListID, name: str, service: ServiceDep):
    with exception_handling():
        return await service.update_list(id, name)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_list(id: TodoListID, service: ServiceDep):
    with exception_handling():
        return await service.delete_list(id)
