import FWCore.ParameterSet.Config as cms

# ---------------------------------------------------------

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'output.root'
options.inputFiles = ['root://eoscms.cern.ch//store/relval/CMSSW_10_1_0_pre2/RelValTTbar_13/MINIAODSIM/100X_mcRun2_asymptotic_v2_FastSim-v1/20000/3E39F14C-0420-E811-B368-0025905A6068.root', 
#		      'root://eoscms.cern.ch//store/relval/CMSSW_10_1_0_pre2/RelValTTbar_13/MINIAODSIM/100X_mcRun2_asymptotic_v2_FastSim-v1/20000/40C11C7A-0E1F-E811-8A3A-0025905A607E.root', 
#		      'root://eoscms.cern.ch//store/relval/CMSSW_10_1_0_pre2/RelValTTbar_13/MINIAODSIM/100X_mcRun2_asymptotic_v2_FastSim-v1/20000/F297A748-B220-E811-B9DD-0CC47A4C8EA8.root'
]
#options.inputFiles = ['root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-2500_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/0A83E4E2-34B6-E611-89A0-549F35AE4FA2.root',
#		      'root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-2500_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/A88400F5-39B6-E611-BEB3-A0369F7F9DE0.root']
#options.inputFiles = ['root://cmsxrootd.fnal.gov//store/relval/CMSSW_9_2_2/RelValTTbar_13/MINIAODSIM/PU25ns_92X_upgrade2017_realistic_v1-v1/10000/8E7EE25F-294E-E711-A5CC-0025905B8610.root']
#options.inputFiles = ['/store/relval/CMSSW_8_0_21/RelValTTbar_13/MINIAODSIM/PU25ns_80X_mcRun2_asymptotic_2016_TrancheIV_v6_Tr4GT_v6-v1/10000/74087230-AB98-E611-93EF-0025905A6138.root']
#options.inputFiles = ['root://eoscms.cern.ch//store/relval/CMSSW_10_1_0_pre2/RelValQCD_FlatPt_15_3000_13/MINIAODSIM/100X_mcRun2_asymptotic_v2_FastSim-v1/20000/8C8833F5-D822-E811-8ED5-0CC47A4D76A2.root']

options.maxEvents = -1

options.register('inputScript', '', VarParsing.multiplicity.singleton, VarParsing.varType.string, "input Script")
options.register('skipEvents', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "skip N events")
options.register('job', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "job number")
options.register('nJobs', 1, VarParsing.multiplicity.singleton, VarParsing.varType.int, "total jobs")
options.register('fjKeepFlavors', [], VarParsing.multiplicity.list, VarParsing.varType.int, "Types of fatjet to keep in this sample")
# options.register('gluonReduction', 0.0, VarParsing.multiplicity.singleton, VarParsing.varType.float, "gluon reduction")
options.register('inputDataset',
                 '',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Input dataset")

options.setupTags(tag='%d', ifCond='nJobs > 1', tagArg='job')
options.parseArguments()

#options.inputDataset='/RelValQCD_FlatPt_15_3000_13/CMSSW_10_1_0_pre2-100X_mcRun2_asymptotic_v2_FastSim-v1/MINIAODSIM'

# ---------------------------------------------------------

process = cms.Process("DNNFiller")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
if not options.inputScript:  # this is probably for testing
	process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.options = cms.untracked.PSet(
   allowUnscheduled = cms.untracked.bool(True),  
   wantSummary=cms.untracked.bool(False)
)

print ('Using output file ' + options.outputFile)

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string(options.outputFile))

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(options.maxEvents))

process.source = cms.Source('PoolSource',
    fileNames=cms.untracked.vstring(options.inputFiles),
    skipEvents=cms.untracked.uint32(options.skipEvents)
)

if options.inputScript:
    process.load(options.inputScript)

numberOfFiles = len(process.source.fileNames)
numberOfJobs = options.nJobs
jobNumber = options.job

process.source.fileNames = process.source.fileNames[jobNumber:numberOfFiles:numberOfJobs]
if options.nJobs > 1:
    print ("running over these files:")
    print (process.source.fileNames)

# ---------------------------------------------------------

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
# process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

# ---------------------------------------------------------

bTagInfos = [
	'pfImpactParameterTagInfos',
	'pfInclusiveSecondaryVertexFinderTagInfos',
	'pfDeepCSVTagInfos',
	'pfBoostedDoubleSVAK8TagInfos'
]

bTagDiscriminators = [
	'softPFMuonBJetTags',
	'softPFElectronBJetTags',
	'pfJetBProbabilityBJetTags',
	'pfJetProbabilityBJetTags',
	'pfCombinedInclusiveSecondaryVertexV2BJetTags',
	'pfDeepCSVJetTags:probudsg',
	'pfDeepCSVJetTags:probb',
	'pfDeepCSVJetTags:probc',
	'pfDeepCSVJetTags:probbb',
	#'pfDeepCSVJetTags:probcc',
	'pfBoostedDoubleSecondaryVertexAK8BJetTags'
]

