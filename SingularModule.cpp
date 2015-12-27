#include <Python.h>

#include <iostream>
using std::cout;
using std::cerr;
using std::endl;

#include <string>
using std::string;

#include <Singular/libsingular.h>
#include <Singular/cntrlc.h>

string singular_return;
string singular_error;

/*
 * Singular init stuff
 */

void WerrorS_for_python(const char *s)
{
  singular_error += s;
}

void PrintS_for_python(const char *s)
{
  singular_return += s;
}

void init_singular_for_python(){
    siInit("/usr/local/bin/Singular"); //FIXME
    init_signals();
    errorreported = 0;
    // init for output:
    WerrorS_callback=WerrorS_for_python;
    PrintS_callback=PrintS_for_python;

    singular_return = string();
    singular_error = string();
}

/*
 * Python functions
 */
extern int inerror;

static PyObject * RunSingularCommand( PyObject* self, PyObject* args ){
    
    singular_return.erase();
    singular_error.erase();
    const char * input_string;
    if (! PyArg_ParseTuple(args, "s", &input_string) )
        return NULL;
    
    const char return_str[] = "return();";
    char *ost = (char *)omalloc0(strlen(input_string) + sizeof(return_str)+1);
    strcpy(ost, input_string);
    strcat(ost,return_str);
    myynest = 1;
    BOOLEAN err = iiAllStart(NULL, ost, BT_proc, 0);
    inerror = 0;
    errorreported = 0;
    omFree(ost);
    
    const char * return_string;
    PyObject* error;
    if(!err){
        return_string = singular_return.c_str();
        error = Py_False;
    }
    else{
        return_string = singular_error.c_str();
        error = Py_True;
    }
    
    return PyTuple_Pack( 2, error, PyUnicode_FromString( return_string ) );
    
}

/*
 * Python init stuff
 */

static PyMethodDef SingularPythonMethods[] = {
    {"RunSingularCommand",  RunSingularCommand, METH_VARARGS,
     "Runs a singular command"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef SingularPythonmodule = {
   PyModuleDef_HEAD_INIT,
   "SingularPython",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   SingularPythonMethods
};

PyMODINIT_FUNC
PyInit_SingularPython(void)
{
    init_singular_for_python();
    return PyModule_Create(&SingularPythonmodule);
}

/*
 * main
 */

int main(int argc, char *argv[]){
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    /* Add a built-in module, before Py_Initialize */

    PyImport_AppendInittab("SingularPython", PyInit_SingularPython);
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyImport_ImportModule("SingularPython");

    PyMem_RawFree(program);
    return 0;
}
