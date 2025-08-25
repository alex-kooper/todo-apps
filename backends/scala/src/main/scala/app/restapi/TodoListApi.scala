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

object TodoListApi:
  type AppTask[A] = RIO[TodoListService & Scope, A]

  def routes: HttpRoutes[AppTask] =
    val dsl = new Http4sDsl[AppTask] {}
    import dsl.*

    HttpRoutes.of[AppTask]:
      case GET -> Root =>
        Ok:
          TodoListService.lists

      case req @ POST -> Root =>
        Created:
          req
            .as[TodoListUpdate]
            .flatMap: todoList =>
              TodoListService.newList(todoList.name)
