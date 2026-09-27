"""trainer tables

Revision ID: 0001
Revises: 
Create Date: 2026-09-27 20:25:06.676733
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('ai_usage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('purpose', sa.String(length=32), nullable=False),
    sa.Column('model', sa.String(length=64), nullable=False),
    sa.Column('input_tokens', sa.Integer(), nullable=False),
    sa.Column('output_tokens', sa.Integer(), nullable=False),
    sa.Column('cache_write_tokens', sa.Integer(), nullable=False),
    sa.Column('cache_read_tokens', sa.Integer(), nullable=False),
    sa.Column('cost_usd', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_usage_created_at'), 'ai_usage', ['created_at'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('tz', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_tg_id'), 'users', ['tg_id'], unique=True)
    op.create_table('training_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('persona_key', sa.String(length=64), nullable=False),
    sa.Column('language', sa.String(length=16), nullable=False),
    sa.Column('difficulty', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('turns', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_sessions_status'), 'training_sessions', ['status'], unique=False)
    op.create_index(op.f('ix_training_sessions_user_id'), 'training_sessions', ['user_id'], unique=False)
    op.create_table('session_reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('score_needs', sa.Integer(), nullable=False),
    sa.Column('score_value', sa.Integer(), nullable=False),
    sa.Column('score_objections', sa.Integer(), nullable=False),
    sa.Column('score_close', sa.Integer(), nullable=False),
    sa.Column('overall', sa.Float(), nullable=False),
    sa.Column('ethics_violation', sa.Boolean(), nullable=False),
    sa.Column('ethics_quote', sa.Text(), nullable=False),
    sa.Column('next_step_with_date', sa.Boolean(), nullable=False),
    sa.Column('question_ratio', sa.Float(), nullable=False),
    sa.Column('avg_words', sa.Float(), nullable=False),
    sa.Column('rephrasings', sa.JSON(), nullable=False),
    sa.Column('strengths', sa.JSON(), nullable=False),
    sa.Column('summary', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_session_reviews_session_id'), 'session_reviews', ['session_id'], unique=True)
    op.create_table('training_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=16), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_messages_session_id'), 'training_messages', ['session_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_training_messages_session_id'), table_name='training_messages')
    op.drop_table('training_messages')
    op.drop_index(op.f('ix_session_reviews_session_id'), table_name='session_reviews')
    op.drop_table('session_reviews')
    op.drop_index(op.f('ix_training_sessions_user_id'), table_name='training_sessions')
    op.drop_index(op.f('ix_training_sessions_status'), table_name='training_sessions')
    op.drop_table('training_sessions')
    op.drop_index(op.f('ix_users_tg_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_ai_usage_created_at'), table_name='ai_usage')
    op.drop_table('ai_usage')
