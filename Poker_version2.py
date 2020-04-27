#In[]:
# Constants
suits = 'CDHS'
ranks = '23456789TJQKA'

from abc import ABCMeta, abstractmethod

class Card(metaclass=ABCMeta):
    """Abstact class for playing cards
    """
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card

    @abstractmethod
    def value(self):
        """Subclasses should implement this method"""
        raise NotImplementedError("value method not implemented")

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()
    def __ge__(self, other): return self.value() >= other.value()
    def __lt__(self, other): return self.value() < other.value()
    def __le__(self, other): return self.value() <= other.value()
    def __eq__(self, other): return self.value() == other.value()
    def __ne__(self, other): return self.value() != other.value()

class PKCard(Card):
    def value(self):
        dic = dict(zip(ranks, range(2, 2+len(ranks))))
        return dic.get(self.card[0])
        pass

if __name__ == '__main__':
    c1 = PKCard('QC')
    c2 = PKCard('9D')
    c3 = PKCard('9C')

    print(f'{c1} {c2} {c3}')

    print(c1 > c2 == c3)

    cards = [c1, c2, c3, PKCard('AS'), PKCard('2D')]
    sorted_cards = sorted(cards)
    print(sorted_cards)
    cards.sort()
    print(cards) 

import random
class Deck:
    def __init__(self, cls):
        cls = []
        for k in suits:
            for i in range(2+len(ranks)):
                cls.append((k,i))
        return(cls)
    
    """def shuffle(self):
        random.shuffle(a)
        pass"""

    def pop(self):
        if self.is_empty():
            return -1
        return self.stack.pop()

    def __str__(self):
        return super().__str__()
    
    def __len__(self):
        return len(self) 

if __name__ == '__main__':
    deck = Deck(PKCard)  # deck of poker cards
    """deck.shuffle()"""
    c = deck[0]
    print('A deck of', c.__class__.__name__)
    print(deck)
    """
    # testing __getitem__ method
    print(deck[-5:])

    while len(deck) >= 10:
        my_hand = []
        your_hand = []
        for i in range(5):
            for hand in (my_hand, your_hand):
                card = deck.pop()
                hand.append(card)
        my_hand.sort(reverse=True)
        your_hand.sort(reverse=True)
        print(my_hand, '>', your_hand, '?', my_hand > your_hand)
"""
    
    

# %%
