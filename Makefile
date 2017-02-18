# prepare environment variables
PACKAGE_NAME			:= fstree
VERSION				:= $(shell cat fstree/version.py | egrep 'version.*=' | awk '{print $NF}' | tr -d "'")
TZ				:= UTC
PYTHONPATH			:= $(shell pwd)
export TZ
export PYTHONPATH

OSNAME	:= $(shell uname)

ifeq ($(OSNAME), Linux)
OPEN	:= gnome-open
else
OPEN	:= open
endif


all: intro tests

bootstrap: remove clean deps build intro

tests: lint unit functional

deps:
	@pip install -U pip
	@pip install -r development.txt

build: clean html-docs
	python setup.py sdist
	@cd dist && tar xzf *.gz
	@ls -l dist/*

remove:
	-@pip uninstall -y fstree

clean:
	@printf "\033[1;33mcleaning garbage files\033[0m\n"
	@rm -rf '*.egg-info'
	@rm -rf 'dist'
	@find . -name '*.pyc' -exec rm -f {} \;


lint:
	@printf "\033[1;30mrunning \033[1;32mflake8\033[1;30m:\033[0m\n"
	@find fstree -name '*.py' | grep -v node | xargs flake8 --ignore=E501 --max-complexity=6
	@printf "\033[1;32mthe code looks great!\033[0m\n"

unit:
	nosetests --rednose --cover-erase tests/unit

functional:
	nosetests --with-spec --spec-color tests/functional/{node,backends,tree}

release: tests build
	# @./.release
	@rm -rf *egg-info* dist/$(PACKAGE_NAME)*.tar.gz
	@twine upload -r gabrielfalcao dist/$(PACKAGE_NAME)*.tar.gz


html-docs:
	cd docs && make linkcheck dummy html

docs: html-docs
	$(OPEN) docs/build/html/index.html
	rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress docs/build/html/ root@falcao.it:/srv/docs/fstree/


intro:
	@printf "\033[0;36mWelcome to the \033[1;36mFSTree $$(python -c 'import fstree;print fstree.version') \033[0;36mdevelopment environment!\033[0m\n"

.PHONY: all tests setup remove build lint unit functional tests setup release html-docs docs clean
