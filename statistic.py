import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
import matplotlib.font_manager as fm

from pingouin import ttest
from plotly.subplots import make_subplots

def twoMeans(total_df,sgg_nm):

  st.markdown('### 육군 5월, 6월 선발 탈락 인원 차이 검증')

  total_df['month'] = total_df['iyyjsijakYm'].dt.month
  apt_df = total_df[(total_df['gunGbnm'] == '육군') & (total_df['month'].isin([5,6]))]

  may_df = apt_df[apt_df['month'] == 5]
  june_df = apt_df[apt_df['month'] == 6]

  st.markdown(f"5월 육군 총 선발 탈락 인원 :  {may_df.groupby('gunGbnm')['extremes'].sum().iloc[0]}")
  st.markdown(f"6월 육군 총 선발 탈락 인원 :  {june_df.groupby('gunGbnm')['extremes'].sum().iloc[0]}")

  result = ttest(may_df['extremes'], june_df['extremes'], paired=False)
  st.dataframe(result, use_container_width=True)

  if result['p-val'].values[0] > 0.05:
    st.markdown('p-val 값이 0.05 초과로 육군 5월, 6월 선발 탈락 인원의 차이는 없다.')
  else:
    st.markdown('p-val 값이 0.05 미만으로 육군 5월, 6월 선발 탈락 인원의 차이는 있다.')

  ###########################################################################################################

  st.markdown(f'### 육군 {sgg_nm} 5월, 6월 선발 탈락 인원 차이 검증')

  total_df['month'] = total_df['iyyjsijakYm'].dt.month
  apt_df = total_df[(total_df['gunGbnm'] == '육군') & (total_df['month'].isin([5,6]))]

  sgg_df = apt_df[apt_df['mojipGbnm'] == sgg_nm]

  sgg_may_df = sgg_df[sgg_df['month'] == 5]
  sgg_june_df = sgg_df[sgg_df['month'] == 6]

  st.markdown(f"{sgg_nm} 5월 육군 총 선발 탈락 인원 : {sgg_may_df['extremes'].sum()}")
  st.markdown(f"{sgg_nm} 6월 육군 총 선발 탈락 인원 : {sgg_june_df['extremes'].sum()}")

  sgg_result = ttest(sgg_may_df['extremes'], sgg_june_df['extremes'], paired=False)
  st.dataframe(sgg_result, use_container_width=True)

  if sgg_result['p-val'].values[0] > 0.05:
    st.markdown('p-val 값이 0.05 초과로 육군 5월, 6월 선발 탈락 인원의 차이는 없다.')
  else:
    st.markdown('p-val 값이 0.05 미만으로 육군 5월, 6월 선발 탈락 인원의 차이는 있다.')

def corrRelation(total_df, sgg_nm):
  
  total_df['month'] = total_df['iyyjsijakYm'].dt.month
  apt_df = total_df[(total_df['gunGbnm'] == '육군') & (total_df['month'].isin([5,6]))]

  st.markdown('### 상관관계 분석 데이터 확인 \n'
              '- 지원율과 선발인원의 상관관계 분석 \n'
              '- 먼저 추출한 데이터 확인\n'
              '- 사용 컬럼: 입영부대명, 모집구분명, 군사특기명, 지원율, 선발인원\n')
  
  corr_df = apt_df[['iybudaeCdm', 'mojipGbnm','gsteukgiNm', 'rate', 'seonbalPcnt']].reset_index(drop=True) # 입영부대명, 모집구분명, 군사특기명, 지원율, 선발인원


  st.dataframe(corr_df.head())

  st.markdown('### 육군 상관관계 분석 시각화 \n'
              '- 육군 5월 ~ 6월 지원율, 선발인원 산포도 그리기 \n')
  
  fig, ax = plt.subplots(figsize=(10,6))
  sns.scatterplot(x='rate', y='seonbalPcnt', data=corr_df, ax=ax)
  st.pyplot(fig)

  # 상관계수 확인
  st.markdown('### 육군 지원율, 선발인원 상관관계 계수 및 검정 \n'
              '- 상관관계 계수를 확인 \n')
  st.dataframe(pg.corr(corr_df['rate'], corr_df['seonbalPcnt']).round(3), use_container_width=False)
  corr_r = pg.corr(corr_df['rate'], corr_df['seonbalPcnt']).round(3)['r']

  if (corr_r.item() > 0.5):
    st.markdown(f'상관계수는 {corr_r.item()}이며, 지원율이 증가할 수록 선발인원이 증가하는 경향성을 가진다')
  elif (corr_r.item() < -0.5):
    st.markdown(f'상관계수는 {corr_r.item()}이며, 지원율이 증가할 수록 선발인원은 감소하는 경향성을 가진다')
  else:
    st.markdown(f'상관계수는 {corr_r.item()}이며, 지원율과 선발인원과의 관계성은 비교적 작다')

  ### 육군 모집병 상관계수 시각화
  st.markdown(f'### 육군 {sgg_nm} 5월, 6월 모집인원 지원율  ~ 선발인원 상관관계 분석 \n')
  sgg_df = corr_df[corr_df['mojipGbnm'] == sgg_nm]
  corr_coef = pg.corr(sgg_df['rate'], sgg_df['seonbalPcnt'])
  st.dataframe(corr_coef, use_container_width=False)

  corr_coef2 = pg.corr(sgg_df['rate'], sgg_df['seonbalPcnt']).round(4)['r']

  if (corr_coef2.item() > 0.5):
    st.markdown(f'상관계수는 {corr_coef2.item()}이며, 지원율이 증가할 수록 선발인원이 증가하는 경향성을 가진다')
  elif (corr_coef2.item() < -0.5):
    st.markdown(f'상관계수는 {corr_coef2.item()}이며, 지원율이 증가할 수록 선발인원은 감소하는 경향성을 가진다')
  else:
    st.markdown(f'상관계수는 {corr_coef2.item()}이며, 지원율과 선발인원과의 관계성은 비교적 작다')

  # 한글 폰트 설정
  path = 'C:\Windows\Fonts\H2MJRE.TTF'
  fontprop = fm.FontProperties(fname=path, size=12)  
  
  fig, ax = plt.subplots(figsize=(10, 6))
  sns.scatterplot(x='rate', y='seonbalPcnt', data=sgg_df)
  ax.text(0.95, 0.05, f"Pearson Correlation : {corr_coef['r'].values[0]:.2f}", 
                                                    transform=ax.transAxes, ha='right', fontsize=12)
  ax.set_title(f'{sgg_nm} 피어슨 상관계수', fontproperties=fontprop)
  st.pyplot(fig)


def showStat(total_df):
  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format=('%Y%m'))

  analisys_nm = st.sidebar.selectbox('분석메뉴', ['두 집단간 차이 검정', '상관분석'])
  sgg_nm = st.sidebar.selectbox('모집구분명', total_df.query('gunGbnm == "육군"')['mojipGbnm'].unique())

  if analisys_nm == '두 집단간 차이 검정':
    twoMeans(total_df,sgg_nm)
  elif analisys_nm == '상관분석':
    corrRelation(total_df, sgg_nm)
    pass
  else:
    st.warning('Error')