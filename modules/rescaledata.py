import sys
import numpy as np
from matgrapher import grapher
try:
    from module.projectexporter import SGProjectExporter as sgp
except:
    from projectexporter import SGProjectExporter as sgp

def loadPorject(project_filename):
    print("Loading data from launcher.")
    if(project_filename[-3:]=="sgp"):
        project = sgp(filename=project_filename)
        return project
    return None

def main():
    labelseparator = ","
    if("-p" in sys.argv):
        project = loadPorject(sys.argv[sys.argv.index("-p")+1])
    if(project!=None):
        for i in range(len(project)):
            file = open("_edited.".join(project.filelist[i].split(".")), "w")
            if('.xy' in project.filelist[i]):
                flabels, fcontent = project.readData(filename=project.filelist[i],
                                    separationChar="\t",
                                    returnLabels=True,
                                    lessInfo=True
                    )
                labelseparator = "\t"
            if('.csv' in project.filelist[i]):
                flabels, fcontent = project.readData(filename=project.filelist[i],
                                    separationChar=",",
                                    returnLabels=True,
                                    lessInfo=True
                    )
            #fcontent = np.asarray(fcontent)
            for o in range(len(flabels)):
                if(o<len(flabels)-1):
                    lcontent = np.asarray(fcontent)[:, flabels[o][0]:flabels[o+1][0]]
                else:
                    lcontent = np.asarray(fcontent)[:, flabels[o][0]:]
                print(lcontent[0, :])
                lcontent[0, :] = (lcontent[0, :]-np.min(lcontent[0, :]))/(np.max(lcontent[0, :])-np.min(lcontent[0, :]))
                lcontent = np.transpose(lcontent)
                print(f"flabels:{flabels[o]}")
                for j in range(len(flabels[o])-1):
                    file.write(f"{flabels[o][j+1]}")
                    if(j<len(flabels[o])-2):
                        file.write(labelseparator)
                    else:
                        file.write("\n")
                for j in range(len(lcontent)):
                    for k in range(len(lcontent[j])):
                        file.write(f"{lcontent[j, k]}")
                        if(k<len(lcontent[j])-1):
                            file.write(labelseparator)
                        else:
                            file.write("\n")
                file.write("\n")
            file.close()
    pass

if(__name__=="__main__"):
    main()
