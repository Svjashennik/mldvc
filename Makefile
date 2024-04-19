all: black lint

activate:
	source /home/nikota/mldvc/.env/bin/activate

lint:
	pylint mldvc --rcfile .pylintrc

black:
	black -S -l 110 mldvc
	black -S -l 110 tests

test:
	python -m unittest discover