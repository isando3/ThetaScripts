### Filter definitions ###
print 'Hello World'
muo_ifile = ['']
ele_ifile = ['mle_theta_0211_rebinned.root']
lep_ifile = ['']

def narrow_resonances(hname):
    if not ('RSgluon' in hname or 'Zprime' in hname): return True
    pname = hname.split('__')[1]
    if ('Wide' in pname) or ('RSgluon' in pname): return False
    mass = pname.strip('Zprime')
    return float(mass) <= 3000

def wide_resonances(hname):
    if not ('RSgluon' in hname or 'Zprime' in hname): return True
    pname = hname.split('__')[1]
    if not 'Wide' in pname: return False
    mass = pname.strip('ZprimeWide')
    return float(mass) <= 3000

def rsg_resonances(hname):
    if not ('RSgluon' in hname or 'Zprime' in hname): return True
    pname = hname.split('__')[1]
    if not 'RSgluon' in pname: return False
    mass = pname.strip('RSgluon')
    return float(mass) <= 3000

def build_boosted_semileptonic_model(files, filter, signal, eflag=False):
    model = build_model_from_rootfile(files, filter, include_mc_uncertainties = True)
    model.fill_histogram_zerobins()
    model.set_signal_processes(signal)

    for p in model.processes:
        model.add_lognormal_uncertainty('lumi', math.log(1.046), p)
        if eflag:
            for obs in ['el_0top0btag_mttbar','el_0top1btag_mttbar','el_1top_mttbar']:
            #for obs in ['el_0top0btag_mttbar','el_0top1btag_mttbar']:
            #for obs in ['el_mttbar']:
                model.add_lognormal_uncertainty('ele_trig', math.log(1.01), p, obs)

    model.add_lognormal_uncertainty('ttbar_rate',   math.log(1.15), 'ttbar')
    model.add_lognormal_uncertainty('wl_rate',      math.log(1.09), 'wl')
    model.add_lognormal_uncertainty('wc_rate',      math.log(1.23), 'wc')
    model.add_lognormal_uncertainty('wb_rate',      math.log(1.23), 'wb')
    #model.add_lognormal_uncertainty('st_rate',      math.log(1.23), 'singletop')
    #model.add_lognormal_uncertainty('zj_rate',      math.log(1.50), 'zlight')
    #model.add_lognormal_uncertainty('diboson_rate', math.log(1.20), 'diboson')

    return model


import exceptions

def build_model(type):

    model = None

    if type == 'narrow_resonances_muon':
        model = build_boosted_semileptonic_model(
           muo_ifile,
           narrow_resonances,
           'Zprime*',
           eflag = False
        )

    elif type == 'wide_resonances_muon':

        model = build_boosted_semileptonic_model(
           muo_ifile,
           wide_resonances,
           'ZprimeWide*',
           eflag = False
        )

    elif type == 'rsg_resonances_muon':

        model = build_boosted_semileptonic_model(
           muo_ifile,
           rsg_resonances,
           'RSgluon*',
           eflag = False
        )

    elif type == 'narrow_resonances_electron':

        model = build_boosted_semileptonic_model(
           ele_ifile,
           narrow_resonances,
           'Zprime*',
           eflag = True
        )

    elif type == 'wide_resonances_electron':

        model = build_boosted_semileptonic_model(
           ele_ifile,
           wide_resonances,
           'ZprimeWide*',
           eflag = True
        )

    elif type == 'rsg_resonances_electron':

        model = build_boosted_semileptonic_model(
           ele_ifile,
           rsg_resonances,
           'RSgluon*',
           eflag = True
        )

    elif type == 'narrow_resonances_lepton':

        model = build_boosted_semileptonic_model(
           lep_ifile,
           narrow_resonances,
           'Zprime*',
           eflag = True
        )

    elif type == 'wide_resonances_lepton':

        model = build_boosted_semileptonic_model(
           lep_ifile,
           wide_resonances,
           'ZprimeWide*',
           eflag = True
        )

    elif type == 'rsg_resonances_lepton':

        model = build_boosted_semileptonic_model(
           lep_ifile,
           rsg_resonances,
           'RSgluon*',
           eflag = True
        )

    else: raise exceptions.ValueError('Type %s is undefined' % type)

