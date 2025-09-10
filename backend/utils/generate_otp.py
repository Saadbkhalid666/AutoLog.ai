from random import random
from math import floor
def generate_otp():
    return str(floor(100000 + random() * 900000))