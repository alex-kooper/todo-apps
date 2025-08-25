package app.restapi

import org.http4s.*
import org.http4s.dsl.Http4sDsl
import org.http4s.ember.server.EmberServerBuilder
import org.http4s.server.Router
import zio.*
import zio.interop.catz.*

import app.domain.models.*
import app.domain.TodoListService

object TodoListApi:
  type AppTask[A] = RIO[Scope, A]

  def routes: HttpRoutes[AppTask] =
    val dsl = new Http4sDsl[AppTask] {}
    import dsl.*

    HttpRoutes.of[AppTask]:
      case GET -> Root / "hello" / name =>
        Ok(s"Hello, $name!")
