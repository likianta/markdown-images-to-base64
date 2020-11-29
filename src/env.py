from platform import system

if system() == 'Windows':
    SYSTEM = 0
else:
    SYSTEM = 1
