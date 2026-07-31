def setup_listeners() -> None:
    from app.listeners import redis_listener  # noqa: F401
    from app.listeners import message_created_listener  # noqa: F401

