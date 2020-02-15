
# coding: utf-8

# In[1]:



"""

Div = League Division
Date = Match Date (dd/mm/yy)
HomeTeam = Home Team
AwayTeam = Away Team
FTHG and HG = Full Time Home Team Goals
FTAG and AG = Full Time Away Team Goals
FTR and Res = Full Time Result (H=Home Win, D=Draw, A=Away Win)
HTHG = Half Time Home Team Goals
HTAG = Half Time Away Team Goals
HTR = Half Time Result (H=Home Win, D=Draw, A=Away Win)

Match Statistics (where available)
Attendance = Crowd Attendance
Referee = Match Referee
HS = Home Team Shots
AS = Away Team Shots
HST = Home Team Shots on Target
AST = Away Team Shots on Target
HHW = Home Team Hit Woodwork
AHW = Away Team Hit Woodwork
HC = Home Team Corners
AC = Away Team Corners
HF = Home Team Fouls Committed
AF = Away Team Fouls Committed
HFKC = Home Team Free Kicks Conceded
AFKC = Away Team Free Kicks Conceded
HO = Home Team Offsides
AO = Away Team Offsides
HY = Home Team Yellow Cards
AY = Away Team Yellow Cards
HR = Home Team Red Cards
AR = Away Team Red Cards


"""
from __future__ import division
import pandas as pd
import numpy as np
import scipy.stats as scipy
import seaborn as sns
def transformResult(row):
    '''Converts results (H,A or D) into numeric values'''
    if(row.FTR == 'H'):
        return 1
    elif(row.FTR == 'A'):
        return -1
    else:
        return 0
def transformResultBack(row,col_name):
    if(row[col_name] == 1):
        return 'H'
    elif(row[col_name] == -1):
        return 'A'
    else:
        return 'D'


def pred():
    
    df = pd.read_csv('SP1.csv')
    pd.set_option("max_column",100)
    pd.set_option("max_row",100)
    df.head()


# In[4]:


    spain_df = df.iloc[:,:22] # Dropping the betting odds because we don't need it for Prediction 
    spain_df = spain_df.drop(['Div','Date'],axis=1)
    spain_df.head()


# In[5]:


    table_features = df.iloc[:,:6]
    table_features.head()


# In[6]:


    table_features = table_features.drop(['FTHG','FTAG','Div','Date'],axis=1)
    table_features.tail()


# In[7]:


    bet_16 = df.iloc[:,22:]
    bet_16.head()


# In[8]:


    spain_df.tail(2)


# In[9]:


    feature_table = df.iloc[:,:22]
    feature_table = feature_table.drop(['Date', 'Div'],axis=1)
    feature_table.head()


# In[10]:


    feature_table.shape


# In[11]:


#Team, Home Goals Score, Away Goals Score, Attack Strength, Home Goals Conceded, Away Goals Conceded, Defensive Strength
    table_16 = pd.DataFrame(columns=('Team','HGS','AGS','HAS','AAS','HGC','AGC','HDS','ADS',))
    table_16 = table_16[:-10]
    table_16.head()


# In[12]:


    spain_df = spain_df[:-10]
    spain_df.shape[0]


# In[13]:


    avg_home_scored = spain_df.FTHG.sum()*1.0 / spain_df.shape[0]
    avg_away_scored = spain_df.FTAG.sum()*1.0 / spain_df.shape[0]
    avg_home_conceded = avg_away_scored
    avg_away_conceded = avg_home_scored
    print("Average number of goals at home:",avg_home_scored)
    print("Average number of goals away:", avg_away_scored)
    print("Average number of goals conceded at home:",avg_home_conceded)
    print("Average number of goals conceded away:",avg_away_conceded)


# YAHA SY PROBLEM AE GI DEKHI

# In[14]:


    _home = spain_df.groupby('HomeTeam')
    _away = spain_df.groupby('AwayTeam')


