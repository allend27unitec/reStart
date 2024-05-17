print("Initializing package from assigment 1 Part_2...")

VERSION = '1.0'

from .message_model import Message,  MessageUpdateRequest

__all__ = ['Message', 'message_model', 'MessageUpdateRequest', 'VERSION']
