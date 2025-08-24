package app.domain

import app.domain.models.TodoList
import app.domain.models.TodoListId

import zio.*
import neotype.common.NonEmptyString

final case class TodoListNotFoundError(id: TodoListId)

trait TodoListService:
  def lists: UIO[Seq[TodoList]]

  def listById(id: TodoListId): IO[TodoListNotFoundError, TodoList]

  def newList(name: NonEmptyString): UIO[TodoList]

  def updateList(
      id: TodoListId,
      name: NonEmptyString
  ): IO[TodoListNotFoundError, TodoList]

  def deleteList(id: TodoListId): IO[TodoListNotFoundError, Unit]
