/*
 * edamame.cxx
 *
 * Copyright 2025 Thomas Castleman <batcastle@draugeros.org>
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

// import libs
#include <iostream>
#include <string>
#include <unistd.h>

using namespace std;

str VERSION = "3.0.8";
str R = "\033[0;31m";
str G = "\033[0;32m";
str Y = "\033[1;33m";
str NC = "\033[0m";
str HELP = "\n"
"Edamame, Version " + VERSION + "\n"
"\n"
"\t    --gui               specify the GUI to use. May throw an error if given toolkit is not available."
"\t-h, --help              print this help dialoge.\n"
"\t    --boot-time         launch Edamame in boot-time mode.\n"
"\t-v, --version           print current version.\n"
"\n"
"Pass nothing to start installer.\n";

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
void launch(str arg)
{
	str command1 = "/usr/bin/xhost";
	str enable = " +si:localuser:root";
	str disable = " -si:localuser:root";
	str command = "echo 'toor' | sudo -S nice -n -10 /usr/share/edamame/engine.py";
	run((command1 + enable).c_str());
	cout << Y << "RUNNING LOG LOCATED AT /tmp/edamame.log" << NC << endl;
	if (arg == "boot_time")
	{
		FILE* file = fopen("/tmp/edamame.log", "w");
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
	elif (arg != "")
	{
		command = command + " --gui=" + arg;
	}
	command = command + " 2>/tmp/edamame.log 1>&2";
	if (chdir("/usr/share/edamame") != 0 )
	{
		cout << R << "COULD NOT CHANGE DIRECTORY! EXITING!" << NC << endl;
		return;
	}
	run(command.c_str());
	run((command1 + disable).c_str());
}

// Launch with no parameter
void launch()
{
	launch("");
}


int main(int argc, char **argv)
{
	if (argc > 1)
	{
		str arg = argv[1];
	    if ((arg == "-v") || (arg == "--version"))
		{
	        cout << "\n" << VERSION << "\n" << endl;
			return 0;
		}
	    elif ((arg == "-h") || (arg == "--help"))
		{
	        cout << HELP << endl;
			return 0;
		}
	    elif (arg == "--boot-time")
		{
	        launch("boot_time");
			return 0;
		}
		elif (arg == "--gui")
		{
			if (argc > 2)
			{
				launch(argv[2]);
				return 0;
			}
			cout << "No GUI method selected. Please select a GUI method to use." << endl;
			return 1;
		}
	    cerr << "Option '" << arg << "' not recognized." << endl;
		cerr << HELP << endl;
		return 1;
	}
	else
	{
	    launch();
	}
	return 0;
}
