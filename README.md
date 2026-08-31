# Backend Armchair AI

## Migraciones: Alembic vs Laravel

Esta tabla sirve como referencia rápida para entender los comandos de migraciones en nuestro stack de Python (usando Alembic) si vienes de un entorno de Laravel.

| Concepto / Acción | En Laravel | En Python (Alembic) |
| :--- | :--- | :--- |
| **Tabla de control** | Laravel crea una tabla llamada `migrations` para saber cuáles ya ejecutó. | Alembic crea una tabla llamada `alembic_version` para exactamente lo mismo. |
| **Crear una migración vacía** | `php artisan make:migration create_orders_table` | `alembic revision -m "create_orders_table"` |
| **Generar migración de forma automática** | (No existe de forma nativa) | `alembic revision --autogenerate -m "nombre"` |
| **Aplicar las migraciones** | `php artisan migrate` | `alembic upgrade head` (o `make migrate` en nuestra config) |
| **Revertir la última migración** | `php artisan migrate:rollback` | `alembic downgrade -1` |
| **Resetear todo** | `php artisan migrate:fresh` | `alembic downgrade base` |


## Truncate tables

```sql
TRUNCATE TABLE orders RESTART IDENTITY CASCADE;
```


## Monitor Redis

```sh
docker exec -it aa-redis redis-cli SUBSCRIBE MessageCreated
```