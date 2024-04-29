
import sys
import os
import base64
import json
datfolder = str(sys.argv[1])
pyfile_src = str(sys.argv[2])
pyfile_dest = str(sys.argv[3])
print(datfolder)
print(pyfile_src)
print(pyfile_dest)

print("-----------")


ret_dict: dict = {}
# READ TARFILE
for filename in os.listdir(datfolder):
    file_name = os.path.join(datfolder, filename)

    # checking if it is a file
    if not os.path.isfile(file_name) or filename.startswith("."):
        continue

    print(file_name)
    pyfile_content = ""
    with open(file_name, mode="rb") as f:
        pyfile_content = f.read()
        #print(pyfile_content)
        ret_dict[filename] = base64.b64encode(pyfile_content).decode('utf-8')



with open(pyfile_src, mode="r") as f:
        p_content = f.read()

p_content =p_content.replace("ZLIBSTREAM",json.dumps(ret_dict))

with open(pyfile_dest, mode='w') as f:
    f.write(p_content)