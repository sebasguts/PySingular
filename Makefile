all: module

module: SingularModule.cpp setup.py
	python setup.py build_ext --inplace