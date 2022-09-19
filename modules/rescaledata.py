import sys
import numpy as np
from matgrapher import grapher
try:
    from module.projectexporter import SGProjectExporter as sgp
except:
    from projectexporter import SGProjectExporter as sgp

def loadPorject(project_filename):
    print("Loading data from launcher. Project: "+project_filename)
    if(project_filename[-3:]=="sgp"):
        project = sgp(filename=project_filename)
        print("Loaded filenames:")
        for i in range(len(project)):
            print(f"[{i}]\t{project.filelist[i]}")
        return project
    return None

def rotationMatrix(a):
    rtmt = [[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]]
    return np.asarray(rtmt)

def generateNACA(thickness, chord, aoa, points=50):
    rt = rotationMatrix(aoa)
    x = np.linspace(0, 1, num=points)
    xr = np.linspace(1, 0, num=points)
    x = x**2*chord
    xr = xr**2*chord
    y = np.zeros(points)
    yr = np.zeros(points)
    for i in range(points):
        y[i] = 5*thickness*(0.2969*np.sqrt((x[i]/chord))-0.1260*(x[i]/chord)-0.3516*(x[i]/chord)**2+0.2843*(x[i]/chord)**3-0.1015*(x[i]/chord)**4)
        yr[i] = -5*thickness*(0.2969*np.sqrt((xr[i]/chord))-0.1260*(xr[i]/chord)-0.3516*(xr[i]/chord)**2+0.2843*(xr[i]/chord)**3-0.1015*(xr[i]/chord)**4)
        #y[i] = 5*thickness*(0.14845/np.sqrt(x[i])-0.1260-0.7032*x[i]+0.8529*x[i]**2-0.406*x[i]**3)
    x = np.append(x, xr)
    y = np.append(y, yr)
    for i in range(len(y)):
        #print(np.asarray([[x[i]], [y[i]], [0]]))
        rv = np.matmul(rt, np.asarray([[x[i]], [y[i]], [0]]))
        x[i] = rv[0]
        y[i] = rv[1]
    #offset = min(x)
    #x = x-offset
    return x, y
    
def generateNACALength(thickness, chord):
    x, y = generateNACA(thickness, chord, 0, points=5000)
    lengthTable = [x[:5000], np.zeros(5000)]
    for i in range(1, 5000):
        lengthTable[1][i] = np.sqrt((x[i]-x[i-1])**2+(y[i]-y[i-1])**2)+lengthTable[1][i-1]
    return lengthTable

def NACADerLine(thickness, chord, x):
    return 5*thickness*(
                0.14845/np.sqrt(x/chord)-
                0.126-
                0.7032*(x/chord)+
                0.8529*np.power(x/chord, 2)-
                0.406*np.power(x/chord, 3)
            )

def findNACALength(thickness, chord, aoa, x):
    #print(f"[findNACALength] thickness={thickness}\tchord={chord}\taoa={aoa}")
    intfuntion = lambda f : np.sqrt(1+NACADerLine(thickness, chord, f/np.cos(aoa))**2)
    xtab = np.linspace(0, x, num=1000)
    ytab = intfuntion(xtab)
    if(np.inf in ytab):
        ytab[np.where(ytab==np.inf)] = 0.0
    res = np.trapz(ytab, x=xtab)
    #print(f"[findNACALength] x={x}\tres={res}")
    return res

def findXFromFunction(x_min, x_max, funtion, function_value, returnDelta=False, lessInfo=True, **kwargs):
    xmin=x_min
    xmax=chord
    x=x_max
    lloc = findNACALength(thickness, chord, aoa, x)
    executable=False
    cycler = 1
    while(np.abs(lloc-function_value)>=epsilon):
        executable=True
        deltax = xmax-xmin
        if(cycler>0):
            x = xmax
        if(cycler<0):
            x = xmin
        lloc=function(kwargs)
        if(cycler<0 and function_value<lloc):
            xmin=x-deltax
            xmax = x
            x=xmin
            lloc=function(kwargs)
            #cycler*=(-1)
        if(cycler>0 and function_value>lloc):
            xmax=x+deltax
            xmin = x
            x=xmax
            lloc=function(kwargs)
            #cycler*=(-1)
        if(cycler<0 and function_value>lloc and executable):
            xmax = xmin+deltax/2
        if(cycler>0 and function_value<lloc and executable):
            xmin = xmax-deltax/2
        cycler=cycler*(-1)
        if(not lessInfo):
            print(f"x={x}\tdelta={lloc-function_value}")
    if(returnDelta):
        return lloc-function_value, x
    return x
