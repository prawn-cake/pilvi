ENV=$(CURDIR)/.env
BIN=$(ENV)/bin
PYTHON=$(BIN)/python
PYVERSION=$(shell $(PYTHON) -c "import sys; print('python{}.{}'.format(sys.version_info.major, sys.version_info.minor))")
MANAGER=$(PYTHON) $(CURDIR)/manage.py
PROJECT=pilvi
SETTINGS=pilvi.settings.project
SETTINGS_TEST=pilvi.settings.test
SETTINGS_PATH=$(CURDIR)/$(shell echo $(SETTINGS) | tr "." "/").py
DJANGO_APP_NAME=management

.PHONY: help
# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile | sed -e 's/^# target: //g'

env: requirements.txt
	[ -d $(ENV) ] || virtualenv --python=python3.5 $(ENV)
	$(ENV)/bin/pip install -r requirements.txt
	touch $(ENV)

.PHONY: shell
# target: shell - Run Django debug shell
shell: $(ENV)
	$(MANAGER) shell_plus --settings=$(SETTINGS)

.PHONY: run
# target: run - Run server
run: env
	$(MANAGER) runserver_plus 0.0.0.0:8003 --settings=$(SETTINGS)

.PHONY: show_urls
show_urls: env
	$(MANAGER) show_urls --settings=$(SETTINGS)

.PHONY: migrations
# target: migrations - create $(DJANGO_APP_NAME) schema migrations
migrations: env
	$(MANAGER) makemigrations --settings=$(SETTINGS) $(DJANGO_APP_NAME)

.PHONY: data_migration
# target: data_migration - create $(DJANGO_APP_NAME) data migration
data_migration: env
	$(MANAGER) makemigrations --empty --settings=$(SETTINGS) $(DJANGO_APP_NAME)


.PHONY: db
# target db - migrate db
db: env
	$(MANAGER) migrate --settings=$(SETTINGS)


.PHONY: test
# target test - test project. Note, sqlite should be installed before, once. (make sqlite).
test: env
	$(MANAGER) test --settings=$(SETTINGS_TEST)
