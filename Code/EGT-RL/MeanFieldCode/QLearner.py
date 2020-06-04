import numpy as np

class QLearner:
    def __init__(self, params, nActions, payOff, nOpponents):
        self.gamma = 0.1
        self.tau   = params[0]
        self.alpha = params[1]

        self.nActions = nActions
        self.nOpponents = nOpponents

        rMin = np.amin(payOff)
        rMax = np.amax(payOff)

        self.qValues = np.random.rand(nActions)*(rMax-rMin)+rMin
        self.partitionFunction = np.sum([np.exp(self.tau * i) for i in self.qValues])
        self.actionProb = [np.exp(self.tau * i) / self.partitionFunction for i in self.qValues]

        self.action = 0
        self.payOffs = []

        self.gamesPlayed = 0

    def selectAction(self):
        self.partitionFunction = np.sum([np.exp(self.tau * i) for i in self.qValues])
        self.actionProb = [np.exp(self.tau * i) / self.partitionFunction for i in self.qValues]

        self.action = np.random.choice([0, 1], p=self.actionProb)

    def playGame(self, opponents, game):
        payOffs = np.array(game[self.action, np.array([o.action for o in opponents])]).T
        self.payOffs += list(payOffs[0])
        for o in range(len(opponents)):
            opponents[o].payOffs += [payOffs[1, o]]


    def qUpdate(self):

        self.payoff = np.mean(self.payOffs[0:self.nOpponents])
        # self.qValues[self.action] = (1 - self.alpha) * self.qValues[self.action] + self.alpha * self.payoff

        self.qValues[self.action] += self.alpha * (self.payoff + self.gamma * max(self.qValues) - self.qValues[self.action])
