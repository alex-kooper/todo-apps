package app.domain

import app.domain.models.TodoItem
import app.domain.models.TodoItemCreate
import app.domain.models.TodoItemUpdate

import zio.*

import app.domain.models.TodoItemId

final case class TodoItemNotFound(id: TodoItemId)

trait TodoItemService:
  def items(
      listId: Option[Int] = None,
      isCompleted: Option[Boolean] = None
  ): UIO[Unit]

  def itemById(id: TodoItemId): IO[TodoItem, TodoItemNotFound]

  def newItem(item: TodoItemCreate): UIO[TodoItem]

  def updateItem(id: TodoItemId, item: TodoItemUpdate): IO[TodoItem, TodoItemNotFound]

  def deleteItem(id: TodoItemId): IO[Unit, TodoItemNotFound]
