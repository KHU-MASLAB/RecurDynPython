# RecurDyn ProcessNet with Python
> Automates RecurDyn operations with ProcessNet and Python.  
For initial setups, please follow this [link](http://www.safetyman.kr/processnet-python-%ec%82%ac%ec%9a%a9%eb%b2%95/) (Korean).    
For official tutorials provided by FunctionBay Inc., refer to this [link](https://www.youtube.com/watch?v=QjCFDidGmHo) (Korean).


### Detailed instructions are provided in [Tutorial.ipynb](https://github.com/hyeonbeenlee/RecurDynPython/blob/main/Tutorial.ipynb)
### For useful tips, check out [Tips.md](https://github.com/hyeonbeenlee/RecurDynPython/blob/main/Tips.md) (Korean)
# Setup
Set `rdSolverDir` to `"<YOUR_RECURDYN_INSTALL_DIR>\Bin\Solver\RDSolverRun.exe"` in [GlobalVariables.py](https://github.com/hyeonbeenlee/RecurDynPython/blob/main/GlobalVariables.py).

# Simulate using GUI solver
![gui_demo](https://github.com/hyeonbeenlee/RecurDynPython/assets/78078652/fc98aef7-bc89-43e6-9415-4245846be155)

Call `analysis.doe_gui.RunDOE_GUI` with arguments.  
**You can modify DOE scenario by editing line 56~65 in [analysis/doe_gui.py](https://github.com/hyeonbeenlee/RecurDynPython/blob/main/analysis/doe_gui.py)`**  
This method is **_not parallelizable_**.

#### Arguments

- `ModelFileDir: str` Absolute path of model file (\*.rdyn).
- `TopFolderName: str` Folder name to create at `ModelFileDir`.
  - Each of simulation results will be saved in this folder.
- `NumCPUCores: int` Number of CPU threads to use per simulation.
  - Must be one of `[0(Auto),1,2,4,8,16]`.
- `EndTime: float` Simulation end time.
- `NumSteps: int` Number of time steps.

```
RunDOE_GUI(
    ModelFileDir=f"{os.getcwd()}/SampleModel.rdyn",
    TopFolderName="TestDOE_GUI",
    NumCPUCores=8,
    EndTime=1,
    NumSteps=100,
)
```

# Simulate using batch solver
> This method is far more stable and parallelizable compared to GUI solvers.  
> It is highly recommended to run DOEs using batch solvers, especially you're handling large, complex model.

![batch_demo](https://github.com/hyeonbeenlee/RecurDynPython/assets/78078652/62b8ddea-f3a2-438a-a322-77b9e1c2b7ec)

Call `analysis.doe_batch.RunDOE_Batch` with arguments.  
**You can control DOE scenario by editing line 59~67 in [analysis/doe_batch.py](https://github.com/hyeonbeenlee/RecurDynPython/blob/main/analysis/doe_batch.py)**  
This method is **_parallelizable_**, but consumes **corresponding number of RecurDyn licenses**.

#### Arguments

- `ModelFileDir: str` Absolute path of model file (\*.rdyn).
- `TopFolderName: str` Folder name to create at `ModelFileDir`.
  - Each of simulation results will be saved in this folder.
- `NumCPUCores: int` Number of CPU threads to use per simulation.
  - Must be one of `[0(Auto),1,2,4,8,16]`.
- `EndTime: float` Simulation end time.
- `NumSteps: int` Number of time steps.
- `NumParallelBatches: int` Number of parallelized DOE runners (\*.bat) to create. 
  - The total number of simulations of your DOE will be splited by ```NumParallelBatches```. For example, if you define DOE with 100 simulations and set this argument to `4`, `RunDOE_Batch` will configure `4` parallelized DOE runners with each of them containing 25 simulations.
- `NumBatRunsOnThisPC: int` Number of runners to immediately execute on your current machine. Defaults to `NumParallelBatches`. Value should be within range of [`0`, `NumParallelBatches`].
  - This argument is configured to run DOE on multiple machines. Comprehensively, if you set `NumParallelBatches` to 10 and set `NumBatRunsOnThisPC` to 3, only the first 3 runners (\*.bat) are executed immediately on current machine. You can transfer rest of the `7` runners with corresponding subfolders (which contains `*.rmd` and `*.rss` + $\alpha$ files) in `ModelFileDir` to other machines and execute them by hand. In this case, you need additional processing to modify RecurDyn solver path defined in runner files.
```
RunDOE_Batch(
    ModelFileDir=f"{os.getcwd()}/SampleModel.rdyn",
    TopFolderName="TestDOE_Batch",
    NumCPUCores=8,
    EndTime=1,
    NumSteps=100,
    NumParallelBatches=5,
)
```

#### Export data from results using `analysis.export_data.rplt2csv`

Numeric simulation results are stored in `*.rplt` format.  
Variable names should be exactly the same to the ones in the `*.rplt`.  
To explicitly check variable names, simply import `*.rplt` file on RecurDyn GUI.
Variables to be exported are defined in `GlobalVariables.GlobVar.DataExportTargets`.  

```
rplt2csv(f"{os.getcwd()}/TestDOE_Batch")
```

The function will recursively scan for all `*.rplt` files in the argument directory, and export variables in `DataExportTargets` in `*.csv` format.
