#!/usr/bin/env python2
# Run the foresting configuration on PbPb in CMSSW_5_3_X, using the new HF/Voronoi jets
# Author: Alex Barbieri
# Date: 2013-10-15

hiTrackQuality = "highPurity"              # iterative tracks
#hiTrackQuality = "highPuritySetWithPV"    # calo-matched tracks

import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')
process.options = cms.untracked.PSet(
    # wantSummary = cms.untracked.bool(True)
    #SkipEvent = cms.untracked.vstring('ProductNotFound')
)

#####################################################################################
# HiForest labelling info
#####################################################################################

process.load("HeavyIonsAnalysis.JetAnalysis.HiForest_cff")
process.HiForest.inputLines = cms.vstring("HiForest V3",)
import subprocess
version = subprocess.Popen(["(cd $CMSSW_BASE/src && git describe --tags)"], stdout=subprocess.PIPE, shell=True).stdout.read()
if version == '':
    version = 'no git info'
process.HiForest.HiForestVersion = cms.untracked.string(version)

#####################################################################################
# Input source
#####################################################################################

process.source = cms.Source("PoolSource",
                            duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
                            fileNames = cms.untracked.vstring(
    #"file:/mnt/hadoop/cms/store/user/vzhukova/HIJING_GEN-SIM_NEWFIX_batch2/Pyquen_allQCDPhoton30_RECO/b7d33bba7673cdb1ee6f4983c0800c79/Pyquen_allQCDPhoton_RECO_42_1_Itt.root"
#'root://xrootd1.cmsaf.mit.edu//store/user/vzhukova/HIJING_MB/HIJING_MB_RECO_v3/13a591fee6315e7fb1e99e6ba8e52eaa/reco_hijing_1001_1_NXZ.root'    
#'root://xrootd1.cmsaf.mit.edu//store/user/vzhukova/HIJING_GEN-SIM_NEWFIX_batch5/Hijing_mix_Dijet80_5p02TeV_v2/a92d7bf0feab41fbd4f9b131cc2a48fe/Hijing_mix_Dijet80_5p02TeV_100_1_rcc.root'
#Jet_MB mixed reco:
'root://xrootd1.cmsaf.mit.edu//store/user/vzhukova/HIJING_GEN-SIM_NEWFIX_batch5/Hijing_mix_Dijet80_5p02TeV_RECO/b7d33bba7673cdb1ee6f4983c0800c79/Hijing_mix_Dijet80_5p02TeV_RECO_10_1_d9Q.root'
))

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1))


#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.ReconstructionHeavyIons_cff')
process.load('RecoHI.HiCentralityAlgos.pACentrality_cfi')
process.load('RecoHI.HiCentralityAlgos.CentralityBin_cfi')

process.load('FWCore.MessageService.MessageLogger_cfi')

# PbPb 53X MC
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'STARTHI53_V28::All', '')

from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import *
overrideGT_pPb5020(process)

process.HeavyIonGlobalParameters = cms.PSet(
    centralityVariable = cms.string("HFtowersTrunc"),
    nonDefaultGlauberModel = cms.string("Hijing"),
    centralitySrc = cms.InputTag("pACentrality"),
    pPbRunFlip = cms.untracked.uint32(211313)
    )

process.pACentrality.producePixelhits = cms.bool(False)

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string("HiForest.root"))

#####################################################################################
# Additional Reconstruction and Analysis: Main Body
#####################################################################################

process.load('Configuration.StandardSequences.Generator_cff')
process.load('RecoJets.Configuration.GenJetParticles_cff')

process.hiGenParticles.srcVector = cms.vstring('generator')

#process.hiCentrality.producePixelhits = False
#process.hiCentrality.producePixelTracks = False
#process.hiCentrality.srcTracks = cms.InputTag("generalTracks")
#process.hiCentrality.srcVertex = cms.InputTag("offlinePrimaryVerticesWithBS")
process.hiEvtPlane.vtxCollection_ = cms.InputTag("offlinePrimaryVerticesWithBS")
process.hiEvtPlane.trackCollection_ = cms.InputTag("generalTracks")

process.load('HeavyIonsAnalysis.JetAnalysis.jets.HiGenJetsCleaned_cff')

process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu3CaloJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs3CaloJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs3PFJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu3PFJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak3PFJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak3CaloJetSequence_pPb_mc_cff')

process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu4CaloJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs4CaloJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs4PFJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu4PFJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak4PFJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak4CaloJetSequence_pPb_mc_cff')

process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu5CaloJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs5CaloJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs5PFJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu5PFJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak5PFJetSequence_pPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak5CaloJetSequence_pPb_mc_cff')

# Difference between HiReRecoJets_pp_cff and HiReRecoJets_HI_cff is
# particle flow collection used.
process.load('HeavyIonsAnalysis.JetAnalysis.jets.HiReRecoJets_pp_cff')

process.voronoiBackgroundPF.src = cms.InputTag("particleFlow")
process.PFTowers.src = cms.InputTag("particleFlow")

