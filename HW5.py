from enum import Enum
import numpy as np
import scr.SamplePathClass as PathCls
import scr.StatisticalClasses as Stat
import scr.FigureSupport as Fig

class Game(object):
    def __init__(self,id, prob_head):
        self._id=id
        self._rnd=np.random
        self._rnd.seed(id)
        self._probHead = prob_head
        self._countWins=0

    def simulate(self, nflips):
        count_tails=0
        for i in range(nflips):

            if self._rnd.random_sample() < self._probHead:
                if count_tails>=2:
                    self._countWins+=1
                count_tails=0
            else:
                count_tails +=1
    def get_reward(self):
        return 100*self._countWins-250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = []

        for n in range(n_games):
            game=Game(id=n, prob_head=prob_head)
            game.simulate(20)
            self._gameRewards.append(game.get_reward())

    def simulate(self):
        return CohortOutcomes(self)

    def get_max(self):
        return max(self._gameRewards)

    def get_min(self):
        return min(self._gameRewards)

    def get_rewards(self):
        return self._gameRewards

    def get_loss(self, n_games):
        loss=0
        for observations in self._gameRewards:
            if observations<250:
                loss+=1

        return loss/n_games




games = SetOfGames(prob_head=0.5, n_games=1000)

print('Maximum Expected reward is:', games.get_max(),'. ' 'Minimum Expected reward is:', games.get_min())

print('The probability that you lose money in this game is:', games.get_loss(1000))
# Problem1. Histogram of Rewards

Fig.graph_histogram(
    observations=games.get_rewards(),
    title='Histogram of Rewards using 1000 games with a fair coin',
    x_label='Rewards',
    y_label='Game Frequency')