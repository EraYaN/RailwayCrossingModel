import os
import sys
import argparse as ap
import subprocess
from mCRL2Bindings import mCRL2System, mCRL2Tools



if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='SystemValidationmCRL2',description='mCRL2 System Validation Build System')
    parser.add_argument('--verify', action="store_true", help='Verify the system')
    parser.add_argument('--show-graph', action="store_true", help='Show the LTS graph')
    parser.add_argument('--disable-lts-compile', action="store_true", help='Skip everything for the LTS compile.')
    #TODO report making
    #parser.add_argument('--output-dir', action="store", help='Output directory',default="../../../docs/lab2")
    parser.add_argument('--trace-action', action="store", help='Project root directory name',default=None)
    parser.add_argument('--project-root', action="store", help='Project root directory name',default="./full-system/full-system")
    parser.add_argument('--project-name', action="store", help='Project base name',default="full-system")
    try:
        verified = False
        opts = parser.parse_args(sys.argv[1:])
        project_dir = opts.project_root
        project_name = opts.project_name

        project_dir = os.path.abspath(project_dir)

        install_dir = os.path.abspath(mCRL2Tools.findInstallPath())

        print(install_dir)

        system = mCRL2System(install_dir,project_dir,True)

        returncode = True

        if not opts.disable_lts_compile:
            print("Compiling mCRL2 to LPS...")
            returncode = system.mcrl22lps("{0}.mcrl2".format(project_name),"{0}.lps".format(project_name))

            if returncode:
                print("Compiling LPS to LTS...")
                returncode = system.lps2lts("{0}.lps".format(project_name),"{0}.lts".format(project_name))

        if opts.verify:
            if returncode:
                print("Compiling LTS to PBES...")
                returncode = system.lts2pbes("{0}.lts".format(project_name),"{0}.pbes".format(project_name),"{0}.mcf".format(project_name))
            if returncode:
                print("Converting PBES to bool...")
                verified = system.pbes2bool("{0}.pbes".format(project_name))

            if verified:
                print("System verified succesfully.")
            else:
                print("System could not be verified.")

        if returncode and opts.trace_action:
            print("Generating Traces...")
            returncode = system.lps2lts("{0}.lps".format(project_name),"{0}.lts".format(project_name))

        if returncode and opts.show_graph:
            system.ltsgraph("{0}.lts".format(project_name))

        print("Done.")
    except SystemExit:
        print('Bad Arguments')