#    for p in ['toptag', 'topmistag', 'bmistag', 'btag']:
#        model.distribution.set_distribution_parameters(p, width = float('inf'), range = [-0.0001,0.0001])
    for p in model.distribution.get_parameters():
        d = model.distribution.get_distribution(p)
        if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
            model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
            if (p == 'toptag'): model.distribution.set_distribution_parameters(p, width = float('Inf'), range = [-5.0, 5.0])
            #if (p == 'topmistag'): model.distribution.set_distribution_parameters(p, width = float('Inf'), range = [-5.0, 5.0])
            #if (p == 'toptag'): model.distribution.set_distribution_parameters(p, width = float('Inf'), range = [-1.0, 1.0])
            #if (p == 'topmistag'): model.distribution.set_distribution_parameters(p, width = float('Inf'), range = [-1.0, 1.0])
            #if (p == 'ttbar_rate'): model.distribution.set_distribution_parameters(p, mean = -0.64, width = 0.0001)
            #if (p == 'st_rate'): model.distribution.set_distribution_parameters(p, mean = 0.68, width = 0.0001)
            #if (p == 'wb_rate'): model.distribution.set_distribution_parameters(p, mean = 0.22, width = 0.0001)
            #if (p == 'wl_rate'): model.distribution.set_distribution_parameters(p, mean = 0.19, width = 0.0001)
            #if (p == 'wc_rate'): model.distribution.set_distribution_parameters(p, mean = 1.85, width = 0.0001)
            #if (p == 'diboson_rate'): model.distribution.set_distribution_parameters(p, mean = 0.08, width = 0.0001)
            #if (p == 'zj_rate'): model.distribution.set_distribution_parameters(p, mean = -0.207, width = 0.0001)
            #if (p == 'pileup'): model.distribution.set_distribution_parameters(p, mean = 1.15, width = 0.0001)
            #if (p == 'matching_wjets'): model.distribution.set_distribution_parameters(p, mean = -0.44, width = 0.0001)
            #if (p == 'jer'): model.distribution.set_distribution_parameters(p, mean = 1.1, width = 0.0001)
            #if (p == 'q2'): model.distribution.set_distribution_parameters(p, mean = 0.26, width = 0.0001)
            #if (p == 'jec'): model.distribution.set_distribution_parameters(p, mean = 0.33, width = 0.0001)
            #if (p == 'eleORjet_trig'): model.distribution.set_distribution_parameters(p, mean = 0.05, width = 0.0001)
            #if (p == 'q2_wjets'): model.distribution.set_distribution_parameters(p, mean = 0.17, width = 0.0001)
            #if (p == 'lumi'): model.distribution.set_distribution_parameters(p, mean = 0.28, width = 0.0001)
            #if (p == 'bmistag'): model.distribution.set_distribution_parameters(p, mean = 0.56, width = 0.0001)
            #if (p == 'eleid'): model.distribution.set_distribution_parameters(p, mean = 0.01, width = 0.0001)
            #if (p == 'btag'): model.distribution.set_distribution_parameters(p, mean = 1.36, width = 0.0001)
            #if (p == 'muoid'): model.distribution.set_distribution_parameters(p, mean = -0.58, width = 0.0001)
            #if (p == 'pdf'): model.distribution.set_distribution_parameters(p, mean = -0.66, width = 0.0001)
    #model.rebin('el_mttbar',50)
    #model.rebin('mu_mttbar',47)
    return model


# Code introduced by theta_driver

# Building the statistical model

options = Options()
options.set('minimizer','strategy','robust')

args = {'type': 'narrow_resonances_electron'}

model = build_model(**args)

print model.distribution.get_parameters()
args = {}


#model_summary(model)
print '/Summary'
results = mle(model, input = 'data', n = 1, with_error = True, signal_prior = 'fix:0', options = options, **args)
print '/MLE'
for r1 in results:
    print r1
    for r2 in results[r1]:
        print r2,results[r1][r2]
    print


report.write_html('htmlout')
#results = bayesian_limits(model, run_theta = True, **args)
#exp, obs = results
#execfile("utils.py")
#limit_table(exp, obs)
