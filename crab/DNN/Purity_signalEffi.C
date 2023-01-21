/* This file plot the signal efficiency and the putity changes with the BDT variable*/
/* root -l 'Purity_signalEffi.C(1)' */

#include<iostream>
using namespace std;

#include"TCanvas.h"
#include "TH1D.h"
#include "TGaxis.h"
#include "TH2D.h"
#include "Hist_Style.h"

void Purity_signalEffi(string lep,string year){
        TString lepton;
	TString Channel;
	std::vector<std::string> channel;
        channel.push_back("Tchannel"); //0
        channel.push_back("Tbarchannel"); //1
        channel.push_back("tw_top"); //2
        channel.push_back("tw_antitop");//3
        channel.push_back("Schannel");//4
        channel.push_back("ttbar_SemiLeptonic");//5
        channel.push_back("ttbar_FullyLeptonic");//6
        channel.push_back("WJetsToLNu_0J");//7
        channel.push_back("WJetsToLNu_1J");//8
        channel.push_back("WJetsToLNu_2J");//9
        channel.push_back("DYJets");//10
        channel.push_back("WWTo2L2Nu");//11
        channel.push_back("WZTo2Q2L");//12
        channel.push_back("ZZTo2Q2L");//13
        channel.push_back("Data"+year+"_2J1T0");//14



	TString x_double = "topMass";
        TString y_double = "Events/20";
        TString brch = "TMath::Log(topMass)";                        //variable to get the signal and backgroung yeild
        Float_t l_bin=TMath::Log(100.0);
        Float_t mx_bin=TMath::Log(400.0);
        Float_t Nu_bin=30;


        /*TString y_double = "Events/20";
        TString brch = "topMass";                        //variable to get the signal and backgroung yeild 
        Float_t l_bin=100.0;
        Float_t mx_bin=400.0;
        Float_t Nu_bin=30;*/


	TTree *tree[int(channel.size())];//cout<<channel.size()<<endl;
        TH1F* h[int(channel.size())];
        TH1F* h_WoAssi[2];
        TString original_file,DNN_output_file;
        TFile* MCIso[int(channel.size())];
        double NonQCDScale_mtwFit, QCDScale_mtwFit;
        TString orignal_file_dir,DNN_file_dir;

        if(lep=="mu"){ lepton = "Muon"; }
        if(lep=="el"){ lepton = "Electron";}

        if(year == "ULpreVFP2016"){
                orignal_file_dir = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/";
                DNN_file_dir = "DNN_output_without_mtwCut/Apply_all/"+year;
                if(lep=="mu"){
                        QCDScale_mtwFit = 10991.0;
                        NonQCDScale_mtwFit = 231378.0;
                }
                if(lep=="el"){
                        QCDScale_mtwFit = 6892.0;
                        NonQCDScale_mtwFit = 146947.0;
                }
        }
        if(year == "ULpostVFP2016"){
                orignal_file_dir = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/";
                DNN_file_dir = "DNN_output_without_mtwCut/Apply_all/"+year;
                if(lep=="mu"){
                        QCDScale_mtwFit = 11457.0;
                        NonQCDScale_mtwFit = 209030.0;
                }
                if(lep=="el"){
                        QCDScale_mtwFit = 12848.0;
                        NonQCDScale_mtwFit = 122089.0;
                }
        }
        if(year == "UL2017"){
                orignal_file_dir = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/";
                DNN_file_dir = "DNN_output_without_mtwCut/Apply_all/"+year;
                if(lep=="mu"){
                        QCDScale_mtwFit = 30145.0;
                        NonQCDScale_mtwFit = 472746.0;
                }
                if(lep=="el"){
                        QCDScale_mtwFit = 7509.0;
                        NonQCDScale_mtwFit = 315426.0;
                }
        }

	for(unsigned int ll=0; ll<channel.size(); ll++){     //get channel
                Channel=channel.at(ll);
                if(Channel!="Data"+year+"_2J1T0"){
                        original_file = orignal_file_dir+"2J1T1/Minitree_"+Channel+"_2J1T1_"+lep+".root";
                        DNN_output_file = DNN_file_dir+"_"+Channel+"_Apply_all_"+lep+".root";
                        cout<<original_file<<endl;
                        cout<<DNN_output_file<<endl;
                }
                else{
                        original_file = orignal_file_dir+"2J1T0/Minitree_"+Channel+"_"+lep+".root";
                        DNN_output_file = DNN_file_dir+"_QCD_Apply_all_"+lep+".root";
                        cout<<original_file<<endl;
                        cout<<DNN_output_file<<endl;
                }
                MCIso[ll] =new  TFile(original_file,"Read");
                cout<<"tree["<<ll<<"]="<<Channel<<endl;
                tree[ll]=(TTree*)MCIso[ll]->Get("Events");
                tree[ll]->AddFriend ("Events",DNN_output_file);
                //tree[ll]->Print();
	}
		

	
	std::ostringstream histogramNameStream1 (std::ostringstream::ate);    //define a array of histogram
	for(int n=0;n<int(channel.size());n++){
                histogramNameStream1.str("h");
                std::string s = std::to_string(n);
                histogramNameStream1 <<n;
                h[n] = new TH1F( histogramNameStream1.str().c_str() ,brch, Nu_bin, l_bin, mx_bin);
                h[n]->Sumw2();
                histogramNameStream1.clear();
                if(n<2){
                        histogramNameStream1.str("h_WoAssi");
                        std::string s = std::to_string(n);
                        histogramNameStream1 <<n;
                        h_WoAssi[n] = new TH1F( histogramNameStream1.str().c_str() ,brch, Nu_bin, l_bin, mx_bin);
                        h_WoAssi[n]->Sumw2();
                        histogramNameStream1.clear();
                }
        }
			
	
	TString MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)";       
        TString Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"; 
    
        for(unsigned int ll=0; ll<channel.size(); ll++){                   //projeting histogram  
                Channel=channel.at(ll);
                std::ostringstream kk;
                kk << ll;
                std::string k("h"+kk.str());
	        std::string k_WoAssi("h_WoAssi"+kk.str());
                if(Channel=="Tchannel" || Channel=="Tbarchannel"){ 
                        tree[ll]->Project(k.c_str(),brch,MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)");
                        //cout<<Channel<<"; Entries = "<<tree[ll]->GetEntriesFast()<<endl;
                        h[ll]->Print();
                        
                        tree[ll]->Project(k_WoAssi.c_str(),brch,MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)");
                        h_WoAssi[ll]->Print();
                }
                else if(Channel!="Data"+year+"_2J1T0"){ 
                        tree[ll]->Project(k.c_str(),brch,MCcut);
                        //cout<<"h["<<ll<<"] = "<<h[ll]->Integral()<<" "<<Channel<<"; Entries = "<<tree[ll]->GetEntriesFast()<<endl;}
                        h[ll]->Print();
                }
                else{ 
                        tree[ll]->Project(k.c_str(),brch,Datacut);
                        //cout<<"h["<<ll<<"]="<<h[ll]->Integral()<<" "<<Channel<<"; Entries = "<<tree[ll]->GetEntriesFast()<<endl;
                        h[ll]->Print();
                }
                //cout<<"tree["<<ll<<"]="<<Channel<<endl;
        }

    
	TH1F *htemp = new TH1F( "htemp","htemp" , Nu_bin, l_bin, mx_bin);   
        cout<<"for total Non-QCD events adding ...... "<<endl;
	for(int i=0;i<channel.size()-1;i++){                                       // SF  calculation for MC
            cout<<channel.at(i)<<", ";
	    htemp->Add(h[i]);
            if(i<2) htemp->Add(h_WoAssi[i]);
        }
        cout<<endl;
        

        double MCSF=0.0 , QCDSF=0.0;
        MCSF=(NonQCDScale_mtwFit/(htemp->Integral()));
        cout<<"htemp->Integral() = "<<htemp->Integral()<<endl;
        cout<<"h[-1]->Integral() = "<<h[channel.size()-1]->Integral()<<"; tree[-1]->GetEntriesFast( = "<<tree[channel.size()-1]->GetEntriesFast()<<endl;
	QCDSF=(QCDScale_mtwFit/(h[channel.size()-1]->Integral()));// SF caluclation for the QCDyeild estimation
        cout<<"QCDSF = "<<QCDSF<<"; MCSF = "<<MCSF<<endl;
        cout<<"MCSF="<<MCSF<<endl; cout<<" QCDSF="<< QCDSF<<endl;
	//htemp->Reset();	
	
	double signalYield_before_cut=0;
	double bkgYield_before_cut=0;

	for(int i=0;i<channel.size();i++){
	        if(i!=channel.size()-1){
                        h[i]->Scale(MCSF);
                        if(i<2) h_WoAssi[i]->Scale(MCSF);
                }
	        else h[i]->Scale(QCDSF);

                if(i<2){
                        signalYield_before_cut += h[i]->Integral();
                        //signalYield_before_cut += h_WoAssi[i]->Integral();
                        bkgYield_before_cut += h_WoAssi[i]->Integral();
                }
	        else bkgYield_before_cut += h[i]->Integral();
                //h[i]->Reset();
        }
        cout<<"signalYield_before_cut = "<<signalYield_before_cut<<"; bkgYield_before_cut = "<<bkgYield_before_cut<<endl;
	for(int k=0;k<channel.size();k++){                                // clear histogram for next loop
                if(k<2){ 
                        h[k]->Print();
                        h_WoAssi[k]->Print();
                        h_WoAssi[k]->Reset();
                        h[k]->Reset();
                }
                else{
                        h[k]->Print();
                        h[k]->Reset();
                }
        }
	


	unsigned int l = 11;
        Float_t x1[l];
        Float_t y1[l];
	Float_t F1x[l];
        Float_t F1y[l];
	for(unsigned int i=0;i<l;i++){x1[i]=0;y1[i]=0;F1x[i]=0;F1y[i]=0;}
        TGraph *puritygr = new TGraph(l,x1,y1);
	TGraph *F1factorgr = new TGraph(l,F1x,F1y);
	TMultiGraph *mg = new TMultiGraph();
        TMultiGraph *mg2 = new TMultiGraph();

	Double_t sx[l]; 
   	Double_t sy[l];
   	Double_t bx[l]; 
   	Double_t by[l];
	for(unsigned int i=0;i<l;i++){sx[i]=0;sy[i]=0;bx[i]=0;by[i]=0;} 
	TGraph *signalEffi = new TGraph(l,sx,sy);	
     	TGraph *bkgEffi = new TGraph(l,bx,by); 

	int i=0;
	for(float cut=0.0;cut<1.0;cut=cut+0.05){   //cut applied on bdt responce 
	        cout<<"cut= "<<cut<<endl;
                std::ostringstream ss;
                ss << cut;
                std::string s(ss.str());
                TString MCcut,mycutQCD;
                
                if(s=="0.0"){
                        MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*(t_ch_CAsi>="+s+")";
                        mycutQCD = "(dR_bJet_lJet>0.4)*(mtwMass>50)*(t_ch_CAsi>="+s+")";
                }
                else{
                        MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*(t_ch_CAsi>"+s+")";  //cuts including BDT cut
                        mycutQCD = "(dR_bJet_lJet>0.4)*(mtwMass>50)*(t_ch_CAsi>"+s+")";
                }
                	
                float sign_yield=0;
                float bkg_yield=0;
                for(unsigned int ll=0; ll<channel.size(); ll++){    //projecting distribution after cut applied
                        Channel=channel.at(ll);
                        std::ostringstream kk;      
                        kk << ll;
	               	std::string k("h"+kk.str());
	               	std::string k_WoAssi("h_WoAssi"+kk.str());
                        //cout<<k<<endl;
                        if(Channel=="Tchannel" || Channel=="Tbarchannel"){
                                tree[ll]->Project(k.c_str(),brch,MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)");
                                //cout<<"h["<<ll<<"] = "<<h[ll]->Integral()<<endl;
                                h[ll]->Scale(MCSF);
                                cout<<"MCSF="<<MCSF<<";channel="<<Channel<<";"<<endl;
                                //h[ll]->Print();
                                
                                tree[ll]->Project(k_WoAssi.c_str(),brch,MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)");
                                //cout<<"h["<<ll<<"] = "<<h[ll]->Integral()<<endl;
                                h_WoAssi[ll]->Scale(MCSF);
                                cout<<"MCSF="<<MCSF<<";channel="<<Channel<<";"<<endl;
                                //h_WoAssi[ll]->Print();
                        }
                        else if(Channel!="Data"+year+"_2J1T0"){
                                tree[ll]->Project(k.c_str(),brch,MCcut);
                                //cout<<"h["<<ll<<"] = "<<h[ll]->Integral()<<endl;
                                h[ll]->Scale(MCSF);
                                cout<<"MCSF="<<MCSF<<";channel="<<Channel<<endl;
                                //h[ll]->Print();
                        }
                        else{ 
                                tree[ll]->Project(k.c_str(),brch,mycutQCD);
                                //cout<<"h["<<ll<<"] = "<<h[ll]->Integral()<<endl;
                                h[ll]->Scale(QCDSF);
                                cout<<"QCDSF="<<QCDSF<<";channel="<<Channel<<endl;
                                //h[ll]->Print();
                        }
                        			
                        if(ll<2){ 
                                sign_yield+=h[ll]->Integral();
                                //sign_yield+=h_WoAssi[ll]->Integral();
                                bkg_yield+=h_WoAssi[ll]->Integral();
                        }
                        else bkg_yield+=h[ll]->Integral(); 
			
                }
	
			

                double signal_eff=(sign_yield/signalYield_before_cut)*100;
                double bkg_eff=(bkg_yield/bkgYield_before_cut)*100;
                double recall = (sign_yield/(sign_yield+(bkgYield_before_cut-bkg_yield)))*100;
		
                double purity=0;
                if((sign_yield+bkg_yield) != 0) purity=(sign_yield/(sign_yield+bkg_yield))*100;  //Purity
                else purity= -10.0; ///Sanity Check; Setting unphysical value to purity which follows 0%<= purity <=100%	
                puritygr->SetPoint(i,cut,purity);   //ploting Tgraph 
                double f1score = (2*purity*recall)/(purity+recall);
                F1factorgr->SetPoint(i,cut,f1score);
                signalEffi->SetPoint(i,cut,signal_eff);
                bkgEffi->SetPoint(i,cut,bkg_eff);
                cout<<"bkgYield_before_cut="<<bkgYield_before_cut<<endl;
                cout<<"signalYield_before_cut="<<signalYield_before_cut<<endl;
                cout<<"bkgYield_after_cut="<<bkg_yield<<endl;
                cout<<"signalYield_after_cut="<<sign_yield<<endl;
                cout<<"sign_eff="<<signal_eff<<endl;
                cout<<"recall = "<<recall<<endl;
                cout<<"purity="<<purity<<endl;
                cout<<"background_eff="<<bkg_eff<<endl;
                i++;
                cout<<"i="<<i;
                for(int k=0;k<channel.size();k++){                                // clear histogram for next loop
                        h[k]->Reset();
                        if(k<2) h_WoAssi[k]->Reset();
                        //cout<<"h["<<k<<"]"<< " is cleared"<<endl;
                }
		cout<<"====================================="<<endl;
	}
		
        puritygr->Print();	
	TCanvas *c2 = new TCanvas("c2","", 600,600,600,600);
	c2->cd();
        TPad *pad = new TPad("grid","",0,0,1,1);
        pad->Draw();
        pad->cd();
        pad->SetGrid();
        pad->SetFillStyle(4000);

	puritygr->SetLineColor(kBlue);
        puritygr->SetLineWidth(3);
        puritygr->SetMarkerColor(kBlue);
        puritygr->SetMarkerStyle(20);
	puritygr->GetHistogram()->GetXaxis()->SetTitle("BDT_cut");
        puritygr->GetHistogram()->GetYaxis()->SetTitle("Efficiency (%)");	
   	
        signalEffi->SetLineColor(kRed);
        signalEffi->SetLineWidth(3);
        signalEffi->SetMarkerColor(kRed);
        signalEffi->SetMarkerStyle(20);
        signalEffi->GetHistogram()->GetXaxis()->SetTitle("BDT_cut");
        signalEffi->GetHistogram()->GetYaxis()->SetTitle("Efficiency (%)");	

        bkgEffi->SetLineColor(kGreen-2);
        bkgEffi->SetLineWidth(3);
        bkgEffi->SetMarkerColor(kGreen-2);
        bkgEffi->SetMarkerStyle(20);
        bkgEffi->GetHistogram()->GetXaxis()->SetTitle("BDT_cut");
        bkgEffi->GetHistogram()->GetYaxis()->SetTitle("Efficiency (%)");

	F1factorgr->SetLineColor(kBlack);
        F1factorgr->SetLineWidth(3);
        F1factorgr->SetMarkerColor(kBlack);
        F1factorgr->SetMarkerStyle(20);
	bkgEffi->GetHistogram()->GetXaxis()->SetTitle("BDT_cut");
        bkgEffi->GetHistogram()->GetYaxis()->SetTitle("Efficiency (%)");

	TLegend* leg=new TLegend(0.55,0.7,0.85,0.85);
        //leg->SetLineColor(0);
        leg->AddEntry(signalEffi,"#epsilon_{Sig}","l");
        leg->AddEntry(bkgEffi,"#epsilon_{Bkg}","l");
        leg->AddEntry(puritygr,"Signal Purity","l");
	//leg->AddEntry(F1factorgr,"F1-Score","l");

     
     
        mg->SetMaximum(118.0);
	mg->Add(signalEffi);
	mg->Add(bkgEffi);
	mg->Add(puritygr);
	//mg->Add(F1factorgr);
	mg->Draw("ACP");
        mg->GetXaxis()->SetTitle("BDT_cut");
        mg->GetYaxis()->SetTitle("Efficiency (%)");
        mg->GetYaxis()->SetTitleOffset(1.2);
        c2->Modified();
	leg->Draw("same");	
	CMSTEXT_variable(year,"2J1T",lep);
        TString outputfile = "Plots/"+year+"_"+lep+"_Effi";
        c2->SaveAs(outputfile+".png");
        c2->SaveAs(outputfile+".pdf"); 
}

