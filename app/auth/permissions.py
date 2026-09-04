# auth/permissions.py

from enum import Enum


class Permission(str, Enum):
    PRODUCT_READ = "product:read"
    PRODUCT_CREATE = "product:create"
    PRODUCT_UPDATE = "product:update"
    PRODUCT_DELETE = "product:delete"