from analysis import T_s
from analysis import backwards_filter

heyo = [0, 1, 2, 3, 4, 5]
time_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
position_data = [0, 10, 11, 8, 6, 4, 3, 11, 3, 2, 3, 3, 3]

print(backwards_filter(heyo, 4))

