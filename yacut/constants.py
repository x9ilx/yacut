import string

ALLOWED_SYMBOLS_FOR_SHORT = string.ascii_letters + string.digits
SHORT_LENGTH = 6
SHORT_PATTERN = r'^[a-zA-z0-9]*$'
NUMBER_OF_SHORT_GENERATION_PASSES = 10
ORIGINAL_LINK_MAX_LENGTH = 1024
SHORT_MAX_LENGTH_FOR_USER = 16
