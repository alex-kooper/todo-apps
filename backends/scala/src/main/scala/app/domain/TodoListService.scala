package app.domain

import app.domain.models.TodoList

import zio.*

final case class TodoListNotFoundError(id: Int)

trait TodoListService:
  def lists: UIO[TodoList]

  def listById(id: Int): IO[TodoList, TodoListNotFoundError]

  def newList(name: String): UIO[TodoList]

  def updateList(id: Int, name: String): IO[TodoList, TodoListNotFoundError]

  def deleteList(id: Int): IO[Unit, TodoListNotFoundError]
