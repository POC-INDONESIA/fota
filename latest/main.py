# POC INDONESIA untuk POC GLOBAL
# Dibuat oleh Ibnu Maksum (ibnux) <oc62nux@pocindonesia.com>
# Hak Cipta POC INDONESIA 2026
# Lintas generasi Lintas Benua
# 
# main.py - AUTO-RUN aplikasi POC INDONESIA (deploy_compiled_pocind.py)
# Dijalankan otomatis oleh QuecPython saat device boot.
#
# CATATAN .mpy: import main mencari main.mpy atau main.py di sys.path.
# File .mpy harus terlebih dahulu dimuat oleh MicroPython tanpa exec().
import sys

sys.path.insert(0, '/usr')
sys.path.insert(0, '/usr/pocind')

# LCD awal: tampilkan layar gelap sesegera mungkin
try:
    import display
    if display.init():
        try:
            import config
            _bg = config.C_BG
        except Exception:
            _bg = 0x18C3
        display.fill_screen(_bg)
except Exception as e:
    print('[BOOT] lcd awal gagal:', e)

print('[BOOT] POC INDONESIA (.mpy)')
try:
    import main
    main.run()
except Exception as e:
    print('[BOOT] GAGAL:', type(e).__name__, e)
    try:
        import usys
        _f = open('/usr/boot_err.txt', 'w')
        _f.write('BOOT ERROR\n')
        try:
            usys.print_exception(e, _f)
        except Exception:
            _f.write('{}: {}\n'.format(type(e).__name__, e))
        _f.write('--- modul ---\n')
        for _k in list(sys.modules.keys()):
            _f.write(str(_k) + '\n')
        _f.close()
    except Exception as e3:
        print('[BOOT] jejak gagal:', e3)
    try:
        import display
        import config
        display.init()
        display.fill_screen(config.C_BG)
        display.text_center(30, 'APP ERROR', config.C_ERR)
        display.text_center(50, str(e)[:25], config.C_TEXT)
        display.text_center(70, 'lihat boot_err.txt', config.C_LOG_OLD)
    except Exception as e2:
        print('[BOOT] layar error gagal:', e2)
