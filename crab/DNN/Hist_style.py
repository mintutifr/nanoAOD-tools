import ROOT as rt
import numpy as np

"""def getregion_tag(region="2J1T",x1=2, y1=0.91, x2=3, y2=205):
        cntrl = rt.TPaveText(x1,y1,x2,y2)
        cntrl.SetFillStyle(0)
        cntrl.SetBorderSize(0)
        cntrl.SetMargin(0)
        cntrl.SetTextFont(42)
        cntrl.SetTextSize(0.05)
        cntrl.SetTextAlign(33)
        cntrl.AddText(region)
        return cntrl"""

def getregion_tag(region="2J1T",x1=0.25, y1=0.82, x2=0.28, y2=0.84):
        cntrl = rt.TPaveText(x1,y1,x2,y2,"brNDC")
        cntrl.SetFillStyle(0)
        cntrl.SetBorderSize(0)
        cntrl.SetMargin(0)
        cntrl.SetTextFont(42)
        cntrl.SetTextSize(0.05)
        cntrl.SetTextAlign(33)
        cntrl.AddText(region)
        return cntrl


def getCMSpre_tag(x1=0.385, y1=0.86, x2=0.495, y2=0.88):
        cntrl = rt.TPaveText(x1,y1,x2,y2,"brNDC")
        cntrl.SetFillStyle(0)
        cntrl.SetBorderSize(0)
        cntrl.SetMargin(0)
        cntrl.SetTextFont(42)
        cntrl.SetTextSize(0.05)
        cntrl.SetTextAlign(33)
        cntrl.AddText("#bf{CMS} #it{Preliminary}")
        return cntrl
def add_cms_prelim(ax, xpos=0.95, ypos=0.95, fontsize=12, ha="left", va="top"):
    ax.text(
        xpos, ypos,
        r"$\bf{CMS}$ $\it{Preliminary}$",
        transform=ax.transAxes,
        ha=ha, va=va,
        fontsize=fontsize
    )
def getCMSIntrenal_tag(x1=0.385, y1=0.86, x2=0.495, y2=0.88):
        cntrl = rt.TPaveText(x1,y1,x2,y2,"brNDC")
        cntrl.SetFillStyle(0)
        cntrl.SetBorderSize(0)
        cntrl.SetMargin(0)
        cntrl.SetTextFont(42)
        cntrl.SetTextSize(0.045)
        cntrl.SetTextAlign(33)
        cntrl.AddText("#bf{CMS} #it{Internal}")
        # cntrl.AddText("#bf{CMS} #it{Work in progress}")
        return cntrl

def leptonjet_tag(lep="mu",x1=0.25, y1=0.82, x2=0.28, y2=0.84):
        cntrl = rt.TPaveText(x1,y1,x2,y2,"brNDC")
        cntrl.SetFillStyle(0)
        cntrl.SetBorderSize(0)
        cntrl.SetMargin(0)
        cntrl.SetTextFont(42)
        cntrl.SetTextSize(0.05)
        cntrl.SetTextAlign(33)
        if(lep=="mu"):cntrl.AddText("#it{#mu+jets},2J1T")
        if(lep=="el"):cntrl.AddText("#it{e+jets},2J1T")
        return cntrl
def add_leptonjet_tag(ax, lep="mu",xpos=0.95, ypos=0.95, fontsize=12, ha="left", va="top"):
    if(lep=="mu"):
        label_text = r"$\it{\mu+jets}$,2J1T"
    elif(lep=="el"):
        label_text = r"$\it{e+jets}$,2J1T"
    ax.text(
        xpos, ypos,
        label_text,
        transform=ax.transAxes,
        ha=ha, va=va,
        fontsize=fontsize
    )
def year_tag(dataYear="UL2016preVFP",x1=0.948, y1=0.8555, x2=0.95, y2=0.84):
        cntrl = rt.TPaveText(x1,y1,x2,y2,"brNDC")
        cntrl.SetFillStyle(0)
        cntrl.SetBorderSize(0)
        cntrl.SetMargin(0)
        cntrl.SetTextFont(42)
        cntrl.SetTextSize(0.035)
        cntrl.SetTextAlign(33)
        if(dataYear=="UL2016preVFP" or dataYear=="ULpreVFP2016"): cntrl.AddText("19.5 fb^{-1} (13 TeV, 2016preVFP)")
        if(dataYear=="UL2016postVFP" or dataYear=="ULpostVFP2016"): cntrl.AddText("16.8 fb^{-1} (13 TeV, 2016postVFP)")
        if(dataYear=="UL2017"): cntrl.AddText("41.5 fb^{-1} (13 TeV, 2017)")
        if(dataYear=="UL2018"): cntrl.AddText("59.8 fb^{-1} (13 TeV, 2018)")
        return cntrl

def add_year_tag(ax, dataYear="UL2018",xpos=0.95, ypos=0.95, fontsize=12, ha="left", va="top"):
    if(dataYear=="UL2016preVFP" or dataYear=="ULpreVFP2016"): label_text = r"19.5 $fb^{-1}$ (13 TeV, 2016preVFP)"
    if(dataYear=="UL2016postVFP" or dataYear=="ULpostVFP2016"): label_text = r"16.8 $fb^{-1}$ (13 TeV, 2016postVFP)"
    if(dataYear=="UL2017"): label_text = r"41.5 $fb^{-1}$ (13 TeV, 2017)"
    if(dataYear=="UL2018"): label_text = r"59.8 $fb^{-1}$ (13 TeV, 2018)"
    ax.text(
        xpos, ypos,
        label_text,
        transform=ax.transAxes,
        ha=ha, va=va,
        fontsize=fontsize
    )
