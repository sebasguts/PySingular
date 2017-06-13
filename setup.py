from distutils.core import setup, Extension
import sys
import subprocess

if sys.version_info < (3,5):
    macro_list = [ ( "PYTHON_VERSION_OLDER_THREE_FIVE", "1" ) ]
else:
    macro_list = [ ]

singular_ldflags=['-lSingular' ]
singular_cflags=[]
try:
    singular_library_dir = subprocess.check_output( [ "libsingular-config", "--prefix" ] )
    singular_library_dir = singular_library_dir.strip()
    singular_library_dir = singular_library_dir.decode( 'utf-8' )
    include_dirs=[ singular_library_dir + '/include/singular' ]
    library_dirs=[ singular_library_dir + '/lib' ]
except FileNotFoundError:
    try:
        singular_cflags = subprocess.check_output( [ "pkg-config", "--cflags", "singular" ] ).strip().decode( 'utf-8' )
        singular_ldflags = subprocess.check_output( [ "pkg-config", "--libs", "singular" ] ).strip().decode( 'utf-8' )
        if singular_cflags.find( "not found" ) < 0:
            raise FileNotFoundError
        singular_cflags = singular_cflags.split()
        singular_ldflags = singular_ldflags.split()
        include_dirs = [ ]
        library_dirs = [ ]
    except FileNotFoundError:
        print( "libsingular-config and pkg-config not found - guessing debian" )
        include_dirs=[ 'usr/include/singular', 'usr/include/singular/singular', 'usr/local/include/singular', 'usr/local/include/singular/singular' ]
        library_dirs=[ 'usr/lib' ]
        singular_ldflags = singular_ldflags + "-lsingular-Singular -ldl -lsingular-polys -lflint -lmpfr -lntl -lgmp -ldl -lsingular-factory -lflint -lmpfr -lntl -lgmp -lsingular-omalloc -lsingular-resources".split()

setup(
    name = 'PySingular',
    version = '0.9.2',
    description = 'A simple interface to Singular',
    author = 'Sebastian Gutsche',
    author_email = 'sebastian.gutsche@gmail.com',
    url = 'https://github.com/sebasguts/SingularPython',
    ext_modules= [ Extension( "PySingular",
                              [ "SingularModule.cpp" ],
                              include_dirs=include_dirs,
                              library_dirs=library_dirs,
                              extra_compile_args=singular_cflags,
                              extra_link_args=singular_ldflags,
                              define_macros = macro_list ) ],
    package_data = { '': [ "COPYING", "GPLv2" ] },
)
