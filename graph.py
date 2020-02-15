import pygal
from pygal.style import Style
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import io
import random


custom_style = Style(
    legend_font_size=22.0,
    value_font_size=22.0,
    tooltip_font_size=22.0,
    major_label_font_size=22.0,
    label_font_sioze=22.0, plot_background='#f9f9f9',
    value_label_font_size=22.0,
    title_font_size=28.0,
    colors=('#0ba0e5', '#e8102d', '#df34f9'))

custom_style1 = Style(
    legend_font_size=22.0,
    value_font_size=22.0,
    tooltip_font_size=22.0,
    major_label_font_size=22.0,
    label_font_sioze=22.0, plot_background='#f9f9f9',
    value_label_font_size=22.0,
    title_font_size=28.0,
    colors=('#e80410', '#55e800', '#17d117'))

custom_style2 = Style(
    legend_font_size=22.0,
    value_font_size=22.0,
    tooltip_font_size=22.0,
    major_label_font_size=22.0,
    label_font_sioze=22.0, plot_background='#f9f9f9',
    value_label_font_size=22.0,
    title_font_size=28.0,
    colors=('#0ace1b', '#0a66fc', '#df34f9'))

custom_style3 = Style(
    legend_font_size=22.0,
    value_font_size=22.0,
    tooltip_font_size=22.0,
    major_label_font_size=22.0,
    label_font_sioze=22.0, plot_background='#f9f9f9',
    value_label_font_size=22.0,
    title_font_size=28.0,
    colors=('#606060', '#00afa4', '#df34f9'))

def bar_chart_1(df):
    df=df.head(10)
    for index,row in df.iterrows():
        if row['ratings']<0:
            df.iloc[index, df.columns.get_loc('ratings')]*= -1
    df=df.sort_values('ratings',ascending=False)
    line_chart = pygal.Bar()
    line_chart.title = 'ELO Ranking'
    team_elo_rating=df.ratings
    clubs=df.club

    for rat,club in zip(team_elo_rating,clubs):
        #print(rat,club)
        line_chart.add(club,rat)
    return line_chart.render_data_uri()
def bar_chart_2(df2):
    df2=df2.head(10)
    line_chart = pygal.Bar()
    line_chart.title = 'Teams rank by dataset'
#line_chart.x_labels = map(str, range(2002, 2013))
    temp=df2.club.unique()
#temp.sort()
    for i in temp:
    #line_chart.add(i,[(df2[df2.club==i].home_win.sum()),(df2[df2.club==i].away_win.sum())])
    #line_chart.add(i+'_Home',[(df2[df2.club==i].matches_won.sum())])
    
    #line_chart.add(i+'_Away',[(df2[df2.club==i].home_win.sum())])
        line_chart.add(i,[(df2[df2.club==i].points.sum())])
    
    return line_chart.render_data_uri()

def transformResultBack(row,col_name):
    if(row[col_name] == 1):
        return 'HomeTeamWins'
    elif(row[col_name] == -1):
        return 'AwayTeamWins'
    else:
        return 'Draw'
def returnTeam(row,col_name):
    if(row[col_name] == 'HomeTeamWins'):
        return row['HomeTeam']
    elif(row[col_name] == 'AwayTeamWins'):
        return row['AwayTeam']
    else:
        return 'Draw'

def plotting(title, arg1, arg2, arg3, val1, val2, val3):
    pie_chart = pygal.Pie(half_pie=True, style=custom_style)
    pie_chart.title = title
    pie_chart.add(arg1, val1)
    pie_chart.add(arg2, val2)
    pie_chart.add(arg3, val3)
    return pie_chart.render_data_uri()
def plotting_pred(title, arg1, arg2, arg3, val1, val2, val3):
    pie_chart = pygal.Pie(inner_radius=.6,half_pie=True, style=custom_style)
    pie_chart.title = title
    pie_chart.add(arg1, val1)
    pie_chart.add(arg2, val2)
    pie_chart.add(arg3, val3)
    return pie_chart.render_data_uri()

def plotting3(title, arg1, arg2, val1, val2, ):
    pie_chart = pygal.HorizontalBar(style=custom_style1)
    pie_chart.title = title
    pie_chart.add(arg1, val1)
    pie_chart.add(arg2, val2)
    return pie_chart.render_data_uri()

def draws(title, arg1, arg2, val1, val2, ):
    pie_chart = pygal.Gauge(human_readable=True, style = custom_style2)
    pie_chart.title = title
    pie_chart.range = [20, 30]
    pie_chart.add(arg1, val1)
    pie_chart.add(arg2, val2)
    return pie_chart.render_data_uri()

def goals(title, arg1 , arg2, val1, val2):
    pie_chart = pygal.Pie(style=custom_style3)
    pie_chart.title = title
    pie_chart.add(arg1, val1)
    pie_chart.add(arg2, val2)
    return pie_chart.render_data_uri()


def plotting_2(title, arg1, arg2, val1, val2):
    pie_chart = pygal.Pie(inner_radius=.3, style=custom_style2)
    pie_chart.title = title
    pie_chart.add(arg1, val1)
    pie_chart.add(arg2, val2)
    return pie_chart.render_data_uri()

def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



# plotting('Wins, looses and Draws on home venue','Home Team','Away Team','Draws',cp,cp1,cp2)
# plotting('Wins, looses and Draws on away venue','Home Team','Away Team','Draws',aw,al,ad)
# plotting('Total Wins, looses and Draws','Home Team','Away Team','Draws',cp+aw,cp1+al,cp2+ad)
# plotting_2('Goals Scored and concede on home venue','Home Goals','Away Goals',homegoalsScored,homegoalsconcede)
# plotting_2('Goals Scored and concede on away venue','Home Goals','Away Goals',awaygoalsScored,awaygoalsconcede)
# plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)
# plotting_2('Total goals Scored and concede ','Total Goals Scored','Total Goals Concede',totalGoals,totalConcede)
# plotting_2('Possesion by home team in home venue ','Home Possesion','Away Possession',homePossession/count,100-(homePossession/count))
# plotting_2('Total Possession ','Home Possesion','Away Possession',(homePossession+awayPossession)/(count*2),100-((homePossession+awayPossession)/(count*2)))
# plotting_2('Fouls by home team in home venue ','Home Fouls','Away Fouls',homeFoulshome,awayFoulshome)
# plotting_2('Fouls by home team in away venue ','Home Fouls','Away Fouls',homeFoulsaway,awayFoulsaway)
# plotting_2('Total Fouls ', 'Home Fouls', 'Away Fouls', totalFoulsHome, totalFoulsAway)
# plotting_2('Offsides by home team in home venue ', 'homeOffsides', 'awayOffsides', homeOffsides, awayOffsides)
# plotting_2('Offsides by home team in away venue ', 'homeOffsides', 'awayOffsides', AawayOffsides, AhomeOffsides)
