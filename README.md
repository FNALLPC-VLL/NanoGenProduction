# NanoGen Generation

Here is described how to generate events including gridpacks for the VLL UFO model (or similar). These instructions were prepared for the LPC machines but it should also work on lxplus.

## GridPack Generation
Create your gridpack following this repository: https://github.com/danielguerrero/UFOModelGeneration.git

## Setup scripts
Get scripts to generated events and analyze them
```
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src
cmsenv
git clone https://github.com/FNALLPC-VLL/NanoGenProduction.git
cd NanoGenProduction
```
## Event Generation
Run VLLs2LLPs_MVLL_X_MA_X_CTAU_X_nanogen_cfg.py to generate events with nanoAOD gen-level information using the created gridpacks
```
Here add instructions
```
## Check lifetime is generated correctly
Run HistogrammerCtau.py  to generate events with nanoAOD gen-level information using the created gridpacks
```
Here add instructions
```
