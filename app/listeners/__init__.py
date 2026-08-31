def setup_listeners() -> None:
    from app.listeners import redis_listener  # noqa: F401
    from app.listeners import create_plan_listener  # noqa: F401