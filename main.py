
#Packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from mplsoccer import PyPizza, add_image, FontManager

from scipy import stats
import math
import warnings


hide_github_icon = """
<style>
.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
</style>
"""
st.markdown(hide_github_icon,unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

#Remove Warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
pd.options.mode.chained_assignment = None 

st.markdown('<p style="font-size: 60px; font-weight: bold;">📈 Player Percentile Rank:</p>', unsafe_allow_html=True)
st.markdown('<p style="font-weight:bold; font-size: 20px; color: #808080;">By SaMiR (<a href="https://twitter.com/26RMCFC" target="_blank">Twitter</a>): @26RMCFC</p>', unsafe_allow_html=True)
st.markdown("""---""")


winger_metrics = ['Player', 'Squad', 'True Age', 'Minutes Played', 'Prog Carries', 'Succ. Dribbles', 'Goals & Assists', 'Goals', 'xG', 'Assists', 'xA', 'Key Passes', 'Zone 14 Passes', 'Wide Received', 'Final 1/3 Carries', 'Shots on Target', 'Att Pen Touches', 'Aerial Won']
attacking_midfielder_metrics = ['Player', 'Squad', 'True Age', 'Minutes Played', 'Goals', 'Assists', 'Passes into PA', 'Passes into Final 1/3', 'Key Passes', 'Succ. Dribbles', 'Prog Carries', 'Final 1/3 Carries', 'Att Pen Touches', 'Prog Passes', 'Recoveries', 'Interceptions', 'Tackles', 'Aerial Won', 'Shots on Target']
central_midfielder_metrics = ['Player', 'Squad', 'True Age', 'Minutes Played', 'Goals & Assists', 'Passes into PA', 'Passes into Final 1/3', 'Key Passes', 'Prog Carries', 'Final 1/3 Carries', 'Att Pen Touches', 'Prog Passes', 'Recoveries', 'Clearances', 'Tkl+Int', 'Interceptions', 'Tackles', 'Tkls Won', 'Aerial Won', 'Passes Completed', 'Passes Received']
fullback_metrics = ['Player', 'Squad', 'True Age', 'Minutes Played', 'Tackles', 'Tkls Won', 'Blocks', 'Interceptions', 'Tkl+Int', 'Clearances', 'Recoveries', 'Prog Passes', 'Passes Completed', 'Prog Carries', 'Aerial Won', 'Crosses', 'xA', 'Key Passes']
centre_forward_metrics = ['Player', 'Squad', 'True Age', 'Minutes Played', 'Goals & Assists', 'Goals', 'Shots on Target', 'Goals per SOT', 'xG', 'npxG', 'Assists', 'xA', 'Att Pen Touches', 'Aerial Won', 'Passes Completed', 'Passes Received', 'Passes into PA']
centre_back_metrics = ['Player', 'Squad', 'True Age', 'Minutes Played', 'Tackles', 'Tkls Won', 'Blocks', 'Recoveries', 'Interceptions', 'Tkl+Int', 'Clearances', 'Aerial Won', 'Aerial Lost', 'Passes Completed', 'Passes Received', 'Prog Passes', 'Prog Carries', 'Through Balls', 'Passes into Final 1/3']

# Read The Data
df = pd.read_csv("./resources/data-top-seven.csv")
df = df.loc[~(df['Position'] == 'Goalkeeper')]

# Rename some columns
df.rename(columns = {
    'Tackles Won Possession': 'Tkls Won', 
    'Passes into Penalty Area': 'Passes into PA', 
    'Successful Dribbles': 'Succ. Dribbles', 
    'Passes into Final Third': 'Passes into Final 1/3',
    'Final Third Carries': 'Final 1/3 Carries',
    'Goals per Shot on Target': 'Goals per SOT',
    'Aerial Duels Won': 'Aerial Won',
    'Aerial Duel Lost': 'Aerial Lost'
}, inplace = True)

#######################################################################

with st.sidebar:
    st.markdown('<h1 style="font-family: Consolas; font-size: 34px;">Select Player Here ...</h1>', unsafe_allow_html=True)
    options = df["Player"].dropna().tolist()
    #np.random.shuffle(options)
    player = st.selectbox('Player', options, index=979)

    #print(player)

    st.markdown('<h1 style="font-family: Consolas; font-size: 34px;">And Let The Magic Happen ➡️</h1>', unsafe_allow_html=True)


player_stats = df.loc[(df['Player'] == player)].reset_index()
position = player_stats['Position'][0]

metrics = []

if(position == 'Winger'):
    metrics = winger_metrics

elif (position == 'Full-Back'):
    metrics = fullback_metrics

elif (position == 'Central Midfielder'):
    metrics = central_midfielder_metrics

elif (position == 'Attacking Midfielder'):
    metrics = attacking_midfielder_metrics

elif (position == 'Centre-Forward'):
    metrics = centre_forward_metrics

elif (position == 'Centre-Back'):
    metrics = centre_back_metrics
    
df = df.loc[(df['Position'] == position)]
df = df.filter(items=metrics).reset_index()

params = list(df.columns)
params = params[5:]

player_stats = df.loc[df['Player'] == player].reset_index()
player_stats = list(player_stats.loc[0])
player_general_info = player_stats[2:6]
player_stats = player_stats[6:]

values = []
for x in range(len(params)):
    values.append(math.floor(stats.percentileofscore(df[params[x]], player_stats[x])))


st.markdown(f'<h4>📊 {player} Per 90:</h4>', unsafe_allow_html=True)

# table
df_table = pd.DataFrame(
   [player_stats],
   columns=params)

st.table(df_table.style.format("{:.2f}"))
st.markdown("""---""")


# fonts
font_normal = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/roboto/'
                          'Roboto%5Bwdth,wght%5D.ttf')
