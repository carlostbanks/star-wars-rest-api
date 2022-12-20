"""empty message

Revision ID: 45e76ad61bee
Revises: 23e9d8aadeb4
Create Date: 2022-12-20 00:10:22.963117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45e76ad61bee'
down_revision = '23e9d8aadeb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicles',
    sa.Column('pilot', sa.String(length=250), nullable=True),
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('vehicle_id')
    )
    op.create_table('characterFavorites',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'character_id')
    )
    op.create_table('planetFavorites',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.planet_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'planet_id')
    )
    op.drop_table('favorites')
    

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    

    op.create_table('favorites',
    sa.Column('date_added', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('favorite_characters', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('favorite_planets', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('favorite_vehicles', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('date_added', name='favorites_pkey'),
    sa.UniqueConstraint('user_id', name='favorites_user_id_key')
    )
    op.drop_table('planetFavorites')
    op.drop_table('characterFavorites')
    op.drop_table('vehicles')
    # ### end Alembic commands ###
