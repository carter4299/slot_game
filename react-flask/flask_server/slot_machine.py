import random
import numpy as np
from server_settings import Settings

def set_reels():
    flag, joker_chance =  False, 0
    reels = [
        np.random.choice(Settings().card_img_names, p=Settings().probabilities, size=(15 + (10 * i))).tolist()
        for i in range(5)
    ]
    for reel in reels:
        for i in range(3):
            if reel[-(i+1)] == 14:
                joker_chance = Settings().probabilities[13] * 1.5 if not flag else joker_chance * 1.5
                flag = True
            elif random.random() < joker_chance:
                reel[-(i+1)] = 14

    return reels
