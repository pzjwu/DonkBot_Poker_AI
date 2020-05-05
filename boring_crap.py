import pandas as pd

preflop_equities_global = pd.read_csv('preflop_equity.csv')
dbn_global = pd.read_csv('Range_CPT.csv')

rfi_out = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                ]

test_rfi = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]

def predict(position, size, action, prev):
    pos = 'Out_Position'
    if position:
        pos = 'In_Position'
    if action == 'call':
        new_outcome = str(dbn_global[(dbn_global['Position'] == pos) & (dbn_global['Action'] == action) & (dbn_global['Prior'] == prev)].iloc[0, 4])
    else:
        new_outcome = str(dbn_global[(dbn_global['Position'] == pos) & (dbn_global['Size'] == size) & (dbn_global['Action'] == action) & (dbn_global['Prior'] == prev)].iloc[0,4])

    return new_outcome

#outcome = str(predict(True, 'Large', 'Call', 'Win'))
#print(outcome)


def get_preflop_equity(converted_hole):
    equity = preflop_equities_global[preflop_equities_global['Cards'] == converted_hole].iloc[0, 1]
    return equity

crap = get_preflop_equity('AAo')
print(crap)

def in_range(ranges, hand):
    hand_mapping = {'A': 0, 'K': 1, 'Q': 2, 'J': 3, 'T': 4, '9':5, '8':6, '7':7, '6':8, '5': 9, '4': 10, '3': 11, '2': 12}
    if hand[2] == 's':
        row_idx = int(hand_mapping.get(hand[0]))
        col_idx = int(hand_mapping.get(hand[1]))
        return ranges[row_idx][col_idx]
    else:
        row_idx = int(hand_mapping.get(hand[1]))
        col_idx = int(hand_mapping.get(hand[0]))
        return ranges[row_idx][col_idx]

print(in_range(test_rfi, '93s'))