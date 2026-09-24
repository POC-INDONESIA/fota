import sys
sys.path.insert(0, '/usr/pocind')
try:
    exec(open('/usr/pocind/main.py').read())
except Exception as e:
    try:
        import usys, machine
        usys.print_exception(e)
    except:
        pass
    try:
        import machine.LCD as LCD
        lcd = LCD.lcd()
        lcd.lcd_clear(0)
        lcd.lcd_display_on()
    except:
        pass
