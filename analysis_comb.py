### Filter definitions ###

muo_ifile = ['thetainput_rebinned.root']
ele_ifile = ['']
lep_ifile = ['']

def narrow_resonances(hname):
    if not ('rsg' in hname or 'zp' in hname): return True
    pname = hname.split('__')[1]
    if ('w10p' in pname) or ('rsg' in pname): return False
    # mass = pname.strip('Zprime')
    mass = pname.split('w')[0].split('zp')[1]
    return float(mass) <= 3000

def wide_resonances(hname):
    if not ('rsg' in hname or 'zp' in hname): return True
    pname = hname.split('__')[1]
    if 'w1p' in pname: return False
    # mass = pname.strip('ZprimeWide')
    mass = pname.split('w')[0].split('zp')[1]
    return float(mass) <= 3000

def rsg_resonances(hname):
    if not ('rsg' in hname or 'zp' in hname): return True
    pname = hname.split('__')[1]
    if not 'rsg' in pname: return False
    #mass = pname.strip('RSgluon')
    mass = pname[3:]
    return float(mass) <= 3000

def build_boosted_semileptonic_model(files, filter, signal, eflag=False):
    model = build_model_from_rootfile(files, filter, include_mc_uncertainties = True)
    model.fill_histogram_zerobins()
    model.set_signal_processes(signal)

    for p in model.processes:
        model.add_lognormal_uncertainty('lumi', math.log(1.026), p)
        #---------------- I COMMENTED OUT FOF NOW - PUT  BACK LATER
        #if eflag:
            #for obs in ['el_0top0btag_mttbar','el_0top1btag_mttbar','el_1top_mttbar']:
                #model.add_lognormal_uncertainty('eleORjet_trig', math.log(1.01), p, obs)
        
    #model.add_lognormal_uncertainty('ttbar_rate',   math.log(1.15), 'ttbar')
    #model.add_lognormal_uncertainty('wl_rate',      math.log(1.09), 'wlight')
    #model.add_lognormal_uncertainty('wc_rate',      math.log(1.23), 'wc')
    #model.add_lognormal_uncertainty('wb_rate',      math.log(1.23), 'wb')
    #model.add_lognormal_uncertainty('st_rate',      math.log(1.23), 'singletop')
    #model.add_lognormal_uncertainty('zj_rate',      math.log(1.50), 'zlight')
    #model.add_lognormal_uncertainty('diboson_rate', math.log(1.20), 'diboson')
        model.add_lognormal_uncertainty('ttbar_rate',   math.log(1.3), 'ttbar')
        model.add_lognormal_uncertainty('wjets_rate',   math.log(1.5), 'wjets')
        
        #model.scale_predictions(0.050761421)  #-------FOR LUMI 1 fb-1
        #model.scale_predictions(0.253807107) #------FOR LUMI 5 fb-1
        return model

import exceptions

def build_model(type):

    model = None

    if type == 'narrow_resonances_muon':
        model = build_boosted_semileptonic_model(
            muo_ifile,
            narrow_resonances,
           'zp*',
           eflag = False
        )
    
    elif type == 'wide_resonances_muon':

        model = build_boosted_semileptonic_model(
           muo_ifile,
           wide_resonances,
           'zp*',
           eflag = False
        )        

    elif type == 'rsg_resonances_muon':

        model = build_boosted_semileptonic_model(
           muo_ifile,
           rsg_resonances,
           'zp*',
           eflag = False
        )

    elif type == 'narrow_resonances_electron':

        model = build_boosted_semileptonic_model(
           ele_ifile,
           narrow_resonances,
           'zp*',
           eflag = True
        )

    elif type == 'wide_resonances_electron':

        model = build_boosted_semileptonic_model(
           ele_ifile,
           wide_resonances,
           'zp*',
           eflag = True
        )

    elif type == 'rsg_resonances_electron':

        model = build_boosted_semileptonic_model(
           ele_ifile,
           rsg_resonances,
           'rsg*',
           eflag = True
        )

    elif type == 'narrow_resonances_lepton':

        model = build_boosted_semileptonic_model(
           lep_ifile,
           narrow_resonances,
           'zp*',
           eflag = True
        )

    elif type == 'wide_resonances_lepton':

        model = build_boosted_semileptonic_model(
           lep_ifile,
           wide_resonances,
           'zp*',
           eflag = True
        )

    elif type == 'rsg_resonances_lepton':

        model = build_boosted_semileptonic_model(
           lep_ifile,
           rsg_resonances,
           'rsg*',
           eflag = True
        )

    else: raise exceptions.ValueError('Type %s is undefined' % type)

    for p in model.distribution.get_parameters():
        d = model.distribution.get_distribution(p)
        if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
            model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
            if (p == 'toptag'): model.distribution.set_distribution_parameters(p, width = float("inf"))

    return model

# Code introduced by theta_driver

# Building the statistical model
args = {'type': 'narrow_resonances_muon'}

model = build_model(**args)

theta_auto.model_summary(model, create_plots=True, all_nominal_templates=False, shape_templates=False, lnmode='sym')

args = {}


results = bayesian_limits(model, what='expected' ,run_theta = True, **args)
#exp, obs = results
exp = results
print exp
#print obs

#execfile("utils.py")
#limit_table(exp, obs)
report.write_html('htmlout')
