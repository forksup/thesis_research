import random
from itertools import product

from Models.model_sources.chain_source import ChainGenerator
from string import ascii_letters
from sklearn.model_selection import train_test_split
from random import randint, uniform
from Models.model_sources.path_encoder import PathEncoder
from datetime import datetime

class HMM_Casual(object):

    @staticmethod
    def gen_data(state_size, order, size, verbose=False):
        cg = ChainGenerator(tuple(ascii_letters[:state_size]), order=order, min_len= order, max_len= order)

        for i, idx in enumerate(product(range(state_size), repeat=order)):
            for s in idx:
                cg.transition_matrix[i][s] *= 10

        for s in range(len(cg.transition_matrix)):
            total = sum(cg.transition_matrix[s])
            if total != 1:
                for ss in range(len(cg.transition_matrix[s])):
                    cg.transition_matrix[s][ss] /= total
        if verbose:
            print(cg.transition_matrix)

        # now normalize in case they do not sum to 1

        x, y = cg.generate_data(size, random_state=datetime.now().second)
        pe = PathEncoder(order)
        pe.fit(x, y)

        x_tr3, y_tr3 = pe.transform(x, y)
        return train_test_split(x_tr3, y_tr3)