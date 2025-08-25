package app.inmemory

import app.domain.models.*
import app.domain
import app.domain.TodoListNotFoundError
import neotype.common.NonEmptyString
import neotype.*
import zio.*

final case class TodoListService(
    currentListId: Ref[TodoListId],
    todoListMap: Ref[Map[TodoListId, TodoList]]
) extends domain.TodoListService:
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
      )

object TodoListService:
  val live: ULayer[TodoListService] =
    ZLayer.scoped {
      for
        currentId <- Ref.make(TodoListId(0))
        todoListMap <- Ref.make(Map.empty[TodoListId, TodoList])
      yield TodoListService(currentId, todoListMap)
    }
