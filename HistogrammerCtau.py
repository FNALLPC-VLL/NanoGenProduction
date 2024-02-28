import ROOT
from ROOT import TFile, TTree, TMath
import sys
import os
import argparse
import math

def ctau(pt,m,eta,vx,vy,vz):
    ct =TMath.Sqrt(vx*vx + vy*vy + vz*vz) * m /(pt*TMath.CosH(eta) )
    return ct
def v(vx,vy,vz):
    v =TMath.Sqrt(vx*vx + vy*vy + vz*vz)
    return v

def reweightcalculator(lenghtrf,oldctau,newctau):
    k        = float(oldctau)/float(newctau)
    alpha    = (lenghtrf)*(  1/float(newctau) - 1/float(oldctau)   )
    reweight = k*k*math.exp( -alpha   )
    return reweight

def Looper(inputfilename,outputfilename):
    #File preparation
    ftmp       = ROOT.TFile.Open("%s.root"%(inputfilename) )
    t          = ftmp.Get('Events')

    #Outputfile
    tmp        = ROOT.TFile.Open("histograms/histos_%s.root"%outputfilename,'RECREATE')

    #Histograms
    h_llp_ctau = ROOT.TH1F("h_llp_ctau","h_llp_ctau",30,0,300)
    h_llp_l    = ROOT.TH1F("h_llp_l","h_llp_l",40,0,10000)
    h_llp_pt   = ROOT.TH1F("h_llp_pt","h_llp_pt",40,0,400)
    h_llp_eta  = ROOT.TH1F("h_llp_eta","h_llp_eta",12,-3.0,3.0)

    #Loop over events
    for e in range(0, t.GetEntries()):
            t.GetEntry(e)
            #Find all possible mothers 
            llp_idx = []
            npart = t.nGenPart    
            for k in range(0,npart):
                part_id = t.GenPart_pdgId[k]
                part_status = t.GenPart_status[k]
                if abs(part_id) == 5000001:
                    llp_idx.append(k)
            #Find the daugthers and mother idxs 
            wllp_idxs=[]
            for j in range(0,npart):
                #Find ws
                w_id  = t.GenPart_pdgId[j]
                w_status = t.GenPart_status[j]
                if abs(w_id) == 5000001: continue
                #Find the llp mother
                w_motheridx  = t.GenPart_genPartIdxMother[j]
                for x in range(0,len(llp_idx)):
                   if llp_idx[x]==w_motheridx:   
                    wllp_idxs.append( [j,w_motheridx] )
            #Check if found a pair
            if len(wllp_idxs)!=4: continue   
            #loop over llp daugthers(photons)
            iscsc  =False
            isdt   =False
            l_1    = 0
            l_3    = 0
            ctau_1 = 0
            ctau_3 = 0
            pt_1   = 0
            pt_3   = 0
            eta_1  = 0
            eta_3  = 0
            for x in range(0,len(wllp_idxs)):
                 pt0  = t.GenPart_pt[wllp_idxs[x][0]] 
                 m0   = t.GenPart_mass[wllp_idxs[x][0]] 
                 eta0 = t.GenPart_eta[wllp_idxs[x][0]] 
                 v0   = v(t.GenPart_vx[wllp_idxs[x][0]],t.GenPart_vy[wllp_idxs[x][0]],t.GenPart_vz[wllp_idxs[x][0]])
                 pt1  = t.GenPart_pt[wllp_idxs[x][1]] 
                 m1   = t.GenPart_mass[wllp_idxs[x][1]] 
                 eta1 = t.GenPart_eta[wllp_idxs[x][1]] 
                 v1   = v(t.GenPart_vx[wllp_idxs[x][1]],t.GenPart_vy[wllp_idxs[x][1]],t.GenPart_vz[wllp_idxs[x][1]])
                 dx  = abs(t.GenPart_vx[wllp_idxs[x][0]]-t.GenPart_vx[wllp_idxs[x][1]]) 
                 dy  = abs(t.GenPart_vy[wllp_idxs[x][0]]-t.GenPart_vy[wllp_idxs[x][1]]) 
                 dz  = abs(t.GenPart_vz[wllp_idxs[x][0]]-t.GenPart_vz[wllp_idxs[x][1]])
                 dr   = math.sqrt(  dx*dx + dy*dy )
                 if x==1: 
                     ctau_1 = ctau(pt1,m1,eta1,dx,dy,dz)
                     l_1    = v(dx,dy,dz)
                     pt_1   = pt1
                     eta_1  = eta1
                 if x==3: 
                     ctau_3 = ctau(pt1,m1,eta1,dx,dy,dz)
                     l_3    = v(dx,dy,dz)
                     pt_3   = pt1
                     eta_3  = eta1
            #histograms
            h_llp_ctau.Fill(ctau_1)
            h_llp_l.Fill(l_1)
            h_llp_pt.Fill(pt_1)
            h_llp_eta.Fill(eta_1)
            h_llp_ctau.Fill(ctau_3)
            h_llp_l.Fill(l_3)
            h_llp_pt.Fill(pt_3)
            h_llp_eta.Fill(eta_3)

    #Close the input your file
    ftmp.Close()
    #Close your output file
    tmp.Write()
    tmp.Close()

###########OPTIONS
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--mvll',    dest='mvll',  help='Mass of the vll', required = True)
parser.add_argument('--ma',      dest='ma',    help='Mass of the a', required = True)
parser.add_argument('--ctau',    dest='ctau',  help='Mass of the ctau (mm)', required = True)
args           = parser.parse_args()
mvll           = args.mvll
ma             = args.ma
actau          = args.ctau

#What signals
signals = [ 
    ['VLLs2LLPs_MVLL_%s_MA_%s_CTAU_%s'%(mvll,ma,actau)],
]

os.system("mkdir histograms")
for k in range (0,len(signals) ):
    print "[INFO] Looping over "+signals[k][0]
    Looper(signals[k][0],signals[k][0])
    print "[INFO] Done with "+signals[k][0]