# In[15]:


    table_16.Team = _home.HomeTeam.all().index
    table_16.HGS = _home.FTHG.sum().values
    table_16.HGC = _home.FTAG.sum().values
    table_16.AGS = _away.FTAG.sum().values
    table_16.AGC = _away.FTHG.sum().values


# In[16]:


#Assuming number of home games = number of away games
    num_games = spain_df.shape[0]/20


# In[17]:


    table_16.HAS = (table_16.HGS / num_games) / avg_home_scored
    table_16.AAS = (table_16.AGS / num_games) / avg_away_scored
    table_16.HDS = (table_16.HGC / num_games) / avg_home_conceded
    table_16.ADS = (table_16.AGC / num_games) / avg_away_conceded
    table_16


# In[18]:


    has_plot = sns.barplot(table_16.Team,table_16.HAS)
    for item in has_plot.get_xticklabels():
        item.set_rotation(90)


# In[19]:


    has_plot = sns.barplot(table_16.Team,table_16.AAS)
    for item in has_plot.get_xticklabels():
        item.set_rotation(90)


# In[20]:


    table_16[table_16.Team == "Real Madrid"]


# In[21]:


''' feature_table contains all the fixtures in the current season.
ftr = full time result
hst = home shots on target
ast = away shots on target
'''

    feature_table = feature_table[['HomeTeam','AwayTeam','FTR','HST','AST']]
        f_HAS = []
        f_HDS = []
        f_AAS = []
        f_ADS = []
    for index,row in feature_table.iterrows():
        f_HAS.append(table_16[table_16['Team'] == row['HomeTeam']]['HAS'].values[0])
        f_HDS.append(table_16[table_16['Team'] == row['HomeTeam']]['HDS'].values[0])
        f_AAS.append(table_16[table_16['Team'] == row['AwayTeam']]['AAS'].values[0])
        f_ADS.append(table_16[table_16['Team'] == row['AwayTeam']]['ADS'].values[0])
    
    feature_table['HAS'] = f_HAS
    feature_table['HDS'] = f_HDS
    feature_table['AAS'] = f_AAS
    feature_table['ADS'] = f_ADS


# In[22]:


    feature_table.head(20)


# In[23]:





# In[24]:


    feature_table["Result"] = feature_table.apply(lambda row: transformResult(row),axis=1)


# In[25]:


    feature_table = feature_table[:-10] #ONLY FOR WEEK 33. REMOVE FROM 34
    feature_table.tail(10)


# In[26]:


    Feautre_train = feature_table[['HST','AST','HAS','HDS','AAS','ADS',]]
    Label_train = feature_table['Result']


# In[27]:


    from sklearn.tree import DecisionTreeClassifier
    from sklearn.naive_bayes import MultinomialNB
    from xgboost import XGBClassifier
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import cross_val_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble import voting_classifier
    from sklearn.svm import LinearSVC


# In[28]:


    clf1 = RandomForestClassifier()
    clf2 = MultinomialNB()
    clf3 = XGBClassifier()
    clf4 = LinearSVC()


# In[29]:


    label_pred = clf4.fit(Feautre_train,Label_train).predict(Feautre_train)
    accuracy_score(label_pred,Label_train)
    scores = cross_val_score(clf1, Feautre_train, Label_train, cv=100)
    print(scores)
    print(scores.mean())


# In[30]:


    label_pred = clf1.fit(Feautre_train,Label_train).predict(Feautre_train)
    accuracy_score(label_pred,Label_train)
    scores = cross_val_score(clf1, Feautre_train, Label_train, cv=100)
    print(scores)
    print(scores.mean())


# In[31]:


    label_pred = clf2.fit(Feautre_train,Label_train).predict(Feautre_train)
    accuracy_score(label_pred,Label_train)
    scores = cross_val_score(clf1, Feautre_train, Label_train, cv=100)
    print(scores)
    print(scores.mean())


