suits = 'CDHS'
ranks = '23456789TJQKA'
values = dict(zip(ranks, range(2, 2+len(ranks))))


# In[ ]:
def is_flush(cards):
    cards_num = cards.split(' ')
    card = []
    for i in cards_num:
        card.append(list(i))   
    test_suit = card[0][1]
    if(all(element[1] == test_suit for element in card)):
        return True
    else:
        return False
    
def is_straight(cards):
    cards_num = cards.split(' ')
    card = []
    for i in cards_num:
        card.append(list(i))
    temp = []
    for i in card:
        if i[0] in values.keys():
            temp.append(values[i[0]])
    temp.sort()
    if temp == [2, 3, 4, 5, 14]:
        return True
    else:
        stop = 1
        for i in range (0, 4):
            if temp[i]+1 != temp[i+1]:
                return False
                stop = 0
        if stop == 1:
            return True


def classify_by_rank(cards):
    cards_num = cards.split(' ')
    card = []
    for i in cards_num:
        card.append(list(i))
    temp = []
    for i in card:
        if i[0] in values.keys():
            temp.append(values[i[0]])
    temp.sort()
    dic = {}
    for i in card:
        if i[0] not in dic:
            dic[i[0]] = []
            dic[i[0]].append(''.join(i))
        else:
            dic[i[0]].append(''.join(i))
    return dic

def find_a_kind(cards):
    cards_by_ranks = classify_by_rank(cards)
    val_num = []
    for i in cards_by_ranks:
        val_num.append(len(cards_by_ranks[i]))
    if 4 in val_num:
        return 'Four of a kind'
    elif 3 in val_num and 2 in val_num:
        return 'Full house'
    elif val_num.count(2) == 2:
        return 'Two pair'
    elif 3 in val_num:
        return 'Three of a kind'
    elif 2 in val_num:
        return 'One pair'
    else:
        return 'High card'

def tell_hand_ranking(cards):
    if is_flush(cards) == True:
        flush = True
    else:
        flush = False
    if is_straight(cards) == True:
        straight = True
    else:
        straight = False
    fak = find_a_kind(cards)
    if flush == True and straight == True:
        return 'Straight flush'
    elif fak == 'Four of a kind':
        return 'Four of a kind'
    elif fak == 'Full house':
        return 'Full house'
    elif flush == True:
        return 'Flush'
    elif straight == True:
        return 'Straight'
    elif fak == 'Three of a kind':
        return 'Three of a kind'
    elif fak == 'Two pair':
        return 'Two pair'
    elif fak == 'One pair':
        return 'One pair'
    else:
        return 'High card'

if __name__ == "__main__":
       
    print(tell_hand_ranking('2S 3S 4S 5S 6S'))
    print(tell_hand_ranking('3S 3D 3H 3C 6S'))
    print(tell_hand_ranking('5S 5D 5H 7D 7S'))
    print(tell_hand_ranking('2S 4S 5S 7S KS'))
    print(tell_hand_ranking('TS JS QS AS KS'))
    print(tell_hand_ranking('2S 2D 2C 4S 7C'))
    print(tell_hand_ranking('2S 2D 4C 4S 7C'))
    print(tell_hand_ranking('2S 2D 3S 5D JD'))
    print(tell_hand_ranking('2S 3D 5C 7D KH'))
