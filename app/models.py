__author__ = 'afordyce'


import random


class RPS_Basic(object):

    actions = ['rock', 'paper', 'scissors']

    def __init__(self, last_result, my_prev, opp_prev):
        self.last_result = last_result
        self.my_prev = my_prev
        self.opp_prev = opp_prev

    def get_next_action(self):
        return random.choice(self.actions)

    @staticmethod
    def trump(selection):
        i = RPS_Basic.actions.index(selection)
        return RPS_Basic.actions[(i+1) % len(RPS_Basic.actions)]


class WangXuZhou(RPS_Basic):

    def __init__(self, last_result, my_prev, opp_prev):
        super(WangXuZhou, self).__init__(last_result, my_prev, opp_prev)

    def get_next_action(self):
        if self.last_result:
            if self.last_result == "win":
                return self.opp_prev
            elif self.last_result == "lose":
                return self.trump(self.opp_prev)
            else:
                return self.trump(self.opp_prev)
        else:
            return random.choice(self.actions)


class AntiWangXuZhou(RPS_Basic):

    def __init__(self, last_result, my_prev, opp_prev):
        super(AntiWangXuZhou, self).__init__(last_result, my_prev, opp_prev)

    def get_next_action(self):
        if self.last_result:
            if self.last_result == "win":
                return self.opp_prev
            elif self.last_result == "lose":
                return self.opp_prev
            else:
                return self.trump(self.opp_prev)
        else:
            return random.choice(self.actions)


class WeightedBot(RPS_Basic):

    opponent_history = []
    my_history = []
    outcome_history = []
    current_score = 0

    def __init__(self, last_result, my_prev, opp_prev):
        super(WeightedBot, self).__init__(last_result, my_prev, opp_prev)

    def get_next_action(self):
        if self.last_result:
            self.update_stats()
            counts = self.opponent_history.count('rock'), self.opponent_history.count('paper'), self.opponent_history.count('scissors')
            return RPS_Basic.actions[counts.index(max(counts))]
        else:
            return random.choice(self.actions)

    def update_stats(self):
        self.opponent_history.append(self.opp_prev)
        self.my_history.append(self.my_prev)
        self.outcome_history.append(self.last_result)
        if self.last_result == "win":
            self.current_score += 1
        elif self.last_result == "lose":
            self.current_score -= 1


class AwesomeBot(WeightedBot):

    def __init__(self, last_result, my_prev, opp_prev):
        super(AwesomeBot, self).__init__(last_result, my_prev, opp_prev)

    def get_next_action(self):
        if self.last_result:
            self.update_stats()
            if len(self.my_history) <= 3:
                return RPS_Basic.actions[len(self.my_history)%3]
            else:
                indices = [i for i, x in enumerate(self.my_history) if x == self.my_prev]
                results = [self.opponent_history[i+1] for i in indices[:-1]]
                counts = results.count('rock'), results.count('paper'), results.count('scissors')
                return RPS_Basic.trump(RPS_Basic.actions[counts.index(max(counts))])
        else:
            return "rock"  # first time


class HubrisBot(AwesomeBot):

    def __init__(self, last_result, my_prev, opp_prev):
        super(HubrisBot, self).__init__(last_result, my_prev, opp_prev)

    def get_next_action(self):
        awesome_action = super(HubrisBot, self).get_next_action()
        return RPS_Basic.trump(awesome_action)
