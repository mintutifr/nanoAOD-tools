#!/usr/bin/env python
import os, sys
import ROOT
def get_histogram(self, name):
    """Return the histogram identified by name from the file.
    """
    # The TFile::Get() method returns a pointer to an object stored in a ROOT file.
    hist = self.file.Get(name)
    if hist:
        return hist
    else:
        raise RuntimeError('Unable to retrieve histogram named {0} from {1}'.format(name, self.filename))


inFile1 = ROOT.TFile.Open ( "b_from_top_Tchannel.root" ," READ ")
inFile2 = ROOT.TFile.Open ( "b_from_top_Tbarchannel.root" ," READ ")

hist1 = nFile1.Get('Histograms/eta_hist')
hist2 = nFile2.Get('Histograms/eta_hist')

    hist.Draw()
    canvas.SaveAs('plot.pdf')
