FILE_DATA = ZLIBSTREAM

def restore_filesystem(_basepath: str = "/", _override: bool = False):
    import ubinascii
    import os


    for k in FILE_DATA:

        if k in os.listdir() and not _override:
            continue
        
        print(k)
        d = FILE_DATA[k]
        ubinascii.a2b_base64(d)

        with open(_basepath + "/" + k, "w") as file:
            file.write(ubinascii.a2b_base64(d))

    # CLEANUP
    del ubinascii
    del os


module("__main.py", base_path="/var/build/src/src")
