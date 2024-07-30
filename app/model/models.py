from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship
)

from datetime import datetime
from app.config.db import Base

from .enums import BoostType, Days


class Player(Base):
    name: Mapped[str]
    player_point_id: Mapped[UUID] = mapped_column(ForeignKey('playerpoint.id'))
    player_point: Mapped['PlayerPoint'] = relationship(
        foreign_keys=[player_point_id])


class Point(Base):
    quantity: Mapped[int]
    days: Mapped[Days]


class Boost(Base):
    type: Mapped[BoostType]
    duration: Mapped[datetime]
    level_reward_id: Mapped[UUID] = mapped_column(ForeignKey('levelreward.id'), nullable=True)
    level_reward: Mapped['LevelReward'] = relationship('LevelReward', back_populates='boosts', foreign_keys=[
                                                       level_reward_id], remote_side='LevelReward.id')


class Prize(Base):
    title: Mapped[str]
    level_reward_id: Mapped[UUID] = mapped_column(ForeignKey('levelreward.id'), nullable=True)
    level_reward: Mapped['LevelReward'] = relationship('LevelReward', back_populates='prizes', foreign_keys=[
                                                       level_reward_id], remote_side='LevelReward.id')


class Level(Base):
    title: Mapped[str]
    order: Mapped[int] = mapped_column(default=0)


class LevelReward(Base):
    level_id: Mapped[UUID] = mapped_column(ForeignKey('level.id'), index=True)

    level: Mapped['Level'] = relationship('Level', foreign_keys=level_id)
    prizes: Mapped[list['Prize']] = relationship(
        'Prize', back_populates='level_reward', foreign_keys='Prize.level_reward_id', cascade="all, delete-orphan")
    boosts: Mapped[list['Boost']] = relationship(
        'Boost', back_populates='level_reward', foreign_keys='Boost.level_reward_id', cascade="all, delete-orphan")


class PlayerLevel(Base):
    player_id: Mapped[UUID] = mapped_column(
        ForeignKey('player.id'), index=True)
    level_reward_id: Mapped[UUID] = mapped_column(ForeignKey('levelreward.id'))
    completed_at: Mapped[datetime] = mapped_column(
        nullable=True, type_=TIMESTAMP(timezone=True))
    is_completed: Mapped[bool] = mapped_column(default=False)
    score: Mapped[int] = mapped_column(default=0)

    level_reward: Mapped['LevelReward'] = relationship(
        foreign_keys=[level_reward_id])
    player: Mapped['Player'] = relationship(foreign_keys=[player_id])


class PlayerPoint(Base):
    last_entry_date: Mapped[datetime]
    point_id: Mapped[UUID]
    sum: Mapped[int]
