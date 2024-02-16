import string
import random


def create_code(size=6, chars=string.ascii_uppercase + string.digits):    
    return ''.join(random.choice(chars) for _ in range(size))