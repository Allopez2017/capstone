import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px


conn = sqlite3.connect("world_series.db")
df = pd.read_sql_query("SELECT * FROM world_series", conn)
conn.close()


st.title("World Series Team Dashboard")
team_list = sorted(df["winner"].dropna().unique())
selected_team = st.sidebar.selectbox("Select a team:", team_list)


team_df = df[df["winner"] == selected_team].sort_values("year")
st.header(f"Wins for {selected_team}")
st.dataframe(team_df.reset_index(drop=True))
st.markdown(f"**Total Wins:** {len(team_df)}")


team_df["Cumulative Wins"] = range(1, len(team_df) + 1)
fig1 = px.line(team_df, x="year", y="Cumulative Wins", title=f"{selected_team} Cumulative Wins")
st.plotly_chart(fig1)


win_counts = df["winner"].value_counts().reset_index()
win_counts.columns = ["Team", "Wins"]
fig2 = px.bar(win_counts, x="Team", y="Wins", title="Total Wins by Team")
st.plotly_chart(fig2)


top5 = win_counts.head(5)
others = pd.DataFrame([["Other Teams", win_counts["Wins"].sum() - top5["Wins"].sum()]], columns=["Team", "Wins"])
pie_df = pd.concat([top5, others])
fig3 = px.pie(pie_df, names="Team", values="Wins", title="Top 5 Teams Win Share")
st.plotly_chart(fig3)

