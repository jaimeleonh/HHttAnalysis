import sys, os
import time
import ROOT as r
from ROOT import gSystem
r.gROOT.SetBatch(True)
from subprocess import call
from samples import samples
import plotTools

import argparse
parser = argparse.ArgumentParser(description='Plotter options')
parser.add_argument('-n','--ntuples', action='store_true', default = False)
parser.add_argument('-c','--copy', action='store_true', default = False)
parser.add_argument('-d','--directory', dest='userCopyPath', default = '')
my_namespace = parser.parse_args()

if my_namespace.ntuples == True :
    print ("Starting ntuplizer for every sample in input")
    time.sleep(2)
    r.gInterpreter.ProcessLine(".x loadExampleAnalysis.C")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    gSystem.Load(dir_path + "analysisCode_C.so")
    from ROOT import analysisCode
else : 
  print("Not making ntuples. If you want to make them, restart with 'yes' as first argument ")
  time.sleep(2)

#path = '/eos/home-j/jleonhol/HHbbtautau/2017/'
path = '/eos/home-c/camendol/SKIMS_Thesis2017/'
#path = '/eos/home-c/camendol/SKIMS_Legacy2018/SKIMS_30Jan2020/'
eosPath = '/eos/home-j/jleonhol/HHbbtautau/'
plotPath = './plots/'


categories = ["noSelection","s1b1jresolvedMcut", "s2b0jresolvedMcut", "VBFtight_DNN", "VBFloose_DNN", "sboostedLLMcut", "VBFloose", "VBFtight"]

if my_namespace.userCopyPath == '' : 
  copyPath = '/eos/home-j/jleonhol/www/HHbbtautau/allVBF_2017/'
else : 
  copyPath = my_namespace.userCopyPath

if (my_namespace.copy == True) :
  rc = call('mkdir ' + copyPath, shell=True)
  rc = call('cp -r /eos/home-j/jleonhol/backup/index_HHbbtautau_php ' + copyPath +  '/index.php' , shell=True)
  for cat in categories : 
    rc = call('mkdir ' + copyPath +  '/' + cat + '/' , shell=True)
    rc = call('cp -r /eos/home-j/jleonhol/backup/index_HHbbtautau_php ' + copyPath + '/' + cat + '/index.php' , shell=True)



rc = call('mkdir ' + plotPath, shell=True)
rc = call('mkdir ' + eosPath + '2017/', shell=True)

files = []
files.append("SKIM_VBF_CV_1_C2V_1_C3_1")
files.append("SKIM_VBF_CV_1_5_C2V_1_C3_1")
files.append("SKIM_VBF_CV_1_C2V_1_C3_0")
files.append("SKIM_VBF_CV_1_C2V_1_C3_2")
files.append("SKIM_VBF_CV_1_C2V_0_C3_2")
files.append("SKIM_VBF_CV_1_C2V_2_C3_1")
#files.append("PrivateGluGlu12JetsHHTo2B2Taus2017_SKIM")


#files.append("SKIM_VBFSM")
files.append("SKIM_GGHSM_xs")
#files.append("SKIM_TT_fullyHad")
#files.append("SKIM_Tau2018A")
#files.append( samples[0] )

for fil in files :
#  if fil not in samples : 
#    print ("ERROR: Sample " + fil + " not found. Skipping" )
#    break
  if my_namespace.ntuples == True :
    print ('Obtaining plot ntuples for ' + fil)
    time.sleep(2) 
    if (fil != 'PrivateGluGlu12JetsHHTo2B2Taus2017_SKIM') : analysis = analysisCode(path + fil, eosPath + '2017/' + fil + '.root')
    else : analysis = analysisCode( '/eos/home-j/jleonhol/HHbbtautau/2017/' + fil, eosPath + '2017/' + fil + '.root')
    analysis.Loop()




whatToPlot = []
stuff = ['HH','tauH','tauH_SVFIT','bH','HHsvfit','HHkinsvfit', 'VBFjet1', 'VBFjet2']
variables = ['pt','eta','mass','phi']
for st in stuff : 
  for var in variables : 
    if 'VBFjet' in st and var == 'mass' : continue 
    whatToPlot.append(st+'_'+var)


whatToPlot += ["VBFjj_mass","VBFjj_deltaPhi", "VBFjj_deltaEta", "VBFgenjj_deltaPhi", "VBFjj_deltaR"]
whatToPlot += ["HH_deltaPhi", "HH_deltaEta", "HH_deltaR"]
whatToPlot += ['HHkinsvfit_bHmass','HHsvfit_deltaPhi', 'HHKin_mass_raw', 'HHKin_chi2'] 
whatToPlot += ['VBFjb_deltaR', 'VBFjTau_deltaR']


plottingStuff = { 'lowlimityaxis' : 0,
            'highlimityaxis' : 1,
            'markersize': 1,
	          'yaxistitleoffset': 1.5,
	          'legxlow' : 0.3075 + 1 * 0.1975,
	          #'legxlow' : 0.3075 + 2 * 0.1975,
	          'legylow': 0.75,
	          'legxhigh': 0.9,
	          'legyhigh': 0.9,
	          'markertypedir':{},
	          'markercolordir':{}, 
   	        }   


for plot in whatToPlot : 
  for cat in categories : 
    listOfPlots = []
    for fil in files :
      plotTools.makePlot(listOfPlots, eosPath + '2017/' + fil + '.root', plot+'_'+cat)
    plotTools.combinePlots (listOfPlots, files, plottingStuff, plotPath, plot+'_'+cat) 


    if my_namespace.copy == True: 
      for ext in ['.png','.pdf','.root'] : rc = call('cp ' + plotPath + plot + '_' + cat + ext + ' ' + copyPath + '/' + cat + '/', shell=True)
      print 'Copying ' +  plotPath + plot + '_' + cat + '.* to ' + copyPath + '/' + cat 
  


