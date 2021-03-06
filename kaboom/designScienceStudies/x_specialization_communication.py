import numpy as np
import time as timer
import multiprocessing
from matplotlib import pyplot as plt
#import pickle
import itertools
import os

from kaboom.params import Params
from kaboom import modelFunctions as m
from kaboom.kaboom import teamWorkProcess


# x: specialization vs communication
#A 1.6 composition vs commRate
def run():
    p= Params()

    p.nAgents = 20
    p.nTeams = 4
    p.nDims = 20
    p.agentTeams = m.specializedTeams(p.nAgents,p.nTeams)
    p.teamDims = m.teamDimensions(p.nDims,p.nTeams) #np.ones([nTeams,nDims])
    pComms = np.linspace(0,1,11)
    p.aiScore = 95

    t0 = timer.time()
    p=Params()
    # selfBias = 0.5
    # curatedTeams = False
#    shareAcrossTeams = True

    p.nAgents = 16
    #Homogeneous teams
    p.nDims = 16
    p.aiScore = 100#300
    p.aiRange = 0

    #p.reps = 1#8

    scoreForNteams = []
    for nTeams in [1,2,4,8,16]:
        p.nTeams = nTeams
        p.agentTeams = m.specializedTeams(p.nAgents,p.nTeams)
        p.teamDims = m.teamDimensions(p.nDims,p.nTeams)

        pComms = np.linspace(0,1,6)

        meetingTimes = 100

        allTeamObjects = []
        for pComm in pComms:
            if __name__ == '__main__' or 'kaboom.designScienceStudies.x_specialization_communication':
                pool = multiprocessing.Pool(processes = 4)
                allTeams = pool.starmap(teamWorkProcess, zip(range(p.reps),itertools.repeat(p)))
                print('next. time: '+str(timer.time()-t0))
                allTeamObjects.append(allTeams)
        # allTeams = [t for tl in allTeamObjects for t in tl]
        scoreForNteams.append(allTeamObjects)
    print("time to complete: "+str(timer.time()-t0))

    teamShapes = [1,2,4,8,16]
    for i in range(len(teamShapes)):
        nT = scoreForNteams[i]
        print(np.shape(nT[0:-1]))
        allTeams = [t for s in nT for t in s]
    #    directory = saveResults(allTeams,'collabTradeoff_'+str(teamShapes[i])+'_team')
        allScores = np.array([t.getBestScore() for set in nT[0:-1] for t in set])*-1
        pC = [pc for pc in pComms[0:-1] for i in range(p.reps)]
        m.plotCategoricalMeans(pC,allScores)
    plt.legend(['flat team of 16','2 subteams of 8','4 subteams of 4','8 subteams of 8','16 subteams of 1'])
    myPath = os.path.dirname(__file__)
    plt.savefig(myPath+"/results/x_communication_structure.pdf")
