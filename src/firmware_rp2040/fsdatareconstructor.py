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


module("tt14.py", base_path="/var/build/src/src")
module("tt24.py", base_path="/var/build/src/src")
module("tt32.py", base_path="/var/build/src/src")
module("vga2_16x16.py", base_path="/var/build/src/src")
module("vga2_16x32.py", base_path="/var/build/src/src")
module("vga2_8x8.py", base_path="/var/build/src/src")
module("vga2_bold_16x16.py", base_path="/var/build/src/src")
module("vga2_bold_16x32.py", base_path="/var/build/src/src")
