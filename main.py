import filecmp
import subprocess
import shutil
import pathlib
import os.path

from creds import get_creds
from gdrive import find_folder_by_id, download_file

if __name__ == '__main__':
    splash = '''
 ███████╗██╗   ██╗ █████╗ ██╗  ████████╗███████╗ ██████╗██╗  ██╗
 ██╔════╝██║   ██║██╔══██╗██║  ╚══██╔══╝██╔════╝██╔════╝██║  ██║
 ███████╗██║   ██║███████║██║     ██║   █████╗  ██║     ███████║
 ╚════██║██║   ██║██╔══██║██║     ██║   ██╔══╝  ██║     ██╔══██║
 ███████║╚██████╔╝██║  ██║███████╗██║   ███████╗╚██████╗██║  ██║
 ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝©
'''

    print(splash)
    print('\n')
    print('Aguarde uns instantes')

    target = 'C:\\SES Client\\ses_client.exe'
    temp = 'c:\\users\\public\\ses_client.exe'
    old = 'c:\\program files\\ses client'
    new = 'c:\\ses client'
    desktop = f'c:\\users\\{os.getenv("USERNAME")}\\desktop'

    en = pathlib.Path('c:\\program files').exists()

    if not en:
        temp = 'c:\\usuários\\público\\ses_client.exe'
        old = 'c:\\arquivos e programas\\ses client'
        desktop = f'c:\\usuários\\{os.getenv("USERNAME")}\\desktop'

    if not pathlib.Path(new).exists():
        shutil.copytree(old, new)

    if not pathlib.Path(r'c:\ses client\update_scripts_ib').exists():
        os.mkdir(r'c:\ses client\update_scripts_ib')

    if not pathlib.Path(r'c:\ses client\update_scripts_ib\.env').exists():
        with open(r'c:\ses client\update_scripts_ib\.env', 'w') as f:
            f.writelines(
                ['# por favor nao deletar esse arquivo, pois eh configuracao de atualizacao do ses_client.exe\n',
                 r'1eUc8RqUlU4rdRd_RiTqWQEpq4v9RVdA4'])

    with open(r'c:\ses client\update_scripts_ib\.env') as f:
        env = f.readlines()

    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
    creds = get_creds(SCOPES)

    folder_dict: dict = find_folder_by_id(creds, env[1])
    ses_client_id = folder_dict['id']

    ses_client_file = download_file(creds, real_file_id=ses_client_id)

    if ses_client_file:
        with open(temp, 'wb') as f:
            f.write(ses_client_file)

        if pathlib.Path(target).exists():
            is_equal = filecmp.cmp(target, temp)
            if not is_equal:
                os.replace(temp, target)
        else:
            os.rename(temp, target)

        log_file = pathlib.Path(
            r'c:\ses client\update_scripts_ib\.log').exists()
        if log_file:
            os.remove(r'c:\ses client\update_scripts_ib\.log')
    else:
        with open(r'c:\ses client\update_scripts_ib\.log', 'w') as f:
            f.write('nao foi possivel fazer download do arquivo do drive')

    subprocess.Popen(r"c:\ses client\ses_client.exe")
