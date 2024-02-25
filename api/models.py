from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean,
    TIMESTAMP,
    DATE,
    text,
    DATETIME,
    UniqueConstraint,
    DECIMAL,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    phone = Column(String(25), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)
    hashed_password = Column(String(200), nullable=False)
    verified = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("current_timestamp()"),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("current_timestamp()"),
        onupdate=datetime.now,
    )
    user_role = relationship("UserRole", back_populates="users")

    def __repr__(self):
        return f"<Users {self.id}>"


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(
        String(45),
        unique=True,
    )
    description = Column(
        Text,
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    user_role = relationship("UserRole", back_populates="role")
    role_permission = relationship("RolePermission", back_populates="role")


    def __repr__(self):
        return f"<Role {self.role}"


class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    __table_args__ = (UniqueConstraint(user_id, role_id, name="user_id_role_id"),)
    users = relationship("Users", back_populates="user_role")
    role = relationship("Role", back_populates="user_role")

    def __repr__(self):
        return f"<UserRole {self.user_role}"


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    permission = Column(
        String(45),
        unique=True,
        nullable=False,
    )
    permission_code = Column(
        String(45),
        unique=True,
        nullable=False,
    )
    system_code = Column(
        String(45),
        unique=False,
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    role_permission = relationship("RolePermission", back_populates="permission")

    def __repr__(self):
        return f"<Permission {self.permission}"


class RolePermission(Base):
    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permission.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="role_id_permission_id"),
    )
    role = relationship("Role", back_populates="role_permission")
    permission = relationship("Permission", back_populates="role_permission")

    def __repr__(self):
        return f"<RolePermission {self.role_permission}"


class District(Base):
    __tablename__ = "District"
    id = Column(Integer, primary_key=True, index=True)
    district = Column(String(100), unique=True, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("current_timestamp()"),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("current_timestamp()"),
        onupdate=datetime.now,
    )

    def __repr__(self):
        return f"<District {self.id}>"
    
class Facility(Base):
    __tablename__ = "facility"
    id = Column(Integer, primary_key=True, index=True)
    facility = Column(String(100), unique=True, index=True)
    district_id = Column(Integer, ForeignKey("district.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("current_timestamp()"),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("current_timestamp()"),
        onupdate=datetime.now,
    )

    def __repr__(self):
        return f"<facility {self.id}>"
    
class Participant(Base):
    __tablename__ = "participant"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100), unique=True, index=True)
    short_code = Column(String(5), unique=True, index=True)
    phone_code = Column(String(5), unique=True, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("current_timestamp()"),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("current_timestamp()"),
        onupdate=datetime.now,
    )

    def __repr__(self):
        return f"<participant {self.id}>"