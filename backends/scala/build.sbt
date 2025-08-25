val scala3Version = "3.7.1"
val http4sVersion = "0.23.30"

lazy val root = project
  .in(file("."))
  .settings(
    name := "scala",
    version := "0.1.0-SNAPSHOT",
    scalaVersion := scala3Version,
    libraryDependencies ++= Seq(
      "org.scalameta" %% "munit" % "1.0.0" % Test,
      "dev.zio" %% "zio" % "2.1.19",
      "io.github.kitlangton" %% "neotype" % "0.3.23",
      "org.http4s" %% "http4s-ember-client" % http4sVersion,
      "org.http4s" %% "http4s-ember-server" % http4sVersion,
      "org.http4s" %% "http4s-dsl" % http4sVersion,
      "org.http4s" %% "http4s-circe" % http4sVersion,
      "io.circe" %% "circe-generic" % "0.14.14",
      "dev.zio" %% "zio-interop-cats" % "23.1.0.5"
    )
  )
