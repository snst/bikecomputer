coverage erase
coverage run --source=. test/main.py
#coverage report --include="*/src/*"
coverage html --include="*/src/*"