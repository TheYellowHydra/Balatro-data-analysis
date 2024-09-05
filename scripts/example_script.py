"""Example on using balatro.py module

It follow the content of the video.
Up to you to try new combinaison 
Made for the video : < insert name and link>.
Author : TheYellowHydra TheYellowHydra@proton.me

Created : 05/09/204
"""
# Pardon me for leaving hard path file like that. No idea how to do it.
import sys
sys.path.append("D:/PROJETS/CODING/balatro/scripts/")
import balatro
poker_data = "D:/PROJETS/CODING/balatro/data/poker_data.csv"
balatro_data = "D:/PROJETS/CODING/balatro/data/balatro_data.csv"
bv = balatro.balatro_visualizer(poker_data,balatro_data, "D:/PROJETS/CODING/balatro/exports/")
bv.print_poker_data()
bv.print_balatro_data()
bv.print_poker_hands_stats()
bv.print_info_combos()
level_0 = bv.generate_stats_score_level(0)
bv.plot_score_stats(level_0,1)
level_1_stats = bv.generate_stats_score_level(1)
bv.plot_score_stats(level_1_stats, 1)
level_0_combos = bv.generate_combo_score_at_level(0)
bv.catplot_combo(level_0_combos,0,1)
level_0_combos_sup_300 = level_0_combos.loc[ level_0_combos['score'] >= 300]
bv.catplot_combo(level_0_combos_sup_300,0,1)
print(level_0_combos_sup_300['Poker Hand'].value_counts())
print(level_0_combos_sup_300.loc[level_0_combos_sup_300['Poker Hand'] == 'Straight'])
bv.power_hands_levels(9,3)