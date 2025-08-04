from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, and_
from app.models import Recipe, Ingredient, recipe_ingredient_table
from app.db import get_db
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

# --- Efficient Recipe Search Implementation ---

async def search_recipes_by_ingredient_name(ingredient_name: str, db: AsyncSession) -> List[Recipe]:
    # Use an efficient join and index
    stmt = (
        select(Recipe)
        .join(recipe_ingredient_table)
        .join(Ingredient)
        .options(selectinload(Recipe.ingredients))
        .where(func.lower(Ingredient.name) == ingredient_name.lower())
    )
    result = await db.execute(stmt)
    return result.scalars().unique().all()

async def filter_recipes_by_category(category: str, db: AsyncSession) -> List[Recipe]:
    # Category is indexed
    stmt = (
        select(Recipe)
        .options(selectinload(Recipe.ingredients))
        .where(func.lower(Recipe.category) == category.lower())
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def search_recipes(
    ingredient_names: Optional[List[str]] = None,
    category: Optional[str] = None,
    db: AsyncSession = None
) -> List[Recipe]:
    """
    Single efficient query to filter by multiple ingredients and (optionally) category.
    Returns recipes that have ALL the specified ingredient_names.
    """
    stmt = select(Recipe).options(selectinload(Recipe.ingredients))
    filters = []

    if category:
        filters.append(func.lower(Recipe.category) == category.lower())

    if ingredient_names:
        lowered = [name.lower().strip() for name in ingredient_names]
        stmt = stmt.join(recipe_ingredient_table).join(Ingredient)
        filters.append(func.lower(Ingredient.name).in_(lowered))
        # For ALL ingredients, group and count
        stmt = stmt.group_by(Recipe.id)
        stmt = stmt.having(func.count(func.distinct(Ingredient.name)) == len(lowered))

    if filters:
        stmt = stmt.where(and_(*filters))

    result = await db.execute(stmt)
    return result.scalars().unique().all()
