import math
def generate_otp ():
    return str(math.floor(100000 + math.random() * 900000))