# In[32]:


    label_pred = clf4.fit(Feautre_train,Label_train).predict(Feautre_train)
    accuracy_score(label_pred,Label_train)
    scores = cross_val_score(clf1, Feautre_train, Label_train, cv=100)
    print(scores)
    print(scores.mean())


# In[33]:


    label_pred = clf3.fit(Feautre_train,Label_train).predict(Feautre_train)
    accuracy_score(label_pred,Label_train)
    scores = cross_val_score(clf1, Feautre_train, Label_train, cv=100)
    print(scores)
    print(scores.mean())


# In[34]:


#ADDING RECENT PERFORMNACE
    ht = spain_df.loc[40].HomeTeam
    at = spain_df.loc[40].AwayTeam


# In[35]:


    feat_table = spain_df.sort_index(ascending=False)
    feat_table = feat_table[['HomeTeam','AwayTeam','FTR','FTHG','FTAG','HS','AS','HC','AC']]


# In[36]:


    new_fixtures = pd.DataFrame( [['La Coruna','Malaga','D',0,0,0,0,0,0],
                                ['Barcelona','Sevilla','D',0,0,0,0,0,0],
                             ['Ath Madrid', 'Sociedad','D',0,0,0,0,0,0],
                             ['Granada','Villarreal','D',0,0,0,0,0,0],
                             ['Sp Gijon', 'Celta','D',0,0,0,0,0,0],
                             ['Valencia', 'Betis','D',0,0,0,0,0,0],
                             ['Espanol', 'Eibar','D',0,0,0,0,0,0],
                             ['Leganes', 'Osasuna','D',0,0,0,0,0,0],
                             ['Real Madrid', 'Alaves','D',0,0,0,0,0,0],
                             ['Ath Bilbao', 'Las Palmas','D',0,0,0,0,0,0]],columns=feat_table.columns)


# In[37]:


    new_feat_table = new_fixtures.append(feat_table,ignore_index=True)
    new_feat_table = new_feat_table.sort_index(ascending=False)
    new_feat_table = new_feat_table.reset_index().drop(['index'], axis=1)
    new_feat_table = new_feat_table.sort_index(ascending=False)
# feat_table = n
    feat_table = new_feat_table
    feat_table.shape


# In[38]:


#Adding k recent performance measures
    feat_table["pastHS"] = 0.0
    feat_table["pastHC"] = 0.0
    feat_table["pastAS"] = 0.0
    feat_table["pastAC"] = 0.0
    feat_table["pastHG"] = 0.0
    feat_table["pastAG"] = 0.0


# In[39]:


    feat_table.head(5)


# In[40]:


# Adding k recent performance metrics. Change value of k.
    k = 3
    for i in range(feat_table.shape[0]-1,-1,-1):
        row = feat_table.loc[i]
        ht = row.HomeTeam
        at = row.AwayTeam
        ht_stats = feat_table.loc[i-1:-1][(feat_table.HomeTeam == ht) | (feat_table.AwayTeam == ht)].head(k)
        at_stats = feat_table.loc[i-1:-1][(feat_table.HomeTeam == at) | (feat_table.AwayTeam == at)].head(k)

        feat_table.set_value(i, 'pastHC', (ht_stats[ht_stats["AwayTeam"] == ht].sum().HC + ht_stats[ht_stats["HomeTeam"] == ht].sum().HC)/k)
        feat_table.set_value(i, 'pastAC', (at_stats[at_stats["AwayTeam"] == at].sum().HC + at_stats[at_stats["HomeTeam"] == at].sum().HC)/k)
        feat_table.set_value(i, 'pastHS', (ht_stats[ht_stats["AwayTeam"] == ht].sum().HS + ht_stats[ht_stats["HomeTeam"] == ht].sum().AS)/k)
        feat_table.set_value(i, 'pastAS', (at_stats[at_stats["AwayTeam"] == at].sum().HS + at_stats[at_stats["HomeTeam"] == at].sum().AS)/k)
        feat_table.set_value(i, 'pastHG', (ht_stats[ht_stats["AwayTeam"] == ht].sum().FTAG + ht_stats[ht_stats["HomeTeam"] == ht].sum().FTHG)/k)
        feat_table.set_value(i, 'pastAG', (at_stats[at_stats["AwayTeam"] == at].sum().FTAG + at_stats[at_stats["HomeTeam"] == at].sum().FTHG)/k)

    f_HAS = []
    f_HDS = []
    f_AAS = []
    f_ADS = []
    for index,row in feat_table.iterrows():
    #print row
        f_HAS.append(table_16[table_16['Team'] == row['HomeTeam']]['HAS'].values[0])
        f_HDS.append(table_16[table_16['Team'] == row['HomeTeam']]['HDS'].values[0])
        f_AAS.append(table_16[table_16['Team'] == row['HomeTeam']]['AAS'].values[0])
        f_ADS.append(table_16[table_16['Team'] == row['HomeTeam']]['ADS'].values[0])
    
    feat_table['HAS'] = f_HAS
    feat_table['HDS'] = f_HDS
    feat_table['AAS'] = f_AAS
    feat_table['ADS'] = f_ADS


