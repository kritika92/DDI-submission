build:
	mkdir -p build/bin
	mkdir -p build/lib
	cp src/pm.py build/bin/pm
	cp -r src/projman build/lib
	chmod -R 777 build
