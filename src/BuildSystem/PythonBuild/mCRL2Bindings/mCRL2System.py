import subprocess
import os
class mCRL2System:
    """Bindings to the mCRL2 system

    Attributes:
        installPath: A string with the full path to the installation (/bin folder) of mCRL2.
        projectPath: A string with the full path to the project files, all files are relative to this.
    """

    def __init__(self, installPath, projectPath, verbose):
        """Return a mCRL2System object whose installPath is *installPath* and project path
        is *projectPath*."""
        self.installPath = installPath
        self.projectPath = projectPath
        self.verbose = verbose
        # Program names
        self.bin_mcrl22lps = os.path.join(installPath,'mcrl22lps')
        self.bin_lps2lts = os.path.join(installPath,'lps2lts')
        self.bin_lts2pbes = os.path.join(installPath,'lts2pbes')
        self.bin_pbes2bool = os.path.join(installPath,'pbes2bool')
        self.bin_tracepp = os.path.join(installPath,'tracepp')
        self.bin_ltsgraph = os.path.join(installPath,'ltsgraph')

    def mcrl22lps(self,inputFile,outputFile):
        cmd = [self.bin_mcrl22lps,inputFile,outputFile,"--lin-method=regular", "--rewriter=jitty"]
        if self.verbose:
            cmd.append("--verbose")
        result = subprocess.run(cmd,cwd=self.projectPath,stdout=subprocess.PIPE,universal_newlines=True)
        return result.returncode == 0

    def lps2lts(self,inputFile,outputFile):
        cmd = [self.bin_lps2lts,inputFile,outputFile,"--rewriter=jitty","--strategy=breadth"]
        if self.verbose:
            cmd.append("--verbose")
        result = subprocess.run(cmd,cwd=self.projectPath,stdout=subprocess.PIPE,universal_newlines=True)
        return result.returncode == 0

    def lps2lts_trace(self,inputFile,outputFile,action):
        cmd = [self.bin_lps2lts,inputFile,outputFile,"--action={0}".format(action), "--trace","--rewriter=jitty", "--strategy=breadth"]
        if self.verbose:
            cmd.append("--verbose")
        result = subprocess.run(cmd,cwd=self.projectPath,stdout=subprocess.PIPE,universal_newlines=True)
        return result.returncode == 0

    def tracepp(self,inputFile,outputFile,format='plain'):
        cmd = [self.bin_tracepp,inputFile,outputFile,"--format={0}".format(format)]
        if self.verbose:
            cmd.append("--verbose")
        result = subprocess.run(cmd,cwd=self.projectPath,stdout=subprocess.PIPE,universal_newlines=True)
        return result.returncode == 0

    def lts2pbes(self,inputFile,outputFile,formula):
        cmd = [self.bin_lts2pbes,inputFile,outputFile,"--formula={0}".format(formula), "--out=pbes"]
        if self.verbose:
            cmd.append("--verbose")
        result = subprocess.run(cmd,cwd=self.projectPath,stdout=subprocess.PIPE,universal_newlines=True)
        return result.returncode == 0

    def pbes2bool(self,inputFile):
        cmd = [self.bin_pbes2bool,inputFile,"--erase=none","--rewriter=jitty","--search=breadth-first","--strategy=0"]
        if self.verbose:
            cmd.append("--verbose")
        result = subprocess.run(cmd,cwd=self.projectPath,stdout=subprocess.PIPE,universal_newlines=True)
        return result.stdout.strip() == 'true'

    def ltsgraph(self,inputFile):
        cmd = [self.bin_ltsgraph,inputFile]
        subprocess.Popen(cmd,cwd=self.projectPath)
        