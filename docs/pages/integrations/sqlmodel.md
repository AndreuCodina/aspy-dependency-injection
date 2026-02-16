# SQLModel integration

## Benefits

It's difficult to setup SQLModel for lots of reasons:

- We can set up SQLModel in different ways, and it's not always clear which one is the best for our application.
- We need to manage the lifetimes of the engine, sessionmaker and sessions ourself.
- We need to manage the disposal of the engine and sessions ourself.
- Code is bloated with context managers, and SQLModel services aren't easily shareable between the functions of our service.
- Sometimes we need to import from SQLAlchemy, sometimes from SQLModel, and it's not always clear which one to use.
- Asynchronous and synchronous services require different setups, different than the default ones.
- Services aren't easily testable.

Wirio can help with that by providing a clean integration that provides:

- Automatic registration of SQLModel services.
- Recommended configuration by default.
- No context managers.
- Consistent and recommended lifetime management out-of-the-box.

## Installation

To use the SQLModel integration, add the `sqlmodel` extra to automatically install the required compatible dependencies.

```bash
uv add wirio[sqlmodel]
```

## Asynchronous setup (recommended)

`add_sqlmodel` configures SQLModel for asynchronous workloads and registers the following services:

- `AsyncEngine` as singleton
- `async_sessionmaker[AsyncSession]` as singleton
- `AsyncSession` as scoped

We only have to provide the connection string, and Wirio will take care of the rest.

```python hl_lines="3"
services = ServiceCollection()
services.add_sqlmodel(
    connection_string="postgresql+asyncpg://<user>:<password>@<host>:<port>/<database>"
)
```

We're using the `asyncpg` driver (`uv add asyncpg`) in the connection string, but we can use any driver supported by SQLModel.

### Imports to resolve registered async services

It's important to import the correct types to resolve the registered services.

```python
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
```

Then, we can use it in the most easy way possible:

```python
class UserService:
    def __init__(self, sql_session: AsyncSession):
        self.sql_session = sql_session
```

## Synchronous setup

`add_sync_sqlmodel` configures SQLModel for synchronous workloads and registers the following services:

- `Engine` as singleton
- `sessionmaker[Session]` as singleton
- `Session` as scoped

We only have to provide the connection string, and Wirio will take care of the rest.

```python hl_lines="3"
services = ServiceCollection()
services.add_sync_sqlmodel(
    connection_string="postgresql+psycopg2://<user>:<password>@<host>:<port>/<database>"
)
```

We're using the `psycopg2` driver (`uv add psycopg2-binary`) in the connection string, but we can use any driver supported by SQLModel.

### Imports to resolve registered synchronous services

It's important to import the correct types to resolve the registered services.

```python
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
```

Then, we can use it in the most easy way possible:

```python
class UserService:
    def __init__(self, sql_session: Session):
        self.sql_session = sql_session
```
