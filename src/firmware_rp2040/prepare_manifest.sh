#!/bin/bash
cd "$(dirname "$0")"
#cd ./microfreezer
#python3 ./microfreezer.py -s ../ -d ../build/
for i in *.py.TEMPLATE; do
    [ -f "$i" ] || break
    
    fbname=$(basename "$i" .TEMPLATE)
    echo "$fbname"
    echo "$i"
    cp "$i" "$fbname"
    
    sed -i -e 's|_SPATH_|'$PWD'|' "$fbname"



    for j in $PWD/src/static_modules/*.py; do
    [ -f "$j" ] || break
        echo "$j"
         
        p="$(basename $j)"
        echo "$p"

   
        echo "module(\""$p\"", base_path=\""$PWD/src/static_modules\"")" >> "$fbname"
    done
done
# generate manifest file by adding all .py files in src into a new manufest file:
# module("foo.py", base_path="src/drivers")
