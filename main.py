import pathlib
from module.finance import Finance 

if __name__ == '__main__':
    file = pathlib.Path('input', 'ОАД1.xlsx')
    calc = Finance(file)
    calc.read()


