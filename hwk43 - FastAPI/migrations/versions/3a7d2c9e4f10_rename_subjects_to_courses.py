"""rename subjects to courses, enrolled_at to joined_at

Revision ID: 3a7d2c9e4f10
Revises: 90be7827e7f6
Create Date: 2026-09-24 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a7d2c9e4f10'
down_revision: Union[str, Sequence[str], None] = '90be7827e7f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Renames keep existing rows instead of dropping and recreating the tables
    op.rename_table('subjects', 'courses')
    op.rename_table('student_subjects', 'student_courses')
    op.alter_column('student_courses', 'subject_id', new_column_name='course_id')
    # joined_at is now filled in by the model's default, not by the database
    op.alter_column('student_courses', 'enrolled_at', new_column_name='joined_at', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('student_courses', 'joined_at', new_column_name='enrolled_at', server_default=sa.text('now()'))
    op.alter_column('student_courses', 'course_id', new_column_name='subject_id')
    op.rename_table('student_courses', 'student_subjects')
    op.rename_table('courses', 'subjects')
