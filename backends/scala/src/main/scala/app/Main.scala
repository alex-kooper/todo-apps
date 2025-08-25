package app

import org.http4s.*
import org.http4s.dsl.Http4sDsl
import org.http4s.ember.server.EmberServerBuilder
import org.http4s.server.Router
import zio.*
import zio.interop.catz.*
import zio.Console.*
import com.comcast.ip4s.*
import app.restapi.TodoListApi
import app.inmemory.TodoListService
import app.domain.TodoListService

object MyApp extends ZIOAppDefault {
  type AppTask[A] = RIO[app.domain.TodoListService & Scope, A]

  val server: TaskLayer[Unit] =
    ZLayer.scoped {
      EmberServerBuilder
        .default[AppTask]
        .withHost(ipv4"0.0.0.0")
        .withPort(port"8080")
        .withHttpApp(Router("/" -> TodoListApi.routes).orNotFound)
        .build
        .toScopedZIO
        .provideSomeLayer(app.inmemory.TodoListService.live)
        .unit
    }

  override def run =
    for
      _ <- ZIO.logInfo(
        "🚀 Starting http4s server at http://localhost:8080/hello/world"
      )
      _ <- ZIO.never.provideLayer(server)
    yield ()
}
