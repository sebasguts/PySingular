from distutils.core import setup, Extension
import sys
import subprocess

if sys.version_info < (3,5):
    macro_list = [ ( "PYTHON_VERSION_OLDER_THREE_FIVE", "1" ) ]
else:
    macro_list = [ ]

if sys.version_info < (3,0):
    FileNotFoundError = OSError

singular_cflags=[]
try:
    singular_library_dir = subprocess.check_output( [ "libsingular-config", "--prefix" ] )
    singular_library_dir = singular_library_dir.strip()
    singular_library_dir = singular_library_dir.decode( 'utf-8' )
    include_dirs=[ singular_library_dir + '/include/singular' ]
    library_dirs=[ singular_library_dir + '/lib' ]
    singular_ldflags=['-lSingular' ]
except FileNotFoundError:
    try:
        singular_cflags_output = subprocess.check_output( [ "pkg-config", "--cflags", "singular" ] ).strip().decode( 'utf-8' )
        if singular_cflags_output.find( "not found" ) == 0:
            raise FileNotFoundError
        singular_cflags = singular_cflags_output.split()
        ## pkg-config ldflags are rubbish
        singular_ldflags = [ '-lsingular-Singular' ]
        include_dirs = [ ]
        library_dirs = [ '/usr/lib' ]
    except FileNotFoundError:
        print( "libsingular-config and pkg-config not found - guessing debian" )
        include_dirs=['/usr/include/x86_64-linux-gnu/singular',
                      '/usr/include/x86_64-linux-gnu/singular/singular',
                      '/usr/include/singular', '/usr/include/singular/singular',
                      '/usr/include/x86_64-linux-gnu/singular',
                      '/usr/include/x86_64-linux-gnu/singular/singular',
                      '/usr/include/singular', '/usr/include/singular/singular',
                      '/usr/include/x86_64-linux-gnu/singular',
                      '/usr/include/singular',
                      '/usr/include/x86_64-linux-gnu/singular',
                      '/usr/include/singular',
                      '/usr/include/x86_64-linux-gnu/singular',
                      '/usr/include/singular']
        library_dirs=[ '/usr/lib' ]
        singular_ldflags = ['-lsingular-Singular' ]

setup(
    name = 'PySingular',
    version = '0.9.4',
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
