IGNORE_ERRORS = E501,F401,F403,F405
PKG = easyrice
PREFIX    ?= /usr
XSESSIONS ?= $(PREFIX)/share/xsessions
PYTHON ?= python3
install:
	# Add .desktop file
	mkdir -p "$(DESTDIR)$(XSESSIONS)"
	cp -p easyrice/easyrice.desktop "$(DESTDIR)$(XSESSIONS)"
	# Make config directory

	# Install package
	python3 -m pip install .

uninstall:
	rm -f "$(DESTDIR)$(XSESSIONS)"/easyrice.desktop
	python3 -m pip uninstall easyrice

deps:
	$(PYTHON) -m pip install --user -r dev-requirements.txt

format:
	$(PYTHON) -m autopep8 --ignore=$(IGNORE_ERRORS) -ir $(PKG)/*

lint:
	$(PYTHON) -m flake8 --ignore=$(IGNORE_ERRORS) $(PKG)