jetCorrectionsAK8 = ('AK8PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
updateJetCollection(
        process,
        labelName = "DeepFlavour",
        jetSource = cms.InputTag('slimmedJetsAK8'),
        jetCorrections = jetCorrectionsAK8,
        pfCandidates = cms.InputTag('packedPFCandidates'),
        pvSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
        svSource = cms.InputTag('slimmedSecondaryVertices'),
        muSource = cms.InputTag('slimmedMuons'),
        elSource = cms.InputTag('slimmedElectrons'),
        btagInfos = bTagInfos,
        btagDiscriminators = bTagDiscriminators,
        explicitJTA = False
)

if hasattr(process,'updatedPatJetsTransientCorrectedDeepFlavour'):
	process.updatedPatJetsTransientCorrectedDeepFlavour.addTagInfos = cms.bool(True) 
	process.updatedPatJetsTransientCorrectedDeepFlavour.addBTagInfo = cms.bool(True)
else:
	raise ValueError('I could not find updatedPatJetsTransientCorrectedDeepFlavour to embed the tagInfos, please check the cfg')
# ---------------------------------------------------------

'''
from RecoJets.JetProducers.ak4GenJets_cfi import ak8GenJets
process.ak8GenJetsWithNu = ak4GenJets.clone(src='packedGenParticles')
 
 ## Filter out neutrinos from packed GenParticles
process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16"))
 ## Define GenJets
process.ak8GenJetsRecluster = ak8GenJets.clone(src='packedGenParticlesForJetsNoNu')

 
process.patGenJetMatchWithNu = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
    src         = cms.InputTag("selectedUpdatedPatJetsDeepFlavour"),      # RECO jets (any View<Jet> is ok) 
    matched     = cms.InputTag("ak8GenJetsWithNu"),        # GEN jets  (must be GenJetCollection)              
    mcPdgId     = cms.vint32(),                      # n/a   
    mcStatus    = cms.vint32(),                      # n/a   
    checkCharge = cms.bool(False),                   # n/a   
    maxDeltaR   = cms.double(0.8),                   # Minimum deltaR for the match   
    #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
    resolveAmbiguities    = cms.bool(True),          # Forbid two RECO objects to match to the same GEN object 
    resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
)

process.patGenJetMatchRecluster = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
    src         = cms.InputTag("selectedUpdatedPatJetsDeepFlavour"),      # RECO jets (any View<Jet> is ok) 
    matched     = cms.InputTag("ak8GenJetsRecluster"),        # GEN jets  (must be GenJetCollection)              
    mcPdgId     = cms.vint32(),                      # n/a   
    mcStatus    = cms.vint32(),                      # n/a   
    checkCharge = cms.bool(False),                   # n/a   
    maxDeltaR   = cms.double(0.8),                   # Minimum deltaR for the match   
    #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
    resolveAmbiguities    = cms.bool(True),          # Forbid two RECO objects to match to the same GEN object 
    resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
)

process.genJetSequence = cms.Sequence(process.packedGenParticlesForJetsNoNu*process.ak4GenJetsWithNu*process.ak4GenJetsRecluster*process.patGenJetMatchWithNu*process.patGenJetMatchRecluster)

# ---------------------------------------------------------

# Very Loose IVF SV collection
from PhysicsTools.PatAlgos.tools.helpers import loadWithPrefix
loadWithPrefix(process, 'RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff', "looseIVF")
process.looseIVFinclusiveCandidateVertexFinder.primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
process.looseIVFinclusiveCandidateVertexFinder.tracks = cms.InputTag("packedPFCandidates")
process.looseIVFinclusiveCandidateVertexFinder.vertexMinDLen2DSig = cms.double(0.)
process.looseIVFinclusiveCandidateVertexFinder.vertexMinDLenSig = cms.double(0.)
process.looseIVFinclusiveCandidateVertexFinder.fitterSigmacut = 20

process.looseIVFcandidateVertexArbitrator.primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
process.looseIVFcandidateVertexArbitrator.tracks = cms.InputTag("packedPFCandidates")
process.looseIVFcandidateVertexArbitrator.secondaryVertices = cms.InputTag("looseIVFcandidateVertexMerger")
process.looseIVFcandidateVertexArbitrator.fitterSigmacut = 20
'''

# ---------------------------------------------------------

# DeepNtuplizer
process.load("DeepNTuples.NtupleAK8.DeepNtuplizerAK8_cfi")
process.deepntuplizer.jets = cms.InputTag('selectedUpdatedPatJetsDeepFlavour')
process.deepntuplizer.bDiscriminators = bTagDiscriminators 
process.deepntuplizer.bDiscriminators.append('pfCombinedMVAV2BJetTags')
process.deepntuplizer.LooseSVs = cms.InputTag("looseIVFinclusiveCandidateSecondaryVertices")

process.deepntuplizer.fjKeepFlavors = cms.untracked.vuint32(options.fjKeepFlavors)
process.deepntuplizer.isQCDSample = ('/QCD_' in options.inputDataset or '/RelValQCD_' in options.inputDataset)

# process.deepntuplizer.gluonReduction = cms.double(options.gluonReduction)
# process.p = cms.Path(process.QGTagger + process.genJetSequence * process.deepntuplizer)
# process.p = cms.Path(process.deepntuplizer)

#Trick to make it work in >=9_1_X
process.tsk = cms.Task()
for mod in process.producers_().itervalues():
    process.tsk.add(mod)
for mod in process.filters_().itervalues():
    process.tsk.add(mod)

process.p = cms.Path(
#	process.QGTagger + process.genJetSequence*  
	process.deepntuplizer,
	process.tsk
	)