# In[41]:


    test_table = feat_table.drop(['FTHG','FTAG','HS','AS','HC','AC'],axis=1)


# In[42]:


    test_table["Result"] = test_table.apply(lambda row: transformResult(row),axis=1)
    test_table.sort_index(inplace=True)


# In[43]:


# num_games decides the train-test split
    print(feat_table.shape)
    num_games = feat_table.shape[0]-10
    num_games


# In[44]:


    Feautre_train = test_table[['pastHS','pastHC','pastAS','pastAC','pastHG','pastAG','HAS','HDS','AAS','ADS']].loc[0:num_games]
    Label_train = test_table['Result'].loc[0:num_games]
    Feautre_test = test_table[['pastHS','pastHC','pastAS','pastAC','pastHG','pastAG','HAS','HDS','AAS','ADS']].loc[num_games:]
    Label_test = test_table['Result'].loc[num_games:]


# ADDING HOME ADVANTAGE 

# In[77]:


    test_table["pastCornerDiff"] = (test_table["pastHC"] - test_table["pastAC"])/k
    test_table["pastGoalDiff"] = (test_table["pastHG"] - test_table["pastAG"])/k
    test_table["pastShotsDiff"] = (test_table["pastHS"] - test_table["pastAG"])/k


# In[78]:


''' number of games to exclude in the training set for validation
For example, if 240 games have been played, test_table has 250 fixtures - the last 10 being the ones that haven't
been played. So, we set aside 20 fixtures from the training set containing 240 fixtures for validation.''' 
    num_games = feat_table.shape[0]-10
    print(num_games)
    v_split = 15
    n_games = num_games - v_split


# In[79]:


    test_table = test_table.fillna(0)


# In[80]:


    test_table.head()


# In[81]:


    test_table.drop(['pastHC','pastAS','pastAC','pastHG','pastAG'],axis=1)
    Feautre_train = test_table[['pastCornerDiff','pastGoalDiff','pastShotsDiff','HAS','HDS','AAS','ADS']].loc[0:n_games]
    Label_train = test_table['Result'].loc[0:n_games]
    Feautre_test = test_table[['pastCornerDiff','pastGoalDiff','pastShotsDiff','HAS','HDS','AAS','ADS']].loc[n_games:num_games-1]
    Label_test = test_table['Result'].loc[n_games:num_games-1]
    Feautre_predict = test_table[['pastCornerDiff','pastGoalDiff','pastShotsDiff','HAS','HDS','AAS','ADS']].loc[num_games:]


# In[83]:


    Feautre_predict


# In[84]:


#KNN
    plot_scores_knn = []
    for b in range(1,50):
        clf_knn = KNeighborsClassifier(n_neighbors=b)
        clf_knn.fit(Feautre_train,Label_train)
        scores = accuracy_score(Label_test,clf_knn.predict(Feautre_test))
        plot_scores_knn.append(scores)

