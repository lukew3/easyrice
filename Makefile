PKG = riceman

PREFIX    ?= /usr
XSESSIONS ?= $(PREFIX)/share/xsessions

install:
	# Add .desktop file
	mkdir -p "$(DESTDIR)$(XSESSIONS)"
	cp -p riceman/riceman.desktop "$(DESTDIR)$(XSESSIONS)"

	# Add basic config structure
	python3 -m pip install .

uninstall:
	rm -f "$(DESTDIR)$(XSESSIONS)"/bspwm.desktop
	python3 -m pip uninstall riceman
