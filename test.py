from flask import Flask, render_template, request
from flask_wtf import FlaskForm
import pandas as pd
from wtforms import SelectField, StringField
import pickle
from jsonC import convert_json_format, convert_json_format1
testTable=pd.read_csv('testtable.csv')
import somefunc as sf
import json
#import ranking as rk 
#from ranking import teamranking
#from predictionMatch import pred as pm
from graph import *
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OurSecretkey'

@app.route('/football_news', methods=['POST', 'GET'])
def football_news():
    url = ('https://newsapi.org/v2/top-headlines?sources=the-sport-bible&apiKey=734b2ba2bec54cfb984dae3b5de43db1')
    response = requests.get(url)
    aa =  response.json()

    url1 = ('https://newsapi.org/v2/top-headlines?sources=football-italia&apiKey=734b2ba2bec54cfb984dae3b5de43db1')
    response1 = requests.get(url1)
    aa1 =  response1.json()

    aL,tL,dL,cL,iL,uL=convert_json_format(aa)
    aL1,tL1,dL1,cL1,iL1,uL1=convert_json_format1(aa1)
    return render_template('news.html' , aL=aL,tL=tL,dL=dL,cL=cL,iL=iL,uL=uL, aL1=aL1,tL1=tL1,dL1=dL1,cL1=cL1,iL1=iL1,uL1=uL1)
@app.route('/team_ranking' , methods=['GET', 'POST'])
def team_ranking():
    df = pd.read_csv('Elo_Ranking_Final.csv')
    table_club = df['club']
    table_rating = df['ratings']
    dfown = pd.read_csv('OurOwnRanking.csv')
    data1=bar_chart_1(df)
    data2=bar_chart_2(dfown)

    return render_template('rank.html', data1=data1,data2=data2 , table_club = table_club, table_rating = table_rating )

@app.route('/prediction_of_match', methods=['GET'])
def prediction_of_match():
    x=sf.laliga_teams2()
    return render_template('pred.html', data=x)


@app.route('/prediction_games', methods=['POST' , 'GET'])
def prediction_games():
    x=sf.laliga_teams2()
    x1=sf.laliga_teams22()
    team1 = ""
    team2 = ""
    if request.method == 'POST':
        result = request.form
        team1 = result['TeamComp1']
        team2 = result['TeamComp2']
        team1 = str(team1)
        team2 = str(team2)
        #print(team1)
        #print(team2)
    errMessage=""
    if(team1==team2):
          errMessage='Two teams cannot be same '
          return render_template('pred.html', data=x, data2= errMessage)
    else:

        df=pd.read_csv('Predfeature.csv')
        df=df.drop(['Unnamed: 0'],axis=1)
        with open('mcompletetraining.pkl' , 'rb') as f:
            mp = pickle.load(f)
            a = mp.predict(df)
        test_table=testTable
        test_table.head()
        test_table=test_table.drop(['Unnamed: 0'],axis=1)
        this_week = test_table[['HomeTeam','AwayTeam']].loc[1890:]
        this_week['Result_ADB']=a
        #print(this_week.head(5))
        this_week["Result_ADB"] = this_week.apply(lambda row: transformResultBack(row,"Result_ADB"),axis=1)
    

        ElClassico=this_week
        Home_team=team1
        Away_team=team2
    #print(Home_team)

        Barcelona = ElClassico[((ElClassico.HomeTeam == Home_team) & (ElClassico.AwayTeam == Away_team))]
        strin=Barcelona.HomeTeam.unique()
        strin2=Barcelona.AwayTeam.unique()
        strin3=Barcelona.Result_ADB.unique()
        t1=strin[0]
        t2=strin2[0]
        t3=strin3[0]
        if(strin3=='HomeTeamWins'):
            po=t1
        elif(strin3=='AwayTeamWins'):
            po=t2
        else:
            po='Draw'
    #winningTeam=str(winningTeam)
    #winningTeam=winningTeam[7]
        are=[po,t3]
    #sti=str(Barcelona['HomeTeam'])
        print(are)
        x1=x1[x1['HomeTeam']==team1]
        x1=x1[x1['AwayTeam']==team2]
        graph_data_1 = plotting_pred('Winning Chances Percentage', team1, team2 , 'Draw', x1.HomeWinningProb*100, x1.AwayWinningProb*100, x1.DrawProb*100)

        return render_template('predic.html', data=x, data1= are,graph_data_1 =graph_data_1)

@app.route('/compareteams', methods=['GET'])
def compareteams():
    return render_template('aaa.html')
    #return render_template('pred.html')
@app.route('/predmatch' , methods=['GET'])
def predmatch():
    df=pm.pred()
    print(df)
    return render_template('student.html')

@app.route('/head', methods=['GET'])
def head():
    x=sf.laliga_teams()
    return render_template('head.html', data = x)