process.jetSequences = cms.Sequence(process.voronoiBackgroundCalo +
                                    process.voronoiBackgroundPF +
                                    process.PFTowers +
                                    process.hiReRecoCaloJets +
                                    process.hiReRecoPFJets +

                                    process.akPu3CaloJetSequence +
                                    process.akVs3CaloJetSequence +
                                    process.akVs3PFJetSequence +
                                    process.akPu3PFJetSequence +
                                    process.ak3PFJetSequence +
                                    process.ak3CaloJetSequence +

                                    process.akPu4CaloJetSequence +
                                    process.akVs4CaloJetSequence +
                                    process.akVs4PFJetSequence +
                                    process.akPu4PFJetSequence +
                                    process.ak4PFJetSequence +
                                    process.ak4CaloJetSequence +

                                    process.akPu5CaloJetSequence +
                                    process.akVs5CaloJetSequence +
                                    process.akVs5PFJetSequence +
                                    process.akPu5PFJetSequence +
                                    process.ak5PFJetSequence +
                                    process.ak5CaloJetSequence

                                    )



process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_mc_cfi')
process.hiEvtAnalyzer.Vertex = cms.InputTag("offlinePrimaryVerticesWithBS")

process.load('HeavyIonsAnalysis.JetAnalysis.HiGenAnalyzer_cfi')

#####################################################################################
# To be cleaned

process.load('HeavyIonsAnalysis.JetAnalysis.ExtraTrackReco_cff')
#process.load('HeavyIonsAnalysis.JetAnalysis.ExtraPfReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_MC_cff')
process.load("HeavyIonsAnalysis.TrackAnalysis.METAnalyzer_cff")
process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzer_pp_cfi")
process.load('HeavyIonsAnalysis.JetAnalysis.rechitanalyzer_pp_cfi')
process.rechitAna = cms.Sequence(process.rechitanalyzer+process.pfTowers)
process.pfcandAnalyzer.skipCharged = False
process.pfcandAnalyzer.pfPtMin = 0

#######################
# V0Analyzer
#######################

##process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("SimTracker.TrackAssociation.TrackAssociatorByHits_cfi")
process.load("SimTracker.TrackAssociation.TrackAssociatorByChi2_cfi")
process.load("RiceHIG.V0Analysis.v0selector_cff")
process.load("RiceHIG.V0Analysis.v0validator_cff")
process.load("RecoVertex.V0Producer.generalV0Candidates_cff")
process.load("V0Analyzer.V0Analyzer.v0analyzer_cfi")

#process.v0analyzerplugin.generalV0_ks = cms.InputTag('selectV0CandidatesNewkshort:Kshort')
#process.v0analyzerplugin.genrealV0_la = cms.InputTag('selectV0CandidatesNewlambda:Lambda')

process.generalV0CandidatesNew = process.generalV0Candidates.clone (
    tkNhitsCut = cms.int32(0),
    tkChi2Cut = cms.double(7.0),
    dauTransImpactSigCut = cms.double(1.0),
    dauLongImpactSigCut = cms.double(1.0),
    xiVtxSignificance3DCut = cms.double(0.0),
    xiVtxSignificance2DCut = cms.double(0.0),
    vtxSignificance2DCut = cms.double(0.0),
    vtxSignificance3DCut = cms.double(4.0)
)

process.v0Validator.kShortCollection = cms.InputTag('selectV0CandidatesNewkshort:Kshort')
process.v0Validator.lambdaCollection = cms.InputTag('selectV0CandidatesNewlambda:Lambda')
process.v0Validator.isMatchByHitsOrChi2 = cms.bool(True)
process.v0Validator.isMergedTruth = cms.bool(True)

process.selectV0CandidatesNewlambda.v0CollName = cms.string("generalV0CandidatesNew")
process.selectV0CandidatesNewkshort.v0CollName = cms.string("generalV0CandidatesNew")

process.selectV0CandidatesNewkshort.cosThetaCut = cms.double(0.99)
process.selectV0CandidatesNewkshort.decayLSigCut = cms.double(5.0)
process.selectV0CandidatesNewkshort.misIDMassCut   = cms.double(0.015)
process.selectV0CandidatesNewkshort.misIDMassCutEE = cms.double(0.015)
process.selectV0CandidatesNewlambda.cosThetaCut = cms.double(0.99)
process.selectV0CandidatesNewlambda.decayLSigCut = cms.double(5.0)
process.selectV0CandidatesNewlambda.misIDMassCut   = cms.double(0.015)
process.selectV0CandidatesNewlambda.misIDMassCutEE = cms.double(0.015)

#process.v0select_analyzer = cms.Sequence(process.selectV0CandidatesNewlambda*process.selectV0CandidatesNewkshort*process.ana)

#########################
# Track Analyzer
#########################
process.hiTracks.cut = cms.string('quality("highPurity")')

# clusters missing in recodebug - to be resolved
process.anaTrack.doPFMatching = False

