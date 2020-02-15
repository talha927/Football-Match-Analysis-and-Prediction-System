
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def teamranking(a1,a2,a3,a4,a5,a6):
    df = pd.read_csv('BestTeams.csv')
    pd.set_option("max_column",100) 
    pd.set_option("max_row",100)

    df=df.drop(['Unnamed: 0'],axis=1)
    df = df.iloc[:,:7]
    df['local_team_won']=df.apply(lambda row: 1 if row['FTHG']>row['FTAG'] else 0,axis=1)
    df['visitor_team_won']=df.apply(lambda row: 1 if row['FTHG']<row['FTAG'] else 0,axis=1)
    df['draw']=df.apply(lambda row: 1 if row['FTHG']==row['FTAG'] else 0,axis=1)
    a=df.groupby(['HomeTeam'])['local_team_won'].sum().reset_index().rename(columns={'HomeTeam': 'club','local_team_won': 'won'})
    b=df.groupby(['AwayTeam'])['visitor_team_won'].sum().reset_index().rename(columns={'AwayTeam': 'club','visitor_team_won': 'won'})
    c=df.groupby(['HomeTeam'])['draw'].sum().reset_index().rename(columns={'HomeTeam': 'club','draw': 'draw'})
    d=df.groupby(['AwayTeam'])['draw'].sum().reset_index().rename(columns={'AwayTeam': 'club','draw': 'draw'})
    e=df.groupby(['HomeTeam'])['visitor_team_won'].sum().reset_index().rename(columns={'HomeTeam': 'club','visitor_team_won': 'lost'})
    f=df.groupby(['AwayTeam'])['local_team_won'].sum().reset_index().rename(columns={'AwayTeam': 'club','local_team_won': 'lost'})
    point_table=a.merge(b,on=['club']).merge(c,on=['club']).merge(d,on=['club']).merge(e,on=['club']).merge(f,on=['club'])
#won_x Win in home Ground
    point_table= point_table.rename(columns={'won_x':'home_win','won_y':'away_win','lost_x':'home_loss','lost_y':'away_loss'})
    point_table['matches_won']=point_table.home_win+point_table.away_win
    point_table['matches_lost']=point_table.home_loss+point_table.away_loss
    point_table['matches_drawn']=point_table.draw_x+point_table.draw_y
    point_table=point_table.drop(['draw_x','draw_y'],axis=1)
    point_table['total_matches']=point_table.matches_won+point_table.matches_lost+point_table.matches_drawn


    point_table['points']=(point_table.matches_won*3)+(point_table.matches_drawn*1)

    g=df.groupby(['HomeTeam'])['FTHG'].sum().reset_index().rename(columns={'HomeTeam': 'club','FTHG': 'home_goals'})
    h=df.groupby(['AwayTeam'])['FTAG'].sum().reset_index().rename(columns={'AwayTeam': 'club','FTAG': 'away_goals'})
    i=df.groupby(['HomeTeam'])['FTAG'].sum().reset_index().rename(columns={'HomeTeam': 'club','FTAG': 'goals_conceded'})
    j=df.groupby(['AwayTeam'])['FTHG'].sum().reset_index().rename(columns={'AwayTeam': 'club','FTHG': 'goals_conceded'})



    point_table=point_table.merge(g,on=['club']).merge(h,on=['club']).merge(i,on=['club']).merge(j,on=['club'])


    point_table['goals_scored']=point_table.home_goals+point_table.away_goals
    point_table['goals_conceded']=point_table.goals_conceded_x+point_table.goals_conceded_y
    point_table['goal_difference']=point_table.goals_scored-point_table.goals_conceded
    point_table= point_table.drop(['goals_conceded_x','goals_conceded_y'],axis=1)


# In[69]:


    point_table= point_table.sort_values(by=['points','goal_difference']).reset_index   ().drop('index',axis=1)


# In[75]:


    point_table.tail(n=20).sort_values('points',ascending=False)
    point_table['season'] = 5



# In[76]:


    df2=point_table.copy()


# In[80]:


    fig1 = df2.groupby(['club'])['home_win'].sum().sort_values(ascending=False).head(20).plot(kind='bar',figsize=(20,8))


# In[82]:


    fig2 = df2.groupby(['club'])['matches_won'].sum().sort_values(ascending=False).head(20).plot(kind='bar',figsize=(20,8))


# In[84]:


    fig3 = df2.groupby(['club'])['goals_scored'].sum().sort_values(ascending=False).head(10).plot(kind='bar', figsize=(20,8))


# In[85]:


    w=df2.groupby(['club'])['home_goals'].sum().sort_values(ascending=False).head(20).reset_index()
    x=df2.groupby(['club'])['away_goals'].sum().sort_values(ascending=False).head(20).reset_index()
    y=df2.groupby(['club'])['goals_scored'].sum().sort_values(ascending=False).head(20).reset_index()
    z=w.merge(x,on=['club']).merge(y,on=['club'])
    a=df2.groupby(['club'])['home_win'].sum().sort_values(ascending=False).head(20).reset_index()
    b=df2.groupby(['club'])['away_win'].sum().sort_values(ascending=False).head(20).reset_index()
    c=df2.groupby(['club'])['matches_won'].sum().sort_values(ascending=False).head(20).reset_index()
    z=a.merge(b,on=['club']).merge(c,on=['club']).merge(z,on=['club'])


    # In[86]:


    fig4 = z.plot(x='club',y=['home_goals','away_goals','goals_scored'], kind="bar",figsize=(15,8))




    fig5 = sns.FacetGrid(z, hue="club", size=8).map(plt.scatter, "goals_scored", "matches_won").add_legend()

    fig6 = z.plot(x='club',y=['home_win','away_win','matches_won'], kind="barh",figsize=(15,10))

    return fig1,fig2,fig3,fig4,fig5,fig6 