#XGBClassifier
    plot_scores_XGB = []
    for i in range(1,100):
        clf_XGB = XGBClassifier(n_estimators=i,max_depth=100)
        clf_XGB.fit(Feautre_train, Label_train)
        scores = accuracy_score(Label_test,clf_XGB.predict(Feautre_test))
        plot_scores_XGB.append(scores)
    
#Logistic Regression
    plot_scores_logreg= []
    cs = [0.01,0.02,0.1,0.5,1,3,4,5,10]
    for c in cs:
        clf_logreg = LogisticRegression(C=c,solver='lbfgs',multi_class='ovr')
        clf_logreg.fit(Feautre_train, Label_train)
        scores = accuracy_score(Label_test,clf_logreg.predict(Feautre_test))
        plot_scores_logreg.append(scores)


# In[86]:


    import matplotlib.pyplot as plt

    fig = plt.figure(figsize = (16,7))

    ax1 = fig.add_subplot(1,3,1)
    ax1.plot(range(1,50),plot_scores_knn);
    ax1.set_title("KNN - Accuracy vs N")
    ax1.set_xticks(range(1,50,5));

    ax2 = fig.add_subplot(1,3,2)
    ax2.plot(range(1,100),plot_scores_XGB);
    ax2.set_xticks(range(1,100,6));
    ax2.set_title("XGB - Accuracy vs n_estimators")

    ax3 = fig.add_subplot(1,3,3)
    ax3.plot(range(1,10),plot_scores_logreg);
    ax3.set_xticks(range(1,10));
    ax3.set_title("Logistic Regression - Accuracy vs C")

    fig.tight_layout()


# In[87]:


    max_knn_n = max(plot_scores_knn)
    max_knn_ind = plot_scores_knn.index(max_knn_n)

    max_XGB_e = max(plot_scores_XGB)
    max_XGB_ind = plot_scores_XGB.index(max_XGB_e) if plot_scores_XGB.index(max_XGB_e)!=0 else 1

    max_logreg_c = max(plot_scores_logreg)
    max_logreg_ind = plot_scores_logreg.index(max_logreg_c)

    print(max_knn_n, max_knn_ind)
    print(max_XGB_e, max_XGB_ind)
    print(max_logreg_c, max_logreg_ind)

#max_knn_ind=15 
#max_XGB_ind=40
#max_logreg_ind=3


# In[88]:


    clf_knn = KNeighborsClassifier(n_neighbors=max_knn_ind).fit(Feautre_train,Label_train)
    clf_XGB = XGBClassifier(n_estimators=max_XGB_ind).fit(Feautre_train,Label_train)
    clf_logreg = LogisticRegression(C=max_logreg_ind,solver='lbfgs',multi_class='ovr').fit(Feautre_train,Label_train)


# In[89]:


    y_pred_knn = clf_knn.predict(Feautre_predict)
    y_pred_XGB = clf_XGB.predict(Feautre_predict)
    y_pred_logreg = clf_logreg.predict(Feautre_predict)


# In[90]:


    this_week = test_table[['HomeTeam','AwayTeam']].loc[num_games:]
    this_week['Result_knn']=y_pred_knn
    this_week['Result_XGB']=y_pred_XGB
    this_week['Result_logreg']=y_pred_logreg


# In[91]:


    return this_week


# In[92]:




# In[93]:


this_week["Res_knn"] = this_week.apply(lambda row: transformResultBack(row,"Result_knn"),axis=1)
this_week["Res_XGB"] = this_week.apply(lambda row: transformResultBack(row,"Result_XGB"),axis=1)
this_week["Res_logreg"] = this_week.apply(lambda row: transformResultBack(row,"Result_logreg"),axis=1)

this_week.drop(["Result_knn", "Result_XGB","Result_logreg"],axis=1,inplace=True)


# In[94]:


print(max_knn_n, max_XGB_e, max_logreg_c)
this_week

