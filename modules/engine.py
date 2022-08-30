# engine.py
# This software is meant to be a SGLauncher-compatible
# replacement for cmpdata.py graph engine.

# self made libraries
from matgrapher import grapher
from projectexporter import SGProjectExporter as sgp

# external libraries
import sys
from os.path import exists as path_exists
import numpy as np

def loadProject(project_filename):
    print("Loading data from launcher.")
    if(project_filename[-3:]=="sgp"):
        project = sgp(filename=project_filename)
        return project
    return None

def main():
    project = sgp()
    # file_contents = []
    gr = grapher.grapher()
    if("-p" in sys.argv):
        project = loadProject(sys.argv[sys.argv.index("-p")+1])

    for i in range(len(project)):
        if('.xy' in project.filelist[i]):
            flabels, fcontent = project.readData(filename=project.filelist[i],
                                    separationChar=" ",
                                    returnLabels=True,
                                    lessInfo=True
                )
        if('.txt' in project.filelist[i]):
            #assume, that .txt file also come from ANSYS Fluent
            flabels, fcontent = project.readData(filename=project.filelist[i],
                                    separationChar=" ",
                                    returnLabels=True,
                                    lessInfo=True
                )
        if('.csv' in project.filelist[i]):
            flabels, fcontent = project.readData(filename=project.filelist[i],
                                    separationChar=",",
                                    returnLabels=True,
                                    lessInfo=True
                )
        print("flabels:")
        print(flabels)
        for o in range(len(flabels)):
            hide_label = False
            if(o<len(flabels)-1):
                lcontent = np.asarray(fcontent)[:, flabels[o][0]:flabels[o+1][0]]
                lcontent = lcontent[:,lcontent[0, :].argsort()]
                ycontent = lcontent[1, :]
                xcontent = lcontent[0, :]
                #gr.loadData(fcontent[0][flabels[o][0]:flabels[o+1][0]], fcontent[1][flabels[o][0]:flabels[o+1][0]])
                if(project.isYLogScaleForced()):
                    ycontent = np.absolute(ycontent)
                if(project.isXLogScaleForced()):
                    xcontent = np.absolute(xcontent)
                gr.loadData(xcontent, ycontent)
            else:
                lcontent = np.asarray(fcontent)[:, flabels[o][0]:]
                lcontent = lcontent[:, lcontent[0, :].argsort()]
                ycontent = lcontent[1, :]
                xcontent = lcontent[0, :]
                #lcontent = sorted(lcontent, key=lambda lcontent: int(lcontent[0]))
                if(project.isYLogScaleForced()):
                    ycontent = np.absolute(ycontent)
                if(project.isXLogScaleForced()):
                    xcontent = np.absolute(xcontent)
                gr.loadData(xcontent, ycontent)
            print(f"Is label {project.getLegend(i)} in gr.labels?")
            print(project.getLegend(i) in gr.labels)
            if(project.getLegend(i) in gr.labels):
                hide_label = True
            gr.loadLabels(project.getLegend(i))
            if(len(gr.labels)>1):
                if(hide_label):
                    print(f"Loading label {project.getLegend(i)}")
                    gr.hideLabel(-1)
            print("Loaded labels:")
            print(gr.labels)
            gr.loadLineStyles(project.getLineStyle(i))
            gr.loadColor(project.getLineColor(i))
            gr.changeLineWidth(project.getLineWidth(i))
            gr.changeLineAlpha(project.getLineAlpha(i))
    gr.generateGraph(axis_names=project.getAxisNames(),
                     x_lim=project.getDomainXSize(),
                     y_lim=project.getDomainYSize(),
                     filename=project.getGraphFileName(),
                     graph_title=project.getGraphTitle(decode=False),
                     plot_size=project.getGraphSize(),
                     save=project.getSaveToggle(),
                     show=project.getSaveToggle(False),
                     log_scale=project.getScaleType()
        )
    pass

if __name__=="__main__":
    main()