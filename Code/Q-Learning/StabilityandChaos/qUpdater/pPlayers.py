import numpy as np
import itertools
import scipy.sparse as sps
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm



def generateGames(gamma, nSim, nAct, nPlayers):
    """
    Draw a random payoff matrix from a multivariate Gaussian, currently the unscaled version.
    gamma: Choice of co-operation parameter
    nAct: Number of actions in the game
    [reward1s, reward2s]: list of payoff matrices
    """

    nElements = nAct ** nPlayers  # number of payoff elements in a player's matrix

    cov = sps.lil_matrix(sps.eye(nPlayers * nElements))

    for i in range(nElements):
        for p in range(1, nPlayers):
            cov[i, i + nElements * p] = gamma / (nPlayers - 1)
            cov[i + nElements * p, i] = gamma / (nPlayers - 1)

    allPayoffs = np.zeros((nPlayers, nElements, nSim))

    for cSim in range(nSim):
        rewards = np.zeros(nPlayers * nElements) + np.linalg.cholesky(cov.todense()) @ np.random.standard_normal(nPlayers * nElements)
        # rewards = np.random.multivariate_normal(np.zeros(nPlayers * nElements), cov=cov.todense())
        each = np.array_split(rewards, nPlayers)
        allPayoffs[:, :, cSim] = each

    return allPayoffs

def getActionProbs(qValues, gameParams, agentParams):
    
    nSim, nPlayers, nActions = gameParams
    alpha, tau, gamma = agentParams
    
    partitionFunction = np.expand_dims(np.sum(np.exp(tau * qValues), axis=1), axis = 1)
    partitionFunction = np.hstack([partitionFunction]*nActions)
    actionProbs = np.exp(tau * qValues)/partitionFunction
    return actionProbs


def qUpdate(qValues, payoffs, gameParams, agentParams):
    nSim, nPlayers, nActions = gameParams
    alpha, tau, gamma = agentParams
    idX = list(itertools.product(list(range(0, nActions)), repeat=nPlayers))
    actionProbs = getActionProbs(qValues, gameParams, agentParams)
    bChoice = np.array([[np.random.choice(list(range(nActions)), p=actionProbs[p, :, s]) for s in range(nSim)] for p in range(nPlayers)])

    rewards = np.array([[payoffs[p, np.where([np.all(idX[i] == np.roll(bChoice[:, s], -1 * p)) for i in range(len(idX))])[0][0], s] for s in range(nSim)] for p in range(nPlayers)])
    for s in range(nSim):
        qValues[range(nPlayers), bChoice[:, s], s] += alpha * (rewards[:, s] - qValues[range(nPlayers), bChoice[:, s], s] + gamma * np.max(qValues[:, :, s], axis = 1))

    return qValues

def checkminMax(allActions, nSim, tol):
    a = np.reshape(allActions, (t0, nSim, nActions * 2))
    relDiff = ((np.max(a, axis=0) - np.min(a, axis=0))/np.min(a, axis=0))
    return np.all(relDiff < tol, axis=1)

def getVariance(allActions):
    h = (1 / nActions) * np.sum((1 / t0) * np.sum(allActions ** 2, axis=0) - ((1 / t0) * np.sum(allActions, axis=0)) ** 2,
                              axis=2)
    v = np.mean(np.var(allActions, axis = 0), axis = 2)
    return v

if __name__ == "__main__":
    
    t0 = 500
    gamma = .1
    tau = 1
    alpha = 0.01
    
    initnSim = 1
    nIter = int(1.5e4)
    nTests = 10
    
    nPlayers = 2
    nActions = 2

    for alpha in np.linspace(1e-2, 5e-2, num=1):
        for Gamma in np.linspace(-1, 0, num=1):
    
            allActions = []
            nSim = initnSim
            converged = 0
    
            payoffs = generateGames(Gamma, nSim, nActions, nPlayers)
            qValues0 = np.random.rand(nPlayers, nActions, nSim)
    
            for cIter in tqdm(range(1001)):
    
                allActions += [getActionProbs(qValues0)]
                qValues0 = qUpdate(qValues0, payoffs, nSim)
    
    allActions = np.array(allActions)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for i in range(nSim):
        plt.plot(allActions[:, 0, 0, i], allActions[:, 1, 0, i])
    
    plt.xlabel('Player 1 Action 1')
    plt.ylabel('Player 2 Action 1')
    # ax.set_zlabel('Player 3 Action 1')
    
    ax.set_xlim([0, 1]), ax.set_ylim([0, 1]), plt.show()