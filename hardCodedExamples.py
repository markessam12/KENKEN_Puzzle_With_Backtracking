# --- Example 1 ---
# --- 9*9 board ,4 operations---
grid = [
    [6,9,7,8,1,3,4,5,2],
    [2,1,4,9,7,6,3,8,5],
    [8,3,1,7,5,9,2,4,6],
    [7,4,8,6,3,5,9,2,1],
    [3,7,5,2,6,8,1,9,4],
    [5,2,6,4,9,1,8,7,3],
    [4,6,2,3,8,7,5,1,9],
    [1,8,9,5,2,4,6,3,7],
    [9,5,3,1,4,2,7,6,8]
]

cages = {
        1: {"value" :4, "op":'/',   "cells":[(2,0),(1,0)]},
        2: {"value" :8, "op":'-',   "cells":[(0,1),(1,1)]},
        3: {"value" :6, "op":'none',"cells":[(0,0)]},
        4: {"value" :28, "op":'*',   "cells":[(0,2),(1,2)]},
        5: {"value" :17, "op":'+',   "cells":[(0,3),(1,3)]},
        6: {"value" :2, "op":'none',"cells":[(6,2)]},
        7: {"value" :21, "op":'*',"cells":[(0,4),(1,4),(0,5)]},
        8: {"value" :160, "op":'*',"cells":[(0,6),(0,7),(1,7)]},
        9: {"value" :60, "op":'*',"cells":[(0,8),(1,8),(2,8)]},
        10: {"value" :84, "op":'*',"cells":[(2,1),(3,0),(3,1)]},
        11: {"value" :7, "op":'-',"cells":[(2,2),(3,2)]},
        12: {"value" :42, "op":'*',"cells":[(2,3),(3,3)]},
        13: {"value" :14, "op":'+',"cells":[(2,4),(2,5)]},
        14: {"value" :36, "op":'*',"cells":[(1,6),(1,5),(2,6)]},
        15: {"value" :8, "op":'*',"cells":[(3,8),(2,7),(3,7)]},
        16: {"value" :105, "op":'*',"cells":[(4,0),(5,0),(4,1)]},
        17: {"value" :7, "op":'+',"cells":[(4,2),(4,3)]},
        18: {"value" :2, "op":'/',"cells":[(3,4),(4,4)]},
        19: {"value" :22, "op":'+',"cells":[(3,5),(3,6),(4,5)]},
        20: {"value" :8, "op":'-',"cells":[(4,6),(4,7)]},
        21: {"value" :1, "op":'-',"cells":[(4,8),(5,8)]},
        22: {"value" :3, "op":'-',"cells":[(6,0),(7,0)]},
        23: {"value" :7, "op":'+',"cells":[(5,3),(6,3)]},
        24: {"value" :17, "op":'+',"cells":[(5,4),(6,4)]},
        25: {"value" :28, "op":'*',"cells":[(5,5),(6,5),(7,5)]},
        26: {"value" :56, "op":'*',"cells":[(5,6),(5,7)]},
        27: {"value" :72, "op":'*',"cells":[(5,1),(5,2),(6,1)]},
        28: {"value" :17, "op":'+',"cells":[(7,1),(7,2)]},
        29: {"value" :7, "op":'+',"cells":[(7,3),(7,4)]},
        30: {"value" :90, "op":'*',"cells":[(6,6),(7,6),(7,7)]},
        31: {"value" :63, "op":'*',"cells":[(6,7),(6,8),(7,8)]},
        32: {"value" :48, "op":'*',"cells":[(8,8),(8,7)]},
        33: {"value" :5, "op":'-',"cells":[(8,5),(8,6)]},
        34: {"value" :4, "op":'/',"cells":[(8,3),(8,4)]},
        35: {"value" :135, "op":'*',"cells":[(8,0),(8,1),(8,2)]},
     }

cages1 = {
          1: {'value': 6, 'op': '*', 'cells': [(0, 0), (1, 0), (2, 0)]},
          2: {'value': 1, 'op': '-', 'cells': [(0, 1), (0, 2)]},
          3: {'value': 1, 'op': '-', 'cells': [(1, 1), (1, 2)]},
          4: {'value': 3, 'op': 'none', 'cells': [(2, 1)]},
          5: {'value': 1, 'op': 'none', 'cells': [(2, 2)]}
          }

#error 2
cages2 = {1: {'value': 3, 'op': '-', 'cells': [(0, 0), (1, 0)]},
          2: {'value': 216, 'op': '*', 'cells': [(2, 0), (3, 0), (3, 1), (2, 1)]},
          3: {'value': 70, 'op': '*', 'cells': [(4, 0), (4, 1), (4, 2)]},
          4: {'value': 21, 'op': '*', 'cells': [(5, 0), (5, 1), (6, 1)]},
          5: {'value': 5, 'op': 'none', 'cells': [(6, 0)]},
          6: {'value': 4, 'op': 'none', 'cells': [(0, 1)]},
          7: {'value': 14, 'op': '+', 'cells': [(1, 1), (1, 2), (1, 3)]},
          8: {'value': 3, 'op': '/', 'cells': [(0, 2), (0, 3)]},
          9: {'value': 12, 'op': '+', 'cells': [(2, 2), (2, 3), (3, 3)]},
          10: {'value': 4, 'op': 'none', 'cells': [(3, 2)]},
          11: {'value': 5, 'op': '/', 'cells': [(5, 2), (5, 3)]},
          12: {'value': 11, 'op': '+', 'cells': [(6, 2), (6, 3), (6, 4)]},
          13: {'value': 3, 'op': 'none', 'cells': [(4, 3)]},
          14: {'value': 2, 'op': '-', 'cells': [(0, 4), (0, 5)]},
          15: {'value': 42, 'op': '*', 'cells': [(1, 4), (2, 4), (2, 5), (1, 5)]},
          16: {'value': 9, 'op': '+', 'cells': [(3, 4), (3, 5), (3, 6)]},
          17: {'value': 144, 'op': '*', 'cells': [(4, 4), (5, 4), (5, 5)]},
          18: {'value': 8, 'op': '*', 'cells': [(4, 5), (4, 6), (5, 6)]},
          19: {'value': 3, 'op': '-', 'cells': [(6, 5), (6, 6)]},
          20: {'value': 90, 'op': '*', 'cells': [(0, 6), (1, 6), (2, 6)]}}

"""
1 4 6 2 5 7 3
4 7 2 5 1 3 6
3 6 1 4 7 2 5
6 2 4 7 3 5 1
2 5 7 3 6 1 4
7 3 5 1 4 6 2
5 1 3 6 2 4 7
"""