package app.restapi

import org.http4s.*
import org.http4s.dsl.Http4sDsl
import org.http4s.ember.server.EmberServerBuilder
import org.http4s.server.Router
import zio.*
import zio.interop.catz.*

import app.domain.models.*
import app.domain.TodoService

import org.http4s.circe.CirceEntityCodec.circeEntityEncoder
import org.http4s.circe.CirceEntityCodec.circeEntityDecoder
import org.http4s.circe.CirceEntityDecoder.circeEntityDecoder
import scala.util.Try
import app.domain.TodoListNotFoundError

object TodoApi:
  type AppTask[A] = RIO[TodoService & Scope, A]

  object TodoListIdPath:
    def unapply(str: String): Option[TodoListId] =
      str.toIntOption.map(id => TodoListId(id))

  def routes: HttpRoutes[AppTask] =
    val dsl = new Http4sDsl[AppTask] {}
    import dsl.*

    HttpRoutes.of[AppTask]:
      case GET -> Root =>
        Ok:
          TodoService.lists

      case GET -> Root / TodoListIdPath(id) =>
        TodoService
          .listById(id)
          .foldZIO(
            { case TodoListNotFoundError(id) =>
              NotFound(s"Todo list with ID $id not found")
            },
            list => Ok(list)
          )

      case req @ POST -> Root =>
        Created:
          req
            .as[TodoListUpdate]
            .flatMap: todoList =>
              TodoService.newList(todoList.name)

      case DELETE -> Root / TodoListIdPath(id) =>
        TodoService
          .deleteList(id)
          .foldZIO(
            { case TodoListNotFoundError(id) =>
              NotFound(s"Todo list with ID $id not found")
            },
            _ => NoContent()
          )

      case req @ PUT -> Root / TodoListIdPath(id) =>
        req
          .as[TodoListUpdate]
          .flatMap: todoList =>
            TodoService
              .updateList(id, todoList.name)
              .foldZIO(
                { case TodoListNotFoundError(id) =>
                  NotFound(s"Todo list with ID $id not found")
                },
                updatedList => Ok(updatedList)
              )