font_italic = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/roboto/'
                          'Roboto-Italic%5Bwdth,wght%5D.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                        'RobotoSlab%5Bwght%5D.ttf')

# instantiate PyPizza class
baker = PyPizza(
    params=params,                  # list of parameters
    straight_line_color="#F2F2F2",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=0,               # linewidth of last circle
    other_circle_lw=0,              # linewidth for other circles
)

# plot pizza
fig, ax = baker.make_pizza(
    values,                                      # list of values
    figsize=(8, 8),                              # adjust figsize according to your need
    color_blank_space=["#C5C5C5"]*len(params),   # use same color to fill blank space
    blank_alpha=0.4,                             # alpha for blank-space colors
    kwargs_slices=dict(
        facecolor="cornflowerblue", edgecolor="#F2F2F2",
        zorder=2, linewidth=1
    ),                                           # values to be used when plotting slices
    kwargs_params=dict(
        color="#000000", fontsize=12,
        fontproperties=font_normal.prop, va="center"
    ),                                           # values to be used when adding parameter
    kwargs_values=dict(
        color="#000000", fontsize=12,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )                                            # values to be used when adding parameter-values
)

# add title
fig.text(
    0.515, 0.97, f"{player_general_info[0]}, {player_general_info[2]} - {player_general_info[1]}", size=22,
    ha="center", fontfamily='DejaVu Sans', fontweight='bold', color="black"
)

# add subtitle
fig.text(
    0.515, 0.94,
    f"Per 90 Percentile Rank | {position} Template | {player_general_info[3]} Minutes Played",
    size=10,
    ha="center", fontfamily='DejaVu Sans', color="black"
)

# add credits
CREDIT_1 = "Data: Opta"
CREDIT_2 = "By: @26RMCFC"

fig.text(
    0.82, 0.005, f"Top 7 European Leagues Players with 1080+ Minutes Included | {CREDIT_1} | {CREDIT_2}", size=9,
    fontproperties=font_italic.prop, color="#000000",
    ha="right"
)

st.pyplot(fig)
