import os
import shutil


def prepare_public():
    current_dir = os.getcwd()
    public_dir = os.path.join(current_dir, 'public')

    if not os.path.exists(public_dir):
        os.mkdir(public_dir)

    for filename in os.listdir(public_dir):
        file_path = os.path.join(public_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    static_dir = os.path.join(current_dir, 'static')
    copy_static(static_dir, public_dir)


def copy_static(src, dest):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            if not os.path.exists(d):
                os.mkdir(d)
            copy_static(s, d)
        else:
            shutil.copy2(s, d)


def main():
    prepare_public()


main()
