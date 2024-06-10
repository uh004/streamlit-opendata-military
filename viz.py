import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px

def meanChart(total_df, sgg_nm):
  st.markdown('## 군구분 모집병 지원 평균 지원율 추세\n')

  filterd_df = total_df[total_df['mojipGbnm'] == sgg_nm]
  filterd_df = filterd_df[filterd_df['iyyjsijakYm'].between('2024-05', '2024-12')]
  result = filterd_df.groupby(['iyyjsijakYm', 'gunGbnm'])['rate'].agg('mean').reset_index()

  df1 = result[result['gunGbnm'] == '해군']
  df2 = result[result['gunGbnm'] == '육군']
  df3 = result[result['gunGbnm'] == '해병']
  df4 = result[result['gunGbnm'] == '공군']

  fig = make_subplots(rows=2, cols=2,
                      shared_xaxes=True,
                      subplot_titles=('해군', '육군', '해병', '공군'),
                      horizontal_spacing=0.15)
  
  fig.add_trace(px.line(df1, x='iyyjsijakYm', y='rate',
                        title='해군 {sgg_nm} 지원율 평균', markers=True).data[0], row=1, col=1)
  fig.add_trace(px.line(df2, x='iyyjsijakYm', y='rate',
                        title='육군 {sgg_nm} 지원율 평균', markers=True).data[0], row=1, col=2)
  fig.add_trace(px.line(df3, x='iyyjsijakYm', y='rate',
                        title='해병 {sgg_nm} 지원율 평균', markers=True).data[0], row=2, col=1)
  fig.add_trace(px.line(df4, x='iyyjsijakYm', y='rate',
                        title='공군 {sgg_nm} 지원율 평균', markers=True).data[0], row=2, col=2)
  fig.update_layout(
    title='군구분 모집병 지원율 평균값 추세 그래프',
    width=800, height=600,
    showlegend=True, template='plotly_white')
  st.plotly_chart(fig)

def cntChart(total_df, sgg_nm):
  st.markdown('## 군구분 모집병 접수인원 추세 \n')

  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format=('%Y%m'))
  total_df['month'] = total_df['iyyjsijakYm'].dt.month

  filterd_df = total_df[total_df['mojipGbnm'] == sgg_nm]
  filterd_df = filterd_df[filterd_df['iyyjsijakYm'].between('2024-05', '2024-12')]

  result = filterd_df.groupby(['month', 'gunGbnm'])['seonbalPcnt'].sum().reset_index() # 접수인원

  df1 = result[result['gunGbnm'] == '해군']
  df2 = result[result['gunGbnm'] == '육군']
  df3 = result[result['gunGbnm'] == '해병']
  df4 = result[result['gunGbnm'] == '공군']

  fig = make_subplots(rows=2, cols=2,
                      shared_xaxes=True,
                      subplot_titles=('해군','육군','해병','공군'),
                      horizontal_spacing=0.15)
  fig.add_trace(px.line(df1, x='month', y='seonbalPcnt',
                        title='해군 선발인원 거래건수', markers=True).data[0], row=1, col=1)
  fig.add_trace(px.line(df2, x='month', y='seonbalPcnt',
                        title='육군 선발인원 거래건수', markers=True).data[0], row=1, col=2)
  fig.add_trace(px.line(df3, x='month', y='seonbalPcnt',
                        title='해병 선발인원 거래건수', markers=True).data[0], row=2, col=1)
  fig.add_trace(px.line(df4, x='month', y='seonbalPcnt',
                        title='공군 선발인원 거래건수', markers=True).data[0], row=2, col=2)
  fig.update_yaxes(tickformat='.0f')
  fig.update_layout(title_text='군구분 모집병 선발인원 추세 그래프',
                  width=800, height=600,
                  showlegend=True, template='plotly_white')
  st.plotly_chart(fig)

def barChart(total_df,sgg_nm):
  st.markdown('## 군구분 접수 선발 탈락 인원')
  sgg_selected = st.selectbox('군구분', total_df['gunGbnm'].unique())

  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format=('%Y%m'))
  total_df['month'] = total_df['iyyjsijakYm'].dt.month

  total_df = total_df[total_df['mojipGbnm'] == sgg_nm]

  total_df = total_df[total_df['iyyjsijakYm'].between('2024-05', '2024-12')]
  result = total_df[total_df['gunGbnm'] == sgg_selected]

  bar_df = result.groupby(['month','gunGbnm'])['extremes'].agg('sum').reset_index()

  df_sorted = bar_df.sort_values('extremes', ascending=False)

  # 바 차트 만들기
  fig = px.bar(df_sorted, x='month', y='extremes')

  # update Layout
  fig.update_yaxes(tickformat='.0f',
                  title_text = '접수 선발 탈락 인원 개수',
                  range=[0, df_sorted['extremes'].max()])
  fig.update_layout(title='Bar Chart - 오름차순',
                    xaxis_title='날짜',
                    yaxis_title='선발 탈락 인원')
  st.plotly_chart(fig)

def showViz(total_df):
  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format=('%Y%m'))

  sgg_nm = st.sidebar.selectbox('모집 구분명', total_df['mojipGbnm'].unique())
  selected = st.sidebar.radio('차트메뉴', ['군구분 모집병 지원율 상황', '군구분 모집병 접수인원', '군구분 모집병 탈락 인원'])

  if selected == '군구분 모집병 지원율 상황':
    meanChart(total_df, sgg_nm)
  elif selected == '군구분 모집병 접수인원':
    cntChart(total_df, sgg_nm)
  elif selected == '군구분 모집병 탈락 인원':
    barChart(total_df, sgg_nm)
  else:
    st.warning('Error')