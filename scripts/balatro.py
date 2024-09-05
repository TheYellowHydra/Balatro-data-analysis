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
        self.score_stats = None
        self.poker_hands_stats = None
        self.generate_poker_hands_stats()
        
        self.balatro_stats = pd.DataFrame(columns=['Poker Hand','Probability', 'min', 'max', 'average'])
        # TODO : Refacto the balatro stats, is it useless?
        # self.generate_balatro_probabilties()
        
    def set_figure_size(self, x_inch, y_inch):
        self.figure_size = (x_inch, y_inch)
        
    def print_poker_data(self):
        print(tabulate(self.poker_data, headers='keys', tablefmt='psql'))
 
    def print_balatro_data(self):
        print(tabulate(self.balatro_data, headers='keys', tablefmt='psql'))
    def generate_poker_hands_stats(self):
        self.poker_hands_stats = poker_balatro.generate_value_stats(cards_values)

    def generate_balatro_probabilties(self):
        self.balatro_stats['Poker Hand'] = self.poker_data['Poker Hand']
        self.balatro_stats['Probability'] = self.poker_data['Probability']
        balatro_probabilties = self.balatro_stats
        poker_data = self.poker_data
        # high card = all other poker Hand probabilties
        for x in range(1,poker_data[self.poker_data.columns[0]].count()):
            balatro_probabilties.loc[balatro_probabilties['Poker Hand'] == 'High card','Probability'] += poker_data.loc[x, 'Probability']
            
        # pair
        balatro_probabilties.loc[balatro_probabilties['Poker Hand'] == 'One pair','Probability'] += poker_data.loc[poker_data['Poker Hand'] == 'Two pair','Probability'].values[0]
        balatro_probabilties.loc[balatro_probabilties['Poker Hand'] == 'One pair','Probability'] += poker_data.loc[poker_data['Poker Hand'] == 'Three of a kind','Probability'].values[0]
        balatro_probabilties.loc[balatro_probabilties['Poker Hand'] == 'One pair','Probability'] += poker_data.loc[poker_data['Poker Hand'] == 'Four of a kind','Probability'].values[0]
        balatro_probabilties.loc[balatro_probabilties['Poker Hand'] == 'One pair','Probability'] += poker_data.loc[poker_data['Poker Hand'] == 'Full house','Probability'].values[0]

        # two pair
        balatro_probabilties.loc[balatro_probabilties['Poker Hand'] == 'Two pair','Probability'] += poker_data.loc[poker_data['Poker Hand'] == 'Full house','Probability'].values[0]

        #three of a kind
        balatro_probabilties.loc[balatro_probabilties['Poker Hand'] == 'Three of a kind','Probability'] += poker_data.loc[poker_data['Poker Hand'] == 'Full house','Probability'].values[0]
        balatro_probabilties.loc[balatro_probabilties['Poker Hand'] == 'Three of a kind','Probability'] += poker_data.loc[poker_data['Poker Hand'] == 'Four of a kind','Probability'].values[0]
 
        # self.generate_average_score()
        
    # I am a mokey to do it like that but it's too late, I will figure it out later
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
                return 10

    def convert_str_combo_to_int(self,combo):
        list = []
        for e in combo:
            list.append(self.get_value_from_str(e))
        return list
                
           

    # def balatro_poker_hand_probabilities(self):
        # ax = sns.barplot(data=self.balatro_probabilties,x="Poker Hand",y="Probability")
        # ax.bar_label(ax.containers[0],label_type='edge')
        # plt.show()

    def min_max_average(self):
        poker_hands_stats = self.poker_hands_stats
        print("Min max average")
        print(poker_hands_stats)
        print(poker_hands_stats[poker_hands_stats['min'] == poker_hands_stats['min'].min()])
        print(poker_hands_stats[poker_hands_stats['min'] == poker_hands_stats['min'].max()])
        print(poker_hands_stats[poker_hands_stats['max'] == poker_hands_stats['max'].min()])
        print(poker_hands_stats[poker_hands_stats['max'] == poker_hands_stats['max'].max()])
        print(poker_hands_stats[poker_hands_stats['average'] == poker_hands_stats['average'].min()])
        print(poker_hands_stats[poker_hands_stats['average'] == poker_hands_stats['average'].max()])

   
    def correlation(self):
        print(np.corrcoef(self.balatro_stats['Probability'], self.balatro_stats['average']))

        print(self.balatro_stats)
        print(self.poker_hands_stats)
        d = pd.merge(self.balatro_stats, self.poker_hands_stats, on= 'Poker Hand', sort= False)
        print(d)
        self.balatro_probabilties = d
        sns.lineplot(data=d, x="Probability", y="average_x")
        plt.show()
    
    def generate_average_score(self):
        self.balatro_stats['average'] = (self.poker_hands_stats['average'] + self.balatro_data['Base chips']) * self.balatro_data['Base mult']
        self.balatro_stats['min'] = (self.poker_hands_stats['min'] + self.balatro_data['Base chips']) * self.balatro_data['Base mult']
        self.balatro_stats['max'] = (self.poker_hands_stats['max'] + self.balatro_data['Base chips']) * self.balatro_data['Base mult']

        dfl = pd.melt(self.balatro_stats, ['Poker Hand'])
        sns.lineplot(data=dfl, x='Poker Hand', y='value', hue='variable',marker='o')
        plt.axhline(y=300, color='b', linestyle='dotted')
        plt.axhline(y=450, color='g', linestyle='dotted')
        plt.axhline(y=600, color='r', linestyle='dotted')
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
       
      
    def plot_score_stats(self, data_frame, level):
        plt.figure(figsize=self.figure_size )
        plt.ylabel('Score', size=16, family='monospace')
        plt.xlabel('Poker Hands', size=16, family='monospace')
        palette = {'max' : 'tab:red', 'min' : 'tab:blue', 'average' : 'tab:orange'}
        plt.axhline(y=300, color='b', linestyle='dotted')
        plt.axhline(y=450, color='g', linestyle='dotted')
        plt.axhline(y=600, color='r', linestyle='dotted')
        
        sns.lineplot(data=data_frame, x='Poker Hand', y='value', hue='variable',marker='o', palette = palette).set(title= 'Maximum, average and minimum score by pokerhand at level : '+str(level))
        plt.savefig(self.export_path+'level'+str(level)+'stats.png')
        plt.show()

    def default_plot_config(self):
        plt.figure(figsize=self.figure_size )
        plt.ylabel('Score', size=16, family='monospace')
        plt.xlabel('Poker Hands', size=16, family='monospace')

    def power_hands_levels(self, level):
        d = pd.DataFrame( columns = ['Poker Hand','variable','value'])
        
        for x in range(level):
            for index, row in self.balatro_data.iterrows():
                avg = self.poker_hands_stats.loc[self.poker_hands_stats['Poker Hand'] == row['Poker Hand'],'average'].values[0]
                # self.balatro_stats.loc[self.balatro_stats['Poker Hand'] == row['Poker Hand'], 'average'].values[0]

                r = [row['Poker Hand'],x, (avg+  row['Base chips'] + (row['LevelUp chips'] *x)) * (  row['Base mult'] + (row['LevelUp mult'] *x))]
                d.loc[len(d.index)] = r
                
        #plt.ylim(0, 1000)
        plt.figure(figsize=self.figure_size )
        plt.ylabel('Score', size=16, family='monospace')
        plt.xlabel('Poker Hands', size=16, family='monospace')
        plt.axhline(y=600, color='b', linestyle='dotted')
        plt.axhline(y=2000, color='g', linestyle='dotted')
        plt.axhline(y=6400, color='r', linestyle='dotted')
        sns.lineplot(data=d , x='Poker Hand', y='value', hue='variable',marker='o').set(title='Poker hand score on average to level : '+str(level))
        plt.savefig(self.export_path+'poker hands average score to level '+str(level)+'.png')
        plt.show()
            
    def balatro_score(self, poker_score,poker_hand):
        chips = (poker_score + self.balatro_data.loc[self.balatro_data['Poker Hand'] == poker_hand, 'Base chips'].values[0] )
        mult = self.balatro_data.loc[self.balatro_data['Poker Hand'] == poker_hand,'Base mult'].values[0]
        return chips * mult
        
    def get_combos(self):
        d = pd.DataFrame( columns = ['Poker Hand','variable','value'])
        for index, row in self.balatro_data.iterrows():
            combo = poker_balatro.get_combo(row['Poker Hand'], cards_index)
            for c in combo:
                r = [row['Poker Hand'], 'combo',c]
                d.loc[len(d.index)] = r
        
        return d
            
            
    def get_combo_score(self, combos):
        dp = pd.DataFrame( columns = ['Poker Hand','variable','value'])
        for index, row in  combos.iterrows():
            r = [row['Poker Hand'],  'score', self.balatro_score(sum(self.convert_str_combo_to_int(row['value'])), row['Poker Hand'])]
            dp.loc[len(dp.index)] = r
        return dp


    def get_list_combo_sup_score(self, data_frame, score ):
        copy = pd.DataFrame( columns = ['Poker Hand','variable','value'])
        for index, row in data_frame.iterrows():
            if row['value'] >= score:
                copy.loc[len(copy.index)] = row
        
        return copy
    
    def catplot_combo_score(self, deta_frame):
        sns.catplot(data=deta_frame , x='Poker Hand', y='value',marker='o', hue='Poker Hand')
        plt.ylabel('Score', size=16, family='monospace')
        plt.xlabel('Poker Hands', size=16, family='monospace')
        plt.title('Combinaison score distribution')
        plt.axhline(y=300, color='b', linestyle='dotted')
        plt.axhline(y=400, color='g', linestyle='dotted')
        plt.axhline(y=600, color='r', linestyle='dotted')
        plt.show()
        


v = balatro_visualizer(sys.argv[1],sys.argv[2], sys.argv[3])
v.print_poker_data()
score = v.generate_stats_score_level(2)
v.plot_score_stats(score,2)

v.power_hands_levels(10)