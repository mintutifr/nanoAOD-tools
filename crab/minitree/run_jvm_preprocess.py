#!/usr/bin/env python3
"""
STEP 1 (run ONCE per year, shared by el and mu):
    run jetVetoMapProducer on the skim trees and store Jet_jetVetoed.

The output mirrors the input directory structure, only the base dir changes:
    /nfs/disk4/Tree_crab_lok/EIGHTEEN/MC/<Channel>/<crab dirs>/tree_N.root
 -> /nfs/disk4/Tree_crab_lok_jvm/EIGHTEEN/MC/<Channel>/<crab dirs>/tree_N.root
so the basename (tree_N.root) is unchanged -> the hadd-placeholder fix and
check_local_pooljob_status_V2.py keep working without any change.

A loose preselection (superset of ALL el+mu regions) is applied to save disk:
    (mu trigger OR el trigger) && MET filters && >=2 jets (no veto, no lepton cleaning)
The jet veto only REMOVES jets, so ">=2 jets before veto" can never reject an
event that has >=2 jets after the veto -> no event of any 2J/3J region is lost.

Usage (driver):
    python3 -u run_jvm_preprocess.py -y UL2018            -j 15
    python3 -u run_jvm_preprocess.py -y UL2018 -data -l mu -j 15
    python3 -u run_jvm_preprocess.py -y UL2018 --no-presel      (full copy, no cut)
Worker mode (called by the driver, one input file per job):
    python3 -u run_jvm_preprocess.py --worker -y UL2018 -i <in.root> -o <out_dir>
"""
import os, sys, glob, shutil, argparse
import multiprocessing as mp

year_folder = {'UL2016preVFP': 'SIXTEEN_preVFP', 'UL2016postVFP': 'SIXTEEN_postVFP',
               'UL2017': 'SEVENTEEN', 'UL2018': 'EIGHTEEN'}

# --- input / output base dirs (must match local_Minitree_UL_job_submission.py) ---
MC_IN_BASE    = '/nfs/home/common/RUN2_UL/Tree_crab/'
DATA_IN_BASE  = '/nfs/home/common/RUN2_UL/Tree_crab/'
JVM_OUT_BASE  = '/nfs/disk3/lokesh/Tree_crab_lok_jvm/'     # <-- choose where step-1 output goes

# --- loose preselection = OR of the el and mu triggers used in cut_strings.py ---
TRIG = {
    'UL2016preVFP' : "(HLT_IsoMu24==1 || HLT_IsoTkMu24==1 || HLT_Ele32_eta2p1_WPTight_Gsf==1)",
    'UL2016postVFP': "(HLT_IsoMu24==1 || HLT_IsoTkMu24==1 || HLT_Ele32_eta2p1_WPTight_Gsf==1)",
    'UL2017'       : "(HLT_IsoMu27==1 || HLT_Ele32_WPTight_Gsf_L1DoubleEG==1)",
    'UL2018'       : "(HLT_IsoMu24==1 || HLT_Ele32_WPTight_Gsf==1)",
}
MET_UL16    = "(Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_BadPFMuonDzFilter && Flag_eeBadScFilter)==1"
MET_UL17_18 = "(Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_BadPFMuonDzFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter)==1"
NJET_LOOSE  = "(Sum$(Jet_pt>40 && abs(Jet_eta)<4.7 && Jet_jetId!=0)>=2)"

def presel_for(year):
    met = MET_UL16 if year.startswith('UL2016') else MET_UL17_18
    return TRIG[year] + " && " + met + " && " + NJET_LOOSE


def run_worker(args):
    # imports here so the driver does not need ROOT / CMSSW python path
    from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
    sys.path.insert(0, os.path.join(os.environ['CMSSW_BASE'],
                'src/PhysicsTools/NanoAODTools/crab/minitree'))
    from jetVetoMapProducer import jetVetoMapProducer

    final = os.path.join(args.out, os.path.basename(args.infile))
    if os.path.isfile(final):
        print("already done, skipping :", final); return
    tmp_dir = os.path.join(args.out, '_tmp')                  # write to tmp, move when complete
    os.makedirs(tmp_dir, exist_ok=True)
    cut = None if args.no_presel else presel_for(args.year)
    print("input  :", args.infile); print("output :", final); print("cut    :", cut)

    p = PostProcessor(tmp_dir, [args.infile], cut, postfix="",
                      modules=[jetVetoMapProducer(args.year)],
                      compression="LZMA:9",            # stored long-term -> better compression than LZ4
                      provenance=False, fwkJobReport=False)
    p.run()
    shutil.move(os.path.join(tmp_dir, os.path.basename(args.infile)), final)  # atomic-ish: only complete files appear
    print("JVM_DONE", final)


def run_cmd(c): os.system(c)

def run_driver(args):
    if args.ISDATA:
        leps = [args.lepton] if args.lepton else ['el', 'mu']
        in_globs = [DATA_IN_BASE + year_folder[args.year] + '/Data_' + l + '/**/*.root' for l in leps]
        in_base = DATA_IN_BASE
    else:
        in_globs = [MC_IN_BASE + year_folder[args.year] + '/MC/' + (args.channel or '*') + '/**/*.root']
        in_base = MC_IN_BASE

    files = sorted(f for g in in_globs for f in glob.glob(g, recursive=True) if '/_tmp/' not in f)
    print("input files :", len(files))
    cmds = []
    for f in files:
        out_dir = os.path.dirname(f).replace(in_base, JVM_OUT_BASE, 1)
        if os.path.isfile(os.path.join(out_dir, os.path.basename(f))): continue
        log = out_dir + '/log/jvm_' + os.path.basename(f).replace('.root', '.txt')
        cmds.append((out_dir, f"python3 -u {os.path.abspath(__file__)} --worker -y {args.year} "
                    f"-i {f} -o {out_dir}{' --no-presel' if args.no_presel else ''} &> {log}"))
    print("jobs to run :", len(cmds))
    if args.dry: print("\n".join(c for _, c in cmds[:5])); return      # dry: write nothing
    for out_dir, _ in cmds: os.makedirs(out_dir + '/log', exist_ok=True)
    cmds = [c for _, c in cmds]
    with mp.Pool(processes=args.nproc) as pool:
        pool.map(run_cmd, cmds)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-y', '--year', required=True, choices=list(year_folder))
    ap.add_argument('-data', '--ISDATA', action='store_true')
    ap.add_argument('-l', '--lepton', default='', help="data only: el or mu (default both)")
    ap.add_argument('-c', '--channel', default='', help="MC only: one channel, e.g. ttbar_SemiLeptonic (default all)")
    ap.add_argument('-j', '--nproc', type=int, default=15)
    ap.add_argument('--no-presel', action='store_true', help="store ALL events (no cut)")
    ap.add_argument('--dry', action='store_true', help="only print the commands")
    ap.add_argument('--worker', action='store_true')
    ap.add_argument('-i', '--infile', default='')
    ap.add_argument('-o', '--out', default='')
    args = ap.parse_args()
    run_worker(args) if args.worker else run_driver(args)
