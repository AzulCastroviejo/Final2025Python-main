"""
Centralized Enums Module

Contains all shared enumeration types used across models and schemas.
"""
from enum import Enum


class DeliveryMethod(str, Enum):
    """Order delivery method options"""
    DRIVE_THRU = "drive_thru"
    ON_HAND = "on_hand"
    HOME_DELIVERY = "home_delivery"


class Status(str, Enum):
    """Order status options"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    CANCELED = "canceled"


class PaymentType(str, Enum):
    """Bill payment type options"""
    CASH = "cash"
    CARD = "card"
    DEBIT = "debit"
    CREDIT = "credit"
    BANK_TRANSFER = "bank_transfer"
