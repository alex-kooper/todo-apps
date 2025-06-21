package app

import zio._
import zio.Console._

object MyApp extends ZIOAppDefault {
  def run = printLine("The server is running...")
}