def findLengthfromNACA(thickness, chord, aoa, l, epsilon=0.00001, returnDelta=False):
    xmin=0
    xmax=chord
    x=xmin
    lloc = findNACALength(thickness, chord, aoa, x)
    executable=False
    cycler = 1
    while(np.abs(lloc-l)>=epsilon):
        executable=True
        deltax = xmax-xmin
        if(cycler>0):
            x = xmax
        if(cycler<0):
            x = xmin
        lloc=findNACALength(thickness, chord, aoa, x)
        if(cycler<0 and l<lloc):
            xmin=x-deltax
            xmax = x
            x=xmin
            lloc=findNACALength(thickness, chord, aoa, x)
            #cycler*=(-1)
        if(cycler>0 and l>lloc):
            xmax=x+deltax
            xmin = x
            x=xmax
            lloc=findNACALength(thickness, chord, aoa, x)
            #cycler*=(-1)
        if(cycler<0 and l>lloc and executable):
            xmax = xmin+deltax/2
        if(cycler>0 and l<lloc and executable):
            xmin = xmax-deltax/2
        cycler=cycler*(-1)
        print(f"x={x}\tdelta={lloc-l}")
    if(returnDelta):
        return lloc-l, x
    return x

def main():
    labelseparator = " "
    separator="\t"
    project=sgp()
    projectFlag = False
    adaptToNACAFlag = False
    scaleFromNacaFlag = False
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
    if(not projectFlag):
        project=None
    
    if(project!=None):
        print("Received project. Iterating filenames.")
        for i in range(len(project)):
            print("Opening filename: "+project.filelist[i])
            file = open("_edited.".join(project.filelist[i].split(".")), "w")
            if('.xy' in project.filelist[i]):
                flabels, fcontent = project.readData(filename=project.filelist[i],
                                    separationChar="\t",
                                    returnLabels=True,
                                    lessInfo=True
                    )
                labelseparator = " "
                separator = "\t"
            if('.csv' in project.filelist[i]):
                flabels, fcontent = project.readData(filename=project.filelist[i],
                                    separationChar=",",
                                    returnLabels=True,
                                    lessInfo=True
                    )
                labelseparator = ","
                separator = ","
            if('.txt' in project.filelist[i]):
                flabels, fcontent = project.readData(filename=project.filelist[i],
                                    separationChar=" ",
                                    labelSeparationChar=" ",
                                    returnLabels=True,
                                    lessInfo=True
                    )
                labelseparator = " "
                separator = "\t"
            #fcontent = np.asarray(fcontent)
            print("flabels:")
            print(flabels)
            for o in range(len(flabels)):
                if(o<len(flabels)-1):
                    lcontent = np.asarray(fcontent)[:, flabels[o][0]:flabels[o+1][0]]
                else:
                    lcontent = np.asarray(fcontent)[:, flabels[o][0]:]
                print(lcontent[0, :])
                print("Arguments:")
                print(sys.argv[1:])
                if("--scale-to-naca" in sys.argv):
                    try:
                        thickness=float(sys.argv[sys.argv.index("--scale-to-naca")+1])
                        aoa=float(sys.argv[sys.argv.index("--scale-to-naca")+2])
                        adaptToNACAFlag=True
                    except:
                        raise Exception("Could not adapt to NACA - wrong arguments. Expected:\n--scale-to-naca [thickness] [angle of attack].")
                if("--scale-from-naca" in sys.argv):
                    try:
                        thickness=float(sys.argv[sys.argv.index("--scale-from-naca")+1])
                        chord=float(sys.argv[sys.argv.index("--scale-from-naca")+2])
                        aoa=float(sys.argv[sys.argv.index("--scale-from-naca")+3])
                        scaleFromNacaFlag=True
                    except:
                        raise Exception("Could not adapt from NACA - wrong arguments. Expected:\n--scale-from-naca [thickness] [chord] [angle of attack].")
                if(adaptToNACAFlag):
                    maxLocalLength = np.max(lcontent[0, :])
                    fullNACALength = findNACALength(thickness, maxLocalLength, aoa, maxLocalLength)
                    for j in range(len(lcontent[0])):
                        lcontent[0, j] = findNACALength(thickness, maxLocalLength, aoa, lcontent[0, j])/fullNACALength
                if(scaleFromNacaFlag):
                    for j in range(len(lcontent[0])):
                        lcontent[0, j] = findLengthfromNACA(thickness, chord, aoa, lcontent[0, j])/chord
                if("--normalise-x" in sys.argv):
                    lcontent[0, :] = (lcontent[0, :]-np.min(lcontent[0, :]))/(np.max(lcontent[0, :])-np.min(lcontent[0, :]))
                if("--normalise-y" in sys.argv):
                    lcontent[1, :] = (lcontent[1, :]-np.min(lcontent[1, :]))/(np.max(lcontent[1, :])-np.min(lcontent[1, :]))
                if("--scale-x" in sys.argv):
                    try:
                        scalar = float(sys.argv[sys.argv.index("--scale-x")+1])
                    except:
                        print("Error: Could not convert x-scaling factor \""+sys.argv[sys.argv.index("--scale-x")+1]+"\" to float.")
                    lcontent[0, :] = lcontent[0, :]*scalar
                if("--scale-y" in sys.argv):
                    try:
                        scalar = float(sys.argv[sys.argv.index("--scale-y")+1])
                    except:
                        print(f"Error: Could not convert x-scaling factor \""+sys.argv[sys.argv.index("--scale-y")+1]+"\" to float.")
                    lcontent[1, :] = lcontent[1, :]*scalar
                print(f"flabels:{flabels[o]}")
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
    pass

if(__name__=="__main__"):
    main()
