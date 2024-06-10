import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
import matplotlib.font_manager as fm

from pingouin import ttest
from plotly.subplots import make_subplots

def Navy(total_df):
  st.markdown('## 해군 입영부대 접수인원 건수 추세 \n')

  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format=('%Y%m'))
  total_df['month'] = total_df['iyyjsijakYm'].dt.month


  filterd_df = total_df[total_df['gunGbnm'] == '해군']
  filterd_df = filterd_df[filterd_df['iyyjsijakYm'].between('2024-05', '2024-12')]

  result = filterd_df.groupby(['month','iybudaeCdm'])['gunGbnm'].count()
  
  bar_df = filterd_df.groupby(['month','iybudaeCdm'])['gunGbnm'].agg('count').reset_index()
  df_sorted = bar_df.sort_values('gunGbnm', ascending=False)

  # 바 차트 만들기
  fig = px.bar(df_sorted, x='month', y='gunGbnm')

  # update Layout
  fig.update_yaxes(tickformat='.0f',
                  title_text = '접수 인원 개수',
                  range=[0, bar_df['gunGbnm'].max()])
  fig.update_layout(title='Bar Chart - 오름차순',
                    xaxis_title='날짜',
                    yaxis_title='접수 인원')
  

  st.dataframe(result, use_container_width=True)
  st.plotly_chart(fig)

def Army(total_df):
  st.markdown('## 육군 입영부대 접수인원 건수 추세 \n')

  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format=('%Y%m'))
  total_df['month'] = total_df['iyyjsijakYm'].dt.month


  filterd_df = total_df[total_df['gunGbnm'] == '육군']
  filterd_df = filterd_df[filterd_df['iyyjsijakYm'].between('2024-05', '2024-12')]

  result = filterd_df.groupby(['month','iybudaeCdm'])['gunGbnm'].count()
  bar_df = filterd_df.groupby(['month','iybudaeCdm'])['gunGbnm'].agg('count').reset_index()
  df_sorted = bar_df.sort_values('gunGbnm', ascending=False)

  # 바 차트 만들기
  fig = px.bar(df_sorted, x='month', y='gunGbnm')

  # update Layout
  fig.update_yaxes(tickformat='.0f',
                  title_text = '접수 인원 개수',
                  range=[0, bar_df['gunGbnm'].max()])
  fig.update_layout(title='Bar Chart - 오름차순',
                    xaxis_title='날짜',
                    yaxis_title='접수 인원')
  

  st.dataframe(result, use_container_width=True)
  st.plotly_chart(fig)

def Marine(total_df):
  st.markdown('## 해병 입영부대 접수인원 건수 추세 \n')

  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format=('%Y%m'))
  total_df['month'] = total_df['iyyjsijakYm'].dt.month


  filterd_df = total_df[total_df['gunGbnm'] == '해병']
  filterd_df = filterd_df[filterd_df['iyyjsijakYm'].between('2024-05', '2024-12')]

  result = filterd_df.groupby(['month','iybudaeCdm'])['gunGbnm'].count()
  bar_df = filterd_df.groupby(['month','iybudaeCdm'])['gunGbnm'].agg('count').reset_index()
  df_sorted = bar_df.sort_values('gunGbnm', ascending=False)

  # 바 차트 만들기
  fig = px.bar(df_sorted, x='month', y='gunGbnm')

  # update Layout
  fig.update_yaxes(tickformat='.0f',
                  title_text = '접수 인원 개수',
                  range=[0, bar_df['gunGbnm'].max()])
  fig.update_layout(title='Bar Chart - 오름차순',
                    xaxis_title='날짜',
                    yaxis_title='접수 인원')
  

  st.dataframe(result, use_container_width=True)
  st.plotly_chart(fig)

def airforce(total_df):
  st.markdown('## 공군 입영부대 접수인원 건수 추세 \n')

  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format=('%Y%m'))
  total_df['month'] = total_df['iyyjsijakYm'].dt.month


  filterd_df = total_df[total_df['gunGbnm'] == '공군']
  filterd_df = filterd_df[filterd_df['iyyjsijakYm'].between('2024-05', '2024-12')]

  result = filterd_df.groupby(['month','iybudaeCdm'])['gunGbnm'].count()
  
  bar_df = filterd_df.groupby(['month','iybudaeCdm'])['gunGbnm'].agg('count').reset_index()
  df_sorted = bar_df.sort_values('gunGbnm', ascending=False)

  # 바 차트 만들기
  fig = px.bar(df_sorted, x='month', y='gunGbnm')

  # update Layout
  fig.update_yaxes(tickformat='.0f',
                  title_text = '접수 인원 개수',
                  range=[0, bar_df['gunGbnm'].max()])
  fig.update_layout(title='Bar Chart - 오름차순',
                    xaxis_title='날짜',
                    yaxis_title='접수 인원')
  

  st.dataframe(result, use_container_width=True)
  st.plotly_chart(fig)
  

def showCamp(total_df):

  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format=('%Y%m'))
  total_df['month'] = total_df['iyyjsijakYm'].dt.month
  selected = st.sidebar.selectbox('군구분', ['해군', '육군', '해병', '공군'])

  if selected == '해군':
    Navy(total_df)
  elif selected == '육군':
    Army(total_df)
    pass
  elif selected == '해병':
    Marine(total_df)
  elif selected == '공군':
    airforce(total_df)
    pass
  else:
    st.warning('Error')
  