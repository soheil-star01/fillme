"""
This module contains all database models for tables.
"""

import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Enum, BINARY, Integer, BigInteger
from sqlalchemy.orm import relationship

from .base import Base
from .contact_info_model import Email

# mariadb doesn't support UUID built-in -> Integer is used


# defining Enum for user type
enum_user_type = Enum(
    'ADMIN',
    'CUSTOMER',
    'EMPLOYEE'
)

# defining Enum for color theme in UserPreferences
enum_color_theme = Enum(
    'SYSTEM',
    'LIGHT',
    'DARK'
)


class User(Base):
    """
    User table
    """

    __tablename__ = 'user'

    id = Column(
        Integer,
        primary_key=True
    )
    uuid = Column(
        BINARY(16),
        unique=True
    )
    zitadel_id = Column(
        BigInteger,
        unique=True
    )
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    username = Column(
        String(50),
        unique=True
    )
    email = Column(
        Integer,
        ForeignKey('email.id')
    )
    session_token = Column(String(50))
    category = Column(enum_user_type)
    contact_id = Column(Integer)
    employee_id = Column(Integer)
    wawi_id = Column(Integer)

    user_role_relationship = relationship(
        'UserRoles',
        back_populates='user_relationship'
    )  # user <-> user_role

    user_preferences_relationship = relationship(
        'UserPreferences',
        back_populates='user_relationship'
    )  # user <-> user_preferences

    email_relationship = relationship(
        'Email',
        back_populates='user_relationship'
    )  # user <-> contact_info.email


    def __repr__(self) -> str:
        return f'<User id={self.id} UUID={self.uuid}>'


class UserRoles(Base):
    """
    UserRoles table
    """

    __tablename__ = 'user_roles'

    id = Column(
        Integer,
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey('user.id')
    )
    role_id = Column(
        Integer,
        ForeignKey('role.id')
    )

    user_relationship = relationship(
        'User',
        back_populates='user_role_relationship'
    )  # user <-> user_role
    role_relationship = relationship(
        'Role',
        back_populates='user_role_relationship'
    )  # user <-> role

    def __init__(self):
        self.id = uuid.uuid4().bytes


class Role(Base):
    """
    Role table
    """

    __tablename__ = 'role'

    id = Column(
        Integer,
        primary_key=True
    )
    app_id = Column(
        Integer,
        ForeignKey('app.id')
    )
    name = Column(String(50))
    user_category = Column(enum_user_type)

    user_role_relationship = relationship(
        'UserRoles',
        back_populates='role_relationship'
    )  # user <-> role
    role_permissions_relationship = relationship(
        'RolePermission',
        back_populates='role_relationship'
    )  # role <-> role_permissions
    app_relationship = relationship(
        'App',
        back_populates='role_relationship'
    )  # role <-> role_permissions


class RolePermission(Base):
    """
    Role Permission table
    """

    __tablename__ = 'role_permission'

    id = Column(
        Integer,
        primary_key=True
    )
    role_id = Column(
        Integer,
        ForeignKey('role.id')
    )
    permissions_id = Column(
        Integer,
        ForeignKey('permission.id')
    )

    role_relationship = relationship(
        'Role',
        back_populates='role_permissions_relationship'
    )  # role_permission <-> role
    permission_relationship = relationship(
        'Permission',
        back_populates='role_permissions_relationship'
    )  # role_permission <-> permission


class Permission(Base):
    """
    Permission table
    """

    __tablename__ = 'permission'

    id = Column(
        Integer,
        primary_key=True
    )
    app_id = Column(
        Integer,
        ForeignKey('app.id'),
        nullable=False
    )
    name = Column(
        String(50),
        nullable=False,
        unique=True
    )

    app_relationship = relationship(
        'App',
        back_populates='permission_relationship'
    )  # app <-> permission
    role_permissions_relationship = relationship(
        'RolePermission',
        back_populates='permission_relationship'
    )  # role_permission <-> permission


class App(Base):
    """
    App table
    """

    __tablename__ = 'app'

    id = Column(
        Integer,
        primary_key=True
    )
    uuid = Column(BINARY(16))
    name = Column(
        String(50),
        nullable=False,
        unique=True
    )
    user_category = Column(
        enum_user_type,
        nullable=False
    )

    role_relationship = relationship(
        'Role',
        back_populates='app_relationship'
    )  # app <-> role
    permission_relationship = relationship(
        'Permission',
        back_populates='app_relationship'
    )  # app <-> permission


class UserPreferences(Base):
    """
    User preferences table
    """

    __tablename__ = 'user_preferences'

    id = Column(
        Integer,
        primary_key=True
    )
    user_id = Column(
        ForeignKey('user.id'),
        nullable=False
    )

    color_theme = Column(
        enum_color_theme,
        default='SYSTEM',
        nullable=False
    )

    user_relationship = relationship(
        'User',
        back_populates='user_preferences_relationship'
    )  # User <-> user_preferences
