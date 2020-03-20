# -*- coding: utf-8 -*-
import ROOT as r
from ROOT import gStyle, gROOT
from copy import deepcopy
import sys
from markerColors import markerColors
r.gROOT.SetBatch(True)



############################################# CHANGE IF NECESSARY ###########################################################

#############################################################################################################################

def makePlot(hlist, fileName, plotscaffold):
    res = r.TFile.Open(fileName)
    print (fileName, plotscaffold)
    
    resplot = res.Get(plotscaffold)
    resplot.Scale (1. / resplot.GetEntries() )

    hlist.append(deepcopy(resplot))
    res.Close(); del res, resplot
    return

def combinePlots (hlist, legends, plottingStuff, path, savescaffold): 
    print "Combining list of plots"
    if len(hlist) == 0: raise RuntimeError("Empty list of plots")
    c   = r.TCanvas("c", "c", 800, 800)

    gStyle.SetOptStat(0)
    leg = r.TLegend(plottingStuff['legxlow'], plottingStuff['legylow'], plottingStuff['legxhigh'], plottingStuff['legyhigh'])
    for iplot in range(len(hlist)):
        hlist[iplot].SetMarkerColor(markerColors[iplot])
        #hlist[iplot].SetMarkerColor(plottingStuff['markercolordir'][hlist[iplot].GetName()])
        hlist[iplot].SetLineColor(markerColors[iplot])
        #hlist[iplot].SetLineColor(plottingStuff['markercolordir'][hlist[iplot].GetName()])
        hlist[iplot].SetMarkerStyle(20)
        #hlist[iplot].SetMarkerStyle(plottingStuff['markertypedir'][hlist[iplot].GetName()])
        leg.AddEntry(hlist[iplot], legends[iplot], "PL")
        hlist[iplot].Draw("same")
        #hlist[iplot].Draw("P" + (iplot == 0) * "A" + (iplot != 0) * "same")

    leg.Draw()
   
    r.gPad.Update()
    #hlist[0].GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'], plottingStuff['highlimityaxis'])
    
    firsttex = r.TLatex()
    firsttex.SetTextSize(0.03)
    firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{CMS} Preliminary")
    firsttex.Draw("same");

    secondtext = r.TLatex()
    toDisplay = r.TString()
    toDisplay  = r.TString("60.0 fb^{-1} 13 TeV")
    secondtext.SetTextSize(0.035)
    secondtext.SetTextAlign(31)
    secondtext.DrawLatexNDC(0.90, 0.91, toDisplay.Data())
    secondtext.Draw("same")


    #c.SetLogy()
    c.SaveAs(path + savescaffold + ".png")
    c.SaveAs(path + savescaffold + ".pdf")
    c.SaveAs(path + savescaffold + ".root")
    c.Close(); del c






if __name__ == '__main__':
  main()
