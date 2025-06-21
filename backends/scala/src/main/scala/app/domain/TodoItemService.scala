package app.domain

import app.domain.models.TodoItem
import app.domain.models.TodoItemCreate
import app.domain.models.TodoItemUpdate

import zio.*

final case class TodoItemNotFound(id: Int)

trait TodoItemService:
  def items(
      listId: Option[Int] = None,
      isCompleted: Option[Boolean] = None
  ): UIO[Unit]

  def itemById(id: Int): IO[TodoItem, TodoItemNotFound]

  def newItem(item: TodoItemCreate): UIO[TodoItem]

  def updateItem(id: Int, item: TodoItemUpdate): IO[TodoItem, TodoItemNotFound]

  def deleteItem(id: Int): IO[Unit, TodoItemNotFound]
