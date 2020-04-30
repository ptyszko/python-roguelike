# WALL = '#'


C_FLOOR = P_FLOOR = '.'
D_STAIRS = U_STAIRS = '>'
<<<<<<< HEAD

'''C_FLOOR = 'c'
P_FLOOR = 'f'
'''
BARS = 'b'
'''D_STAIRS = 'd'
U_STAIRS = 'u'
'''
=======
BARS = 'b'
>>>>>>> small_changes
WALL = 'W'
STONE = 'S'

STARTPOINT = 'P'
FLOOR = {P_FLOOR, C_FLOOR, STARTPOINT}
STAIRS = {D_STAIRS, U_STAIRS}
TRAVERSABLE = STAIRS | FLOOR

"""
c - podłoga korytarza
W - ściana
f - podłoga celi
b - krata
d - schody dół
u - schody góra
S - kamień
P - początek
"""
