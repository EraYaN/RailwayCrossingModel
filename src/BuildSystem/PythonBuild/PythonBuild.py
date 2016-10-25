import os
import glob
import sys
import argparse as ap
import subprocess
from mCRL2Bindings import mCRL2System, mCRL2Tools

import colorama
colorama.init(autoreset=True)

C_RED = colorama.Fore.RED+colorama.Style.BRIGHT
C_GREEN = colorama.Fore.GREEN+colorama.Style.BRIGHT
C_CYAN = colorama.Fore.CYAN+colorama.Style.BRIGHT

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='SystemValidationmCRL2',description='mCRL2 System Validation Build System')
    parser.add_argument('--verify', action="store_true", help='Verify the system')
    parser.add_argument('--show-graph', action="store_true", help='Show the LTS graph')
    parser.add_argument('--disable-lts-compile', action="store_true", help='Skip everything for the LTS compile.')
    #TODO report making
    parser.add_argument('--output-dir', action="store", help='Output subdirectory',default="out")
    parser.add_argument('--trace-action', action="store", help='Project root directory name',default=None)
    parser.add_argument('--project-root', action="store", help='Project root directory name',default="./full-system/full-system")
    parser.add_argument('--project-name', action="store", help='Project base name',default="full-system")
    try:
        verified = False
        opts = parser.parse_args(sys.argv[1:])
        project_dir = os.path.abspath(opts.project_root)
        project_name = opts.project_name
        output_dir = opts.output_dir

        
        if not os.path.exists(os.path.join(project_dir,output_dir)):
            print("Creating output directory {0}".format(os.path.join(project_dir,output_dir)))
            os.makedirs(os.path.join(project_dir,output_dir))

        project_dir = os.path.abspath(project_dir)

        install_dir = os.path.abspath(mCRL2Tools.findInstallPath())

        print(install_dir)

        system = mCRL2System(install_dir,project_dir,False)

        returncode = True

        if not opts.disable_lts_compile:
            print("Compiling mCRL2 to LPS...")
            returncode = system.mcrl22lps("{0}.mcrl2".format(project_name),os.path.join(output_dir,"{0}.lps".format(project_name)))

            if returncode:
                print("Compiling LPS to LTS...")
                returncode = system.lps2lts(os.path.join(output_dir,"{0}.lps".format(project_name)),os.path.join(output_dir,"{0}.lts".format(project_name)))
        
        if opts.verify:
            if returncode:
                print("Preprocessing PRE.MCF...")
                mcf_rules = []
                with open(os.path.join(project_dir,"{0}.pre.mcf".format(project_name)),'r') as mcf_file:
                    for line in mcf_file:
                        line = line.strip()
                        splitted_line = line.split("%")
                        name = ''
                        if len(splitted_line)>1:
                            name = splitted_line[1].strip()
                        
                        line = splitted_line[0].strip()
                        if line == "&&":
                            continue;
                        if line == "":
                            continue;
                       
                        mcf_rules.append({"rule":splitted_line[0],"name":name,"result":None})

                mcf_rule_count = len(mcf_rules)
                print(C_CYAN+"Found {0} MCF rules...".format(mcf_rule_count))
                current_rule = 0
                for rule in mcf_rules:
                    with open(os.path.join(project_dir,output_dir,"{0}.{1}.tmp.mcf".format(project_name,current_rule)),'w') as mcf_out_file:
                        mcf_out_file.write(rule['rule'])

                    if returncode:
                        print("Compiling LTS to PBES ({0} of {1})...".format(current_rule+1,mcf_rule_count))
                        returncode = system.lts2pbes(os.path.join(output_dir,"{0}.lts".format(project_name)),os.path.join(output_dir,"{0}.pbes".format(project_name)),os.path.join(output_dir,"{0}.{1}.tmp.mcf".format(project_name,current_rule)))
                    if returncode:
                        print("Converting PBES to bool ({0} of {1})...".format(current_rule+1,mcf_rule_count))
                        verified = system.pbes2bool(os.path.join(output_dir,"{0}.pbes".format(project_name)))
                        rule['result'] = verified
                        if verified:
                            print(C_GREEN+"Rule #{0} \"{1}\" verified succesfully.".format(current_rule+1,rule['name']))
                        else:
                            print(C_RED+"Rule #{0} \"{1}\" could not be verified.".format(current_rule+1,rule['name']))

                        current_rule += 1

        if returncode and opts.trace_action:
            print("Generating Traces...")
            returncode = system.lps2lts_trace(os.path.join(output_dir,"{0}.lps".format(project_name)),os.path.join(output_dir,"{0}.lts".format(project_name)),opts.trace_action)
            if returncode:
                files = glob.glob(os.path.join(project_dir,output_dir,"{0}*{1}.trc".format(project_name,opts.trace_action)))
                files_count = len(files)
                print(C_CYAN+"Found {0} Traces...".format(files_count))

                current_trace = 0
                for file in files:
                    returncode = system.tracepp(file,os.path.join(output_dir,"{0}.txt".format(file)))
                    if returncode:
                        print("Processed trace {0}...".format(current_trace+1))

                    current_trace += 1


        if returncode and opts.show_graph:
            system.ltsgraph("{0}.lts".format(project_name))

        print("Done.")
    except SystemExit:
        print('Bad Arguments')