#####################
# photons
process.interestingTrackEcalDetIds.TrackCollection = cms.InputTag("hiGeneralTracks")
process.load("RecoEcal.EgammaCoreTools.EcalNextToDeadChannelESProducer_cff")
process.load('HeavyIonsAnalysis.JetAnalysis.ExtraEGammaReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.EGammaAnalyzers_cff')
process.multiPhotonAnalyzer.GenEventScale = cms.InputTag("generator")
process.multiPhotonAnalyzer.HepMCProducer = cms.InputTag("generator")
process.multiPhotonAnalyzer.gsfElectronCollection = cms.untracked.InputTag("ecalDrivenGsfElectrons")
process.load("edwenger.HiTrkEffAnalyzer.TrackSelections_cff")
process.hiGoodTracks.src = cms.InputTag("generalTracks")
process.hiGoodTracks.vertices = cms.InputTag("offlinePrimaryVerticesWithBS")
process.cleanPhotons.primaryVertexProducer = cms.string("offlinePrimaryVerticesWithBS")
process.reducedEcalRecHitsEB = cms.EDProducer("ReducedRecHitCollectionProducer",
    interestingDetIdCollections = cms.VInputTag(cms.InputTag("interestingEcalDetIdEB"), cms.InputTag("interestingEcalDetIdEBU")),
    recHitsLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    reducedHitsCollection = cms.string('')
)
process.reducedEcalRecHitsEE = cms.EDProducer("ReducedRecHitCollectionProducer",
    interestingDetIdCollections = cms.VInputTag(cms.InputTag("interestingEcalDetIdEE")),
    recHitsLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    reducedHitsCollection = cms.string('')
)
process.patPhotons.addPhotonID = cms.bool(False)
process.photonMatch.matched = cms.InputTag("hiGenParticles")
process.multiPhotonAnalyzer.GammaEtaMax = cms.untracked.double(100)
process.multiPhotonAnalyzer.GammaPtMin = cms.untracked.double(10)
process.RandomNumberGeneratorService.multiPhotonAnalyzer = process.RandomNumberGeneratorService.generator.clone()

process.genStep = cms.Path(process.hiGenParticles *
                           process.hiGenParticlesForJets)

process.photonStep = cms.Path(process.hiGoodTracks * process.photon_extra_reco * process.makeHeavyIonPhotons)
process.photonStep.remove(process.interestingTrackEcalDetIds)
process.photonStep.remove(process.seldigis)
process.extrapatstep = cms.Path(process.selectedPatPhotons)

#####################
# muons
######################
process.load("HeavyIonsAnalysis.MuonAnalysis.hltMuTree_cfi")
process.hltMuTree.doGen = cms.untracked.bool(True)
process.load("RecoHI.HiMuonAlgos.HiRecoMuon_cff")
process.muons.JetExtractorPSet.JetCollectionLabel = cms.InputTag("akVs3PFJets")
process.globalMuons.TrackerCollectionLabel = "generalTracks"
process.muons.TrackExtractorPSet.inputTrackCollection = "generalTracks"
process.muons.inputCollectionLabels = ["generalTracks", "globalMuons", "standAloneMuons:UpdatedAtVtx", "tevMuons:firstHit", "tevMuons:picky", "tevMuons:dyt"]


process.temp_step = cms.Path(
                             process.ak2HiGenJets +
                             process.ak3HiGenJets +
                             process.ak4HiGenJets +
                             process.ak5HiGenJets +
                             process.ak6HiGenJets +
                             process.ak7HiGenJets)

process.ana_step = cms.Path(
                            process.pACentrality +
                            process.centralityBin +
                            process.hiEvtPlane +
                            process.heavyIon*
                            process.hiEvtAnalyzer*
                            process.HiGenParticleAna*
                            process.hiGenJetsCleaned*
                            process.jetSequences +
                              #process.multiPhotonAnalyzer +
                            process.pfcandAnalyzer +
                            process.rechitAna +
#temp                            process.hltMuTree +
                            process.HiForest +
                            process.cutsTPForFak +
                            process.cutsTPForEff +
                            process.ppTrack*
                            process.generalV0CandidatesNew*
                            process.selectV0CandidatesNewlambda*
                            process.selectV0CandidatesNewkshort*
                            process.ana
)

process.load('HeavyIonsAnalysis.JetAnalysis.EventSelection_cff')
process.phltJetHI = cms.Path( process.hltJetHI )
#process.pcollisionEventSelection = cms.Path(process.collisionEventSelection)
process.pHBHENoiseFilter = cms.Path( process.HBHENoiseFilter )
process.phfCoincFilter = cms.Path(process.hfCoincFilter )
process.phfCoincFilter3 = cms.Path(process.hfCoincFilter3 )
#process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter )
process.phltPixelClusterShapeFilter = cms.Path(process.siPixelRecHits*process.hltPixelClusterShapeFilter )
process.phiEcalRecHitSpikeFilter = cms.Path(process.hiEcalRecHitSpikeFilter )

# Customization
from HeavyIonsAnalysis.JetAnalysis.customise_cfi import *
setPhotonObject(process,"cleanPhotons")

process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')

process.hltAna = cms.Path(process.hltanalysis)
process.pAna = cms.EndPath(process.skimanalysis)
