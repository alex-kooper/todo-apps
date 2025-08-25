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

object TodoListService:
  def lists: ZIO[TodoListService, Nothing, Seq[TodoList]] =
    ZIO.serviceWithZIO(_.lists)

  def listById(
      id: TodoListId
  ): ZIO[TodoListService, TodoListNotFoundError, TodoList] =
    ZIO.serviceWithZIO(_.listById(id))

  def newList(name: NonEmptyString): ZIO[TodoListService, Nothing, TodoList] =
    ZIO.serviceWithZIO(_.newList(name))

  def updateList(
      id: TodoListId,
      name: NonEmptyString
  ): ZIO[TodoListService, TodoListNotFoundError, TodoList] =
    ZIO.serviceWithZIO(_.updateList(id, name))

  def deleteList(
      id: TodoListId
  ): ZIO[TodoListService, TodoListNotFoundError, Unit] =
    ZIO.serviceWithZIO(_.deleteList(id))
