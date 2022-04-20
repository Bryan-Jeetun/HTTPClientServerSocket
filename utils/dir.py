import os


def makedirs(name, mode=0o777, exist_ok=False):
    head, tail = os.path.split(name)
    if not tail:
        head, tail = os.path.split(head)
    if head and tail and not os.path.exists(head):
        try:
            makedirs(head, exist_ok=exist_ok)
        except FileExistsError:
            pass
        cdir = os.curdir
        if isinstance(tail, bytes):
            cdir = bytes(os.curdir, 'ASCII')
        if tail == cdir:
            return
    try:
        if '.' in name:
            print("Skipping " + name + " cuz it's a file extension and not folder")
        else:
            os.mkdir(name, mode)
    except OSError:
        if not exist_ok or not os.path.isdir(name):
            raise