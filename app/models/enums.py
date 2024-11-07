import enum


class RoleType(enum.Enum):
    customer = "customer"
    admin = "admin"


class State(enum.Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"

