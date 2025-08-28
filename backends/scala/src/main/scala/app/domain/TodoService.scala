package app.domain

import app.domain.models.*

import zio.*
import neotype.common.NonEmptyString

final case class TodoListNotFoundError(id: TodoListId)
final case class TodoItemNotFoundError(id: TodoItemId)

trait TodoService:
  def lists: UIO[Seq[TodoList]]

  def listById(id: TodoListId): IO[TodoListNotFoundError, TodoList]

  def newList(name: NonEmptyString): UIO[TodoList]

  def updateList(
      id: TodoListId,
      name: NonEmptyString
  ): IO[TodoListNotFoundError, TodoList]

  def deleteList(id: TodoListId): IO[TodoListNotFoundError, Unit]

  def items(
      listId: Option[TodoListId] = None,
      isCompleted: Option[Boolean] = None
  ): UIO[Seq[TodoItem]]

  def itemById(id: TodoItemId): IO[TodoItemNotFoundError, TodoItem]

  def newItem(item: TodoItemCreate): IO[TodoListNotFoundError, TodoItem]

  def updateItem(
      id: TodoItemId,
      item: TodoItemUpdate
  ): IO[TodoItemNotFoundError, TodoItem]

  def deleteItem(id: TodoItemId): IO[TodoItemNotFoundError, Unit]

object TodoService:
  def lists: ZIO[TodoService, Nothing, Seq[TodoList]] =
    ZIO.serviceWithZIO(_.lists)

  def listById(
      id: TodoListId
  ): ZIO[TodoService, TodoListNotFoundError, TodoList] =
    ZIO.serviceWithZIO(_.listById(id))

  def newList(name: NonEmptyString): ZIO[TodoService, Nothing, TodoList] =
    ZIO.serviceWithZIO(_.newList(name))

  def updateList(
      id: TodoListId,
      name: NonEmptyString
  ): ZIO[TodoService, TodoListNotFoundError, TodoList] =
    ZIO.serviceWithZIO(_.updateList(id, name))

  def deleteList(
      id: TodoListId
  ): ZIO[TodoService, TodoListNotFoundError, Unit] =
    ZIO.serviceWithZIO(_.deleteList(id))
