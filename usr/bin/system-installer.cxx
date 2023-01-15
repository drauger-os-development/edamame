/*
 * system-installer.cxx
 *
 * Copyright 2022 Thomas Castleman <contact@draugeros.org>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 *
 *
 */

 //define macros
#define elif else if
#define str string
#define str_list vector<str>
#define int_list vector<int>
#define float_list vector<float>
#define bool_list vector<bool>
#define PY_SSIZE_T_CLEAN

 // import libs
 #include <iostream>
 #include <string>
 // #include <bits/stdc++.h>
 // #include <sys/stat.h>
 // #include <sstream>
 #include <vector>
 // #include <unistd.h>
 // #include <regex>
 // #include <stdlib.h>
 #include <fstream>
 #include <Python.h>
 // #include <stdio.h>

using namespace std;

str VERSION = "2.4.7";
str R = "\033[0;31m";
str G = "\033[0;32m";
str Y = "\033[1;33m";
str NC = "\033[0m";
str HELP = "\n"
"system-installer, Version " + VERSION + "\n"
"\n"
"\t-h, --help              print this help dialoge.\n"
"\t    --boot-time         launch system-installer in boot-time mode.\n"
"\t-v, --version           print current version.\n"
"\n"
"Pass nothing to start installer.\n";

wchar_t* Py_Init()
{
	wchar_t *program = Py_DecodeLocale("system-installer", NULL);
	Py_SetProgramName(program);
	Py_Initialize();
	return program;
}

str run(const char* cmd) {
    char buffer[128];
    str result = "";
    FILE* pipe = popen(cmd, "r");
    if (!pipe) throw std::runtime_error("popen() failed!");
    try {
        while (fgets(buffer, sizeof buffer, pipe) != NULL)
        {
            result += buffer;
        }
    }
    catch (...) {
        pclose(pipe);
        throw;
    }
    pclose(pipe);
    return result;
}


// Launch with boot time parameter
void launch(bool boot_time)
{
	str command1 = "/usr/bin/xhost";
	str enable = " +si:localuser:root";
	str disable = " -si:localuser:root";
	str command = "echo 'toor' | sudo -S /usr/share/system-installer/engine.py";
	run((command1 + enable).c_str());
	cout << Y << "RUNNING LOG LOCATED AT /tmp/system-installer.log" << NC << endl;
	wchar_t *program = Py_Init();
	if (boot_time)
	{

		PyRun_SimpleString("import de_control.enable as de_enable\n"
	                       "de_enable.immersion()\n");
		FILE* file = fopen("/tmp/system-installer.log", "w");
		if (file != NULL)
		{
			fputs("STARTING IN BOOT-TIME MODE\n", file);
			fclose(file);
		}
		else
		{
			cerr << "Failed to write to log file!" << endl;
		}
		command = command + " --boot-time";
	}
	command = command + " 2>/tmp/system-installer.log 1>&2";
	run(command.c_str());
	if (boot_time)
	{
		PyRun_SimpleString("import de_control.disable as de_disable\n"
	                       "de_disable.immersion()\n");
		if (Py_FinalizeEx() < 0)
		{
			exit(120);
		}
		PyMem_RawFree(program);
	}
	run((command1 + disable).c_str());
}

// Launch with no parameter
void launch()
{
	launch(false);
}


int main(int argc, char **argv)
{
	if (argc > 1)
	{
		str arg = argv[1];
	    if ((arg == "-v") || (arg == "--version"))
		{
	        cout << "\n" << VERSION << "\n" << endl;
		}
	    elif ((arg == "-h") || (arg == "--help"))
		{
	        cout << HELP << endl;
		}
	    elif (arg == "--boot-time")
		{
	        launch(true);
		}
	    else
		{
	        cerr << "Option " << arg << " not recognized." << endl;
	        cerr << HELP << endl;
		}
	}
	else
	{
	    launch();
	}
	return 0;
}
