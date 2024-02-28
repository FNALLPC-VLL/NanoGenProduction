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
Run VLLs2LLPs_MVLL_MA_CTAU_nanogen_cfg.py to generate events with branches of nanoAOD gen-level information using the created gridpacks. Edit the mVLL, mA and ctau values at the top of the script to match your gridpack. In the example, we are generating 1000 events with mVLL=200 GeV, mA=2 GeV, and ctau=850 mm.
```
cmsRun -n 6 VLLs2LLPs_MVLL_MA_CTAU_nanogen_cfg.py
```
## Check lifetime is generated correctly
Run HistogrammerCtau.py to generate events with nanoAOD gen-level information using the created gridpacks
```
python HistogrammerCtau.py --mvll 200 --ma 2 --ctau 850
```
