clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:    
	sudo apt install python3-pip -y
	pip3 install -e .
	pip3 install -r stomble_assignment/requirements.txt

tests:
	pytest

run:
	python3 stomble_assignment/src/api.py

