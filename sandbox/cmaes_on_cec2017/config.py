from cec2017.functions import *


NUM_RUNS = 51
MAX_FES = 2e5
HEADERS = ('name', 'function', 'dimenstions', 'constraints')
FUNCTIONS = [
    ('f1', f1, [2, 10, 20, 30, 50, 100], (-100, 100)),
    ('f2', f2, [2, 10, 20, 30, 50, 100], (-100, 100)),
    ('f3', f3, [2, 10, 20, 30, 50, 100], (-100, 100)),
    ('f4', f4, [2, 10, 20, 30, 50, 100], (-10, 10)),
    ('f5', f5, [2, 10, 20, 30, 50, 100], (-10, 10)),
    ('f6', f6, [2, 10, 20, 30, 50, 100], (-20, 20)),
    ('f7', f7, [2, 10, 20, 30, 50, 100], (-50, 50)),
    ('f8', f8, [2, 10, 20, 30, 50, 100], (-100, 100)),
    ('f9', f9, [2, 10, 20, 30, 50, 100], (-10, 10)),
    ('f10', f10, [2, 10, 20, 30, 50, 100], (-100, 100)),
]