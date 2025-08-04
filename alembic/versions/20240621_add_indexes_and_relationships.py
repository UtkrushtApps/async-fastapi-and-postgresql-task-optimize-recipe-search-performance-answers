"""
Add indexes, constraints, and optimize relationships for searchable columns
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_index('ix_recipes_category', 'recipes', ['category'])
    op.create_index('ix_ing_name', 'ingredients', ['name'])
    op.create_index('ix_recipe_name', 'recipes', ['name'])
    op.create_index('ix_recipe_ingredient_recipe_id', 'recipe_ingredient', ['recipe_id'])
    op.create_index('ix_recipe_ingredient_ingredient_id', 'recipe_ingredient', ['ingredient_id'])
    op.create_index('ix_recipes_name_category', 'recipes', ['name','category'])
    op.create_unique_constraint('uix_recipe_ingredient', 'recipe_ingredient', ['recipe_id', 'ingredient_id'])

def downgrade():
    op.drop_constraint('uix_recipe_ingredient', 'recipe_ingredient', type_='unique')
    op.drop_index('ix_recipes_name_category', table_name='recipes')
    op.drop_index('ix_recipe_ingredient_ingredient_id', table_name='recipe_ingredient')
    op.drop_index('ix_recipe_ingredient_recipe_id', table_name='recipe_ingredient')
    op.drop_index('ix_recipe_name', table_name='recipes')
    op.drop_index('ix_ing_name', table_name='ingredients')
    op.drop_index('ix_recipes_category', table_name='recipes')
