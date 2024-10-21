"""create classes table

Revision ID: 2a5c9da3d7ca
Revises:
Create Date: 2024-09-14 11:26:33.849246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.type_api import UserDefinedType


# Define the custom Vector type here or import it if defined elsewhere
class Vector(UserDefinedType):
    def get_col_spec(self):
        return "VECTOR(2048)"  # Specify the dimension of your vector

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None
            return value

        return process


# revision identifiers, used by Alembic.
revision: str = '2a5c9da3d7ca'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Ensure the extension for UUID generation is enabled
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"vector\"")

    # Create the classes table with a UUID primary key
    op.create_table(
        'class',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('date', sa.String(length=50), nullable=False),
        sa.Column('classroom', sa.String(length=255), nullable=False),
        sa.Column('audio', sa.Text, nullable=True),
        sa.Column('status', sa.Enum('failed', 'running', 'completed', name='class_status'), nullable=False)
    )

    op.create_table(
        'processed_class',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('class_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('class.id', ondelete="CASCADE"),
                  nullable=False),
        sa.Column('audio_text', sa.LargeBinary, nullable=True),
        sa.Column('summary_text', sa.Text, nullable=True),
        sa.Column('embeddings', Vector(), nullable=True)
    )


def downgrade():
    # Drop the table and extension
    op.drop_table('class')
    op.drop_table('processed_class')
    op.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\"")
    op.execute("DROP EXTENSION IF EXISTS \"vector\"")
