void unnamed()
{
//=========Macro generated from canvas: c1/
//=========  (Fri Jan 27 14:13:51 2023) by ROOT version 6.12/07
   TCanvas *c1 = new TCanvas("c1", "",600,480,600,600);
   gStyle->SetOptStat(0);
   c1->SetHighLightColor(2);
   c1->Range(0,0,1,1);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(2);
   c1->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: pad1
   TPad *pad1 = new TPad("pad1", "pad1",0,0.195259,1,0.990683);
   pad1->Draw();
   pad1->cd();
   pad1->Range(-25,-6358.241,225,65082.67);
   pad1->SetFillColor(0);
   pad1->SetBorderMode(0);
   pad1->SetBorderSize(2);
   pad1->SetTickx(1);
   pad1->SetTicky(1);
   pad1->SetBottomMargin(0.089);
   pad1->SetFrameBorderMode(0);
   pad1->SetFrameBorderMode(0);
   
   THStack *hs = new THStack();
   hs->SetName("hs");
   hs->SetTitle(";;Events");
   hs->SetMaximum(55179.6);
   
   TH1F *hs_stack_1 = new TH1F("hs_stack_1","",20,0,200);
   hs_stack_1->SetMinimum(0);
   hs_stack_1->SetMaximum(57938.58);
   hs_stack_1->SetDirectory(0);
   hs_stack_1->SetStats(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   hs_stack_1->SetLineColor(ci);
   hs_stack_1->GetXaxis()->SetLabelFont(42);
   hs_stack_1->GetXaxis()->SetLabelSize(0.035);
   hs_stack_1->GetXaxis()->SetTitleSize(0.035);
   hs_stack_1->GetXaxis()->SetTitleFont(42);
   hs_stack_1->GetYaxis()->SetTitle("Events");
   hs_stack_1->GetYaxis()->SetLabelFont(42);
   hs_stack_1->GetYaxis()->SetLabelSize(0.035);
   hs_stack_1->GetYaxis()->SetTitleSize(0.035);
   hs_stack_1->GetYaxis()->SetTitleOffset(0);
   hs_stack_1->GetYaxis()->SetTitleFont(42);
   hs_stack_1->GetZaxis()->SetLabelFont(42);
   hs_stack_1->GetZaxis()->SetLabelSize(0.035);
   hs_stack_1->GetZaxis()->SetTitleSize(0.035);
   hs_stack_1->GetZaxis()->SetTitleFont(42);
   hs->SetHistogram(hs_stack_1);
   
   
   TH1F *QCD_DD_stack_1 = new TH1F("QCD_DD_stack_1","",20,0,200);
   QCD_DD_stack_1->SetBinContent(6,1164.173);
   QCD_DD_stack_1->SetBinContent(7,1153.573);
   QCD_DD_stack_1->SetBinContent(8,1099.969);
   QCD_DD_stack_1->SetBinContent(9,1008.486);
   QCD_DD_stack_1->SetBinContent(10,817.3534);
   QCD_DD_stack_1->SetBinContent(11,636.7329);
   QCD_DD_stack_1->SetBinContent(12,468.7967);
   QCD_DD_stack_1->SetBinContent(13,323.5357);
   QCD_DD_stack_1->SetBinContent(14,231.8788);
   QCD_DD_stack_1->SetBinContent(15,155.3389);
   QCD_DD_stack_1->SetBinContent(16,110.162);
   QCD_DD_stack_1->SetBinContent(17,79.32011);
   QCD_DD_stack_1->SetBinContent(18,57.68736);
   QCD_DD_stack_1->SetBinContent(19,44.65557);
   QCD_DD_stack_1->SetBinContent(20,30.32061);
   QCD_DD_stack_1->SetBinContent(21,127.0164);
   QCD_DD_stack_1->SetBinError(6,582.0863);
   QCD_DD_stack_1->SetBinError(7,576.7867);
   QCD_DD_stack_1->SetBinError(8,549.9847);
   QCD_DD_stack_1->SetBinError(9,504.2431);
   QCD_DD_stack_1->SetBinError(10,408.6767);
   QCD_DD_stack_1->SetBinError(11,318.3665);
   QCD_DD_stack_1->SetBinError(12,234.3983);
   QCD_DD_stack_1->SetBinError(13,161.7679);
   QCD_DD_stack_1->SetBinError(14,115.9394);
   QCD_DD_stack_1->SetBinError(15,77.66943);
   QCD_DD_stack_1->SetBinError(16,55.081);
   QCD_DD_stack_1->SetBinError(17,39.66006);
   QCD_DD_stack_1->SetBinError(18,28.84368);
   QCD_DD_stack_1->SetBinError(19,22.32779);
   QCD_DD_stack_1->SetBinError(20,1.623025);
   QCD_DD_stack_1->SetBinError(21,3.321898);
   QCD_DD_stack_1->SetEntries(86431);
   QCD_DD_stack_1->SetStats(0);

   ci = TColor::GetColor("#cccccc");
   QCD_DD_stack_1->SetFillColor(ci);

   ci = TColor::GetColor("#cccccc");
   QCD_DD_stack_1->SetLineColor(ci);
   QCD_DD_stack_1->SetLineWidth(2);
   QCD_DD_stack_1->GetXaxis()->SetLabelFont(42);
   QCD_DD_stack_1->GetXaxis()->SetLabelSize(0.035);
   QCD_DD_stack_1->GetXaxis()->SetTitleSize(0.035);
   QCD_DD_stack_1->GetXaxis()->SetTitleFont(42);
   QCD_DD_stack_1->GetYaxis()->SetLabelFont(42);
   QCD_DD_stack_1->GetYaxis()->SetLabelSize(0.035);
   QCD_DD_stack_1->GetYaxis()->SetTitleSize(0.035);
   QCD_DD_stack_1->GetYaxis()->SetTitleOffset(0);
   QCD_DD_stack_1->GetYaxis()->SetTitleFont(42);
   QCD_DD_stack_1->GetZaxis()->SetLabelFont(42);
   QCD_DD_stack_1->GetZaxis()->SetLabelSize(0.035);
   QCD_DD_stack_1->GetZaxis()->SetTitleSize(0.035);
   QCD_DD_stack_1->GetZaxis()->SetTitleFont(42);
   hs->Add(QCD_DD_stack_1,"");
   
   TH1F *EWK_bkg_stack_2 = new TH1F("EWK_bkg_stack_2","mtwMass",20,0,200);
   EWK_bkg_stack_2->SetBinContent(6,7971.044);
   EWK_bkg_stack_2->SetBinContent(7,9696.391);
   EWK_bkg_stack_2->SetBinContent(8,9603.308);
   EWK_bkg_stack_2->SetBinContent(9,9363.208);
   EWK_bkg_stack_2->SetBinContent(10,7835.178);
   EWK_bkg_stack_2->SetBinContent(11,6399.362);
   EWK_bkg_stack_2->SetBinContent(12,4248.79);
   EWK_bkg_stack_2->SetBinContent(13,2972.687);
   EWK_bkg_stack_2->SetBinContent(14,1890.193);
   EWK_bkg_stack_2->SetBinContent(15,1315.404);
   EWK_bkg_stack_2->SetBinContent(16,1014.821);
   EWK_bkg_stack_2->SetBinContent(17,650.8397);
   EWK_bkg_stack_2->SetBinContent(18,402.841);
   EWK_bkg_stack_2->SetBinContent(19,282.185);
   EWK_bkg_stack_2->SetBinContent(20,171.545);
   EWK_bkg_stack_2->SetBinContent(21,589.7796);
   EWK_bkg_stack_2->SetBinError(6,797.1044);
   EWK_bkg_stack_2->SetBinError(7,969.6391);
   EWK_bkg_stack_2->SetBinError(8,960.3308);
   EWK_bkg_stack_2->SetBinError(9,936.3208);
   EWK_bkg_stack_2->SetBinError(10,783.5178);
   EWK_bkg_stack_2->SetBinError(11,639.9362);
   EWK_bkg_stack_2->SetBinError(12,424.879);
   EWK_bkg_stack_2->SetBinError(13,297.2687);
   EWK_bkg_stack_2->SetBinError(14,189.0193);
   EWK_bkg_stack_2->SetBinError(15,131.5404);
   EWK_bkg_stack_2->SetBinError(16,101.4821);
   EWK_bkg_stack_2->SetBinError(17,65.08397);
   EWK_bkg_stack_2->SetBinError(18,40.2841);
   EWK_bkg_stack_2->SetBinError(19,28.2185);
   EWK_bkg_stack_2->SetBinError(20,47.5891);
   EWK_bkg_stack_2->SetBinError(21,85.82943);
   EWK_bkg_stack_2->SetEntries(77927);
   EWK_bkg_stack_2->SetStats(0);

   ci = TColor::GetColor("#339933");
   EWK_bkg_stack_2->SetFillColor(ci);

   ci = TColor::GetColor("#339933");
   EWK_bkg_stack_2->SetLineColor(ci);
   EWK_bkg_stack_2->SetLineWidth(2);
   EWK_bkg_stack_2->GetXaxis()->SetLabelFont(42);
   EWK_bkg_stack_2->GetXaxis()->SetLabelSize(0.035);
   EWK_bkg_stack_2->GetXaxis()->SetTitleSize(0.035);
   EWK_bkg_stack_2->GetXaxis()->SetTitleFont(42);
   EWK_bkg_stack_2->GetYaxis()->SetLabelFont(42);
   EWK_bkg_stack_2->GetYaxis()->SetLabelSize(0.035);
   EWK_bkg_stack_2->GetYaxis()->SetTitleSize(0.035);
   EWK_bkg_stack_2->GetYaxis()->SetTitleOffset(0);
   EWK_bkg_stack_2->GetYaxis()->SetTitleFont(42);
   EWK_bkg_stack_2->GetZaxis()->SetLabelFont(42);
   EWK_bkg_stack_2->GetZaxis()->SetLabelSize(0.035);
   EWK_bkg_stack_2->GetZaxis()->SetTitleSize(0.035);
   EWK_bkg_stack_2->GetZaxis()->SetTitleFont(42);
   hs->Add(EWK_bkg_stack_2,"");
   
   TH1F *top_bkg_172p5_stack_3 = new TH1F("top_bkg_172p5_stack_3","mtwMass",20,0,200);
   top_bkg_172p5_stack_3->SetBinContent(6,26916.84);
   top_bkg_172p5_stack_3->SetBinContent(7,29894.7);
   top_bkg_172p5_stack_3->SetBinContent(8,31234.42);
   top_bkg_172p5_stack_3->SetBinContent(9,30012.06);
   top_bkg_172p5_stack_3->SetBinContent(10,26182.75);
   top_bkg_172p5_stack_3->SetBinContent(11,21039.87);
   top_bkg_172p5_stack_3->SetBinContent(12,16037.84);
   top_bkg_172p5_stack_3->SetBinContent(13,11782);
   top_bkg_172p5_stack_3->SetBinContent(14,8643.986);
   top_bkg_172p5_stack_3->SetBinContent(15,6304.492);
   top_bkg_172p5_stack_3->SetBinContent(16,4667.673);
   top_bkg_172p5_stack_3->SetBinContent(17,3486.003);
   top_bkg_172p5_stack_3->SetBinContent(18,2664.305);
   top_bkg_172p5_stack_3->SetBinContent(19,2053.185);
   top_bkg_172p5_stack_3->SetBinContent(20,1600.888);
   top_bkg_172p5_stack_3->SetBinContent(21,6844.773);
   top_bkg_172p5_stack_3->SetBinError(6,1615.011);
   top_bkg_172p5_stack_3->SetBinError(7,1793.682);
   top_bkg_172p5_stack_3->SetBinError(8,1874.065);
   top_bkg_172p5_stack_3->SetBinError(9,1800.724);
   top_bkg_172p5_stack_3->SetBinError(10,1570.965);
   top_bkg_172p5_stack_3->SetBinError(11,1262.392);
   top_bkg_172p5_stack_3->SetBinError(12,962.2705);
   top_bkg_172p5_stack_3->SetBinError(13,706.9199);
   top_bkg_172p5_stack_3->SetBinError(14,518.6392);
   top_bkg_172p5_stack_3->SetBinError(15,378.2695);
   top_bkg_172p5_stack_3->SetBinError(16,280.0604);
   top_bkg_172p5_stack_3->SetBinError(17,209.1602);
   top_bkg_172p5_stack_3->SetBinError(18,159.8583);
   top_bkg_172p5_stack_3->SetBinError(19,123.1911);
   top_bkg_172p5_stack_3->SetBinError(20,9.917778);
   top_bkg_172p5_stack_3->SetBinError(21,20.83967);
   top_bkg_172p5_stack_3->SetEntries(5058669);
   top_bkg_172p5_stack_3->SetStats(0);

   ci = TColor::GetColor("#cc9900");
   top_bkg_172p5_stack_3->SetFillColor(ci);

   ci = TColor::GetColor("#cc9900");
   top_bkg_172p5_stack_3->SetLineColor(ci);
   top_bkg_172p5_stack_3->SetLineWidth(2);
   top_bkg_172p5_stack_3->GetXaxis()->SetTitle("m_{t}");
   top_bkg_172p5_stack_3->GetXaxis()->SetLabelFont(42);
   top_bkg_172p5_stack_3->GetXaxis()->SetLabelSize(0.035);
   top_bkg_172p5_stack_3->GetXaxis()->SetTitleSize(0.035);
   top_bkg_172p5_stack_3->GetXaxis()->SetTitleFont(42);
   top_bkg_172p5_stack_3->GetYaxis()->SetLabelFont(42);
   top_bkg_172p5_stack_3->GetYaxis()->SetLabelSize(0.035);
   top_bkg_172p5_stack_3->GetYaxis()->SetTitleSize(0.035);
   top_bkg_172p5_stack_3->GetYaxis()->SetTitleOffset(0);
   top_bkg_172p5_stack_3->GetYaxis()->SetTitleFont(42);
   top_bkg_172p5_stack_3->GetZaxis()->SetLabelFont(42);
   top_bkg_172p5_stack_3->GetZaxis()->SetLabelSize(0.035);
   top_bkg_172p5_stack_3->GetZaxis()->SetTitleSize(0.035);
   top_bkg_172p5_stack_3->GetZaxis()->SetTitleFont(42);
   hs->Add(top_bkg_172p5_stack_3,"");
   
   TH1F *top_sig_172p5_stack_4 = new TH1F("top_sig_172p5_stack_4","mtwMass",20,0,200);
   top_sig_172p5_stack_4->SetBinContent(6,3828.643);
   top_sig_172p5_stack_4->SetBinContent(7,4469.363);
   top_sig_172p5_stack_4->SetBinContent(8,4893.798);
   top_sig_172p5_stack_4->SetBinContent(9,4731.825);
   top_sig_172p5_stack_4->SetBinContent(10,4008.733);
   top_sig_172p5_stack_4->SetBinContent(11,2923.96);
   top_sig_172p5_stack_4->SetBinContent(12,1891.197);
   top_sig_172p5_stack_4->SetBinContent(13,1114.468);
   top_sig_172p5_stack_4->SetBinContent(14,599.4007);
   top_sig_172p5_stack_4->SetBinContent(15,307.0598);
   top_sig_172p5_stack_4->SetBinContent(16,158.8913);
   top_sig_172p5_stack_4->SetBinContent(17,80.68047);
   top_sig_172p5_stack_4->SetBinContent(18,41.86274);
   top_sig_172p5_stack_4->SetBinContent(19,22.59671);
   top_sig_172p5_stack_4->SetBinContent(20,14.65902);
   top_sig_172p5_stack_4->SetBinContent(21,24.1633);
   top_sig_172p5_stack_4->SetBinError(6,574.2964);
   top_sig_172p5_stack_4->SetBinError(7,670.4045);
   top_sig_172p5_stack_4->SetBinError(8,734.0697);
   top_sig_172p5_stack_4->SetBinError(9,709.7737);
   top_sig_172p5_stack_4->SetBinError(10,601.31);
   top_sig_172p5_stack_4->SetBinError(11,438.594);
   top_sig_172p5_stack_4->SetBinError(12,283.6796);
   top_sig_172p5_stack_4->SetBinError(13,167.1701);
   top_sig_172p5_stack_4->SetBinError(14,89.9101);
   top_sig_172p5_stack_4->SetBinError(15,46.05897);
   top_sig_172p5_stack_4->SetBinError(16,23.8337);
   top_sig_172p5_stack_4->SetBinError(17,12.10207);
   top_sig_172p5_stack_4->SetBinError(18,6.279411);
   top_sig_172p5_stack_4->SetBinError(19,3.389507);
   top_sig_172p5_stack_4->SetBinError(20,0.8947774);
   top_sig_172p5_stack_4->SetBinError(21,1.261932);
   top_sig_172p5_stack_4->SetEntries(656409);
   top_sig_172p5_stack_4->SetStats(0);

   ci = TColor::GetColor("#ff0000");
   top_sig_172p5_stack_4->SetFillColor(ci);

   ci = TColor::GetColor("#ff0000");
   top_sig_172p5_stack_4->SetLineColor(ci);
   top_sig_172p5_stack_4->SetLineWidth(2);
   top_sig_172p5_stack_4->GetXaxis()->SetTitle("M_{top}");
   top_sig_172p5_stack_4->GetXaxis()->SetLabelFont(42);
   top_sig_172p5_stack_4->GetXaxis()->SetLabelSize(0.035);
   top_sig_172p5_stack_4->GetXaxis()->SetTitleSize(0.035);
   top_sig_172p5_stack_4->GetXaxis()->SetTitleFont(42);
   top_sig_172p5_stack_4->GetYaxis()->SetLabelFont(42);
   top_sig_172p5_stack_4->GetYaxis()->SetLabelSize(0.035);
   top_sig_172p5_stack_4->GetYaxis()->SetTitleSize(0.035);
   top_sig_172p5_stack_4->GetYaxis()->SetTitleOffset(0);
   top_sig_172p5_stack_4->GetYaxis()->SetTitleFont(42);
   top_sig_172p5_stack_4->GetZaxis()->SetLabelFont(42);
   top_sig_172p5_stack_4->GetZaxis()->SetLabelSize(0.035);
   top_sig_172p5_stack_4->GetZaxis()->SetTitleSize(0.035);
   top_sig_172p5_stack_4->GetZaxis()->SetTitleFont(42);
   hs->Add(top_sig_172p5_stack_4,"");
   hs->Draw("hist");
   
   TLegend *leg = new TLegend(0.6019365,0.5548435,0.8093552,0.7902614,NULL,"brNDC");
   leg->SetBorderSize(1);
   leg->SetTextSize(0.045);
   leg->SetLineColor(0);
   leg->SetLineStyle(1);
   leg->SetLineWidth(1);
   leg->SetFillColor(0);
   leg->SetFillStyle(1001);
   TLegendEntry *entry=leg->AddEntry("data_obs","Data","ple1");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(20);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("top_sig_172p5_stack_4","#it{t}-ch.","f");

   ci = TColor::GetColor("#ff0000");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);

   ci = TColor::GetColor("#ff0000");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(2);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("top_bkg_172p5_stack_3","t#bar{t}","f");

   ci = TColor::GetColor("#cc9900");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);

   ci = TColor::GetColor("#cc9900");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(2);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("EWK_bkg_stack_2","V+Jets, VV","f");

   ci = TColor::GetColor("#339933");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);

   ci = TColor::GetColor("#339933");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(2);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("QCD_DD_stack_1","QCD","f");

   ci = TColor::GetColor("#cccccc");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);

   ci = TColor::GetColor("#cccccc");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(2);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   leg->Draw();
   
   TPaveText *pt = new TPaveText(0.3,0.9,0.38,0.92,"br");
   pt->SetBorderSize(0);
   pt->SetFillStyle(0);
   pt->SetTextAlign(13);
   pt->SetTextFont(42);
   pt->SetTextSize(0.02);
   TText *pt_LaTex = pt->AddText("2J1T");
   pt->Draw();
   
   pt = new TPaveText(0.35,0.84,0.43,0.88,"brNDC");
   pt->SetBorderSize(0);
   pt->SetFillStyle(0);
   pt->SetTextAlign(33);
   pt->SetTextFont(42);
   pt->SetTextSize(0.05);
   pt_LaTex = pt->AddText("#bf{CMS} #it{Preliminary}");
   pt->Draw();
   
   pt = new TPaveText(0.29,0.82,0.32,0.84,"brNDC");
   pt->SetBorderSize(0);
   pt->SetFillStyle(0);
   pt->SetTextAlign(33);
   pt->SetTextFont(42);
   pt->SetTextSize(0.05);
   pt_LaTex = pt->AddText("#it{e+jets}");
   pt->Draw();
   
   pt = new TPaveText(35,84,43,88,"br");
   pt->SetBorderSize(0);
   pt->SetFillStyle(0);
   pt->SetTextAlign(33);
   pt->SetTextFont(42);
   pt->SetTextSize(0.03);
   pt_LaTex = pt->AddText("41.5 fb^{-1} (13 TeV, 2017)");
   pt->Draw();
   
   TH1F *data_obs__1 = new TH1F("data_obs__1","",20,0,200);
   data_obs__1->SetBinContent(6,40777);
   data_obs__1->SetBinContent(7,43878);
   data_obs__1->SetBinContent(8,45983);
   data_obs__1->SetBinContent(9,43630);
   data_obs__1->SetBinContent(10,37894);
   data_obs__1->SetBinContent(11,30256);
   data_obs__1->SetBinContent(12,22625);
   data_obs__1->SetBinContent(13,16544);
   data_obs__1->SetBinContent(14,11433);
   data_obs__1->SetBinContent(15,8242);
   data_obs__1->SetBinContent(16,5761);
   data_obs__1->SetBinContent(17,4189);
   data_obs__1->SetBinContent(18,3103);
   data_obs__1->SetBinContent(19,2284);
   data_obs__1->SetBinContent(20,1755);
   data_obs__1->SetBinContent(21,6896);
   data_obs__1->SetEntries(325250);
   data_obs__1->SetStats(0);
   data_obs__1->SetMarkerStyle(20);
   data_obs__1->GetXaxis()->SetLabelFont(42);
   data_obs__1->GetXaxis()->SetLabelSize(0.035);
   data_obs__1->GetXaxis()->SetTitleSize(0.035);
   data_obs__1->GetXaxis()->SetTitleFont(42);
   data_obs__1->GetYaxis()->SetLabelFont(42);
   data_obs__1->GetYaxis()->SetLabelSize(0.035);
   data_obs__1->GetYaxis()->SetTitleSize(0.035);
   data_obs__1->GetYaxis()->SetTitleOffset(0);
   data_obs__1->GetYaxis()->SetTitleFont(42);
   data_obs__1->GetZaxis()->SetLabelFont(42);
   data_obs__1->GetZaxis()->SetLabelSize(0.035);
   data_obs__1->GetZaxis()->SetTitleSize(0.035);
   data_obs__1->GetZaxis()->SetTitleFont(42);
   data_obs__1->Draw("Same;E1");
   pad1->Modified();
   c1->cd();
  
