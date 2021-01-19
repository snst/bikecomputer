d="$(dirname $(readlink -f $0))"
env /usr/bin/python3 -- "$d/emu/main.py"
