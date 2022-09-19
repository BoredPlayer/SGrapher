import sys
import numpy as np
from matgrapher import grapher
try:
    from module.projectexporter import SGProjectExporter as sgp
except:
    from projectexporter import SGProjectExporter as sgp

#safe project loader
try:
    from modules.rescaledata import loadPorject
except:
    from rescaledata import loadPorject

def main():
    project = sgp()
    excluded_column = []
    if("-p" in sys.argv):
        project = loadPorject(sys.argv[sys.argv.index("-p")+1])
    if("-f" in sys.argv):
        fn = sys.argv[sys.argv.index("-f")+1]
        if("\\" in fn):
            fn = "/".join(sys.argv[sys.argv.index("-f")+1].split("\\"))
        project.filelist.append(fn)
    if("-X" in sys.argv):
        xcolumn = int(sys.argv[sys.argv.index("-X")+1])
    else:
        xcolumn = 0
    if("-e" in sys.argv):
        cllist = sys.argv[sys.argv.index("-e")+1].split(",")
        for excl in cllist:
            try:
                excluded_column.append(int(excl))
            except:
                print(f"Invalid column number: {excl}")
    if("-l" in sys.argv):
        labelSeparationChar = sys.argv[sys.argv.index("-l")+1]
    else:
        labelSeparationChar = ' '
    if("-s" in sys.argv):
        separationChar = sys.argv[sys.argv.index("-s")+1]
    else:
        separationChar = ' '
    
    for filename in project.filelist:
        labels, contents = project.readData(filename, returnLabels=True, separationChar=separationChar, labelSeparationChar=labelSeparationChar, lessInfo=True)
        print(f"filename: {filename}\nFolder path: "+"/".join(filename.split("/")[:-1]))
        for flabels in range(len(labels)):
            for lnum, label in enumerate(labels[flabels][1:]):
                if(lnum!=xcolumn):
                    filetitle = filename.split("/")[-1].split(".")[0]+"_"+label.strip('"()')
                    print(f"Label: {filetitle}")
                    filepath = "/".join(filename.split("/")[:-1])+"/"+filetitle+'.'+filename.split("/")[-1].split(".")[-1]
                    print(f"Opening: {filepath}")
                    file = open(filepath, "w")
                    file.write(labels[flabels][1+xcolumn]+labelSeparationChar+label+"\n")
                    if(flabels<len(labels)-1):
                        LS = labels[flabels][0]
                        LE = labels[flabels][1]
                    else:
                        LS = labels[flabels][0]
                        LE = len(contents[0])
                    print(f"LS={LS}\nLE={LE}")
                    for cindex in range(LS, LE):
                        file.write(str(contents[xcolumn][cindex])+separationChar+str(contents[lnum][cindex])+"\n")
                    file.close()


if(__name__=="__main__"):
    main()