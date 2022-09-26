import sys
import numpy as np
try:
    from modules.projectexporter import SGProjectExporter as sgp
except:
    from projectexporter import SGProjectExporter as sgp
#safe project loader
try:
    from modules.rescaledata import loadPorject
except:
    from rescaledata import loadPorject

def averageBySpan(lcontent, column=0, epsilon=1e-10):
    resarray=[]
    for i in range(len(lcontent)):
        resarray.append([])
    for o in range(len(lcontent)):
        resarray[o].append(lcontent[o, 0])
    for i in range(1, len(lcontent[column])):
        if(lcontent[column, i]>resarray[column][-1]-epsilon and lcontent[column, i]<resarray[column][-1]+epsilon):
            for o in range(len(lcontent)):
                if(o!=column):
                    resarray[o][-1] = (resarray[o][-1]*(i)+lcontent[o, i])/(i+1)
        else:
            for o in range(len(lcontent)):
                resarray[o].append(lcontent[o, i])
    return np.asarray(resarray)

def main():
    labelseparator = " "
    separator="\t"
    project=sgp()
    projectFlag = False
    adaptToNACAFlag = False
    scaleFromNacaFlag = False
    customSepFlag = False
    extension = ""
    extensionFlag = False
    epsilon=1e-10
    basePath = ""
    if("--path" in sys.argv):
        basePath = sys.argv[sys.argv.index("--path")+1]
        if(basePath[-1]!='/'):
            basePath+='/'
    if("-d" in sys.argv):
        basePath = sys.argv[sys.argv.index("-d")+1]
        if(basePath[-1]!='/'):
            basePath+='/'
    if("--project" in sys.argv):
        project = loadPorject(basePath+sys.argv[sys.argv.index("--project")+1])
        projectFlag = True
    if("-p" in sys.argv):
        project = loadPorject(basePath+sys.argv[sys.argv.index("-p")+1])
        projectFlag = True
    if("--files" in sys.argv):
        project.insertDefaultTypes()
        for i in range(sys.argv.index("-f")+1, len(sys.argv)):
            if(sys.argv[i][0]!='-'):
                project.addDataFile(basePath+sys.argv[i], project.typelist[0][0])
            else:
                break
        projectFlag = True
    if("-f" in sys.argv):
        project.insertDefaultTypes()
        for i in range(sys.argv.index("-f")+1, len(sys.argv)):
            if(sys.argv[i][0]!='-'):
                project.addDataFile(basePath+sys.argv[i], project.typelist[0][0])
            else:
                break
        projectFlag = True
    if("-e" in sys.argv):
        try:
            epsilon=float(sys.argv[sys.argv.index("-e")+1])
        except:
            print(f"Could not read espilon value. Setting to {epsilon}")
    if("--epsilon" in sys.argv):
        try:
            epsilon=float(sys.argv[sys.argv.index("--epsilon")+1])
        except:
            print(f"Could not read espilon value. Setting to {epsilon}")
    if(not projectFlag):
        project=None
    if("--set-separators" in sys.argv):
        separator = sys.argv[sys.argv.index("--set-separators")+1]
        labelseparator = sys.argv[sys.argv.index("--set-separators")+2]
        if(separator=='space'):
            separator = ' '
        if(labelseparator=='space'):
            labelseparator = ' '
        customSepFlag=True
    if("--change-ex" in sys.argv):
        extension = sys.argv[sys.argv.index("--change-ex")+1]
        if(extension[0]!='.'):
            extension = '.'+extension
        extensionFlag=True

    if(project!=None):
        print("Received project. Iterating filenames.")
        for i in range(len(project)):
            print("Opening filename: "+project.filelist[i])
            if(not customSepFlag):
                if('.xy' in project.filelist[i]):
                    flabels, fcontent = project.readData(filename=project.filelist[i],
                                        separationChar="\t",
                                        returnLabels=True,
                                        lessInfo=True
                        )
                    labelseparator = " "
                    separator = "\t"
                    if(not extensionFlag):
                        extension = '.xy'
                if('.csv' in project.filelist[i]):
                    flabels, fcontent = project.readData(filename=project.filelist[i],
                                        separationChar=",",
                                        returnLabels=True,
                                        lessInfo=True
                        )
                    labelseparator = ","
                    separator = ","
                    if(not extensionFlag):
                        extension = '.csv'
                if('.txt' in project.filelist[i]):
                    flabels, fcontent = project.readData(filename=project.filelist[i],
                                        separationChar=" ",
                                        labelSeparationChar=" ",
                                        returnLabels=True,
                                        lessInfo=True
                        )
                    labelseparator = " "
                    separator = "\t"
                    if(not extensionFlag):
                        extension = '.txt'
            else:
                flabels, fcontent = project.readData(filename = project.filelist[i],
                                    separationChar=separator,
                                    labelSeparationChar=labelseparator,
                                    returnLabels=True,
                                    terminator=None,
                                    lessInfo=True
                )
                if(not extensionFlag):
                    if(len(project.filelist[i].split(".")[-1])>1):
                        extension = '.'+project.filelist[i].split(".")[-1]
                    else:
                        extension = ''
            #fcontent = np.asarray(fcontent)
            print("flabels:")
            print(flabels)
            file = open('.'.join(project.filelist[i].split(".")[:-1])+"_spanaveraged"+extension, "w")
            for o in range(len(flabels)):
                set_column=0
                if(o<len(flabels)-1):
                    lcontent = np.asarray(fcontent)[:, flabels[o][0]:flabels[o+1][0]]
                else:
                    lcontent = np.asarray(fcontent)[:, flabels[o][0]:]
                print(lcontent[0, :])
                print("Arguments:")
                print(sys.argv[1:])
                #arguments
                if("--column" in sys.argv):
                    try:
                        set_column=int(sys.argv[sys.argv.index("--column")+1])
                    except:
                        print("Could not read column. Setting to 0")
                        set_column=0
                lcontent = averageBySpan(lcontent, column=set_column, epsilon=epsilon)
                #data saving
                lcontent = np.transpose(lcontent)
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
                            file.write(separator)
                        else:
                            file.write("\n")
                file.write("\n")
            file.close()

if(__name__=="__main__"):
    main()