'''@app.route('/head', methods=['GET'])
def compareteams22():
    return render_template('aaa.html')
'''
@app.route('/comp', methods=['POST', 'GET'])
def comp1():
    team1 = ""
    teams2 = ""
    if request.method == 'POST':
        result = request.form
        team1 = result['TeamComp1']
        team2 = result['TeamComp2']
        team1 = str(team1)
        team2 = str(team2)
        print(team1)
        print(team2)
        laliga = pd.read_csv('FootballEurope.csv')

    laliga['winner'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row['awayGoalFT'] else 0,axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    ElClassico = laliga
    Barcelona = ElClassico[((ElClassico.homeTeam == team1) | (ElClassico.awayTeam == team1))]
    Madrid = ElClassico[((ElClassico.homeTeam == team2) | (ElClassico.awayTeam == team2))]
    BarcaHome = Barcelona[Barcelona.homeTeam == team1]
    BarcaAway = Barcelona[Barcelona.awayTeam == team1]
    MadridHome = Madrid[Madrid.homeTeam == team2]
    MadridAway = Madrid[Madrid.awayTeam == team2]

    # In[4]:

    BarcaWins = BarcaHome['local_team_won'].sum() + BarcaAway['visitor_team_won'].sum()
    BarcaLooses = BarcaAway['local_team_won'].sum() + BarcaHome['visitor_team_won'].sum()
    MadridWins = MadridHome['local_team_won'].sum() + MadridAway['visitor_team_won'].sum()
    MadridLooses = MadridAway['local_team_won'].sum() + MadridHome['visitor_team_won'].sum()
    barcahomeGoals = BarcaHome['homeGoalFT'].sum()
    barcaawaygoals = BarcaAway['awayGoalFT'].sum()
    madridhomeGoals = MadridHome['homeGoalFT'].sum()
    madridawaygoals = MadridAway['awayGoalFT'].sum()

    barcaPossesion = (BarcaAway['homePossessionFT'].sum() / (len(laliga) * 100)) + (
                BarcaAway['awayPossessionFT'].sum() / (len(laliga) * 100))
    madridpossesion = (MadridHome['homePossessionFT'].sum() / (len(laliga) * 100)) + (
                MadridAway['awayPossessionFT'].sum() / (len(laliga) * 100))

    # MadridWins=MadridHome['local_team_won'].sum() + MadridAway['visitor_team_won'].sum()
    BarcaDraws = Barcelona['draw'].sum()
    MadridDraws = Madrid['draw'].sum()
    print(team1, ' win = ', BarcaWins)
    print(team1, ' looses = ', BarcaLooses)
    print(team1, ' draws = ', BarcaDraws)
    print(team2, ' win = ', MadridWins)
    print(teams2, ' looses = ', MadridLooses)
    print(team2, ' draws = ', MadridDraws)
    graph_data = plotting3('Number of Wins', team1, team2, BarcaWins, MadridWins)
    graph_data1 = plotting3('Number of Loses', team1, team2, BarcaLooses, MadridLooses)
    graph_data2 = draws('Number of Draws', team1, team2, BarcaDraws, MadridDraws)
    graph_data_goals = goals('Number of Aways Goals', team1, team2, barcaawaygoals, madridawaygoals)
    graph_data_homegoals = plotting3('Number of Home Goals', team1, team2, barcahomeGoals, madridhomeGoals)
    possesion = goals('Possesion in Percentage %', team1, team2, barcaPossesion, madridpossesion)

    return render_template('compare.html', graph_data=graph_data, graph_data1=graph_data1, graph_data2=graph_data2,
                           graph_data_goals=graph_data_goals, graph_data_homegoals=graph_data_homegoals,
                           possesion=possesion)


@app.route('/thehead', methods=['POST', 'GET'])
def thehead():
    x=sf.laliga_teams()
    team1 = ""
    teams2 = ""
    if request.method == 'POST':
        result = request.form
        team1 = result['TeamComp1']
        team2 = result['TeamComp2']
        team1 = str(team1)
        team2 = str(team2)
        print(team1)
        print(team2)
        laliga = pd.read_csv('FootballEurope.csv')


    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row['awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    ElClassico = laliga
    Barcelona = ElClassico[((ElClassico.homeTeam == team1) & (ElClassico.awayTeam == team2))]
    Madrid = ElClassico[((ElClassico.homeTeam == team2) & (ElClassico.awayTeam == team1))]
    BarcaHome = Barcelona
    BarcaAway = Madrid
    MadridHome = Madrid
    MadridAway = Barcelona

    # In[4]:

    BarcaWins = BarcaHome['local_team_won'].sum() + BarcaAway['visitor_team_won'].sum()
    BarcaLooses = BarcaAway['local_team_won'].sum() + BarcaHome['visitor_team_won'].sum()
    MadridWins = MadridHome['local_team_won'].sum() + MadridAway['visitor_team_won'].sum()
    MadridLooses = MadridAway['local_team_won'].sum() + MadridHome['visitor_team_won'].sum()
    barcahomeGoals = BarcaHome['homeGoalFT'].sum()
    barcaawaygoals = BarcaAway['awayGoalFT'].sum()
    madridhomeGoals = MadridHome['homeGoalFT'].sum()
    madridawaygoals = MadridAway['awayGoalFT'].sum()

    barcaPossesion = (BarcaAway['homePossessionFT'].sum() / len(laliga) * 100) + (
                BarcaAway['awayPossessionFT'].sum() / len(laliga) * 100)
    madridpossesion = (MadridHome['homePossessionFT'].sum() / len(laliga) * 100) + (
                MadridAway['awayPossessionFT'].sum() / len(laliga) * 100)

    # MadridWins=MadridHome['local_team_won'].sum() + MadridAway['visitor_team_won'].sum()
    BarcaDraws = Barcelona['draw'].sum()
    MadridDraws = Madrid['draw'].sum()
    print(team1, ' win = ', BarcaWins)
    print(team1, ' looses = ', BarcaLooses)
    print(team1, ' draws = ', BarcaDraws)
    print(team2, ' win = ', MadridWins)
    print(teams2, ' looses = ', MadridLooses)
    print(team2, ' draws = ', MadridDraws)
    graph_data = plotting3('Number of Wins', team1, team2, BarcaWins, MadridWins)
    graph_data1 = plotting3('Number of Loses', team1, team2, BarcaLooses, MadridLooses)
    graph_data2 = draws('Number of Draws', team1, team2, BarcaDraws, MadridDraws)
    graph_data_goals = goals('Number of Aways Goals', team1, team2, barcaawaygoals, madridawaygoals)
    graph_data_homegoals = plotting3('Number of Home Goals', team1, team2, barcahomeGoals, madridhomeGoals)
    possesion = goals('Possesion in Percentage %', team1, team2, barcaPossesion, madridpossesion)

    return render_template('headtoheadmain.html', graph_data=graph_data, graph_data1=graph_data1, graph_data2=graph_data2,
                           graph_data_goals=graph_data_goals, graph_data_homegoals=graph_data_homegoals,
                           possesion=possesion, data=x)


@app.route('/result', methods=['POST', 'GET'])
def result():
    team = ""
    if request.method == 'POST':
        result = request.form
        team = result['Name']
        team = str(team)

    laliga = pd.read_csv('FootballEurope.csv')

    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row['awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == team]
    barcaAway = laliga[laliga.awayTeam == team]
    x = pd.DataFrame(barcelona)
    cp = 0
    cp1 = 0
    cp2 = 0
    tot = 0
    for index, row in x.iterrows():
        tot += 1
        if (row['local_team_won'] == 1):
            cp = cp + 1
        elif (row['visitor_team_won'] == 1):
            cp1 = cp1 + 1
        elif (row['draw'] == 1):
            cp2 = cp2 + 1
    print('Total no of home games are', tot)
    print('Total no of home wins are', cp)
    print('Total no of home looses are', cp1)
    print('Total no of home draws are', cp2)
    x = pd.DataFrame(barcaAway)
    aw = 0
    al = 0
    ad = 0
    at = 0
    for index, row in x.iterrows():
        at += 1
        if (row['local_team_won'] == 1):
            al = al + 1
        elif (row['visitor_team_won'] == 1):
            aw = aw + 1
        elif (row['draw' == 1]):
            ad = ad + 1
    print('Total no of away games are', at)
    print('Total no of away wins are', aw)
    print('Total no of away looses are', al)
    print('Total no of away draws are', ad)
    print('Average won draw and loose are')
    print('Total     wins         looses        draws')
    print(tot + at, '      ', cp + aw, '        ', cp2 + al, '          ', cp2 + ad)
    barcelona = laliga[laliga.homeTeam == 'Real Madrid']
    barcaAway = laliga[laliga.awayTeam == 'Real Madrid']
    x = pd.DataFrame(barcelona)
    homegoalsScored = 0
    homegoalsconcede = 0
    awaygoalsScored = 0
    awaygoalsconcede = 0

    for index, row in x.iterrows():
        homegoalsScored = homegoalsScored + row['homeGoalFT']
        homegoalsconcede = homegoalsconcede + row['awayGoalFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awaygoalsScored = awaygoalsScored + row['awayGoalFT']
        awaygoalsconcede = awaygoalsconcede + row['homeGoalFT']
    print('Home Goals scored are ', homegoalsScored)
    print('Home Goals concede are ', homegoalsconcede)
    print('Away Goals scored are ', awaygoalsScored)
    print('Away Goals concede are ', awaygoalsconcede)

    totalGoals = homegoalsScored + awaygoalsScored

    totalConcede = homegoalsconcede + awaygoalsconcede

    print('Total:    Scored      Concede')
    print('         ', totalGoals, '     ', totalConcede)
    x = pd.DataFrame(barcelona)
    homePossession = 0
    awayPossession = 0
    totalPossession = 0
    count = 0
    for index, row in x.iterrows():
        count += 1
        homePossession += row['homePossessionFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awayPossession += row['awayPossessionFT']
    print('Home possesion average', homePossession / count)
    print('Away possesion average', awayPossession / count)
    print('Total possesion average', (homePossession + awayPossession) / (count * 2))
    x = pd.DataFrame(barcelona)
    homeFoulshome = 0
    awayFoulshome = 0
    homeFoulsaway = 0
    awayFoulsaway = 0
    totalFouls = 0
    for index, row in x.iterrows():
        homeFoulshome += row['homeFoulsCommitedFT']
        awayFoulshome += row['awayFoulsCommitedFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        homeFoulsaway += row['awayFoulsCommitedFT']
        awayFoulsaway += row['homeFoulsCommitedFT']
    print('Home fouls in home ground = ', homeFoulshome)
    print('away fouls in home ground = ', awayFoulshome)
    print('Home fouls in away ground = ', homeFoulsaway)
    print('away fouls in away ground = ', awayFoulsaway)
    totalFoulsHome = homeFoulshome + homeFoulsaway
    totalFoulsAway = awayFoulshome + awayFoulsaway
    print('Total Fouls done = ', totalFoulsHome)
    print('Total Fouls suffer = ', totalFoulsAway)
    x = pd.DataFrame(barcelona)
    homeShots = 0
    awayShots = 0

    homeShotsOnTarget = 0
    awayShotsOnTarget = 0

    AhomeShots = 0
    AawayShots = 0

    AhomeShotsOnTarget = 0
    AawayShotsOnTarget = 0

    for index, row in x.iterrows():
        homeShots += row['homeShotsTotalFT']
        homeShotsOnTarget += row['homeShotsOnTargetFT']
        awayShots += row['awayShotsTotalFT']
        awayShotsOnTarget += row['awayShotsOnTargetFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        AhomeShots += row['awayShotsTotalFT']
        AhomeShotsOnTarget += row['awayShotsOnTargetFT']
        AawayShots += row['homeShotsTotalFT']
        AawayShotsOnTarget += row['homeShotsOnTargetFT']
    print('Home shots attempt on home venue = ', homeShots)
    print('Home shots on target on home venue = ', homeShotsOnTarget)
    print('Away shots attempt on home venue = ', awayShots)
    print('Away shots on target on home venue = ', awayShotsOnTarget)
    print('Home shots attempt on away venue = ', AhomeShots)
    print('Home shots on target on away venue = ', AhomeShotsOnTarget)
    print('Away shots attempt on away venue = ', AawayShots)
    print('Away shots on target on away venue = ', AawayShotsOnTarget)
    x = pd.DataFrame(barcelona.head(50))
    homeOffsides = 0
    awayOffsides = 0
    AhomeOffsides = 0
    AawayOffsides = 0
    totalOffsides = 0
    for index, row in x.iterrows():
        homeOffsides += row['homeOffsidesCaughtFT']
        awayOffsides += row['awayOffsidesCaughtFT']

    x = pd.DataFrame(barcaAway.head(50))
    for index, row in x.iterrows():
        AhomeOffsides += row['awayOffsidesCaughtFT']
        AawayOffsides += row['homeOffsidesCaughtFT']
    print('Home offsides in home venue ', homeOffsides)
    print('Away offsides in home venue ', awayOffsides)
    print('Home offsides in away venue ', AawayOffsides)
    print('Away offsides in away venue ', AhomeOffsides)
    graph_data = plotting('Result on Home Venue', 'Home Team', 'Away Team', 'Draws', cp, cp1, cp2)
    graph_data_1 = plotting('Result on Away Venue', 'Home Team', 'Away Team', 'Draws', aw, al, ad)
    graph_data_2 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    # graph_data_3 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    graph_data_3 = plotting_2('Goals Scored and concede on Home venue', 'Home Goals', 'Away Goals', homegoalsScored,
                              homegoalsconcede)
    graph_data_4 = plotting_2('Goals Scored and concede on Away venue', 'Home Goals', 'Away Goals', awaygoalsScored,
                              awaygoalsconcede)
    graph_data_5 = plotting_2('Total goals Scored and concede ', 'Total Goals Scored', 'Total Goals Concede',
                              totalGoals, totalConcede)
    graph_data_6 = plotting_2('Possesion in home venue ', 'Home Possesion', 'Away Possession', homePossession / count,
                              100 - (homePossession / count))
    # graph_data_6 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)

    graph_data_7 = plotting_2('Total Possession ', 'Home Possesion', 'Away Possession',
                              (homePossession + awayPossession) / (count * 2),
                              100 - ((homePossession + awayPossession) / (count * 2)))
    graph_data_8 = plotting_2('Fouls in home venue ', 'Home Fouls', 'Away Fouls', homeFoulshome, awayFoulshome)
    graph_data_9 = plotting_2('Fouls in away venue ', 'Home Fouls', 'Away Fouls', homeFoulsaway, awayFoulsaway)
    graph_data_10 = plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
    graph_data_11 = plotting_2('Offsides  in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides, awayOffsides)
    graph_data_12 = plotting_2('Offsides  in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides, AhomeOffsides)
    return render_template("realmadrid.html", graph_data=graph_data, graph_data_1=graph_data_1,
                           graph_data_2=graph_data_2, graph_data_3=graph_data_3, graph_data_4=graph_data_4,
                           graph_data_5=graph_data_5, graph_data_6=graph_data_6, graph_data_7=graph_data_7,
                           graph_data_8=graph_data_8, graph_data_9=graph_data_9, graph_data_10=graph_data_10,
                           graph_data_11=graph_data_11, graph_data_12=graph_data_12)


@app.route('/')
def index():
    return render_template('checkfile.html')

@app.route('/prediction' , methods=['GET'])
def prediction():
    return render_template('prediction.html')

@app.route('/this' , methods=['GET'])
def thisnavbar():
    return render_template('testnav.html')


"""@app.route('/admin' , methods=['GET'])
def admin():
    return render_template('admin.html')
"""
@app.route('/navbar', methods=['GET'])
def navbar():
    return render_template('navbar.html')

@app.route('/barcapage', methods=['GET'])
def barcapage():
    laliga = pd.read_csv('FootballEurope.csv')
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row['awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == 'Barcelona']
    barcaAway = laliga[laliga.awayTeam == 'Barcelona']
    x = pd.DataFrame(barcelona)
    cp = 0
    cp1 = 0
    cp2 = 0
    tot = 0
    for index, row in x.iterrows():
        tot += 1
        if (row['local_team_won'] == 1):
            cp = cp + 1
        elif (row['visitor_team_won'] == 1):
            cp1 = cp1 + 1
        elif (row['draw'] == 1):
            cp2 = cp2 + 1
    print('Total no of home games are', tot)
    print('Total no of home wins are', cp)
    print('Total no of home looses are', cp1)
    print('Total no of home draws are', cp2)
    x = pd.DataFrame(barcaAway)
    aw = 0
    al = 0
    ad = 0
    at = 0
    for index, row in x.iterrows():
        at += 1
        if (row['local_team_won'] == 1):
            al = al + 1
        elif (row['visitor_team_won'] == 1):
            aw = aw + 1
        elif (row['draw' == 1]):
            ad = ad + 1
    print('Total no of away games are', at)
    print('Total no of away wins are', aw)
    print('Total no of away looses are', al)
    print('Total no of away draws are', ad)
    print('Average won draw and loose are')
    print('Total     wins         looses        draws')
    print(tot + at, '      ', cp + aw, '        ', cp2 + al, '          ', cp2 + ad)
    barcelona = laliga[laliga.homeTeam == 'Barcelona']
    barcaAway = laliga[laliga.awayTeam == 'Barcelona']
    x = pd.DataFrame(barcelona)
    homegoalsScored = 0
    homegoalsconcede = 0
    awaygoalsScored = 0
    awaygoalsconcede = 0

    for index, row in x.iterrows():
        homegoalsScored = homegoalsScored + row['homeGoalFT']
        homegoalsconcede = homegoalsconcede + row['awayGoalFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awaygoalsScored = awaygoalsScored + row['awayGoalFT']
        awaygoalsconcede = awaygoalsconcede + row['homeGoalFT']
    print('Home Goals scored are ', homegoalsScored)
    print('Home Goals concede are ', homegoalsconcede)
    print('Away Goals scored are ', awaygoalsScored)
    print('Away Goals concede are ', awaygoalsconcede)

    totalGoals = homegoalsScored + awaygoalsScored

    totalConcede = homegoalsconcede + awaygoalsconcede

    print('Total:    Scored      Concede')
    print('         ', totalGoals, '     ', totalConcede)
    x = pd.DataFrame(barcelona)
    homePossession = 0
    awayPossession = 0
    totalPossession = 0
    count = 0
    for index, row in x.iterrows():
        count += 1
        homePossession += row['homePossessionFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awayPossession += row['awayPossessionFT']
    print('Home possesion average', homePossession / count)
    print('Away possesion average', awayPossession / count)
    print('Total possesion average', (homePossession + awayPossession) / (count * 2))
    x = pd.DataFrame(barcelona)
    homeFoulshome = 0
    awayFoulshome = 0
    homeFoulsaway = 0
    awayFoulsaway = 0
    totalFouls = 0
    for index, row in x.iterrows():
        homeFoulshome += row['homeFoulsCommitedFT']
        awayFoulshome += row['awayFoulsCommitedFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        homeFoulsaway += row['awayFoulsCommitedFT']
        awayFoulsaway += row['homeFoulsCommitedFT']
    print('Home fouls in home ground = ', homeFoulshome)
    print('away fouls in home ground = ', awayFoulshome)
    print('Home fouls in away ground = ', homeFoulsaway)
    print('away fouls in away ground = ', awayFoulsaway)
    totalFoulsHome = homeFoulshome + homeFoulsaway
    totalFoulsAway = awayFoulshome + awayFoulsaway
    print('Total Fouls done = ', totalFoulsHome)
    print('Total Fouls suffer = ', totalFoulsAway)
    x = pd.DataFrame(barcelona)
    homeShots = 0
    awayShots = 0

    homeShotsOnTarget = 0
    awayShotsOnTarget = 0

    AhomeShots = 0
    AawayShots = 0

    AhomeShotsOnTarget = 0
    AawayShotsOnTarget = 0

    for index, row in x.iterrows():
        homeShots += row['homeShotsTotalFT']
        homeShotsOnTarget += row['homeShotsOnTargetFT']
        awayShots += row['awayShotsTotalFT']
        awayShotsOnTarget += row['awayShotsOnTargetFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        AhomeShots += row['awayShotsTotalFT']
        AhomeShotsOnTarget += row['awayShotsOnTargetFT']
        AawayShots += row['homeShotsTotalFT']
        AawayShotsOnTarget += row['homeShotsOnTargetFT']
    print('Home shots attempt on home venue = ', homeShots)
    print('Home shots on target on home venue = ', homeShotsOnTarget)
    print('Away shots attempt on home venue = ', awayShots)
    print('Away shots on target on home venue = ', awayShotsOnTarget)
    print('Home shots attempt on away venue = ', AhomeShots)
    print('Home shots on target on away venue = ', AhomeShotsOnTarget)
    print('Away shots attempt on away venue = ', AawayShots)
    print('Away shots on target on away venue = ', AawayShotsOnTarget)
    x = pd.DataFrame(barcelona.head(50))
    homeOffsides = 0
    awayOffsides = 0
    AhomeOffsides = 0
    AawayOffsides = 0
    totalOffsides = 0
    for index, row in x.iterrows():
        homeOffsides += row['homeOffsidesCaughtFT']
        awayOffsides += row['awayOffsidesCaughtFT']

    x = pd.DataFrame(barcaAway.head(50))
    for index, row in x.iterrows():
        AhomeOffsides += row['awayOffsidesCaughtFT']
        AawayOffsides += row['homeOffsidesCaughtFT']
    print('Home offsides in home venue ', homeOffsides)
    print('Away offsides in home venue ', awayOffsides)
    print('Home offsides in away venue ', AawayOffsides)
    print('Away offsides in away venue ', AhomeOffsides)
    graph_data =plotting('Result on Home Venue', 'Home Team', 'Away Team', 'Draws', cp, cp1, cp2)
    graph_data_1=plotting('Result on Away Venue','Home Team','Away Team','Draws',aw,al,ad)
    graph_data_2=plotting('Matches won','Home Team','Away Team','Draws',cp+aw,cp1+al,cp2+ad)
    #graph_data_3 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    graph_data_3 =plotting_2('Goals Scored and concede on Home venue','Home Goals','Away Goals',homegoalsScored,homegoalsconcede)
    graph_data_4 =plotting_2('Goals Scored and concede on Away venue','Home Goals','Away Goals',awaygoalsScored,awaygoalsconcede)
    graph_data_5 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)
    graph_data_6 = plotting_2('Possesion in home venue ', 'Home Possesion', 'Away Possession', homePossession / count, 100 - (homePossession / count))
    # graph_data_6 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)

    graph_data_7=plotting_2('Total Possession ','Home Possesion','Away Possession',(homePossession+awayPossession)/(count*2),100-((homePossession+awayPossession)/(count*2)))
    graph_data_8 = plotting_2('Fouls in home venue ','Home Fouls','Away Fouls',homeFoulshome,awayFoulshome)
    graph_data_9 = plotting_2('Fouls in away venue ','Home Fouls','Away Fouls',homeFoulsaway,awayFoulsaway)
    graph_data_10 =plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
    graph_data_11 =plotting_2('Offsides  in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides, awayOffsides)
    graph_data_12 =plotting_2('Offsides  in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides, AhomeOffsides)
    return render_template("barca.html", graph_data=graph_data, graph_data_1=graph_data_1,graph_data_2=graph_data_2,graph_data_3=graph_data_3, graph_data_4=graph_data_4,graph_data_5=graph_data_5,graph_data_6=graph_data_6, graph_data_7=graph_data_7,graph_data_8=graph_data_8,graph_data_9=graph_data_9, graph_data_10=graph_data_10,graph_data_11=graph_data_11,graph_data_12=graph_data_12)

@app.route('/madridpage', methods=['GET'])
def madridpage():
    laliga = pd.read_csv('FootballEurope.csv')
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row['awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == 'Real Madrid']
    barcaAway = laliga[laliga.awayTeam == 'Real Madrid']
    x = pd.DataFrame(barcelona)
    cp = 0
    cp1 = 0
    cp2 = 0
    tot = 0
    for index, row in x.iterrows():
        tot += 1
        if (row['local_team_won'] == 1):
            cp = cp + 1
        elif (row['visitor_team_won'] == 1):
            cp1 = cp1 + 1
        elif (row['draw'] == 1):
            cp2 = cp2 + 1
    print('Total no of home games are', tot)
    print('Total no of home wins are', cp)
    print('Total no of home looses are', cp1)
    print('Total no of home draws are', cp2)
    x = pd.DataFrame(barcaAway)
    aw = 0
    al = 0
    ad = 0
    at = 0
    for index, row in x.iterrows():
        at += 1
        if (row['local_team_won'] == 1):
            al = al + 1
        elif (row['visitor_team_won'] == 1):
            aw = aw + 1
        elif (row['draw' == 1]):
            ad = ad + 1
    print('Total no of away games are', at)
    print('Total no of away wins are', aw)
    print('Total no of away looses are', al)
    print('Total no of away draws are', ad)
    print('Average won draw and loose are')
    print('Total     wins         looses        draws')
    print(tot + at, '      ', cp + aw, '        ', cp2 + al, '          ', cp2 + ad)
    barcelona = laliga[laliga.homeTeam == 'Real Madrid']
    barcaAway = laliga[laliga.awayTeam == 'Real Madrid']
    x = pd.DataFrame(barcelona)
    homegoalsScored = 0
    homegoalsconcede = 0
    awaygoalsScored = 0
    awaygoalsconcede = 0

    for index, row in x.iterrows():
        homegoalsScored = homegoalsScored + row['homeGoalFT']
        homegoalsconcede = homegoalsconcede + row['awayGoalFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awaygoalsScored = awaygoalsScored + row['awayGoalFT']
        awaygoalsconcede = awaygoalsconcede + row['homeGoalFT']
    print('Home Goals scored are ', homegoalsScored)
    print('Home Goals concede are ', homegoalsconcede)
    print('Away Goals scored are ', awaygoalsScored)
    print('Away Goals concede are ', awaygoalsconcede)

    totalGoals = homegoalsScored + awaygoalsScored

    totalConcede = homegoalsconcede + awaygoalsconcede

    print('Total:    Scored      Concede')
    print('         ', totalGoals, '     ', totalConcede)
    x = pd.DataFrame(barcelona)
    homePossession = 0
    awayPossession = 0
    totalPossession = 0
    count = 0
    for index, row in x.iterrows():
        count += 1
        homePossession += row['homePossessionFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awayPossession += row['awayPossessionFT']
    print('Home possesion average', homePossession / count)
    print('Away possesion average', awayPossession / count)
    print('Total possesion average', (homePossession + awayPossession) / (count * 2))
    x = pd.DataFrame(barcelona)
    homeFoulshome = 0
    awayFoulshome = 0
    homeFoulsaway = 0
    awayFoulsaway = 0
    totalFouls = 0
    for index, row in x.iterrows():
        homeFoulshome += row['homeFoulsCommitedFT']
        awayFoulshome += row['awayFoulsCommitedFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        homeFoulsaway += row['awayFoulsCommitedFT']
        awayFoulsaway += row['homeFoulsCommitedFT']
    print('Home fouls in home ground = ', homeFoulshome)
    print('away fouls in home ground = ', awayFoulshome)
    print('Home fouls in away ground = ', homeFoulsaway)
    print('away fouls in away ground = ', awayFoulsaway)
    totalFoulsHome = homeFoulshome + homeFoulsaway
    totalFoulsAway = awayFoulshome + awayFoulsaway
    print('Total Fouls done = ', totalFoulsHome)
    print('Total Fouls suffer = ', totalFoulsAway)
    x = pd.DataFrame(barcelona)
    homeShots = 0
    awayShots = 0

    homeShotsOnTarget = 0
    awayShotsOnTarget = 0

    AhomeShots = 0
    AawayShots = 0

    AhomeShotsOnTarget = 0
    AawayShotsOnTarget = 0

    for index, row in x.iterrows():
        homeShots += row['homeShotsTotalFT']
        homeShotsOnTarget += row['homeShotsOnTargetFT']
        awayShots += row['awayShotsTotalFT']
        awayShotsOnTarget += row['awayShotsOnTargetFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        AhomeShots += row['awayShotsTotalFT']
        AhomeShotsOnTarget += row['awayShotsOnTargetFT']
        AawayShots += row['homeShotsTotalFT']
        AawayShotsOnTarget += row['homeShotsOnTargetFT']
    print('Home shots attempt on home venue = ', homeShots)
    print('Home shots on target on home venue = ', homeShotsOnTarget)
    print('Away shots attempt on home venue = ', awayShots)
    print('Away shots on target on home venue = ', awayShotsOnTarget)
    print('Home shots attempt on away venue = ', AhomeShots)
    print('Home shots on target on away venue = ', AhomeShotsOnTarget)
    print('Away shots attempt on away venue = ', AawayShots)
    print('Away shots on target on away venue = ', AawayShotsOnTarget)
    x = pd.DataFrame(barcelona.head(50))
    homeOffsides = 0
    awayOffsides = 0
    AhomeOffsides = 0
    AawayOffsides = 0
    totalOffsides = 0
    for index, row in x.iterrows():
        homeOffsides += row['homeOffsidesCaughtFT']
        awayOffsides += row['awayOffsidesCaughtFT']

    x = pd.DataFrame(barcaAway.head(50))
    for index, row in x.iterrows():
        AhomeOffsides += row['awayOffsidesCaughtFT']
        AawayOffsides += row['homeOffsidesCaughtFT']
    print('Home offsides in home venue ', homeOffsides)
    print('Away offsides in home venue ', awayOffsides)
    print('Home offsides in away venue ', AawayOffsides)
    print('Away offsides in away venue ', AhomeOffsides)
    graph_data =plotting('Barcelona number of wins and looses on home ground', 'Barcelona', 'Barcelona opponent', 'Draws', cp, cp1, cp2)
    graph_data_1=plotting('Barcelona number of wins and looses on away', 'Barcelona', 'Barcelona opponent', 'Draws',aw,al,ad)
    graph_data_2=plotting('Matches won','Home Team','Away Team','Draws',cp+aw,cp1+al,cp2+ad)
    #graph_data_3 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    graph_data_3 =plotting_2('Goals Scored and concede on Home venue','Home Goals','Away Goals',homegoalsScored,homegoalsconcede)
    graph_data_4 =plotting_2('Goals Scored and concede on Away venue','Home Goals','Away Goals',awaygoalsScored,awaygoalsconcede)
    graph_data_5 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)
    graph_data_6 = plotting_2('Possesion in home venue ', 'Home Possesion', 'Away Possession', homePossession / count, 100 - (homePossession / count))
    # graph_data_6 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)

    graph_data_7=plotting_2('Total Possession ','Home Possesion','Away Possession',(homePossession+awayPossession)/(count*2),100-((homePossession+awayPossession)/(count*2)))
    graph_data_8 =plotting_2('Fouls in home venue ','Home Fouls','Away Fouls',homeFoulshome,awayFoulshome)
    graph_data_9 =plotting_2('Fouls in away venue ','Home Fouls','Away Fouls',homeFoulsaway,awayFoulsaway)
    graph_data_10 =plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
    graph_data_11 =plotting_2('Offsides  in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides, awayOffsides)
    graph_data_12 =plotting_2('Offsides  in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides, AhomeOffsides)
    return render_template("realmadrid.html", graph_data=graph_data, graph_data_1=graph_data_1,graph_data_2=graph_data_2,graph_data_3=graph_data_3, graph_data_4=graph_data_4,graph_data_5=graph_data_5,graph_data_6=graph_data_6, graph_data_7=graph_data_7,graph_data_8=graph_data_8,graph_data_9=graph_data_9, graph_data_10=graph_data_10,graph_data_11=graph_data_11,graph_data_12=graph_data_12)

@app.route('/atletico', methods=['GET'])
def atletico():
    laliga = pd.read_csv('FootballEurope.csv')
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row['awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == 'Atletico']
    barcaAway = laliga[laliga.awayTeam == 'Atletico']
    x = pd.DataFrame(barcelona)
    cp = 0
    cp1 = 0
    cp2 = 0
    tot = 0
    for index, row in x.iterrows():
        tot += 1
        if (row['local_team_won'] == 1):
            cp = cp + 1
        elif (row['visitor_team_won'] == 1):
            cp1 = cp1 + 1
        elif (row['draw'] == 1):
            cp2 = cp2 + 1
    print('Total no of home games are', tot)
    print('Total no of home wins are', cp)
    print('Total no of home looses are', cp1)
    print('Total no of home draws are', cp2)
    x = pd.DataFrame(barcaAway)
    aw = 0
    al = 0
    ad = 0
    at = 0
    for index, row in x.iterrows():
        at += 1
        if (row['local_team_won'] == 1):
            al = al + 1
        elif (row['visitor_team_won'] == 1):
            aw = aw + 1
        elif (row['draw' == 1]):
            ad = ad + 1
    print('Total no of away games are', at)
    print('Total no of away wins are', aw)
    print('Total no of away looses are', al)
    print('Total no of away draws are', ad)
    print('Average won draw and loose are')
    print('Total     wins         looses        draws')
    print(tot + at, '      ', cp + aw, '        ', cp2 + al, '          ', cp2 + ad)
    barcelona = laliga[laliga.homeTeam == 'Atletico']
    barcaAway = laliga[laliga.awayTeam == 'Atletico']
    x = pd.DataFrame(barcelona)
    homegoalsScored = 0
    homegoalsconcede = 0
    awaygoalsScored = 0
    awaygoalsconcede = 0

    for index, row in x.iterrows():
        homegoalsScored = homegoalsScored + row['homeGoalFT']
        homegoalsconcede = homegoalsconcede + row['awayGoalFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awaygoalsScored = awaygoalsScored + row['awayGoalFT']
        awaygoalsconcede = awaygoalsconcede + row['homeGoalFT']
    print('Home Goals scored are ', homegoalsScored)
    print('Home Goals concede are ', homegoalsconcede)
    print('Away Goals scored are ', awaygoalsScored)
    print('Away Goals concede are ', awaygoalsconcede)

    totalGoals = homegoalsScored + awaygoalsScored

    totalConcede = homegoalsconcede + awaygoalsconcede

    print('Total:    Scored      Concede')
    print('         ', totalGoals, '     ', totalConcede)
    x = pd.DataFrame(barcelona)
    homePossession = 0
    awayPossession = 0
    totalPossession = 0
    count = 0
    for index, row in x.iterrows():
        count += 1
        homePossession += row['homePossessionFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awayPossession += row['awayPossessionFT']
    print('Home possesion average', homePossession / count)
    print('Away possesion average', awayPossession / count)
    print('Total possesion average', (homePossession + awayPossession) / (count * 2))
    x = pd.DataFrame(barcelona)
    homeFoulshome = 0
    awayFoulshome = 0
    homeFoulsaway = 0
    awayFoulsaway = 0
    totalFouls = 0
    for index, row in x.iterrows():
        homeFoulshome += row['homeFoulsCommitedFT']
        awayFoulshome += row['awayFoulsCommitedFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        homeFoulsaway += row['awayFoulsCommitedFT']
        awayFoulsaway += row['homeFoulsCommitedFT']
    print('Home fouls in home ground = ', homeFoulshome)
    print('away fouls in home ground = ', awayFoulshome)
    print('Home fouls in away ground = ', homeFoulsaway)
    print('away fouls in away ground = ', awayFoulsaway)
    totalFoulsHome = homeFoulshome + homeFoulsaway
    totalFoulsAway = awayFoulshome + awayFoulsaway
    print('Total Fouls done = ', totalFoulsHome)
    print('Total Fouls suffer = ', totalFoulsAway)
    x = pd.DataFrame(barcelona)
    homeShots = 0
    awayShots = 0

    homeShotsOnTarget = 0
    awayShotsOnTarget = 0

    AhomeShots = 0
    AawayShots = 0

    AhomeShotsOnTarget = 0
    AawayShotsOnTarget = 0

    for index, row in x.iterrows():
        homeShots += row['homeShotsTotalFT']
        homeShotsOnTarget += row['homeShotsOnTargetFT']
        awayShots += row['awayShotsTotalFT']
        awayShotsOnTarget += row['awayShotsOnTargetFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        AhomeShots += row['awayShotsTotalFT']
        AhomeShotsOnTarget += row['awayShotsOnTargetFT']
        AawayShots += row['homeShotsTotalFT']
        AawayShotsOnTarget += row['homeShotsOnTargetFT']
    print('Home shots attempt on home venue = ', homeShots)
    print('Home shots on target on home venue = ', homeShotsOnTarget)
    print('Away shots attempt on home venue = ', awayShots)
    print('Away shots on target on home venue = ', awayShotsOnTarget)
    print('Home shots attempt on away venue = ', AhomeShots)
    print('Home shots on target on away venue = ', AhomeShotsOnTarget)
    print('Away shots attempt on away venue = ', AawayShots)
    print('Away shots on target on away venue = ', AawayShotsOnTarget)
    x = pd.DataFrame(barcelona.head(50))
    homeOffsides = 0
    awayOffsides = 0
    AhomeOffsides = 0
    AawayOffsides = 0
    totalOffsides = 0
    for index, row in x.iterrows():
        homeOffsides += row['homeOffsidesCaughtFT']
        awayOffsides += row['awayOffsidesCaughtFT']

    x = pd.DataFrame(barcaAway.head(50))
    for index, row in x.iterrows():
        AhomeOffsides += row['awayOffsidesCaughtFT']
        AawayOffsides += row['homeOffsidesCaughtFT']
    print('Home offsides in home venue ', homeOffsides)
    print('Away offsides in home venue ', awayOffsides)
    print('Home offsides in away venue ', AawayOffsides)
    print('Away offsides in away venue ', AhomeOffsides)
    graph_data = plotting('Real Madrid number of wins and looses', 'Barcelona', 'Barcelona opponent', 'Draws', cp, cp1, cp2)
    graph_data_1 = plotting('Result on Home Venue', 'Home Team', 'Away Team', 'Draws', aw, al, ad)
    graph_data_2 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    # graph_data_3 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    graph_data_3 = plotting_2('Goals Scored and concede on Home venue', 'Home Goals', 'Away Goals', homegoalsScored,
                              homegoalsconcede)
    graph_data_4 = plotting_2('Goals Scored and concede on Away venue', 'Home Goals', 'Away Goals', awaygoalsScored,
                              awaygoalsconcede)
    graph_data_5 = plotting_2('Total goals Scored and concede ', 'Total Goals Scored', 'Total Goals Concede',
                              totalGoals, totalConcede)
    graph_data_6 = plotting_2('Possesion in home venue ', 'Home Possesion', 'Away Possession', homePossession / count,
                              100 - (homePossession / count))
    # graph_data_6 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)

    graph_data_7 = plotting_2('Total Possession ', 'Home Possesion', 'Away Possession',
                              (homePossession + awayPossession) / (count * 2),
                              100 - ((homePossession + awayPossession) / (count * 2)))
    graph_data_8 = plotting_2('Fouls in home venue ', 'Home Fouls', 'Away Fouls', homeFoulshome, awayFoulshome)
    graph_data_9 = plotting_2('Fouls in away venue ', 'Home Fouls', 'Away Fouls', homeFoulsaway, awayFoulsaway)
    graph_data_10 = plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
    graph_data_11 = plotting_2('Offsides  in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides, awayOffsides)
    graph_data_12 = plotting_2('Offsides  in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides, AhomeOffsides)
    return render_template("atletico.html", graph_data=graph_data, graph_data_1=graph_data_1,
                           graph_data_2=graph_data_2, graph_data_3=graph_data_3, graph_data_4=graph_data_4,
                           graph_data_5=graph_data_5, graph_data_6=graph_data_6, graph_data_7=graph_data_7,
                           graph_data_8=graph_data_8, graph_data_9=graph_data_9, graph_data_10=graph_data_10,
                           graph_data_11=graph_data_11, graph_data_12=graph_data_12)

@app.route('/sevilla', methods=['GET'])
def sevilla():
    laliga = pd.read_csv('FootballEurope.csv')
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row[
            'awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == 'Sevilla']
    barcaAway = laliga[laliga.awayTeam == 'Sevilla']
    x = pd.DataFrame(barcelona)
    cp = 0
    cp1 = 0
    cp2 = 0
    tot = 0
    for index, row in x.iterrows():
        tot += 1
        if (row['local_team_won'] == 1):
            cp = cp + 1
        elif (row['visitor_team_won'] == 1):
            cp1 = cp1 + 1
        elif (row['draw'] == 1):
            cp2 = cp2 + 1
    print('Total no of home games are', tot)
    print('Total no of home wins are', cp)
    print('Total no of home looses are', cp1)
    print('Total no of home draws are', cp2)
    x = pd.DataFrame(barcaAway)
    aw = 0
    al = 0
    ad = 0
    at = 0
    for index, row in x.iterrows():
        at += 1
        if (row['local_team_won'] == 1):
            al = al + 1
        elif (row['visitor_team_won'] == 1):
            aw = aw + 1
        elif (row['draw' == 1]):
            ad = ad + 1
    print('Total no of away games are', at)
    print('Total no of away wins are', aw)
    print('Total no of away looses are', al)
    print('Total no of away draws are', ad)
    print('Average won draw and loose are')
    print('Total     wins         looses        draws')
    print(tot + at, '      ', cp + aw, '        ', cp2 + al, '          ', cp2 + ad)
    barcelona = laliga[laliga.homeTeam == 'Atletico']
    barcaAway = laliga[laliga.awayTeam == 'Atletico']
    x = pd.DataFrame(barcelona)
    homegoalsScored = 0
    homegoalsconcede = 0
    awaygoalsScored = 0
    awaygoalsconcede = 0

    for index, row in x.iterrows():
        homegoalsScored = homegoalsScored + row['homeGoalFT']
        homegoalsconcede = homegoalsconcede + row['awayGoalFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awaygoalsScored = awaygoalsScored + row['awayGoalFT']
        awaygoalsconcede = awaygoalsconcede + row['homeGoalFT']
    print('Home Goals scored are ', homegoalsScored)
    print('Home Goals concede are ', homegoalsconcede)
    print('Away Goals scored are ', awaygoalsScored)
    print('Away Goals concede are ', awaygoalsconcede)

    totalGoals = homegoalsScored + awaygoalsScored

    totalConcede = homegoalsconcede + awaygoalsconcede

    print('Total:    Scored      Concede')
    print('         ', totalGoals, '     ', totalConcede)
    x = pd.DataFrame(barcelona)
    homePossession = 0
    awayPossession = 0
    totalPossession = 0
    count = 0
    for index, row in x.iterrows():
        count += 1
        homePossession += row['homePossessionFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awayPossession += row['awayPossessionFT']
    print('Home possesion average', homePossession / count)
    print('Away possesion average', awayPossession / count)
    print('Total possesion average', (homePossession + awayPossession) / (count * 2))
    x = pd.DataFrame(barcelona)
    homeFoulshome = 0
    awayFoulshome = 0
    homeFoulsaway = 0
    awayFoulsaway = 0
    totalFouls = 0
    for index, row in x.iterrows():
        homeFoulshome += row['homeFoulsCommitedFT']
        awayFoulshome += row['awayFoulsCommitedFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        homeFoulsaway += row['awayFoulsCommitedFT']
        awayFoulsaway += row['homeFoulsCommitedFT']
    print('Home fouls in home ground = ', homeFoulshome)
    print('away fouls in home ground = ', awayFoulshome)
    print('Home fouls in away ground = ', homeFoulsaway)
    print('away fouls in away ground = ', awayFoulsaway)
    totalFoulsHome = homeFoulshome + homeFoulsaway
    totalFoulsAway = awayFoulshome + awayFoulsaway
    print('Total Fouls done = ', totalFoulsHome)
    print('Total Fouls suffer = ', totalFoulsAway)
    x = pd.DataFrame(barcelona)
    homeShots = 0
    awayShots = 0

    homeShotsOnTarget = 0
    awayShotsOnTarget = 0

    AhomeShots = 0
    AawayShots = 0

    AhomeShotsOnTarget = 0
    AawayShotsOnTarget = 0

    for index, row in x.iterrows():
        homeShots += row['homeShotsTotalFT']
        homeShotsOnTarget += row['homeShotsOnTargetFT']
        awayShots += row['awayShotsTotalFT']
        awayShotsOnTarget += row['awayShotsOnTargetFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        AhomeShots += row['awayShotsTotalFT']
        AhomeShotsOnTarget += row['awayShotsOnTargetFT']
        AawayShots += row['homeShotsTotalFT']
        AawayShotsOnTarget += row['homeShotsOnTargetFT']
    print('Home shots attempt on home venue = ', homeShots)
    print('Home shots on target on home venue = ', homeShotsOnTarget)
    print('Away shots attempt on home venue = ', awayShots)
    print('Away shots on target on home venue = ', awayShotsOnTarget)
    print('Home shots attempt on away venue = ', AhomeShots)
    print('Home shots on target on away venue = ', AhomeShotsOnTarget)
    print('Away shots attempt on away venue = ', AawayShots)
    print('Away shots on target on away venue = ', AawayShotsOnTarget)
    x = pd.DataFrame(barcelona.head(50))
    homeOffsides = 0
    awayOffsides = 0
    AhomeOffsides = 0
    AawayOffsides = 0
    totalOffsides = 0
    for index, row in x.iterrows():
        homeOffsides += row['homeOffsidesCaughtFT']
        awayOffsides += row['awayOffsidesCaughtFT']

    x = pd.DataFrame(barcaAway.head(50))
    for index, row in x.iterrows():
        AhomeOffsides += row['awayOffsidesCaughtFT']
        AawayOffsides += row['homeOffsidesCaughtFT']
    print('Home offsides in home venue ', homeOffsides)
    print('Away offsides in home venue ', awayOffsides)
    print('Home offsides in away venue ', AawayOffsides)
    print('Away offsides in away venue ', AhomeOffsides)
    graph_data = plotting('Barcelona number of wins and looses', 'Barcelona', 'Barcelona opponent', 'Draws', cp, cp1, cp2)
    graph_data_1 = plotting('Result on Away Venue', 'Home Team', 'Away Team', 'Draws', aw, al, ad)
    graph_data_2 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    # graph_data_3 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    graph_data_3 = plotting_2('Goals Scored and concede on Home venue', 'Home Goals', 'Away Goals', homegoalsScored,
                              homegoalsconcede)
    graph_data_4 = plotting_2('Goals Scored and concede on Away venue', 'Home Goals', 'Away Goals', awaygoalsScored,
                              awaygoalsconcede)
    graph_data_5 = plotting_2('Total goals Scored and concede ', 'Total Goals Scored', 'Total Goals Concede',
                              totalGoals, totalConcede)
    graph_data_6 = plotting_2('Possesion in home venue ', 'Home Possesion', 'Away Possession',
                              homePossession / count,
                              100 - (homePossession / count))
    # graph_data_6 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)

    graph_data_7 = plotting_2('Total Possession ', 'Home Possesion', 'Away Possession',
                              (homePossession + awayPossession) / (count * 2),
                              100 - ((homePossession + awayPossession) / (count * 2)))
    graph_data_8 = plotting_2('Fouls in home venue ', 'Home Fouls', 'Away Fouls', homeFoulshome, awayFoulshome)
    graph_data_9 = plotting_2('Fouls in away venue ', 'Home Fouls', 'Away Fouls', homeFoulsaway, awayFoulsaway)
    graph_data_10 = plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
    graph_data_11 = plotting_2('Offsides  in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides,
                               awayOffsides)
    graph_data_12 = plotting_2('Offsides  in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides,
                               AhomeOffsides)
    return render_template("sevilla.html", graph_data=graph_data, graph_data_1=graph_data_1,
                           graph_data_2=graph_data_2, graph_data_3=graph_data_3, graph_data_4=graph_data_4,
                           graph_data_5=graph_data_5, graph_data_6=graph_data_6, graph_data_7=graph_data_7,
                           graph_data_8=graph_data_8, graph_data_9=graph_data_9, graph_data_10=graph_data_10,
                           graph_data_11=graph_data_11, graph_data_12=graph_data_12)

@app.route('/valencia' , methods=['GET'])
def valencia():
    laliga = pd.read_csv('FootballEurope.csv')
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row[
            'awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == 'Valencia']
    barcaAway = laliga[laliga.awayTeam == 'Valencia']
    x = pd.DataFrame(barcelona)
    cp = 0
    cp1 = 0
    cp2 = 0
    tot = 0
    for index, row in x.iterrows():
        tot += 1
        if (row['local_team_won'] == 1):
            cp = cp + 1
        elif (row['visitor_team_won'] == 1):
            cp1 = cp1 + 1
        elif (row['draw'] == 1):
            cp2 = cp2 + 1
    print('Total no of home games are', tot)
    print('Total no of home wins are', cp)
    print('Total no of home looses are', cp1)
    print('Total no of home draws are', cp2)
    x = pd.DataFrame(barcaAway)
    aw = 0
    al = 0
    ad = 0
    at = 0
    for index, row in x.iterrows():
        at += 1
        if (row['local_team_won'] == 1):
            al = al + 1
        elif (row['visitor_team_won'] == 1):
            aw = aw + 1
        elif (row['draw' == 1]):
            ad = ad + 1
    print('Total no of away games are', at)
    print('Total no of away wins are', aw)
    print('Total no of away looses are', al)
    print('Total no of away draws are', ad)
    print('Average won draw and loose are')
    print('Total     wins         looses        draws')
    print(tot + at, '      ', cp + aw, '        ', cp2 + al, '          ', cp2 + ad)
    barcelona = laliga[laliga.homeTeam == 'Valencia']
    barcaAway = laliga[laliga.awayTeam == 'Valencia']
    x = pd.DataFrame(barcelona)
    homegoalsScored = 0
    homegoalsconcede = 0
    awaygoalsScored = 0
    awaygoalsconcede = 0

    for index, row in x.iterrows():
        homegoalsScored = homegoalsScored + row['homeGoalFT']
        homegoalsconcede = homegoalsconcede + row['awayGoalFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awaygoalsScored = awaygoalsScored + row['awayGoalFT']
        awaygoalsconcede = awaygoalsconcede + row['homeGoalFT']
    print('Home Goals scored are ', homegoalsScored)
    print('Home Goals concede are ', homegoalsconcede)
    print('Away Goals scored are ', awaygoalsScored)
    print('Away Goals concede are ', awaygoalsconcede)

    totalGoals = homegoalsScored + awaygoalsScored

    totalConcede = homegoalsconcede + awaygoalsconcede

    print('Total:    Scored      Concede')
    print('         ', totalGoals, '     ', totalConcede)
    x = pd.DataFrame(barcelona)
    homePossession = 0
    awayPossession = 0
    totalPossession = 0
    count = 0
    for index, row in x.iterrows():
        count += 1
        homePossession += row['homePossessionFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awayPossession += row['awayPossessionFT']
    print('Home possesion average', homePossession / count)
    print('Away possesion average', awayPossession / count)
    print('Total possesion average', (homePossession + awayPossession) / (count * 2))
    x = pd.DataFrame(barcelona)
    homeFoulshome = 0
    awayFoulshome = 0
    homeFoulsaway = 0
    awayFoulsaway = 0
    totalFouls = 0
    for index, row in x.iterrows():
        homeFoulshome += row['homeFoulsCommitedFT']
        awayFoulshome += row['awayFoulsCommitedFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        homeFoulsaway += row['awayFoulsCommitedFT']
        awayFoulsaway += row['homeFoulsCommitedFT']
    print('Home fouls in home ground = ', homeFoulshome)
    print('away fouls in home ground = ', awayFoulshome)
    print('Home fouls in away ground = ', homeFoulsaway)
    print('away fouls in away ground = ', awayFoulsaway)
    totalFoulsHome = homeFoulshome + homeFoulsaway
    totalFoulsAway = awayFoulshome + awayFoulsaway
    print('Total Fouls done = ', totalFoulsHome)
    print('Total Fouls suffer = ', totalFoulsAway)
    x = pd.DataFrame(barcelona)
    homeShots = 0
    awayShots = 0

    homeShotsOnTarget = 0
    awayShotsOnTarget = 0

    AhomeShots = 0
    AawayShots = 0

    AhomeShotsOnTarget = 0
    AawayShotsOnTarget = 0

    for index, row in x.iterrows():
        homeShots += row['homeShotsTotalFT']
        homeShotsOnTarget += row['homeShotsOnTargetFT']
        awayShots += row['awayShotsTotalFT']
        awayShotsOnTarget += row['awayShotsOnTargetFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        AhomeShots += row['awayShotsTotalFT']
        AhomeShotsOnTarget += row['awayShotsOnTargetFT']
        AawayShots += row['homeShotsTotalFT']
        AawayShotsOnTarget += row['homeShotsOnTargetFT']
    print('Home shots attempt on home venue = ', homeShots)
    print('Home shots on target on home venue = ', homeShotsOnTarget)
    print('Away shots attempt on home venue = ', awayShots)
    print('Away shots on target on home venue = ', awayShotsOnTarget)
    print('Home shots attempt on away venue = ', AhomeShots)
    print('Home shots on target on away venue = ', AhomeShotsOnTarget)
    print('Away shots attempt on away venue = ', AawayShots)
    print('Away shots on target on away venue = ', AawayShotsOnTarget)
    x = pd.DataFrame(barcelona.head(50))
    homeOffsides = 0
    awayOffsides = 0
    AhomeOffsides = 0
    AawayOffsides = 0
    totalOffsides = 0
    for index, row in x.iterrows():
        homeOffsides += row['homeOffsidesCaughtFT']
        awayOffsides += row['awayOffsidesCaughtFT']

    x = pd.DataFrame(barcaAway.head(50))
    for index, row in x.iterrows():
        AhomeOffsides += row['awayOffsidesCaughtFT']
        AawayOffsides += row['homeOffsidesCaughtFT']
    print('Home offsides in home venue ', homeOffsides)
    print('Away offsides in home venue ', awayOffsides)
    print('Home offsides in away venue ', AawayOffsides)
    print('Away offsides in away venue ', AhomeOffsides)
    graph_data = plotting('Result on Home Venue', 'Home Team', 'Away Team', 'Draws', cp, cp1, cp2)
    graph_data_1 = plotting('Result on Away Venue', 'Home Team', 'Away Team', 'Draws', aw, al, ad)
    graph_data_2 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    # graph_data_3 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    graph_data_3 = plotting_2('Goals Scored and concede on Home venue', 'Home Goals', 'Away Goals', homegoalsScored,
                              homegoalsconcede)
    graph_data_4 = plotting_2('Goals Scored and concede on Away venue', 'Home Goals', 'Away Goals', awaygoalsScored,
                              awaygoalsconcede)
    graph_data_5 = plotting_2('Total goals Scored and concede ', 'Total Goals Scored', 'Total Goals Concede',
                              totalGoals, totalConcede)
    graph_data_6 = plotting_2('Possesion in home venue ', 'Home Possesion', 'Away Possession',
                              homePossession / count,
                              100 - (homePossession / count))
    # graph_data_6 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)

    graph_data_7 = plotting_2('Total Possession ', 'Home Possesion', 'Away Possession',
                              (homePossession + awayPossession) / (count * 2),
                              100 - ((homePossession + awayPossession) / (count * 2)))
    graph_data_8 = plotting_2('Fouls in home venue ', 'Home Fouls', 'Away Fouls', homeFoulshome, awayFoulshome)
    graph_data_9 = plotting_2('Fouls in away venue ', 'Home Fouls', 'Away Fouls', homeFoulsaway, awayFoulsaway)
    graph_data_10 = plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
    graph_data_11 = plotting_2('Offsides  in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides,
                               awayOffsides)
    graph_data_12 = plotting_2('Offsides  in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides,
                               AhomeOffsides)
    return render_template("Valencia.html", graph_data=graph_data, graph_data_1=graph_data_1,
                           graph_data_2=graph_data_2, graph_data_3=graph_data_3, graph_data_4=graph_data_4,
                           graph_data_5=graph_data_5, graph_data_6=graph_data_6, graph_data_7=graph_data_7,
                           graph_data_8=graph_data_8, graph_data_9=graph_data_9, graph_data_10=graph_data_10,
                           graph_data_11=graph_data_11, graph_data_12=graph_data_12)

@app.route('/betis', methods=['GET'])
def betis():
    laliga = pd.read_csv('FootballEurope.csv')
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row[
            'awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == 'Real Betis']
    barcaAway = laliga[laliga.awayTeam == 'Real Betis']
    x = pd.DataFrame(barcelona)
    cp = 0
    cp1 = 0
    cp2 = 0
    tot = 0
    for index, row in x.iterrows():
        tot += 1
        if (row['local_team_won'] == 1):
            cp = cp + 1
        elif (row['visitor_team_won'] == 1):
            cp1 = cp1 + 1
        elif (row['draw'] == 1):
            cp2 = cp2 + 1
    print('Total no of home games are', tot)
    print('Total no of home wins are', cp)
    print('Total no of home looses are', cp1)
    print('Total no of home draws are', cp2)
    x = pd.DataFrame(barcaAway)
    aw = 0
    al = 0
    ad = 0
    at = 0
    for index, row in x.iterrows():
        at += 1
        if (row['local_team_won'] == 1):
            al = al + 1
        elif (row['visitor_team_won'] == 1):
            aw = aw + 1
        elif (row['draw' == 1]):
            ad = ad + 1
    print('Total no of away games are', at)
    print('Total no of away wins are', aw)
    print('Total no of away looses are', al)
    print('Total no of away draws are', ad)
    print('Average won draw and loose are')
    print('Total     wins         looses        draws')
    print(tot + at, '      ', cp + aw, '        ', cp2 + al, '          ', cp2 + ad)
    barcelona = laliga[laliga.homeTeam == 'Real Betis']
    barcaAway = laliga[laliga.awayTeam == 'Real Betis']
    x = pd.DataFrame(barcelona)
    homegoalsScored = 0
    homegoalsconcede = 0
    awaygoalsScored = 0
    awaygoalsconcede = 0

    for index, row in x.iterrows():
        homegoalsScored = homegoalsScored + row['homeGoalFT']
        homegoalsconcede = homegoalsconcede + row['awayGoalFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awaygoalsScored = awaygoalsScored + row['awayGoalFT']
        awaygoalsconcede = awaygoalsconcede + row['homeGoalFT']
    print('Home Goals scored are ', homegoalsScored)
    print('Home Goals concede are ', homegoalsconcede)
    print('Away Goals scored are ', awaygoalsScored)
    print('Away Goals concede are ', awaygoalsconcede)

    totalGoals = homegoalsScored + awaygoalsScored

    totalConcede = homegoalsconcede + awaygoalsconcede

    print('Total:    Scored      Concede')
    print('         ', totalGoals, '     ', totalConcede)
    x = pd.DataFrame(barcelona)
    homePossession = 0
    awayPossession = 0
    totalPossession = 0
    count = 0
    for index, row in x.iterrows():
        count += 1
        homePossession += row['homePossessionFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awayPossession += row['awayPossessionFT']
    print('Home possesion average', homePossession / count)
    print('Away possesion average', awayPossession / count)
    print('Total possesion average', (homePossession + awayPossession) / (count * 2))
    x = pd.DataFrame(barcelona)
    homeFoulshome = 0
    awayFoulshome = 0
    homeFoulsaway = 0
    awayFoulsaway = 0
    totalFouls = 0
    for index, row in x.iterrows():
        homeFoulshome += row['homeFoulsCommitedFT']
        awayFoulshome += row['awayFoulsCommitedFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        homeFoulsaway += row['awayFoulsCommitedFT']
        awayFoulsaway += row['homeFoulsCommitedFT']
    print('Home fouls in home ground = ', homeFoulshome)
    print('away fouls in home ground = ', awayFoulshome)
    print('Home fouls in away ground = ', homeFoulsaway)
    print('away fouls in away ground = ', awayFoulsaway)
    totalFoulsHome = homeFoulshome + homeFoulsaway
    totalFoulsAway = awayFoulshome + awayFoulsaway
    print('Total Fouls done = ', totalFoulsHome)
    print('Total Fouls suffer = ', totalFoulsAway)
    x = pd.DataFrame(barcelona)
    homeShots = 0
    awayShots = 0

    homeShotsOnTarget = 0
    awayShotsOnTarget = 0

    AhomeShots = 0
    AawayShots = 0

    AhomeShotsOnTarget = 0
    AawayShotsOnTarget = 0

    for index, row in x.iterrows():
        homeShots += row['homeShotsTotalFT']
        homeShotsOnTarget += row['homeShotsOnTargetFT']
        awayShots += row['awayShotsTotalFT']
        awayShotsOnTarget += row['awayShotsOnTargetFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        AhomeShots += row['awayShotsTotalFT']
        AhomeShotsOnTarget += row['awayShotsOnTargetFT']
        AawayShots += row['homeShotsTotalFT']
        AawayShotsOnTarget += row['homeShotsOnTargetFT']
    print('Home shots attempt on home venue = ', homeShots)
    print('Home shots on target on home venue = ', homeShotsOnTarget)
    print('Away shots attempt on home venue = ', awayShots)
    print('Away shots on target on home venue = ', awayShotsOnTarget)
    print('Home shots attempt on away venue = ', AhomeShots)
    print('Home shots on target on away venue = ', AhomeShotsOnTarget)
    print('Away shots attempt on away venue = ', AawayShots)
    print('Away shots on target on away venue = ', AawayShotsOnTarget)
    x = pd.DataFrame(barcelona.head(50))
    homeOffsides = 0
    awayOffsides = 0
    AhomeOffsides = 0
    AawayOffsides = 0
    totalOffsides = 0
    for index, row in x.iterrows():
        homeOffsides += row['homeOffsidesCaughtFT']
        awayOffsides += row['awayOffsidesCaughtFT']

    x = pd.DataFrame(barcaAway.head(50))
    for index, row in x.iterrows():
        AhomeOffsides += row['awayOffsidesCaughtFT']
        AawayOffsides += row['homeOffsidesCaughtFT']
    print('Home offsides in home venue ', homeOffsides)
    print('Away offsides in home venue ', awayOffsides)
    print('Home offsides in away venue ', AawayOffsides)
    print('Away offsides in away venue ', AhomeOffsides)
    graph_data = plotting('Result on Home Venue', 'Home Team', 'Away Team', 'Draws', cp, cp1, cp2)
    graph_data_1 = plotting('Result on Away Venue', 'Home Team', 'Away Team', 'Draws', aw, al, ad)
    graph_data_2 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    # graph_data_3 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    graph_data_3 = plotting_2('Goals Scored and concede on Home venue', 'Home Goals', 'Away Goals', homegoalsScored,
                              homegoalsconcede)
    graph_data_4 = plotting_2('Goals Scored and concede on Away venue', 'Home Goals', 'Away Goals', awaygoalsScored,
                              awaygoalsconcede)
    graph_data_5 = plotting_2('Total goals Scored and concede ', 'Total Goals Scored', 'Total Goals Concede',
                              totalGoals, totalConcede)
    graph_data_6 = plotting_2('Possesion in home venue ', 'Home Possesion', 'Away Possession',
                              homePossession / count,
                              100 - (homePossession / count))
    # graph_data_6 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)

    graph_data_7 = plotting_2('Total Possession ', 'Home Possesion', 'Away Possession',
                              (homePossession + awayPossession) / (count * 2),
                              100 - ((homePossession + awayPossession) / (count * 2)))
    graph_data_8 = plotting_2('Fouls in home venue ', 'Home Fouls', 'Away Fouls', homeFoulshome, awayFoulshome)
    graph_data_9 = plotting_2('Fouls in away venue ', 'Home Fouls', 'Away Fouls', homeFoulsaway, awayFoulsaway)
    graph_data_10 = plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
    graph_data_11 = plotting_2('Offsides  in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides,
                               awayOffsides)
    graph_data_12 = plotting_2('Offsides  in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides,
                               AhomeOffsides)
    return render_template("betis.html", graph_data=graph_data, graph_data_1=graph_data_1,
                           graph_data_2=graph_data_2, graph_data_3=graph_data_3, graph_data_4=graph_data_4,
                           graph_data_5=graph_data_5, graph_data_6=graph_data_6, graph_data_7=graph_data_7,
                           graph_data_8=graph_data_8, graph_data_9=graph_data_9, graph_data_10=graph_data_10,
                           graph_data_11=graph_data_11, graph_data_12=graph_data_12)

@app.route('/athletic' , methods=['GET'])
def athletic():
    laliga = pd.read_csv('FootballEurope.csv')
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row[
            'awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == 'Real Betis']
    barcaAway = laliga[laliga.awayTeam == 'Real Betis']
    x = pd.DataFrame(barcelona)
    cp = 0
    cp1 = 0
    cp2 = 0
    tot = 0
    for index, row in x.iterrows():
        tot += 1
        if (row['local_team_won'] == 1):
            cp = cp + 1
        elif (row['visitor_team_won'] == 1):
            cp1 = cp1 + 1
        elif (row['draw'] == 1):
            cp2 = cp2 + 1
    print('Total no of home games are', tot)
    print('Total no of home wins are', cp)
    print('Total no of home looses are', cp1)
    print('Total no of home draws are', cp2)
    x = pd.DataFrame(barcaAway)
    aw = 0
    al = 0
    ad = 0
    at = 0
    for index, row in x.iterrows():
        at += 1
        if (row['local_team_won'] == 1):
            al = al + 1
        elif (row['visitor_team_won'] == 1):
            aw = aw + 1
        elif (row['draw' == 1]):
            ad = ad + 1
    print('Total no of away games are', at)
    print('Total no of away wins are', aw)
    print('Total no of away looses are', al)
    print('Total no of away draws are', ad)
    print('Average won draw and loose are')
    print('Total     wins         looses        draws')
    print(tot + at, '      ', cp + aw, '        ', cp2 + al, '          ', cp2 + ad)
    barcelona = laliga[laliga.homeTeam == 'Athletic Club']
    barcaAway = laliga[laliga.awayTeam == 'Athletic Club']
    x = pd.DataFrame(barcelona)
    homegoalsScored = 0
    homegoalsconcede = 0
    awaygoalsScored = 0
    awaygoalsconcede = 0

    for index, row in x.iterrows():
        homegoalsScored = homegoalsScored + row['homeGoalFT']
        homegoalsconcede = homegoalsconcede + row['awayGoalFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awaygoalsScored = awaygoalsScored + row['awayGoalFT']
        awaygoalsconcede = awaygoalsconcede + row['homeGoalFT']
    print('Home Goals scored are ', homegoalsScored)
    print('Home Goals concede are ', homegoalsconcede)
    print('Away Goals scored are ', awaygoalsScored)
    print('Away Goals concede are ', awaygoalsconcede)

    totalGoals = homegoalsScored + awaygoalsScored
    totalConcede = homegoalsconcede + awaygoalsconcede
    print('Total:    Scored      Concede')
    print('         ', totalGoals, '     ', totalConcede)
    x = pd.DataFrame(barcelona)
    homePossession = 0
    awayPossession = 0
    totalPossession = 0
    count = 0
    for index, row in x.iterrows():
        count += 1
        homePossession += row['homePossessionFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awayPossession += row['awayPossessionFT']
    print('Home possesion average', homePossession / count)
    print('Away possesion average', awayPossession / count)
    print('Total possesion average', (homePossession + awayPossession) / (count * 2))
    x = pd.DataFrame(barcelona)
    homeFoulshome = 0
    awayFoulshome = 0
    homeFoulsaway = 0
    awayFoulsaway = 0
    totalFouls = 0
    for index, row in x.iterrows():
        homeFoulshome += row['homeFoulsCommitedFT']
        awayFoulshome += row['awayFoulsCommitedFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        homeFoulsaway += row['awayFoulsCommitedFT']
        awayFoulsaway += row['homeFoulsCommitedFT']
    print('Home fouls in home ground = ', homeFoulshome)
    print('away fouls in home ground = ', awayFoulshome)
    print('Home fouls in away ground = ', homeFoulsaway)
    print('away fouls in away ground = ', awayFoulsaway)
    totalFoulsHome = homeFoulshome + homeFoulsaway
    totalFoulsAway = awayFoulshome + awayFoulsaway
    print('Total Fouls done = ', totalFoulsHome)
    print('Total Fouls suffer = ', totalFoulsAway)
    x = pd.DataFrame(barcelona)
    homeShots = 0
    awayShots = 0

    homeShotsOnTarget = 0
    awayShotsOnTarget = 0

    AhomeShots = 0
    AawayShots = 0

    AhomeShotsOnTarget = 0
    AawayShotsOnTarget = 0

    for index, row in x.iterrows():
        homeShots += row['homeShotsTotalFT']
        homeShotsOnTarget += row['homeShotsOnTargetFT']
        awayShots += row['awayShotsTotalFT']
        awayShotsOnTarget += row['awayShotsOnTargetFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        AhomeShots += row['awayShotsTotalFT']
        AhomeShotsOnTarget += row['awayShotsOnTargetFT']
        AawayShots += row['homeShotsTotalFT']
        AawayShotsOnTarget += row['homeShotsOnTargetFT']
    print('Home shots attempt on home venue = ', homeShots)
    print('Home shots on target on home venue = ', homeShotsOnTarget)
    print('Away shots attempt on home venue = ', awayShots)
    print('Away shots on target on home venue = ', awayShotsOnTarget)
    print('Home shots attempt on away venue = ', AhomeShots)
    print('Home shots on target on away venue = ', AhomeShotsOnTarget)
    print('Away shots attempt on away venue = ', AawayShots)
    print('Away shots on target on away venue = ', AawayShotsOnTarget)
    x = pd.DataFrame(barcelona.head(50))
    homeOffsides = 0
    awayOffsides = 0
    AhomeOffsides = 0
    AawayOffsides = 0
    totalOffsides = 0
    for index, row in x.iterrows():
        homeOffsides += row['homeOffsidesCaughtFT']
        awayOffsides += row['awayOffsidesCaughtFT']

    x = pd.DataFrame(barcaAway.head(50))
    for index, row in x.iterrows():
        AhomeOffsides += row['awayOffsidesCaughtFT']
        AawayOffsides += row['homeOffsidesCaughtFT']
    print('Home offsides in home venue ', homeOffsides)
    print('Away offsides in home venue ', awayOffsides)
    print('Home offsides in away venue ', AawayOffsides)
    print('Away offsides in away venue ', AhomeOffsides)
    graph_data = plotting('Result on Home Venue', 'Home Team', 'Away Team', 'Draws', cp, cp1, cp2)
    graph_data_1 = plotting('Result on Away Venue', 'Home Team', 'Away Team', 'Draws', aw, al, ad)
    graph_data_2 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    # graph_data_3 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    graph_data_3 = plotting_2('Goals Scored and concede on Home venue', 'Home Goals', 'Away Goals', homegoalsScored,
                              homegoalsconcede)
    graph_data_4 = plotting_2('Goals Scored and concede on Away venue', 'Home Goals', 'Away Goals', awaygoalsScored,
                              awaygoalsconcede)
    graph_data_5 = plotting_2('Total goals Scored and concede ', 'Total Goals Scored', 'Total Goals Concede',
                              totalGoals, totalConcede)
    graph_data_6 = plotting_2('Possesion in home venue ', 'Home Possesion', 'Away Possession',
                              homePossession / count,
                              100 - (homePossession / count))
    # graph_data_6 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)

    graph_data_7 = plotting_2('Total Possession ', 'Home Possesion', 'Away Possession',
                              (homePossession + awayPossession) / (count * 2),
                              100 - ((homePossession + awayPossession) / (count * 2)))
    graph_data_8 = plotting_2('Fouls in home venue ', 'Home Fouls', 'Away Fouls', homeFoulshome, awayFoulshome)
    graph_data_9 = plotting_2('Fouls in away venue ', 'Home Fouls', 'Away Fouls', homeFoulsaway, awayFoulsaway)
    graph_data_10 = plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
    graph_data_11 = plotting_2('Offsides  in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides,
                               awayOffsides)
    graph_data_12 = plotting_2('Offsides  in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides,
                               AhomeOffsides)
    return render_template("athletic.html", graph_data=graph_data, graph_data_1=graph_data_1,
                           graph_data_2=graph_data_2, graph_data_3=graph_data_3, graph_data_4=graph_data_4,
                           graph_data_5=graph_data_5, graph_data_6=graph_data_6, graph_data_7=graph_data_7,
                           graph_data_8=graph_data_8, graph_data_9=graph_data_9, graph_data_10=graph_data_10,
                           graph_data_11=graph_data_11, graph_data_12=graph_data_12)

@app.route('/villareal' , methods=['GET'])
def villareal():
    laliga = pd.read_csv('FootballEurope.csv')
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row[
            'awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == 'Villareal']
    barcaAway = laliga[laliga.awayTeam == 'Villareal']
    x = pd.DataFrame(barcelona)
    cp = 0
    cp1 = 0
    cp2 = 0
    tot = 0
    for index, row in x.iterrows():
        tot += 1
        if (row['local_team_won'] == 1):
            cp = cp + 1
        elif (row['visitor_team_won'] == 1):
            cp1 = cp1 + 1
        elif (row['draw'] == 1):
            cp2 = cp2 + 1
    print('Total no of home games are', tot)
    print('Total no of home wins are', cp)
    print('Total no of home looses are', cp1)
    print('Total no of home draws are', cp2)
    x = pd.DataFrame(barcaAway)
    aw = 0
    al = 0
    ad = 0
    at = 0
    for index, row in x.iterrows():
        at += 1
        if (row['local_team_won'] == 1):
            al = al + 1
        elif (row['visitor_team_won'] == 1):
            aw = aw + 1
        elif (row['draw' == 1]):
            ad = ad + 1
    print('Total no of away games are', at)
    print('Total no of away wins are', aw)
    print('Total no of away looses are', al)
    print('Total no of away draws are', ad)
    print('Average won draw and loose are')
    print('Total     wins         looses        draws')
    print(tot + at, '      ', cp + aw, '        ', cp2 + al, '          ', cp2 + ad)
    barcelona = laliga[laliga.homeTeam == 'Villareal']
    barcaAway = laliga[laliga.awayTeam == 'Villareal']
    x = pd.DataFrame(barcelona)
    homegoalsScored = 0
    homegoalsconcede = 0
    awaygoalsScored = 0
    awaygoalsconcede = 0

    for index, row in x.iterrows():
        homegoalsScored = homegoalsScored + row['homeGoalFT']
        homegoalsconcede = homegoalsconcede + row['awayGoalFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awaygoalsScored = awaygoalsScored + row['awayGoalFT']
        awaygoalsconcede = awaygoalsconcede + row['homeGoalFT']
    print('Home Goals scored are ', homegoalsScored)
    print('Home Goals concede are ', homegoalsconcede)
    print('Away Goals scored are ', awaygoalsScored)
    print('Away Goals concede are ', awaygoalsconcede)

    totalGoals = homegoalsScored + awaygoalsScored

    totalConcede = homegoalsconcede + awaygoalsconcede

    print('Total:    Scored      Concede')
    print('         ', totalGoals, '     ', totalConcede)
    x = pd.DataFrame(barcelona)
    homePossession = 0
    awayPossession = 0
    totalPossession = 0
    count = 0
    for index, row in x.iterrows():
        count += 1
        homePossession += row['homePossessionFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awayPossession += row['awayPossessionFT']
    print('Home possesion average', homePossession / count)
    print('Away possesion average', awayPossession / count)
    print('Total possesion average', (homePossession + awayPossession) / (count * 2))
    x = pd.DataFrame(barcelona)
    homeFoulshome = 0
    awayFoulshome = 0
    homeFoulsaway = 0
    awayFoulsaway = 0
    totalFouls = 0
    for index, row in x.iterrows():
        homeFoulshome += row['homeFoulsCommitedFT']
        awayFoulshome += row['awayFoulsCommitedFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        homeFoulsaway += row['awayFoulsCommitedFT']
        awayFoulsaway += row['homeFoulsCommitedFT']
    print('Home fouls in home ground = ', homeFoulshome)
    print('away fouls in home ground = ', awayFoulshome)
    print('Home fouls in away ground = ', homeFoulsaway)
    print('away fouls in away ground = ', awayFoulsaway)
    totalFoulsHome = homeFoulshome + homeFoulsaway
    totalFoulsAway = awayFoulshome + awayFoulsaway
    print('Total Fouls done = ', totalFoulsHome)
    print('Total Fouls suffer = ', totalFoulsAway)
    x = pd.DataFrame(barcelona)
    homeShots = 0
    awayShots = 0

    homeShotsOnTarget = 0
    awayShotsOnTarget = 0

    AhomeShots = 0
    AawayShots = 0

    AhomeShotsOnTarget = 0
    AawayShotsOnTarget = 0

    for index, row in x.iterrows():
        homeShots += row['homeShotsTotalFT']
        homeShotsOnTarget += row['homeShotsOnTargetFT']
        awayShots += row['awayShotsTotalFT']
        awayShotsOnTarget += row['awayShotsOnTargetFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        AhomeShots += row['awayShotsTotalFT']
        AhomeShotsOnTarget += row['awayShotsOnTargetFT']
        AawayShots += row['homeShotsTotalFT']
        AawayShotsOnTarget += row['homeShotsOnTargetFT']
    print('Home shots attempt on home venue = ', homeShots)
    print('Home shots on target on home venue = ', homeShotsOnTarget)
    print('Away shots attempt on home venue = ', awayShots)
    print('Away shots on target on home venue = ', awayShotsOnTarget)
    print('Home shots attempt on away venue = ', AhomeShots)
    print('Home shots on target on away venue = ', AhomeShotsOnTarget)
    print('Away shots attempt on away venue = ', AawayShots)
    print('Away shots on target on away venue = ', AawayShotsOnTarget)
    x = pd.DataFrame(barcelona.head(50))
    homeOffsides = 0
    awayOffsides = 0
    AhomeOffsides = 0
    AawayOffsides = 0
    totalOffsides = 0
    for index, row in x.iterrows():
        homeOffsides += row['homeOffsidesCaughtFT']
        awayOffsides += row['awayOffsidesCaughtFT']

    x = pd.DataFrame(barcaAway.head(50))
    for index, row in x.iterrows():
        AhomeOffsides += row['awayOffsidesCaughtFT']
        AawayOffsides += row['homeOffsidesCaughtFT']
    print('Home offsides in home venue ', homeOffsides)
    print('Away offsides in home venue ', awayOffsides)
    print('Home offsides in away venue ', AawayOffsides)
    print('Away offsides in away venue ', AhomeOffsides)
    graph_data = plotting('Result on Home Venue', 'Home Team', 'Away Team', 'Draws', cp, cp1, cp2)
    graph_data_1 = plotting('Result on Away Venue', 'Home Team', 'Away Team', 'Draws', aw, al, ad)
    graph_data_2 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    # graph_data_3 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    graph_data_3 = plotting_2('Goals Scored and concede on Home venue', 'Home Goals', 'Away Goals', homegoalsScored,
                              homegoalsconcede)
    graph_data_4 = plotting_2('Goals Scored and concede on Away venue', 'Home Goals', 'Away Goals', awaygoalsScored,
                              awaygoalsconcede)
    graph_data_5 = plotting_2('Total goals Scored and concede ', 'Total Goals Scored', 'Total Goals Concede',
                              totalGoals, totalConcede)
    graph_data_6 = plotting_2('Possesion in home venue ', 'Home Possesion', 'Away Possession',
                              homePossession / count,
                              100 - (homePossession / count))
    # graph_data_6 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)

    graph_data_7 = plotting_2('Total Possession ', 'Home Possesion', 'Away Possession',
                              (homePossession + awayPossession) / (count * 2),
                              100 - ((homePossession + awayPossession) / (count * 2)))
    graph_data_8 = plotting_2('Fouls in home venue ', 'Home Fouls', 'Away Fouls', homeFoulshome, awayFoulshome)
    graph_data_9 = plotting_2('Fouls in away venue ', 'Home Fouls', 'Away Fouls', homeFoulsaway, awayFoulsaway)
    graph_data_10 = plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
    graph_data_11 = plotting_2('Offsides  in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides,
                               awayOffsides)
    graph_data_12 = plotting_2('Offsides  in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides,
                               AhomeOffsides)
    return render_template("villareal.html", graph_data=graph_data, graph_data_1=graph_data_1,
                           graph_data_2=graph_data_2, graph_data_3=graph_data_3, graph_data_4=graph_data_4,
                           graph_data_5=graph_data_5, graph_data_6=graph_data_6, graph_data_7=graph_data_7,
                           graph_data_8=graph_data_8, graph_data_9=graph_data_9, graph_data_10=graph_data_10,
                           graph_data_11=graph_data_11, graph_data_12=graph_data_12)

@app.route('/getafe' , methods=['GET'])
def getafe():
    laliga = pd.read_csv('FootballEurope.csv')
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row[
            'awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    barcelona = laliga[laliga.homeTeam == 'Getafe']
    barcaAway = laliga[laliga.awayTeam == 'Getafe']
    x = pd.DataFrame(barcelona)
    cp = 0
    cp1 = 0
    cp2 = 0
    tot = 0
    for index, row in x.iterrows():
        tot += 1
        if (row['local_team_won'] == 1):
            cp = cp + 1
        elif (row['visitor_team_won'] == 1):
            cp1 = cp1 + 1
        elif (row['draw'] == 1):
            cp2 = cp2 + 1
    print('Total no of home games are', tot)
    print('Total no of home wins are', cp)
    print('Total no of home looses are', cp1)
    print('Total no of home draws are', cp2)
    x = pd.DataFrame(barcaAway)
    aw = 0
    al = 0
    ad = 0
    at = 0
    for index, row in x.iterrows():
        at += 1
        if (row['local_team_won'] == 1):
            al = al + 1
        elif (row['visitor_team_won'] == 1):
            aw = aw + 1
        elif (row['draw' == 1]):
            ad = ad + 1
    print('Total no of away games are', at)
    print('Total no of away wins are', aw)
    print('Total no of away looses are', al)
    print('Total no of away draws are', ad)
    print('Average won draw and loose are')
    print('Total     wins         looses        draws')
    print(tot + at, '      ', cp + aw, '        ', cp2 + al, '          ', cp2 + ad)
    barcelona = laliga[laliga.homeTeam == 'Villareal']
    barcaAway = laliga[laliga.awayTeam == 'Villareal']
    x = pd.DataFrame(barcelona)
    homegoalsScored = 0
    homegoalsconcede = 0
    awaygoalsScored = 0
    awaygoalsconcede = 0

    for index, row in x.iterrows():
        homegoalsScored = homegoalsScored + row['homeGoalFT']
        homegoalsconcede = homegoalsconcede + row['awayGoalFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awaygoalsScored = awaygoalsScored + row['awayGoalFT']
        awaygoalsconcede = awaygoalsconcede + row['homeGoalFT']
    print('Home Goals scored are ', homegoalsScored)
    print('Home Goals concede are ', homegoalsconcede)
    print('Away Goals scored are ', awaygoalsScored)
    print('Away Goals concede are ', awaygoalsconcede)

    totalGoals = homegoalsScored + awaygoalsScored

    totalConcede = homegoalsconcede + awaygoalsconcede

    print('Total:    Scored      Concede')
    print('         ', totalGoals, '     ', totalConcede)
    x = pd.DataFrame(barcelona)
    homePossession = 0
    awayPossession = 0
    totalPossession = 0
    count = 0
    for index, row in x.iterrows():
        count += 1
        homePossession += row['homePossessionFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        awayPossession += row['awayPossessionFT']
    print('Home possesion average', homePossession / count)
    print('Away possesion average', awayPossession / count)
    print('Total possesion average', (homePossession + awayPossession) / (count * 2))
    x = pd.DataFrame(barcelona)
    homeFoulshome = 0
    awayFoulshome = 0
    homeFoulsaway = 0
    awayFoulsaway = 0
    totalFouls = 0
    for index, row in x.iterrows():
        homeFoulshome += row['homeFoulsCommitedFT']
        awayFoulshome += row['awayFoulsCommitedFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        homeFoulsaway += row['awayFoulsCommitedFT']
        awayFoulsaway += row['homeFoulsCommitedFT']
    print('Home fouls in home ground = ', homeFoulshome)
    print('away fouls in home ground = ', awayFoulshome)
    print('Home fouls in away ground = ', homeFoulsaway)
    print('away fouls in away ground = ', awayFoulsaway)
    totalFoulsHome = homeFoulshome + homeFoulsaway
    totalFoulsAway = awayFoulshome + awayFoulsaway
    print('Total Fouls done = ', totalFoulsHome)
    print('Total Fouls suffer = ', totalFoulsAway)
    x = pd.DataFrame(barcelona)
    homeShots = 0
    awayShots = 0

    homeShotsOnTarget = 0
    awayShotsOnTarget = 0

    AhomeShots = 0
    AawayShots = 0

    AhomeShotsOnTarget = 0
    AawayShotsOnTarget = 0

    for index, row in x.iterrows():
        homeShots += row['homeShotsTotalFT']
        homeShotsOnTarget += row['homeShotsOnTargetFT']
        awayShots += row['awayShotsTotalFT']
        awayShotsOnTarget += row['awayShotsOnTargetFT']
    x = pd.DataFrame(barcaAway)
    for index, row in x.iterrows():
        AhomeShots += row['awayShotsTotalFT']
        AhomeShotsOnTarget += row['awayShotsOnTargetFT']
        AawayShots += row['homeShotsTotalFT']
        AawayShotsOnTarget += row['homeShotsOnTargetFT']
    print('Home shots attempt on home venue = ', homeShots)
    print('Home shots on target on home venue = ', homeShotsOnTarget)
    print('Away shots attempt on home venue = ', awayShots)
    print('Away shots on target on home venue = ', awayShotsOnTarget)
    print('Home shots attempt on away venue = ', AhomeShots)
    print('Home shots on target on away venue = ', AhomeShotsOnTarget)
    print('Away shots attempt on away venue = ', AawayShots)
    print('Away shots on target on away venue = ', AawayShotsOnTarget)
    x = pd.DataFrame(barcelona.head(50))
    homeOffsides = 0
    awayOffsides = 0
    AhomeOffsides = 0
    AawayOffsides = 0
    totalOffsides = 0
    for index, row in x.iterrows():
        homeOffsides += row['homeOffsidesCaughtFT']
        awayOffsides += row['awayOffsidesCaughtFT']

    x = pd.DataFrame(barcaAway.head(50))
    for index, row in x.iterrows():
        AhomeOffsides += row['awayOffsidesCaughtFT']
        AawayOffsides += row['homeOffsidesCaughtFT']
    print('Home offsides in home venue ', homeOffsides)
    print('Away offsides in home venue ', awayOffsides)
    print('Home offsides in away venue ', AawayOffsides)
    print('Away offsides in away venue ', AhomeOffsides)
    graph_data = plotting('Result on Home Venue', 'Home Team', 'Away Team', 'Draws', cp, cp1, cp2)
    graph_data_1 = plotting('Result on Away Venue', 'Home Team', 'Away Team', 'Draws', aw, al, ad)
    graph_data_2 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    # graph_data_3 = plotting('Matches won', 'Home Team', 'Away Team', 'Draws', cp + aw, cp1 + al, cp2 + ad)
    graph_data_3 = plotting_2('Goals Scored and concede on Home venue', 'Home Goals', 'Away Goals', homegoalsScored,
                              homegoalsconcede)
    graph_data_4 = plotting_2('Goals Scored and concede on Away venue', 'Home Goals', 'Away Goals', awaygoalsScored,
                              awaygoalsconcede)
    graph_data_5 = plotting_2('Total goals Scored and concede ', 'Total Goals Scored', 'Total Goals Concede',
                              totalGoals, totalConcede)
    graph_data_6 = plotting_2('Possesion in home venue ', 'Home Possesion', 'Away Possession',
                              homePossession / count,
                              100 - (homePossession / count))
    # graph_data_6 =plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)
    graph_data_7 = plotting_2('Total Possession ', 'Home Possesion', 'Away Possession',
                              (homePossession + awayPossession) / (count * 2),
                              100 - ((homePossession + awayPossession) / (count * 2)))
    graph_data_8 = plotting_2('Fouls in home venue ', 'Home Fouls', 'Away Fouls', homeFoulshome, awayFoulshome)
    graph_data_9 = plotting_2('Fouls in away venue ', 'Home Fouls', 'Away Fouls', homeFoulsaway, awayFoulsaway)
    graph_data_10 = plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
    graph_data_11 = plotting_2('Offsides  in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides,
                               awayOffsides)
    graph_data_12 = plotting_2('Offsides  in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides,
                               AhomeOffsides)
    return render_template("getafe.html", graph_data=graph_data, graph_data_1=graph_data_1,
                           graph_data_2=graph_data_2, graph_data_3=graph_data_3, graph_data_4=graph_data_4,
                           graph_data_5=graph_data_5, graph_data_6=graph_data_6, graph_data_7=graph_data_7,
                           graph_data_8=graph_data_8, graph_data_9=graph_data_9, graph_data_10=graph_data_10,
                           graph_data_11=graph_data_11, graph_data_12=graph_data_12)
@app.route('/club', methods=['GET'])
def club():
    return render_template('club.html')
"""
@app.route('/compareteams', methods = ['GET'])
def compareteams():
    laliga = pd.read_csv('FootballEurope.csv')
    laliga['winner'] = laliga.apply(
        lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 2 if row['homeGoalFT'] < row['awayGoalFT'] else 0,
        axis=1)
    laliga = laliga[laliga.division == 'La_Liga']
    laliga['local_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] > row['awayGoalFT'] else 0, axis=1)
    laliga['visitor_team_won'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] < row['awayGoalFT'] else 0, axis=1)
    laliga['draw'] = laliga.apply(lambda row: 1 if row['homeGoalFT'] == row['awayGoalFT'] else 0, axis=1)
    ElClassico = laliga
    Barcelona = ElClassico[((ElClassico.homeTeam == 'Barcelona') | (ElClassico.awayTeam == 'Barcelona'))]
    Madrid = ElClassico[((ElClassico.homeTeam == 'Real Madrid') | (ElClassico.awayTeam == 'Real Madrid'))]
    BarcaHome = Barcelona[Barcelona.homeTeam == 'Barcelona']
    BarcaAway = Barcelona[Barcelona.awayTeam == 'Barcelona']
    MadridHome = Madrid[Madrid.homeTeam == 'Real Madrid']
    MadridAway = Madrid[Madrid.awayTeam == 'Real Madrid']

    # In[4]:

    BarcaWins = BarcaHome['local_team_won'].sum() + BarcaAway['visitor_team_won'].sum()
    BarcaLooses = BarcaAway['local_team_won'].sum() + BarcaHome['visitor_team_won'].sum()
    MadridWins = MadridHome['local_team_won'].sum() + MadridAway['visitor_team_won'].sum()
    MadridLooses = MadridAway['local_team_won'].sum() + MadridHome['visitor_team_won'].sum()
    barcahomeGoals = BarcaHome['homeGoalFT'].sum()
    barcaawaygoals = BarcaAway['awayGoalFT'].sum()
    madridhomeGoals = MadridHome['homeGoalFT'].sum()
    madridawaygoals = MadridAway['awayGoalFT'].sum()

    barcaPossesion =  (BarcaAway['homePossessionFT'].sum()/len(laliga)*100) + (BarcaAway['awayPossessionFT'].sum()/len(laliga)*100)
    madridpossesion = (MadridHome['homePossessionFT'].sum()/len(laliga)*100 )+ (MadridAway['awayPossessionFT'].sum()/len(laliga)*100)



    # MadridWins=MadridHome['local_team_won'].sum() + MadridAway['visitor_team_won'].sum()
    BarcaDraws = Barcelona['draw'].sum()
    MadridDraws = Madrid['draw'].sum()
    print('Barcelona win = ', BarcaWins)
    print('Barcelona looses = ', BarcaLooses)
    print('BarcaDraws draws = ', BarcaDraws)
    print('Madrid win = ', MadridWins)
    print('Madrid looses = ', MadridLooses)
    print('Madrid draws = ', MadridDraws)
    graph_data = plotting3('Number of Wins', 'Barcelona', 'RealMadrid', BarcaWins, MadridWins)
    graph_data1 = plotting3('Number of Loses', 'Barcelona', 'RealMadrid', BarcaLooses, MadridLooses)
    graph_data2 = draws('Number of Draws', 'Barcelona', 'RealMadrid', BarcaDraws, MadridDraws)
    graph_data_goals = goals('Number of Aways Goals' , 'Barcelona ' , 'RealMadrid' , barcaawaygoals , madridawaygoals)
    graph_data_homegoals = plotting3('Number of Home Goals', 'Barcelona', 'RealMadrid', barcahomeGoals, madridhomeGoals)
    possesion = goals('Possesion in Percentage %', 'Barcelona', 'RealMadrid', barcaPossesion, madridpossesion)

    return render_template('compare.html', graph_data=graph_data, graph_data1=graph_data1, graph_data2=graph_data2 , graph_data_goals = graph_data_goals , graph_data_homegoals = graph_data_homegoals,possesion = possesion)

"""
if __name__ == "__main__":
    app.run(debug=True)
