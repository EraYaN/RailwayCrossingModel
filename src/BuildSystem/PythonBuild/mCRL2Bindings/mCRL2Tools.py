import os

def findInstallPath():
    if os.name == 'nt':
        import winreg
        REG_PATH = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\mCRL2"
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_READ)
       
            value, regtype = winreg.QueryValueEx(registry_key, 'DisplayIcon')
        except EnvironmentError:
            return None

        return os.path.join(value,'bin')
    elif os.name == 'posix':
        return ''
    else:
        return ''