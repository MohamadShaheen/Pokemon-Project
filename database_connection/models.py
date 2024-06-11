from sqlalchemy.orm import relationship
from database_connection.database import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey


class Pokemon(Base):
    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    height = Column(Integer)
    weight = Column(Integer)
    trainer = relationship('TrainerPokemon', back_populates='pokemon')
    type = relationship('TypePokemon', back_populates='pokemon')


class Trainer(Base):
    __tablename__ = 'trainers'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    town = Column(String(50))
    pokemon = relationship('TrainerPokemon', back_populates='trainer')


class TrainerPokemon(Base):
    __tablename__ = 'trainer_pokemon'

    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('trainers.id'))
    pokemon_id = Column(Integer, ForeignKey('pokemons.id'))
    trainer = relationship('Trainer', back_populates='pokemon')
    pokemon = relationship('Pokemon', back_populates='trainer')


class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    pokemon = relationship('TypePokemon', back_populates='type')


class TypePokemon(Base):
    __tablename__ = 'type_pokemon'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('types.id'))
    pokemon_id = Column(Integer, ForeignKey('pokemons.id'))
    type = relationship('Type', back_populates='pokemon')
    pokemon = relationship('Pokemon', back_populates='type')


Base.metadata.create_all(engine)

