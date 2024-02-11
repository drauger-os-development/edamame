#!/usr/bin/bash
# Use this file to parse compile.conf, compile the files listed inside, then remove the source files
# This process requires Nuitka.

            ### SETUP ###

if $(echo "$*" | grep -qE "\-\-help|\-h"); then
    echo -e "Nuitka Compile Script, v0.0.3

\t--dry-run                  Print what would be run if fully ran.
\t--force, -f                Force running on raw Git repo. (Risk of potential data loss)
\t--help, -h                 Print this help dialog and exit.
\t--preserve-source, -p      Build, but do not delete source files after build.
"
    exit
fi

if $(echo "$*" | grep -qE "\-\-dry\-run"); then
    echo "NOTE: DRY RUN MODE ENGAGED!"
    dry_run=1
else
    dry_run=0
fi

if $(ls -a | grep -q ".git"); then
    echo "ERROR: RUNNING ON RAW GIT REPOSITORY"
    if $(echo "$*" | grep -qE "\-\-force|\-f"); then
        echo "NOTE: OVERRIDING ERROR!!!!!"
        echo "IF THIS IS A MISTAKE, RUN \`git reset --hard' to recover any lost data."
    else
        echo "EXITING TO PROTECT DATA!"
        exit 1
    fi
fi

which nuitka 1>/dev/null 2>/dev/null
if [ "$?" == "1" ]; then
    which nuitka3 1>/dev/null 2>/dev/null
    if [ "$?" == "1" ]; then
        echo "FATAL ERROR: Nuitka not found. Please install Nuitka from your package manager."
        exit 2
    else
        nuitka_command=$(which nuitka3)
    fi
else
    nuitka_command=$(which nuitka)
fi

# Read and parse settings file
settings=$(grep -v "^#" compile.conf)
module_files=$(echo "$settings" | grep "^mod " | awk '{print $2}')
module_settings=$(echo "$settings" | grep "^mod_options=" | sed 's/mod_options=//g' | sed 's/"//g')
standalone_files=$(echo "$settings" | grep "^sa " | awk '{print $2}')
standalone_settings=$(echo "$settings" | grep "^sa_options=" | sed 's/sa_options=//g' | sed 's/"//g')
global_settings=$(echo "$settings" | grep "^global_options=" | sed 's/global_options=//g' | sed 's/"//g')
job_count=$(echo "$settings" | grep "^jobs=" | sed 's/jobs=//g' | sed 's/"//g')

            ### COMPILATION ###

# Compile Modules
if [ "$module_files" != "" ]; then
    if [ "$dry_run" == "0" ]; then
        for each in $module_files; do
            name=${each##*/}
            echo -e "\t\t\t### BUILDING $name ###"
            $nuitka_command --module $global_settings $module_settings $each
            dest=${each%/*}
            source=$(ls ${name%.py}*.so)
            mv -v "$source" "$dest"
        done
    else
        echo "Would run: $nuitka_command --module $global_settings $module_settings"
        echo "On each of: $module_files"
    fi
else
    echo "NOTE: No module files defined for compilation. Skipping module compilation..."
fi

# Compile StandAlone
# Compile Modules
if [ "$sa_files" != "" ]; then
    if [ "$dry_run" == "0" ]; then
        $nuitka_command --standalone $global_settings $standalone_settings $standalone_files
    else
        echo "Would run: $nuitka_command --standalone $global_settings $standalone_settings $standalone_files"
    fi
else
    echo "NOTE: No standalone files defined for compilation. Skipping standalone compilation..."
fi

            ### CLEAN UP ###
if [ "$dry_run" == "0" ]; then
    if $(echo "$*" | grep -qE "\-\-preserve\-source|\-p"); then
        echo "NOTE: Not deleting source files!"
    else
        rm -vf $module_files $standalone_files
    fi
else
    echo "Would run: rm -vf $module_files $standalone_files"
fi
