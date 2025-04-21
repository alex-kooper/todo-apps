from contextlib import contextmanager
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.models import TodoList, TodoListID
from app.domain.todo_list_repository import TodoListNotFoundError, TodoListRepository

router = APIRouter(
    prefix="/todo-lists",
    tags=["todo-lists"],
    responses={404: {"description": "TODO list not found"}},
)

_repository: TodoListRepository


def get_repository():
    return _repository


def repository(repository: TodoListRepository):
    global _repository
    _repository = repository


RepositoryDep = Annotated[TodoListRepository, Depends(get_repository)]


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
async def lists(repo: RepositoryDep):
    return await repo.lists()


@router.get("/{id}", response_model=TodoList)
async def list_by_id(id: TodoListID, repo: RepositoryDep):
    with exception_handling():
        return await repo.list_by_id(id)


@router.post("/", response_model=TodoList)
async def new_list(name: str, repo: RepositoryDep):
    return await repo.new_list(name)


@router.put("/{id}", response_model=TodoList)
async def update_list(id: TodoListID, name: str, repo: RepositoryDep):
    with exception_handling():
        return await repo.update_list(id, name)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_list(id: TodoListID, repo: RepositoryDep):
    with exception_handling():
        return await repo.delete_list(id)
