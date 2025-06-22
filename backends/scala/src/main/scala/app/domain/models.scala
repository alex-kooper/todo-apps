package app.domain.models

import neotype.*
import neotype.common.NonEmptyString

type TodoItemId = TodoItemId.Type
object TodoItemId extends Newtype[Int]

type TodoListId = TodoListId.Type
object TodoListId extends Newtype[Int]

type TodoItemPriority = TodoItemPriority.Type
object TodoItemPriority extends Newtype[Int]

final case class TodoItemCreate(
    listId: TodoListId,
    title: NonEmptyString,
    isCompleted: Boolean,
    priority: TodoItemPriority
)

final case class TodoItemUpdate(
    listId: Option[TodoListId],
    title: Option[NonEmptyString],
    isCompleted: Option[Boolean],
    priority: Option[TodoItemPriority]
)

final case class TodoItem(
    id: TodoItemId,
    listId: TodoListId,
    title: NonEmptyString,
    isCompleted: Boolean,
    priority: TodoItemPriority
)

final case class TodoList(
    id: TodoListId,
    name: NonEmptyString
)
