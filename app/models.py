from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Table, Index, Text, UniqueConstraint
)

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base(cls=AsyncAttrs)

# Association table for many-to-many relationship between Recipe and Ingredient
recipe_ingredient_table = Table(
    'recipe_ingredient',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id', ondelete="CASCADE"), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id', ondelete="CASCADE"), primary_key=True),
    Index('ix_recipe_ingredient_recipe_id', 'recipe_id'),
    Index('ix_recipe_ingredient_ingredient_id', 'ingredient_id'),
    UniqueConstraint('recipe_id', 'ingredient_id', name='uix_recipe_ingredient'),
)

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    instructions = Column(Text, nullable=True)

    # relationships
    ingredients = relationship('Ingredient', secondary=recipe_ingredient_table, back_populates='recipes', lazy='selectin')

    __table_args__ = (
        Index('ix_recipes_category', 'category'),
        Index('ix_recipes_name_category', 'name', 'category'),
    )

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True, unique=True)

    # relationships
    recipes = relationship('Recipe', secondary=recipe_ingredient_table, back_populates='ingredients', lazy='selectin')

    __table_args__ = (
        Index('ix_ingredients_name', 'name'),
    )
