from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    SALES = "sales"
    PURCHASE = "purchase"
    CUSTOMER = "customer"
    VENDOR = "vendor"
