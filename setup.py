from distutils.core import setup, Extension
import sys
import subprocess

if sys.version_info < (3,5):
    macro_list = [ ( "PYTHON_VERSION_OLDER_THREE_FIVE", "1" ) ]
else:
    macro_list = [ ]

singular_library_dir = subprocess.check_output( [ "libsingular-config", "--prefix" ] )
singular_library_dir = singular_library_dir.strip()
singular_library_dir = singular_library_dir.decode( 'utf-8' )

setup(
    name = 'PySingular',
    version = '0.9.1',
    description = 'A simple interface to Singular',
    author = 'Sebastian Gutsche',
    author_email = 'sebastian.gutsche@gmail.com',
    url = 'https://github.com/sebasguts/SingularPython',
    ext_modules= [ Extension( "PySingular",
                              [ "SingularModule.cpp" ],
                              include_dirs=[ singular_library_dir + '/include/singular' ],
                              library_dirs=[ singular_library_dir + '/lib' ],
                              extra_link_args=['-lSingular' ],
                              define_macros = macro_list ) ],
    package_data = { '': [ "COPYING", "GPLv2" ] },
)
