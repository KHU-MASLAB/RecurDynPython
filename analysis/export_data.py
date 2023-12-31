from recurdyn import *
import os
import glob
from datetime import datetime
import time

from recurdyn import *
from GlobalVariables import GlobVar
from . import initialize, dispose


def rplt2csv(SolverFilesPath: str):
    """
    Scans and reads all *.rplt files in the SolverFilesAbsPath (recursively scanned).
    Then export values from Var.DataExportTargets in *.csv format.
    :param SolverFilesPath: rplt files directory
    :return:
    """
    application, model_document, plot_document, model = initialize()
    application.CloseAllPlotDocument()
    os.makedirs(SolverFilesPath, exist_ok=True)
    RPLTlist = glob.glob(f"{SolverFilesPath}\\**\\*.rplt", recursive=True)
    datetime.now().strftime("%Y.%m.%d - %H:%M:%S")
    AnalysisStartTime = time.perf_counter()
    for idx_rplt, rplt in enumerate(RPLTlist):
        application.NewPlotDocument("PlotDoc")
        application.OpenPlotDocument(rplt)
        plot_document = application.ActivePlotDocument
        rpltname = os.path.basename(rplt).split(".")[:-1]
        if len(os.path.basename(rplt).split(".")) > 2:
            rpltname = ".".join(os.path.basename(rplt).split(".")[:-1])
        else:
            rpltname = "".join(rpltname)
        DataExportTargets = [
            f"{rpltname}/{target}" for target in GlobVar.DataExportTargets
        ]
        CSVpath = f"{SolverFilesPath}\\{rpltname}.csv"
        plot_document.ExportData(CSVpath, DataExportTargets, True, False, 8)
        application.ClosePlotDocument(plot_document)
        application.PrintMessage(
            f"Data exported {CSVpath} ({idx_rplt + 1}/{len(RPLTlist)})"
        )
        print(f"Data exported({idx_rplt + 1}/{len(RPLTlist)}) {CSVpath} ")
    AnalysisEndTime = time.perf_counter()
    s = AnalysisEndTime - AnalysisStartTime
    print(f"Export finished within {s:.2f}sec.")
