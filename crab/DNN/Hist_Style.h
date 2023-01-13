THStack *Hist_Style(THStack *h, TString xtitle, TString ytitle, Style_t LFont=42,float ymaxRange=0.0){
  //h->SetMarkerColor(kBlack);
  //h->SetLineColor(kBlack);
  //  h->SetMarkerStyle(4);
  //  h->SetMarkerSize(0.7);
  h->SetTitle("");
  //h->GetXaxis()->SetTitle(xtitle);
  h->GetXaxis()->SetLabelFont(LFont);
  h->GetXaxis()->SetLabelSize(0.0);
  h->GetXaxis()->SetTitleSize(0.02);
  h->GetXaxis()->SetTitleFont(6);
//  h->GetXaxis()->CenterTitle(true);
//  h->GetXaxis()->SetNdivisions(507);
//  h->GetXaxis()->SetRangeUser(0.0, 2.0);
  
  h->GetYaxis()->SetTitle(ytitle);
  h->GetYaxis()->SetLabelFont(LFont);
  h->GetYaxis()->SetLabelSize(0.025);
  h->GetYaxis()->SetTitleSize(0.05);
  h->GetYaxis()->SetTitleOffset(0.8);
  h->GetYaxis()->SetTitleFont(42);
  TAxis* a = h->GetYaxis();
  a->SetNdivisions(15);
  a->SetTickSize(0.01);
  TAxis* b = h->GetXaxis();
  b->SetNdivisions(10);
  b->SetTickSize(0.01);
 // h->GetYaxis()->SetRangeUser(0,ymaxRange);
//  h->GetYaxis()->CenterTitle(true);
//  h->GetYaxis()->SetNdivisions(507);
    h->SetMaximum(ymaxRange);
	h->SetMinimum(0.001);
  //  h->GetZaxis()->SetLabelFont(LFont);
  //  h->GetZaxis()->SetLabelSize(0.035);
  //  h->GetZaxis()->SetTitleSize(0.035);
  //  h->GetZaxis()->SetTitleFont(42);
  THStack *hnew = (THStack*)h->Clone("new");
  return hnew;
}

void CMSTEXT_variable(string year="2016",string region="2J1T", string lepton_flv="mu",bool mtwcut=false,bool BDTcut=false,bool tch_Alternatemass=false,bool preliminary_tag=true){

        TPaveText* cntrl0;
	if(mtwcut==true) cntrl0 = new TPaveText(0.23, 0.950, 0.36, 0.96, "brNDC");
	else if(mtwcut!=true) cntrl0 = new TPaveText(0.1, 0.91, 0.16, 0.935, "brNDC");
      	cntrl0->SetFillStyle(0);
      	cntrl0->SetBorderSize(0);
      	cntrl0->SetMargin(0);
      	cntrl0->SetTextFont(42);
      	cntrl0->SetTextSize(0.03);
      	cntrl0->SetTextAlign(33);
      	if(region=="2J1T" && mtwcut==true && BDTcut==true) cntrl0->AddText("2J1T");// , I_{rel} > 0.2 "); // #slash{p}_{T} > 30 GeV");
	if(region=="2J1T" && mtwcut==true) cntrl0->AddText("2J1T , m_{T}^{W}> 50 GeV");//, BDT>0.8 ");
	else if(region=="2J0T" && mtwcut==true) cntrl0->AddText("2J0T , m_{T}^{W}> 50 GeV");
	else if(region=="3J1T" && mtwcut==true) cntrl0->AddText("3J1T , m_{T}^{W}> 50 GeV");
	else if(region=="3J2T" && mtwcut==true) cntrl0->AddText("3J2T , m_{T}^{W}> 50 GeV");
	else if(region=="2J1T" && mtwcut!=true) cntrl0->AddText("2J1T");
	else if(region=="2J0T" && mtwcut!=true) cntrl0->AddText("2J0T");
	else if(region=="3J1T" && mtwcut!=true) cntrl0->AddText("3J1T");
	else if(region=="3J2T" && mtwcut!=true) cntrl0->AddText("3J2T");
        cntrl0->Draw();

	TPaveText* cmstext ;
	if(preliminary_tag) cmstext = new TPaveText(0.4385, 0.86, 0.485, 0.88, "brNDC");
	else cmstext = new TPaveText(0.21, 0.86, 0.235, 0.88, "brNDC");
      	cmstext->SetFillStyle(0);
      	cmstext->SetBorderSize(0);
      	cmstext->SetMargin(0);
      	cmstext->SetTextFont(42);
      	cmstext->SetTextSize(0.05);
      	cmstext->SetTextAlign(33);
      	if(preliminary_tag) cmstext->AddText("#bf{CMS} #it{Preliminary}");
		else cmstext->AddText("#bf{CMS}");
		((TText*)cmstext->GetListOfLines()->Last())->SetTextFont(42);
		cmstext->Draw();

        TPaveText* finalstat = new TPaveText(0.305, 0.82, 0.338, 0.84, "brNDC");
      	finalstat->SetFillStyle(0);
      	finalstat->SetBorderSize(0);
      	finalstat->SetMargin(0);
      	finalstat->SetTextFont(42);
      	finalstat->SetTextSize(0.05);
      	finalstat->SetTextAlign(33);
      	if(lepton_flv=="mu") finalstat->AddText(Form("#mu +""#it{ jets}"));
		else if(lepton_flv=="el") finalstat->AddText(Form("#it{e + jets}"));
		else finalstat->AddText(Form("#it{l^{#pm} + jets}"));
		((TText*)cmstext->GetListOfLines()->Last())->SetTextFont(42);
		finalstat->Draw();

	TPaveText* lumitext;
	if(tch_Alternatemass && mtwcut) lumitext = new TPaveText(0.7355, 0.950,0.7555, 0.96, "brNDC");
	else if(tch_Alternatemass==false && mtwcut) lumitext = new TPaveText(0.8355, 0.91,0.9, 0.955, "brNDC");
	else if(tch_Alternatemass==false && mtwcut==false) lumitext = new TPaveText(0.8355, 0.91,0.9, 0.955, "brNDC");
      	lumitext->SetFillStyle(0);
      	lumitext->SetBorderSize(0);
      	lumitext->SetMargin(0);
      	lumitext->SetTextFont(42);
      	lumitext->SetTextSize(0.03);
      	lumitext->SetTextAlign(33);
        if(year=="ULpreVFP2016"){lumitext->AddText("19.5 fb^{-1} (13 TeV, 2016preVFP)");((TText*)lumitext->GetListOfLines()->Last())->SetTextFont(42);}
        if(year=="ULpostVFP2016"){lumitext->AddText("16.8 fb^{-1} (13 TeV, 2016postVFP)");((TText*)lumitext->GetListOfLines()->Last())->SetTextFont(42);}
        if(year=="UL2017"){lumitext->AddText("41.5 fb^{-1} (13 TeV, 2017)");((TText*)lumitext->GetListOfLines()->Last())->SetTextFont(42);}
	lumitext->Draw();
}
