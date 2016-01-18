from distutils.core import setup, Extension

setup(
    name = 'SingularPython',
    version = '0.1',
    description = 'A simple interface to singular',
    author = 'Sebastian Gutsche',
    author_email = 'sebastian.gutsche@gmail.com',
    url = 'https://github.com/sebasguts/SingularPython',
    ext_modules= [ Extension( "SingularPython",
                              [ "SingularModule.cpp" ],
                              include_dirs=['/usr/local/include/singular', '/usr/local/include/', '/usr/include' ],
                              library_dirs=['/usr/local/lib', '/usr/lib' ],
                              extra_link_args=['-lSingular', '-lpolys', '-lfactory', '-lresources', '-lomalloc', '-lflint', '-lntl', '-lgmp', '-lreadline', '-ldl', '-pthread' ] ) ],
)