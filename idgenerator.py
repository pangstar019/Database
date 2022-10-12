
from math import floor
import random



def generatingvalues(n, type):
    values = []
    upperletters = 'ABCDEFGHIJKLMNOPQRSTUVwXYZ'
    lowerletters = 'abcdefghijklmnopqrstuvwxyz'

    for i in range(0,n):
        if type == 'digits':
            values.append(str(random.randrange(0,9)))
        elif type == 'lower':
            values.append(random.choice(lowerletters))
        elif type == 'upper':
            values.append(random.choice(upperletters))
    return values

def generate(n):

    # Generate password
    n_upper = floor(n/3)
    n_lower = floor(n/3)
    n_digits = floor(n/3) + n%3
    password = []

    upper = generatingvalues(n_upper, 'upper')
    password.extend(upper)

    lower = generatingvalues(n_lower, 'lower')
    password.extend(lower)

    digits = generatingvalues(n_digits, 'digits')
    password.extend(digits)

    random.shuffle(password)
    password = ''.join(map(str,password))

    return password
