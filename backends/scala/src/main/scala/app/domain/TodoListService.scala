package app.domain

import app.domain.models.TodoList
import app.domain.models.TodoListId

import zio.*
import neotype.common.NonEmptyString

final case class TodoListNotFoundError(id: TodoListId)

trait TodoListService:
  def lists: UIO[TodoList]

  def listById(id: TodoListId): IO[TodoList, TodoListNotFoundError]

  def newList(name: NonEmptyString): UIO[TodoList]

  def updateList(id: TodoListId, name: NonEmptyString): IO[TodoList, TodoListNotFoundError]

  def deleteList(id: TodoListId): IO[Unit, TodoListNotFoundError]
