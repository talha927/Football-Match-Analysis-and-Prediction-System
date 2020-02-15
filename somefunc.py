import pygal
from pygal.style import Style
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import pandas as pd
oururl="FootballEurope.csv"

def laliga_teams():
    laliga = pd.read_csv(oururl)
    laliga = laliga[laliga.division == 'La_Liga']
    x=laliga.homeTeam.unique()
    x.sort()   
    return x
def laliga_teams2():
    laliga = pd.read_csv('testtable.csv')
    #laliga = laliga[laliga.division == 'La_Liga']
    x=laliga.HomeTeam.unique()
    x.sort()   
    return x

def laliga_teams22():
    laliga = pd.read_csv('BettingPlayersPredictionDone.csv')
    #laliga = laliga[laliga.division == 'La_Liga']
    x=laliga.HomeTeam.unique()
    x.sort()   
    return laliga

def all_teams():
    laliga = pd.read_csv(oururl)
    #laliga = laliga[laliga.division == 'La_Liga']
    x=laliga.homeTeam.unique()
    return x

def all_analysis(teamname):
    my_dict=dict()
    laliga = pd.read_csv(oururl)
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row['awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == teamname]
    barcaAway = laliga[laliga.awayTeam == teamname]
    
    stir=teamname+' number of wins at home'
    stir=str(stir)
    my_dict.update({stir:barcelona['local_team_won'].sum()})
    
    stir=teamname+' number of looses at home'
    stir=str(stir)
    my_dict.update({stir:barcelona['visitor_team_won'].sum()})
   
    stir=teamname+' number of draws at home'
    stir=str(stir)
    my_dict.update({stir:barcelona['draw'].sum()})
    
    stir=teamname+' number of wins at away'
    stir=str(stir)
    my_dict.update({stir:barcaAway['visitor_team_won'].sum()})
    
    stir=teamname+' number of looses at away'
    stir=str(stir)
    my_dict.update({stir:barcaAway['local_team_won'].sum()})
   
    stir=teamname+' number of draws at away'
    stir=str(stir)
    my_dict.update({stir:barcaAway['draw'].sum()})
    
    stir=teamname+' number of goals scored at home'
    stir=str(stir)
    my_dict.update({stir:barcelona['homeGoalFT'].sum()})
    
    stir=teamname+' number of goals concede at home'
    stir=str(stir)
    my_dict.update({stir:barcelona['awayGoalFT'].sum()})
    
    stir=teamname+' number of goals scored at away'
    stir=str(stir)
    my_dict.update({stir:barcaAway['awayGoalFT'].sum()})
    
    stir=teamname+' number of goals concede at away'
    stir=str(stir)
    my_dict.update({stir:barcaAway['homeGoalFT'].sum()})

    stir=teamname+' Possession at home'
    stir=str(stir)
    my_dict.update({stir:barcelona['homePossessionFT'].sum()})
    
    
    stir=teamname+' Possession at away'
    stir=str(stir)
    my_dict.update({stir:barcaAway['awayPossessionFT'].sum()})
    
    
    stir=teamname+' number of fouls done at home'
    stir=str(stir)
    my_dict.update({stir:barcelona['homeFoulsCommitedFT'].sum()})
    
    stir=teamname+' number of fouls concede at home'
    stir=str(stir)
    my_dict.update({stir:barcelona['awayFoulsCommitedFT'].sum()})
    
    stir=teamname+' number of fouls done at away'
    stir=str(stir)
    my_dict.update({stir:barcaAway['awayFoulsCommitedFT'].sum()})
    
    stir=teamname+' number of fouls concede at away'
    stir=str(stir)
    my_dict.update({stir:barcaAway['homeFoulsCommitedFT'].sum()})
    
    stir=teamname+' number of offsides at home'
    stir=str(stir)
    my_dict.update({stir:barcelona['homeOffsidesCaughtFT'].sum()})
    
    stir=teamname+' opponent number of offsides at home'
    stir=str(stir)
    my_dict.update({stir:barcelona['awayOffsidesCaughtFT'].sum()})
    
    stir=teamname+' number of offsides at away'
    stir=str(stir)
    my_dict.update({stir:barcaAway['awayOffsidesCaughtFT'].sum()})
    
    stir=teamname+' opponent number of offsides at away'
    stir=str(stir)
    my_dict.update({stir:barcaAway['homeOffsidesCaughtFT'].sum()})
    
    #homeOffsidesCaughtFT
    return my_dict