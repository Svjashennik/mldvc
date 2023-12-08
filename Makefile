all: black lint

lint:
	pylint mldvc --rcfile .pylintrc

black:
	black -S -l 110 mldvc
	black -S -l 110 tests