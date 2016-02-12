from ROOT import *
import sys

#using dictionaries to loop over all systematics
#to change names of samples accordingly
systematic_direction={'nominal':'(wgtMC__muR_ct__muF_up)*(wgtMC__pileupSF_ct)*(wgtMC__btagSF_ct)*(wgtMC__ttagSF_ct)', 'btag__plus':'(wgtMC__muR_ct__muF_up)*(wgtMC__pileupSF_ct)*(wgtMC__btagSF_upB)*(wgtMC__ttagSF_ct)','btag__minus':'(wgtMC__muR_ct__muF_up)*(wgtMC__pileupSF_ct)*(wgtMC__btagSF_dnB)*(wgtMC__ttagSF_ct)','toptag__plus':'(wgtMC__muR_ct__muF_up)*(wgtMC__pileupSF_ct)*(wgtMC__btagSF_ct)*(wgtMC__ttagSF_upT)','toptag__minus':'(wgtMC__muR_ct__muF_up)*(wgtMC__pileupSF_ct)*(wgtMC__btagSF_ct)*(wgtMC__ttagSF_dnT)','pileup__plus':'(wgtMC__muR_ct__muF_up)*(wgtMC__pileupSF_up)*(wgtMC__btagSF_ct)*(wgtMC__ttagSF_ct)', 'pileup__minus': '(wgtMC__muR_ct__muF_up)*(wgtMC__pileupSF_dn)*(wgtMC__btagSF_ct)*(wgtMC__ttagSF_ct)'}
#samplelist = {'DATA':'uhh2.AnalysisModuleRunner.DATA.SingleEG.root', 'ttbar':'uhh2.AnalysisModuleRunner.MC.TTbar.root'}
samplelist = {'Zprime2000':'uhh2.AnalysisModuleRunner.MC.Zp01w2000.root','DATA':'uhh2.AnalysisModuleRunner.DATA.SingleMU.root','wc':'uhh2.AnalysisModuleRunner.MC.WJetsToLNu_HT__C.root','wl':'uhh2.AnalysisModuleRunner.MC.WJetsToLNu_HT__L.root','wb':'uhh2.AnalysisModuleRunner.MC.WJetsToLNu_HT__B.root','ttbar':'uhh2.AnalysisModuleRunner.MC.TTbar.root'}
#samplelist = {'DATA':'uhh2.AnalysisModuleRunner.DATA.SingleEG.root','wc':'uhh2.AnalysisModuleRunner.MC.WJetsToLNu__C.root','wl':'uhh2.AnalysisModuleRunner.MC.WJetsToLNu__L.root','ttbar':'uhh2.AnalysisModuleRunner.MC.TTbar.root','Zprime500':'uhh2.AnalysisModuleRunner.MC.Zp01w0500.root', 'Zprime1000':'uhh2.AnalysisModuleRunner.MC.Zp01w1000.root',  'Zprime1500':'uhh2.AnalysisModuleRunner.MC.Zp01w1500.root', 'Zprime2000':'uhh2.AnalysisModuleRunner.MC.Zp01w2000.root', 'Zprime3000':'uhh2.AnalysisModuleRunner.MC.Zp01w3000.root', 'Zprime4000':'uhh2.AnalysisModuleRunner.MC.Zp01w4000.root', 'ZprimeWide500':'uhh2.AnalysisModuleRunner.MC.Zp10w0500.root', 'ZprimeWide1000':'uhh2.AnalysisModuleRunner.MC.Zp10w1000.root', 'ZprimeWide1500':'uhh2.AnalysisModuleRunner.MC.Zp10w1500.root', 'ZprimeWide2000':'uhh2.AnalysisModuleRunner.MC.Zp10w2000.root', 'ZprimeWide3000':'uhh2.AnalysisModuleRunner.MC.Zp10w3000.root', 'ZprimeWide4000':'uhh2.AnalysisModuleRunner.MC.Zp10w4000.root'}
categories=['T1','T0B','T0B0']
#categories=['T1','T0B']
fout = TFile('mu_mle_theta_0210_nosignal.root', 'recreate')
gROOT.SetBatch(kTRUE)
SetMemoryPolicy(kMemoryStrict )
for cat in categories:
    cut_string='(muoN==1 & rec_chi2<30.'
    if cat == 'T1':
        h_string='mu_1top_mttbar__'
        for key_sample in samplelist:
            #open file and get analysis tree
            myfile = TFile(samplelist[key_sample])
            print "opening", myfile
            mytree = myfile.Get("AnalysisTree")
            print "getting", mytree
            mytree.SetAlias("invmass","sqrt(pow(rec_tlep.Energy()+rec_thad.Energy(),2)-(pow(rec_thad.Px(),2)+pow(rec_thad.Py(),2)+pow(rec_thad.Pz(),2)+pow(rec_tlep.Px(),2)+pow(rec_tlep.Py(),2)+pow(rec_tlep.Pz(),2)+2*(rec_thad.Px()*rec_tlep.Px()+rec_thad.Py()*rec_tlep.Py()+rec_thad.Pz()*rec_tlep.Pz())))") 
            #cut_string += ' & ttagN==1 & ttagevt==1 & btagN>0)*'
            if key_sample == 'DATA':
                cut = str(cut_string+' & ttagN==1 & ttagevt==1 & btagN>0)')
                print "Processing: ",key_sample
                print "Applying cut:",cut
                mytree.Draw("invmass>>temp",cut)
                temp.SetName(h_string+key_sample)
                fout.WriteObject(temp,h_string+key_sample)
                del temp
            else:
                for syst in systematic_direction:
                    cut = str(cut_string+' & ttagN==1 & ttagevt==1 & btagN>0)*(wgtMC__GEN)*'+systematic_direction[syst])
                    print "Processing: ",key_sample
                    print "Applying cut:",cut
                    if syst == 'nominal':
                    #temp = h_string+key_sample
                        mytree.Draw("invmass>>temp",cut)
                        temp.SetName(h_string+key_sample)
                        fout.WriteObject(temp,h_string+key_sample)
                        del temp
                    elif 'nominal' not in syst:
                    #temp = h_string+key_sample+"__"+syst
                        mytree.Draw("invmass>>temp",cut)
                        temp.SetName(h_string+key_sample+"__"+syst)
                        fout.WriteObject(temp,h_string+key_sample+"__"+syst)
                        del temp
    elif cat == 'T0B':
        h_string='mu_0top1btag_mttbar__'
        for key_sample in samplelist:
            #open file and get analysis tree
            myfile = TFile(samplelist[key_sample])
            print "opening", myfile
            mytree = myfile.Get("AnalysisTree")
            print "getting", mytree
            mytree.SetAlias("invmass","sqrt(pow(rec_tlep.Energy()+rec_thad.Energy(),2)-(pow(rec_thad.Px(),2)+pow(rec_thad.Py(),2)+pow(rec_thad.Pz(),2)+pow(rec_tlep.Px(),2)+pow(rec_tlep.Py(),2)+pow(rec_tlep.Pz(),2)+2*(rec_thad.Px()*rec_tlep.Px()+rec_thad.Py()*rec_tlep.Py()+rec_thad.Pz()*rec_tlep.Pz())))") 
            #cut_string += ' & ttagN==0 & ttagevt==0 & btagN>0)*'
            if key_sample == 'DATA':
                cut = str(cut_string+' & ttagN==0 & ttagevt==0 & btagN>1)')
                print "Processing: ",key_sample
                print "Applying cut:",cut
                mytree.Draw("invmass>>temp2",cut)
                temp2.SetName(h_string+key_sample)
                fout.WriteObject(temp2,h_string+key_sample)
                del temp2
            else:
                for syst in systematic_direction:
                    cut = str(cut_string+' & ttagN==0 & ttagevt==0 & btagN>1)*(wgtMC__GEN)*'+systematic_direction[syst])
                    print "Processing: ",key_sample
                    print "Applying cut:",cut
                    if syst == 'nominal':
                    #temp2 = h_string+key_sample
                        mytree.Draw("invmass>>temp2",cut)
                        temp2.SetName(h_string+key_sample)
                        fout.WriteObject(temp2,h_string+key_sample)
                        del temp2
                    elif 'nominal' not in syst:
                    #temp2 = h_string+key_sample+"__"+syst
                        mytree.Draw("invmass>>temp2",cut)
                        temp2.SetName(h_string+key_sample+"__"+syst)
                        fout.WriteObject(temp2,h_string+key_sample+"__"+syst)
                #fout.WriteObject(temp2,h_string+key_sample+"__"+syst) 
                        del temp2
    elif cat == 'T0B0':
        h_string='mu_0top0btag_mttbar__'
        for key_sample in samplelist:
            #open file and get analysis tree
            myfile = TFile(samplelist[key_sample])
            print "opening", myfile
            mytree = myfile.Get("AnalysisTree")
            print "getting", mytree
            mytree.SetAlias("invmass","sqrt(pow(rec_tlep.Energy()+rec_thad.Energy(),2)-(pow(rec_thad.Px(),2)+pow(rec_thad.Py(),2)+pow(rec_thad.Pz(),2)+pow(rec_tlep.Px(),2)+pow(rec_tlep.Py(),2)+pow(rec_tlep.Pz(),2)+2*(rec_thad.Px()*rec_tlep.Px()+rec_thad.Py()*rec_tlep.Py()+rec_thad.Pz()*rec_tlep.Pz())))") 
            #cut_string += ' & ttagN==0 & ttagevt==0 & btagN==0)*'
            if key_sample == 'DATA':
                cut = str(cut_string+' & ttagN==0 & ttagevt==0 & btagN==0)')
                print "Processing: ",key_sample
                print "Applying cut:",cut
                mytree.Draw("invmass>>temp3",cut)
                temp3.SetName(h_string+key_sample)
                fout.WriteObject(temp3,h_string+key_sample)
                del temp3
            else:
                for syst in systematic_direction:
                    cut = str(cut_string+' & ttagN==0 & ttagevt==0 & btagN==0)*(wgtMC__GEN)*'+systematic_direction[syst])
                    print "Processing: ",key_sample
                    print "Applying cut:",cut
                    if syst == 'nominal':
                    #temp3 = h_string+key_sample
                        mytree.Draw("invmass>>temp3",cut)
                        temp3.SetName(h_string+key_sample)
                    #mytree.Draw("invmass>>temp3",cut)
                        fout.WriteObject(temp3,h_string+key_sample)
                        del temp3
                    elif 'nominal' not in syst:
                    #temp3 = h_string+key_sample+"__"+syst
                        mytree.Draw("invmass>>temp3",cut)
                        temp3.SetName(h_string+key_sample+"__"+syst)
                        fout.WriteObject(temp3,h_string+key_sample+"__"+syst)
                #fout.WriteObject(temp3,h_string+key_sample+"__"+syst)
                        del temp3

