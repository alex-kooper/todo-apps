package app.restapi

import org.http4s.*
import org.http4s.dsl.Http4sDsl
import org.http4s.ember.server.EmberServerBuilder
import org.http4s.server.Router
import zio.*
import zio.interop.catz.*

import app.domain.models.*
import app.domain.TodoListService

import org.http4s.circe.CirceEntityCodec.circeEntityEncoder
import org.http4s.circe.CirceEntityCodec.circeEntityDecoder
import org.http4s.circe.CirceEntityDecoder.circeEntityDecoder
import scala.util.Try
import app.domain.TodoListNotFoundError

object TodoListApi:
  type AppTask[A] = RIO[TodoListService & Scope, A]

  object TodoListIdPath:
    def unapply(str: String): Option[TodoListId] =
      str.toIntOption.map(id => TodoListId(id))

  def routes: HttpRoutes[AppTask] =
    val dsl = new Http4sDsl[AppTask] {}
    import dsl.*

    HttpRoutes.of[AppTask]:
      case GET -> Root =>
        Ok:
          TodoListService.lists

      case GET -> Root / TodoListIdPath(id) =>
        TodoListService
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
              TodoListService.newList(todoList.name)

      case DELETE -> Root / TodoListIdPath(id) =>
        TodoListService
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
            TodoListService
              .updateList(id, todoList.name)
              .foldZIO(
                { case TodoListNotFoundError(id) =>
                  NotFound(s"Todo list with ID $id not found")
                },
                updatedList => Ok(updatedList)
              )
