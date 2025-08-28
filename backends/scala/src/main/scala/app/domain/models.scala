package app.domain.models

import neotype.*
import neotype.common.NonEmptyString
import neotype.interop.circe.given

import io.circe.Codec
import io.circe.{Encoder, Decoder}
import io.circe.generic.semiauto.*

type TodoItemId = TodoItemId.Type
object TodoItemId extends Newtype[Int]:
  given Ordering[TodoItemId] = Ordering.by(_.unwrap)

type TodoListId = TodoListId.Type
object TodoListId extends Newtype[Int]:
  given Ordering[TodoListId] = Ordering.by(_.unwrap)

type TodoItemPriority = TodoItemPriority.Type
object TodoItemPriority extends Newtype[Int]:
  given Ordering[TodoItemPriority] = Ordering.by(_.unwrap)

final case class TodoItemCreate(
    listId: TodoListId,
    title: NonEmptyString,
    isCompleted: Boolean,
    priority: TodoItemPriority
) derives Codec

final case class TodoItemUpdate(
    listId: Option[TodoListId],
    title: Option[NonEmptyString],
    isCompleted: Option[Boolean],
    priority: Option[TodoItemPriority]
) derives Codec

final case class TodoItem(
    id: TodoItemId,
    listId: TodoListId,
    title: NonEmptyString,
    isCompleted: Boolean,
    priority: TodoItemPriority
) derives Codec

final case class TodoList(
    id: TodoListId,
    name: NonEmptyString
) derives Codec

final case class TodoListUpdate(
    name: NonEmptyString
) derives Codec
