package app.domain.models

final case class TodoItemCreate(
    listId: Int,
    title: String,
    isCompleted: Boolean,
    priority: Int
)

final case class TodoItemUpdate(
    listId: Option[Int],
    title: Option[String],
    isCompleted: Option[Boolean],
    priority: Option[Int]
)

final case class TodoItem(
    id: Int,
    listId: Int,
    title: String,
    isCompleted: Boolean,
    priority: Int
)

final case class TodoList(
    id: Int,
    name: String
)
