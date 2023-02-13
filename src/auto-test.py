import random
import pexpect, os, sys
from PIL import ImageGrab

INPUT_CODE = './input'
SAVED_LOC = './output'
NUMBER_OF_TEST = 5

def ls_subfolders(rootdir):
    sub_folders_n_files = []
    for path, _, files in os.walk(rootdir):
        for name in files:
            sub_folders_n_files.append(os.path.join(path, name))
    return sorted(sub_folders_n_files)

if __name__ == '__main__':

    print(ls_subfolders(INPUT_CODE))

    for filepath in ls_subfolders(INPUT_CODE):
        _, filename = os.path.split(filepath)
        saved_loc = f'{SAVED_LOC}/{filename}'

        try:
            if not os.path.exists(saved_loc):
                os.makedirs(os.path.join(saved_loc))
                print(f'''Created folder: {saved_loc}''')
        except FileExistsError:
            pass

        for test_no in range(NUMBER_OF_TEST):
            proc = pexpect.spawn(filepath)
            while True:
                proc.expect ('.*')
                proc.sendline(f'{random.randint(6,12)}')
                if not proc.isalive():
                    print(f'---- TEST of {filename}: {test_no} ----')
                    proc.expect(pexpect.EOF)
                    print(proc.before.decode('latin-1'))
                    proc.kill(0)

                    # take screenshot
                    screenshot = ImageGrab.grab()
                    screenshot.save(f'{saved_loc}/{test_no}.png', 'PNG')
                    del screenshot
                    break

        # clear output on each file
        os.system('clear')