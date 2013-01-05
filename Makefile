.PHONY: clean pyflakes pep setup upgrade freeze updatecache
SHELL := /bin/bash

# these files should pass pyflakes
# exclude ./env/, which may contain virtualenv packages
PYFLAKES_WHITELIST=$(shell find . -name "*.py" ! -path "./build/*" \
                    ! -path "./env/*" ! -path "./.tox/*")

# Local development management
clean:
	find -L . -name "*~" -exec rm -fr {} \;
	find -L . -name "*.pyc" -exec rm -fr {} \;

pyflakes:
	pyflakes ${PYFLAKES_WHITELIST}

pep:
	pep8 website

setup: requirements.txt
	virtualenv env --python=python2.7
	./env/bin/pip install -r requirements.txt

upgrade:
	./env/bin/pip freeze --local | grep -v '^\-e' | cut -d = -f 1 | xargs pip install -U

freeze:
	./env/bin/pip freeze --local > requirements.txt

updatecache:
	./env/bin/python ./manager.py updatecache -c prod
