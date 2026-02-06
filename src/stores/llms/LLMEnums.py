from enum import Enum

class LLMEnum(Enum):

    OPENAI="OPENAI"
    GOOGLE="GOOGLE"

class OPENAIENUMS(Enum):

    USER="user"
    ASSITANT="assitant"
    SYSTEM="system"


class GOOGLEENUMS(Enum):
    SYSTEM_INSTRUCTIONS="you are a helpful assitant who will answer the question base on the provided context in a helpful tone"
    USER="user"
    ASSITANT="assitant"
    SYSTEM="system"
    