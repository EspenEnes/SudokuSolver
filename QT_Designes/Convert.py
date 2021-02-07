import os

for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".ui"):
            new = file[0:-2] + "py"
            os.system(f'cmd /c "pyuic5 {file} -o {new} "')
            