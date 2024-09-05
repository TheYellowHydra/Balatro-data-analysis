"""Short module to visualize data in balatro
Made for the video : < insert name and link>.
This module have some functions to visualise Balatro data, as how much points you could expect from a poker hand.

Author : TheYellowHydra TheYellowHydra@proton.me

Created : 05/09/204
"""

import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import poker_balatro
import numpy as np
from tabulate import tabulate
from scipy.stats.stats import pearsonr

# Since it's poker and pker variables should not move in time, I put it directly in the class. Please forgive me
cards_values = [2,3,4,5,6,7,8,9,10,10,10,10,11]
cards_index = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
base_chips_purple_stake = [100,300,1000,3200,9000,25000,60000,11000,200000]
class balatro_visualizer:

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
        
    def __init__(self, p_poker_data, p_balatro_data,export_path):
    
        # Plot config : 
        self.figure_size = (19.20,10.80)
        sns.set(style="ticks", context="talk")
        plt.style.use("dark_background")
        
        # TODO : Chechk if export path valid
        self.export_path = export_path
        
        self.poker_data = pd.read_csv(p_poker_data).convert_dtypes()
        self.balatro_data =  pd.read_csv(p_balatro_data).convert_dtypes()
        
        # How much each poker hands brin at min,max,average
        self.poker_hands_stats = self.generate_poker_hands_stats()
        self.combos = self.generate_combos(cards_index)
        

    def set_figure_size(self, x_inch, y_inch):
        self.figure_size = (x_inch, y_inch)
        
    def generate_poker_hands_stats(self):
        return poker_balatro.generate_value_stats(cards_values)

    def generate_combos(self, cards):
        df = pd.DataFrame( columns = ['Poker Hand','combo','score'])
        for index, row in self.balatro_data.iterrows():
            combo = self.get_combos(row['Poker Hand'], cards_index)
            for c in combo:
                r = [row['Poker Hand'], c,self.combo_to_score(c)]
                df.loc[len(df.index)] = r
        return df

    def generate_combo_score_at_level(self,level):
        df = self.combos.copy()
        for index, row in df.iterrows():
            df.at[index,'score'] = self.balatro_score(row['combo'], row['Poker Hand'], level)
        return  df



    def print_poker_data(self):
        print(tabulate(self.poker_data, headers='keys', tablefmt='psql'))

    def print_balatro_data(self):
        print(tabulate(self.balatro_data, headers='keys', tablefmt='psql'))

    def print_poker_hands_stats(self):
        print(tabulate(self.poker_hands_stats, headers='keys', tablefmt='psql'))
        
    def print_info_combos(self):
        print(self.combos['Poker Hand'].value_counts())
        


    def get_combos(self,poker_hand,cards):
        return poker_balatro.get_combo(poker_hand,cards)


        
        
    def combo_to_score(self,combo):
        list = []
        for e in combo:
            list.append(self.get_value_from_str(e))
        return sum(list)
  
    def balatro_score(self, combinaison,poker_hand, level):
        balatro_hand_data = self.balatro_data.loc[self.balatro_data['Poker Hand'] == poker_hand]
        chips = (self.combo_to_score(combinaison) + balatro_hand_data['Base chips'].values[0] ) + (balatro_hand_data['LevelUp chips'].values[0] * level)
        mult = balatro_hand_data['Base mult'].values[0] + (balatro_hand_data['LevelUp mult'].values[0] * level)
        return chips * mult
        
    def catplot_combo(self, data_frame,level,level_blinds = -1):
        melt = data_frame.melt(id_vars=['Poker Hand','combo'])
        sns.catplot(data=melt , x='Poker Hand', y='value',marker='o', hue='Poker Hand', height =6, aspect=5)
        plt.ylabel('Score', size=16, family='monospace')
        plt.xlabel('Poker Hands', size=16, family='monospace')
        plt.title('Combinaison score distribution level '+str(level))
        
        self._level_blinds_display(level_blinds)
        plt.savefig(self.export_path+'catplot of combos level '+str(level)+'.png')
        plt.show()         

        
    def generate_stats_score_level(self, level):
        score_stats = pd.DataFrame(columns = ['Poker Hand','min', 'max', 'average'])
        self.score_stats = score_stats
        for index, row in self.balatro_data.iterrows():
            poker_hand_min = self.poker_hands_stats.loc[self.poker_hands_stats['Poker Hand'] == row['Poker Hand'], 'min'].values[0]
            poker_hand_max = self.poker_hands_stats.loc[self.poker_hands_stats['Poker Hand'] == row['Poker Hand'], 'max'].values[0]
            poker_hand_average = self.poker_hands_stats.loc[self.poker_hands_stats['Poker Hand'] == row['Poker Hand'], 'average'].values[0]
            
            min = (poker_hand_min + row['Base chips'] + (row['LevelUp chips']*level)) *(row['Base mult']+ (row['LevelUp mult']*level))
            max = (poker_hand_max + row['Base chips'] +  (row['LevelUp chips']*level)) * (row['Base mult']+ (row['LevelUp mult']*level))
            average = (poker_hand_average + row['Base chips'] + (row['LevelUp chips']*level)) * (row['Base mult']+ (row['LevelUp mult']*level))
            
            r = [row['Poker Hand'], min,max,average]
            score_stats.loc[len(score_stats.index)] = r
      
        defl = score_stats.melt(id_vars=['Poker Hand'])
        return defl
        
    def get_value_from_str(self,symbole):
        match symbole:
            case '2':
                return 2
            case '3':
                return 3
            case '4':
                return 4
            case '5':
                return 5
            case '6':
                return 6
            case '7':
                return 7
            case '8':
                return 8
            case '9':
                return 9
            case '10':
                return 10
            case 'J':
                return 10
            case 'Q':
                return 10
            case 'K':
                return 10
            case 'A':
                return 11

   
    def plot_score_stats(self, data_frame, level ):
        plt.figure(figsize=self.figure_size )
        plt.ylabel('Score', size=16, family='monospace')
        plt.xlabel('Poker Hands', size=16, family='monospace')
        palette = {'max' : 'tab:red', 'min' : 'tab:blue', 'average' : 'tab:orange'}
        self._level_blinds_display(level)
        sns.lineplot(data=data_frame, x='Poker Hand', y='value', hue='variable',marker='o', palette = palette).set(title= 'Maximum, average and minimum score by pokerhand at level : '+str(level))
        plt.savefig(self.export_path+'level'+str(level)+'stats.png')
        plt.show()

    def _level_blinds_display(self, level_blinds = -1):
        if level_blinds != -1:
            plt.axhline(y=base_chips_purple_stake[level_blinds], color='b', linestyle='dotted', label='Small blind ante '+str(level_blinds))
            plt.axhline(y=base_chips_purple_stake[level_blinds] * 1.5, color='g', linestyle='dotted',label='Big blind  ante '+str(level_blinds))
            plt.axhline(y=base_chips_purple_stake[level_blinds] * 2, color='r', linestyle='dotted',label='Boss blind  ante '+str(level_blinds))
            plt.axhline(y=base_chips_purple_stake[level_blinds] * 4, color='tab:purple', linestyle='dotted',label='Wall blind  ante '+str(level_blinds))

    def default_plot_config(self):
        plt.figure(figsize=self.figure_size )
        plt.ylabel('Score', size=16, family='monospace')
        plt.xlabel('Poker Hands', size=16, family='monospace')

    def power_hands_levels(self, level, level_blinds = -1 ):
        d = pd.DataFrame( columns = ['Poker Hand','variable','value'])
        for x in range(level+1):
            for index, row in self.balatro_data.iterrows():
                avg = self.poker_hands_stats.loc[self.poker_hands_stats['Poker Hand'] == row['Poker Hand'],'average'].values[0]
                r = [row['Poker Hand'],x, (avg+  row['Base chips'] + (row['LevelUp chips'] *x)) * (  row['Base mult'] + (row['LevelUp mult'] *x))]
                d.loc[len(d.index)] = r
        plt.figure(figsize=self.figure_size )
        plt.ylabel('Score', size=16, family='monospace')
        plt.xlabel('Poker Hands', size=16, family='monospace')
        self._level_blinds_display(level_blinds)
        sns.lineplot(data=d , x='Poker Hand', y='value', hue='variable',marker='o').set(title='Poker hand score on average to level : '+str(level))
       
        plt.savefig(self.export_path+'poker hands average score to level '+str(level)+'.png')
        plt.show()
            
 


        

