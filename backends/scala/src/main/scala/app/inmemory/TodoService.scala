package app.inmemory

import app.domain.models.*
import app.domain
import app.domain.*
import neotype.common.NonEmptyString
import neotype.*
import zio.*

final case class TodoService(
    currentListId: Ref[TodoListId],
    todoListMap: Ref[Map[TodoListId, TodoList]],
    currentItemId: Ref[TodoItemId],
    todoItemMap: Ref[Map[TodoItemId, TodoItem]]
) extends domain.TodoService:
  override def lists: UIO[Seq[TodoList]] =
    todoListMap.get.map(_.values.toSeq.sortBy(_.id))

  override def listById(id: TodoListId): IO[TodoListNotFoundError, TodoList] =
    todoListMap.get.flatMap { map =>
      ZIO.fromOption(map.get(id)).mapError(_ => TodoListNotFoundError(id))
    }

  override def newList(name: NonEmptyString): UIO[TodoList] =
    currentListId
      .updateAndGet(id => TodoListId(id.unwrap + 1))
      .flatMap { todoListId =>
        val todoList = TodoList(todoListId, name)
        todoListMap.update(_ + (todoListId -> todoList)).as(todoList)
      }

  override def updateList(
      id: TodoListId,
      name: NonEmptyString
  ): IO[TodoListNotFoundError, TodoList] =
    todoListMap
      .modify { map =>
        map.get(id) match
          case None => (None, map)
          case Some(_) =>
            val updatedList = TodoList(id, name)
            (Some(updatedList), map + (id -> updatedList))
      }
      .flatMap(
        ZIO.fromOption(_).mapError(_ => TodoListNotFoundError(id))
      )

  override def deleteList(id: TodoListId): IO[TodoListNotFoundError, Unit] =
    todoListMap
      .modify { map =>
        map.get(id) match
          case None => (None, map)
          case Some(_) =>
            (Some(()), map - id)
      }
      .flatMap(
        ZIO.fromOption(_).mapError(_ => TodoListNotFoundError(id))
      ) *> deleteItemsByListId(id)

  override def items(
      listId: Option[TodoListId] = None,
      isCompleted: Option[Boolean] = None
  ): UIO[Seq[TodoItem]] =
    todoItemMap.get.map: todoItemMap =>
      todoItemMap.values
        .filter(item => listId.forall(_ == item.listId))
        .filter(item => isCompleted.forall(_ == item.isCompleted))
        .toSeq
        .sortBy(_.priority)

  override def itemById(
      id: TodoItemId
  ): IO[domain.TodoItemNotFoundError, TodoItem] =
    todoItemMap.get.flatMap { map =>
      ZIO
        .fromOption(map.get(id))
        .mapError(_ => domain.TodoItemNotFoundError(id))
    }

  override def newItem(
      item: TodoItemCreate
  ): IO[TodoListNotFoundError, TodoItem] =
    listById(item.listId) *>
      currentItemId
        .updateAndGet(id => TodoItemId(id.unwrap + 1))
        .flatMap { todoItemId =>
          val todoItem = TodoItem(
            todoItemId,
            item.listId,
            item.title,
            item.isCompleted,
            item.priority
          )
          todoItemMap.update(_ + (todoItemId -> todoItem)).as(todoItem)
        }

  override def deleteItem(
      id: TodoItemId
  ): IO[TodoItemNotFoundError, Unit] =
    todoItemMap
      .modify { map =>
        map.get(id) match
          case None => (None, map)
          case Some(_) =>
            (Some(()), map - id)
      }
      .flatMap(
        ZIO.fromOption(_).mapError(_ => TodoItemNotFoundError(id))
      )

  override def updateItem(
      id: TodoItemId,
      item: TodoItemUpdate
  ): IO[TodoItemNotFoundError, TodoItem] =
    todoItemMap
      .modify { map =>
        map.get(id) match
          case None => (None, map)
          case Some(existingItem) =>
            val updatedItem = updateItem(existingItem, item)
            (Some(updatedItem), map + (id -> updatedItem))
      }
      .flatMap(
        ZIO.fromOption(_).mapError(_ => TodoItemNotFoundError(id))
      )

  private def updateItem(item: TodoItem, update: TodoItemUpdate): TodoItem =
    TodoItem(
      item.id,
      update.listId.getOrElse(item.listId),
      update.title.getOrElse(item.title),
      update.isCompleted.getOrElse(item.isCompleted),
      update.priority.getOrElse(item.priority)
    )

  private def deleteItemsByListId(listId: TodoListId): UIO[Unit] =
    todoItemMap.update { map =>
      map.filterNot { case (_, item) => item.listId == listId }
    }

object TodoService:
  val live: ULayer[TodoService] =
    ZLayer.scoped {
      for
        currentListId <- Ref.make(TodoListId(0))
        todoListMap <- Ref.make(Map.empty[TodoListId, TodoList])
        currentItemId <- Ref.make(TodoItemId(0))
        todoItemMap <- Ref.make(Map.empty[TodoItemId, TodoItem])
      yield TodoService(
        currentListId,
        todoListMap,
        currentItemId,
        todoItemMap
      )
    }
