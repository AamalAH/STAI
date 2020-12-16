import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from time import time
from tqdm import tqdm
from os import mkdir
from qUpdater.TwoPlayers import *

mkdir("Figures")
mkdir("Data")

gamma = 0.1
Gamma = 0.1
tau = 5e-2

nActions = 2
t0 = 500

initnSim = 1

nSim = 1
nIter = int(1.5e3)
nNbr = 24


def KantzLCE(data):
    return [np.mean(np.linalg.norm(data[i, 1:, 0, :] - data[i, 0, 0, :], axis=1)) for i in range(nIter)]



for alpha in tqdm(np.linspace(1e-2, 5e-2, num=10)):
    for Gamma in np.linspace(-1, 1, num=10):
        payoffs = generateGames(Gamma, nSim, nActions)
        allActions = []

        qValues0 = np.random.rand(2 * nActions, nSim)
        allQ = [qValues0] + [qValues0 + 0.01 * np.random.multivariate_normal(np.zeros(2 * nActions), np.eye(2 * nActions)).reshape((2*nActions, nSim)) for i in range(nNbr)]
        allQ = [q.reshape((2, nActions, nSim)) for q in allQ]

        for cIter in range(nIter):
            allQ = [qUpdate(q, payoffs, nSim, nActions, agentParams=(alpha, tau, gamma)) for q in allQ]
            allActions += [[getActionProbs(q, nSim, agentParams=(alpha, tau, gamma)) for q in allQ]]

        allActions = np.array(allActions).reshape((nIter, nNbr+1, nSim, 2 * nActions))

        dS = KantzLCE(allActions)

        plt.plot(np.log(dS)), plt.savefig("Figures/tau_{0}_alpha_{1}_Gamma_{2}.png".format(tau, alpha, Gamma)), plt.close()
        with open("Data/tau_{0}_alpha_{1}_Gamma_{2}.txt".format(tau, alpha, Gamma), 'w') as f:
            f.write(str(dS))
            f.close()

