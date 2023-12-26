all: black lint

activate:
	. /home/nikota/.virtualenvs/dataversioncontrol/bin/activate

lint:
	pylint mldvc --rcfile .pylintrc

black:
	black -S -l 110 mldvc
	black -S -l 110 tests