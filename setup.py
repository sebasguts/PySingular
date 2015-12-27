from distutils.core import setup, Extension

setup(
    ext_modules=[ Extension( "SingularPython",
                             [ "SingularModule.cpp" ],
                             include_dirs=['/usr/local/include/singular', '/usr/local/include/', '/usr/include' ],
                             library_dirs=['/usr/local/lib', '/usr/lib' ],
                             extra_link_args=['-lSingular', '-lpolys', '-lfactory', '-lresources', '-lomalloc', '-lflint', '-lntl', '-lgmp', '-lreadline', '-ldl', '-pthread' ] ) ],
)