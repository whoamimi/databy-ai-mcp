from enum import StrEnum


class BusinessDomain(StrEnum):
    CHAT_HISTORY = "Chat History"
    TRANSACTIONS = "B2C/B2B Transactions"
    LOGISTICS = "Logistic Dataset"
    TIME_SERIES = "Time Series"
    SENSORY = "Sensory Dataset"
    USER_EVENT = "User Event"


class CleanState(StrEnum):
    MESS = "mess"
    MODERATE = "moderate"
    CLEAN = "clean"
