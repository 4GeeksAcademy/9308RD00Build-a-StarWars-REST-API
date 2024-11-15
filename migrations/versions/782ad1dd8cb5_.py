"""empty message

Revision ID: 782ad1dd8cb5
Revises: a5cffa318ac2
Create Date: 2024-11-15 20:16:20.832347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '782ad1dd8cb5'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('gender', sa.String(length=250), nullable=False),
    sa.Column('eye_color', sa.String(length=250), nullable=False),
    sa.Column('hair_color', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('terrain', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('favorite_planet', sa.String(length=250), nullable=True),
    sa.Column('favorite_people', sa.String(length=250), nullable=True),
    sa.Column('user_to_fav', sa.Integer(), nullable=True),
    sa.Column('user_to_fav_planet', sa.Integer(), nullable=True),
    sa.Column('user_to_fav_char', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_to_fav'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_to_fav_char'], ['character.id'], ),
    sa.ForeignKeyConstraint(['user_to_fav_planet'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstname', sa.String(length=250), nullable=False))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.drop_constraint('user_email_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint('user_email_key', ['email'])
        batch_op.alter_column('is_active',
               existing_type=sa.String(length=250),
               type_=sa.BOOLEAN(),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
        batch_op.drop_column('firstname')

    op.drop_table('favorite')
    op.drop_table('planet')
    op.drop_table('character')
    # ### end Alembic commands ###