// ------------>Primitives in pad: pad2
   TPad *pad2 = new TPad("pad2", "pad2",0,0,1,0.2621035);
   pad2->Draw();
   pad2->cd();
   pad2->Range(-25,0.001206402,225,1.545665);
   pad2->SetFillColor(0);
   pad2->SetBorderMode(0);
   pad2->SetBorderSize(2);
   pad2->SetGridy();
   pad2->SetTickx(1);
   pad2->SetTicky(1);
   pad2->SetTopMargin(0);
   pad2->SetBottomMargin(0.3);
   pad2->SetFrameBorderMode(0);
   pad2->SetFrameBorderMode(0);
   
   TH1D *Band__2 = new TH1D("Band__2","",20,0,200);
   Band__2->SetBinContent(1,1);
   Band__2->SetBinContent(2,1);
   Band__2->SetBinContent(3,1);
   Band__2->SetBinContent(4,1);
   Band__2->SetBinContent(5,1);
   Band__2->SetBinContent(6,1);
   Band__2->SetBinContent(7,1);
   Band__2->SetBinContent(8,1);
   Band__2->SetBinContent(9,1);
   Band__2->SetBinContent(10,1);
   Band__2->SetBinContent(11,1);
   Band__2->SetBinContent(12,1);
   Band__2->SetBinContent(13,1);
   Band__2->SetBinContent(14,1);
   Band__2->SetBinContent(15,1);
   Band__2->SetBinContent(16,1);
   Band__2->SetBinContent(17,1);
   Band__2->SetBinContent(18,1);
   Band__2->SetBinContent(19,1);
   Band__2->SetBinContent(20,1);
   Band__2->SetBinContent(21,1);
   Band__2->SetBinError(6,0.05071126);
   Band__2->SetBinError(7,0.04770317);
   Band__2->SetBinError(8,0.04815719);
   Band__2->SetBinError(9,0.04733951);
   Band__2->SetBinError(10,0.04772008);
   Band__2->SetBinError(11,0.04771543);
   Band__2->SetBinError(12,0.04916154);
   Band__2->SetBinError(13,0.05056433);
   Band__2->SetBinError(14,0.05055398);
   Band__2->SetBinError(15,0.05179893);
   Band__2->SetBinError(16,0.04942195);
   Band__2->SetBinError(17,0.05058291);
   Band__2->SetBinError(18,0.05182349);
   Band__2->SetBinError(19,0.05079661);
   Band__2->SetBinError(20,0.02584789);
   Band__2->SetBinError(21,0.01059322);
   Band__2->SetMinimum(0.464544);
   Band__2->SetMaximum(1.545665);
   Band__2->SetEntries(21);

   ci = TColor::GetColor("#333333");
   Band__2->SetFillColor(ci);
   Band__2->SetFillStyle(3001);

   ci = TColor::GetColor("#000099");
   Band__2->SetLineColor(ci);
   Band__2->GetXaxis()->SetNdivisions(10);
   Band__2->GetXaxis()->SetLabelFont(42);
   Band__2->GetXaxis()->SetLabelSize(0.1);
   Band__2->GetXaxis()->SetTitleSize(0.12);
   Band__2->GetXaxis()->SetTitleFont(42);
   Band__2->GetYaxis()->SetTitle("Data/MC");
   Band__2->GetYaxis()->CenterTitle(true);
   Band__2->GetYaxis()->SetNdivisions(10);
   Band__2->GetYaxis()->SetLabelFont(42);
   Band__2->GetYaxis()->SetLabelSize(0.07);
   Band__2->GetYaxis()->SetTitleSize(0.12);
   Band__2->GetYaxis()->SetTickLength(0.01);
   Band__2->GetYaxis()->SetTitleOffset(0.35);
   Band__2->GetYaxis()->SetTitleFont(42);
   Band__2->GetZaxis()->SetLabelFont(42);
   Band__2->GetZaxis()->SetLabelSize(0.035);
   Band__2->GetZaxis()->SetTitleSize(0.035);
   Band__2->GetZaxis()->SetTitleFont(42);
   Band__2->Draw("E2");
   
   Double_t divide_data_obs_by_top_sig_172p5_fx3001[15] = {
   55,
   65,
   75,
   85,
   95,
   105,
   115,
   125,
   135,
   145,
   155,
   165,
   175,
   185,
   195};
   Double_t divide_data_obs_by_top_sig_172p5_fy3001[15] = {
   1.022474,
   0.970451,
   0.9818819,
   0.9670716,
   0.9755428,
   0.9760024,
   0.9990451,
   1.021696,
   1.005943,
   1.01976,
   0.9679836,
   0.9749016,
   0.9798856,
   0.9506282,
   0.9656585};
   Double_t divide_data_obs_by_top_sig_172p5_felx3001[15] = {
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5};
   Double_t divide_data_obs_by_top_sig_172p5_fely3001[15] = {
   0.05088204,
   0.04785241,
   0.04829883,
   0.04749135,
   0.04790794,
   0.04796964,
   0.04953018,
   0.05110304,
   0.05133761,
   0.05291408,
   0.05095451,
   0.05268573,
   0.05462811,
   0.05445093,
   0.03461532};
   Double_t divide_data_obs_by_top_sig_172p5_fehx3001[15] = {
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5,
   5};
   Double_t divide_data_obs_by_top_sig_172p5_fehy3001[15] = {
   0.05361297,
   0.05039558,
   0.05085908,
   0.05000424,
   0.05044272,
   0.05050957,
   0.0521768,
   0.05385899,
   0.05416554,
   0.05587976,
   0.05385234,
   0.05576516,
   0.05792628,
   0.05783043,
   0.03590494};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(15,divide_data_obs_by_top_sig_172p5_fx3001,divide_data_obs_by_top_sig_172p5_fy3001,divide_data_obs_by_top_sig_172p5_felx3001,divide_data_obs_by_top_sig_172p5_fehx3001,divide_data_obs_by_top_sig_172p5_fely3001,divide_data_obs_by_top_sig_172p5_fehy3001);
   grae->SetName("divide_data_obs_by_top_sig_172p5");
   grae->SetTitle("");
   grae->SetMarkerStyle(20);
   grae->SetMarkerSize(0.89);
   
   TH1F *Graph_divide_data_obs_by_top_sig_172p53001 = new TH1F("Graph_divide_data_obs_by_top_sig_172p53001","",100,0,200);
   Graph_divide_data_obs_by_top_sig_172p53001->SetMinimum(0.8781862);
   Graph_divide_data_obs_by_top_sig_172p53001->SetMaximum(1.094078);
   Graph_divide_data_obs_by_top_sig_172p53001->SetDirectory(0);
   Graph_divide_data_obs_by_top_sig_172p53001->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_divide_data_obs_by_top_sig_172p53001->SetLineColor(ci);
   Graph_divide_data_obs_by_top_sig_172p53001->GetXaxis()->SetLabelFont(42);
   Graph_divide_data_obs_by_top_sig_172p53001->GetXaxis()->SetLabelSize(0.035);
   Graph_divide_data_obs_by_top_sig_172p53001->GetXaxis()->SetTitleSize(0.035);
   Graph_divide_data_obs_by_top_sig_172p53001->GetXaxis()->SetTitleFont(42);
   Graph_divide_data_obs_by_top_sig_172p53001->GetYaxis()->SetLabelFont(42);
   Graph_divide_data_obs_by_top_sig_172p53001->GetYaxis()->SetLabelSize(0.035);
   Graph_divide_data_obs_by_top_sig_172p53001->GetYaxis()->SetTitleSize(0.035);
   Graph_divide_data_obs_by_top_sig_172p53001->GetYaxis()->SetTitleOffset(0);
   Graph_divide_data_obs_by_top_sig_172p53001->GetYaxis()->SetTitleFont(42);
   Graph_divide_data_obs_by_top_sig_172p53001->GetZaxis()->SetLabelFont(42);
   Graph_divide_data_obs_by_top_sig_172p53001->GetZaxis()->SetLabelSize(0.035);
   Graph_divide_data_obs_by_top_sig_172p53001->GetZaxis()->SetTitleSize(0.035);
   Graph_divide_data_obs_by_top_sig_172p53001->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_divide_data_obs_by_top_sig_172p53001);
   
   grae->Draw("pe1, ");
   pad2->Modified();
   c1->cd();
   c1->Modified();
   c1->cd();
   c1->SetSelected(c1);
}
