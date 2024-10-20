from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Fetch database URL from environment variables
DB_URL = os.getenv('DB_URL', 'postgresql://postgres:password@localhost:5432/postgres')

# Add your model's MetaData object here
# for 'autogenerate' support
target_metadata = None


# Create a connection to the database
def run_migrations_offline():
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(DB_URL, poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


context.configure(
    url=DB_URL,
    target_metadata=target_metadata,
    dialect_opts={"paramstyle": "named"},
    offline=True
)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
