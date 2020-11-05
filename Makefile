PKG = easyrice
PREFIX    ?= /usr
XSESSIONS ?= $(PREFIX)/share/xsessions

install:
	# Add .desktop file
	mkdir -p "$(DESTDIR)$(XSESSIONS)"
	cp -p easyrice/easyrice.desktop "$(DESTDIR)$(XSESSIONS)"

	# Install package
	python3 -m pip install .

uninstall:
	rm -f "$(DESTDIR)$(XSESSIONS)"/bspwm.desktop
	python3 -m pip uninstall easyrice
