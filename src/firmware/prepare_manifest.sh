#!/bin/bash
cd "$(dirname "$0")"

# generate manifest file by adding all modules .py files in src/static_modules into a new manifest file
# also: prelace _SPATH_ with the current abs paths of the file in order to make them searchable by micropython build script
for i in manifest_*.py.TEMPLATE; do
    [ -f "$i" ] || break
    
    fbname=$(basename "$i" .TEMPLATE)
    echo "$fbname"
    echo "$i"
    cp "$i" "$fbname"
    
    sed -i -e 's|_SPATH_|'$PWD'|' "$fbname"


    echo -e "\n\n" >> "$fbname"
    for j in $PWD/src/static_modules/*.py; do
    [ -f "$j" ] || break
        echo "$j"
         
        p="$(basename $j)"
        echo "$p"
        # ADD CUSTOM PYTHON MODULES FROM static_modules FOLDER
        # module("foo.py", base_path="src/drivers")
        echo "module(\""$p\"", base_path=\""$PWD/src/static_modules\"")" >> "$fbname"
    done
done

