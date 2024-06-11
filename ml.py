import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from prophet import Prophet
import numpy as np
from prophet.plot import plot_plotly
import matplotlib.font_manager as fm
import os

def home() :
  st.markdown("### 기계학습 예측 개요 \n"
              "- 군구분 평균 인원 지원율 예측 그래프 추세 \n"
              "- 육군 모집병 평균 인원 지원율 예측 그래프 추세 \n")

def predictType(total_df):
    # 한글 폰트 설정
    # path = 'C:\Windows\Fonts\H2MJRE.TTF'
    path = os.path.join(os.getcwd(), "Nanum_Gothic/NanumGothic-Bold.ttf")
    fontprop = fm.FontProperties(fname=path, size=12)  
    
    # Correct the date format and add a default day for proper datetime conversion
    total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format='%Y%m')
    total_df['month'] = total_df['iyyjsijakYm'].dt.month
    types = list(total_df['gunGbnm'].unique())
    
    periods = int(st.number_input('향후 예측 기간을 지정하세요(1일 ~ 100일)', 
                                  min_value=0, max_value=100, step=10))
    
    fig, ax = plt.subplots(figsize=(10, 6), sharex=True, ncols=2, nrows=2)
    for i in range(0, len(types)):
        # 프로핏 모델 객체 인스턴스 만들기
        model = Prophet()
        

        # 훈련 데이터(데이터프레임) 만들기
        total_df2 = total_df.loc[total_df['gunGbnm'] == types[i], ['iyyjsijakYm','gunGbnm', 'rate']]
        summary_df = total_df2.groupby(['iyyjsijakYm', 'gunGbnm'])['rate'].agg('mean').reset_index()
        summary_df = summary_df.rename(columns = {'iyyjsijakYm' : 'ds', 'rate' : 'y'})
        
        # 훈련 데이터(데이터프레임)로 학습(피팅)하여 prophet 모델 만들기
        model.fit(summary_df)
        
        # 예측결과를 저장할 데이터프레임 준비하기
        future1 = model.make_future_dataframe(periods=periods)
        
        # 예측하기
        forcast1 = model.predict(future1)
        
        x = i // 2
        y = i % 2
        
        # 주거 유형별 예측치 시각화
        fig = model.plot(forcast1, uncertainty=True, ax=ax[x, y])
        ax[x, y].set_title(f'{types[i]} 평균 지원율 예측 시나리오 {periods}일간', 
                          fontproperties=fontprop)
        ax[x, y].set_xlabel(f'날짜', fontproperties=fontprop)
        ax[x, y].set_ylabel(f'평균지원율', fontproperties=fontprop)
        for tick in ax[x, y].get_xticklabels():
            tick.set_rotation(30)
    
    plt.tight_layout()
    st.pyplot(fig)

def predictDistrict(total_df) :
  # 한글 폰트 설정
  # path = 'C:\Windows\Fonts\H2MJRE.TTF'
  path = os.path.join(os.getcwd(), "Nanum_Gothic/NanumGothic-Bold.ttf")
  fontprop = fm.FontProperties(fname=path, size=12) 
  
  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format='%Y%m')
  
  # total_df = total_df[total_df['gunGbnm'] == '육군']
  
  sgg_nms = list(total_df['mojipGbnm'].unique())
  print(sgg_nms)
  
  # 자치구 이름 sgg_nms에서 nan 제거
  sgg_nms = [x for x in sgg_nms if x is not np.nan]
  print(sgg_nms)
  
  periods = int(st.number_input('향후 예측 기간을 지정하세요(1일 ~ 100일)', 
                min_value=0, max_value=100, step=10))
  
  fig, ax = plt.subplots(figsize=(30, 10), sharex=True, sharey=False, ncols=5, nrows=6)

  st.markdown('### 군구분 모집병 향후 예측 기간')

  # 서브플롯의 최대 행과 열 수 설정
  M_row = 6  # 최대 행 수
  M_col = 5  # 최대 열 수

  # 플롯할 항목 수에 따라 행과 열 수 계산
  N = len(sgg_nms)  # 플롯할 항목 수
  n_row = N // M_col + (1 if N % M_col > 0 else 0)  # 행 수 계산
  n_col = min(N, M_col)  # 열 수 계산

  fig, ax = plt.subplots(figsize=(20, 10), sharex=True, sharey=False, ncols=n_col, nrows=n_row)
  
  loop  = 0
  for sgg_nm in sgg_nms :
    # 프로핏 모델 객체 인스턴스 만들기
    model = Prophet()

    total_df2 = total_df.loc[total_df['mojipGbnm'] == sgg_nm, ['iyyjsijakYm', 'rate']]
    
    summary_df = total_df2.groupby('iyyjsijakYm')['rate'].agg('mean').reset_index()
    summary_df = summary_df.rename(columns = {'iyyjsijakYm' : 'ds', 'rate' : 'y'})

    # Check if summary_df has at least 2 non-NaN rows
    if summary_df['y'].dropna().shape[0] < 2:
        print(f"Skipping {sgg_nm} due to insufficient data.")
        continue
    
    print(sgg_nm)
    
    # 훈련 데이터(데이터프레임)로 학습(피팅)하여 prophet 모델 만들기
    model.fit(summary_df)
    
    # 예측결과를 저장할 데이터프레임 준비하기
    future = model.make_future_dataframe(periods=periods)
    
    #  prodict() 함수를 활용하여 25개 자치구별 28일치의 데이터를 예측하기
    forcast = model.predict(future)
    
    x = loop // 5
    y = loop % 5   
    loop = loop + 1
    
    # 주거 유형별 예측치 시각화
    fig = model.plot(forcast, uncertainty=True, ax=ax[x, y])
    ax[x, y].set_title(f'{sgg_nm} 평균 지원율 예측 시나리어 {periods}일간', 
                        fontproperties=fontprop)
    ax[x, y].set_xlabel(f'날짜', fontproperties=fontprop)
    ax[x, y].set_ylabel(f'평균지원율', fontproperties=fontprop)
    for tick in ax[x, y].get_xticklabels():
      tick.set_rotation(30)
  
  plt.tight_layout()
  st.pyplot(fig)

def reportMain():
  st.markdown("## 데이터 분석 환경\n"
              "\n**Python 프로그램 개발 시, Spyder나 VScode 등의 통합 개발 환경(IDE)을 사용할 수 있습니다. 본 프로젝트에서는 VScode 개발 환경을 사용하여 개발을 진행하였습니다. 데이터 분석에 사용한 라이브러리로는 Pandas, Matplotlib, Seaborn 등의 패키지를 설치하고 활용하였습니다.**\n")
  
  st.markdown('## 데이터 수집\n'
              '\n**본 프로젝트에서는 『공공데이터포털 병무청_모집병 군지원 접수현황』의 데이터를 Open API를 활용하여 수집하였습니다. 공공데이터 포털로부터 제공된 데이터를 통해 분석에 필요한 자료를 확보하였습니다.**')
  
  st.markdown('## 데이터 전처리\n'
              '\n**수집한 자료를 Python 데이터 프레임으로 읽어온 후, Pandas 패키지를 사용하여 데이터 전처리를 수행하였습니다. 이 과정에서 데이터 프레임에서 필요한 칼럼을 추가하거나 삭제하여 분석에 적합한 형태로 변환하였습니다.**')
  
  st.markdown("## 데이터 통계 분석\n"
              "\n**전처리된 데이터 프레임을 대상으로 Pandas를 활용하여 상관관계 분석, 집단 간 평균값의 통계적 유의미성을 분석하는 t-검정을 수행하였습니다. 이러한 통계 분석을 통해 데이터의 의미를 도출하였습니다.**\n")
  
  st.markdown("## 데이터 시각화\n"
              "\n**통계 분석 결과를 해석하기 위해 Matplotlib과 Seaborn 등의 시각화 패키지를 활용하여 산포도 등을 그렸습니다. 이를 통해 데이터를 시각적으로 표현하고, 보다 직관적으로 이해할 수 있었습니다.**\n")
  
  st.markdown('## 인공지능 모델 활용 예측\n'
              '\n**Python으로 Meta에서 개발한 시계열 데이터에 특화된 인공지능 예측 모델인 Prophet을 활용하여 병무청_모집병 군지원 접수현황에 대한 예측을 수행하였습니다. Prophet을 통해 향후 접수 현황을 예측하고, 이를 바탕으로 분석 결과를 도출하였습니다.**')
  
  st.markdown("## 웹 배포\n"
              "\n**분석 결과를 대시보드 형태로 시각화하여 웹에 배포하기 위해 Streamlit 패키지를 활용하였습니다. Streamlit을 사용하여 손쉽게 대시보드를 제작하고, 이를 GitHub Repository에 저장하여 웹으로 배포하였습니다.**\n")


def run_ml_home(total_df):
  st.markdown("### 군구분 모집 지원율 예측 개요 \n"
              "###### 사용한 알고리즘 : Prophet은 사용자 친화적인 API를 제공하여, 데이터 과학자가 아닌 사람들도 쉽게 예측 모델을 만들 수 있습니다. 파이썬과 R 라이브러리로 제공되며, 직관적인 함수와 매개변수 설정으로 간단하게 예측 작업을 수행할 수 있습니다.")
    
  selected = option_menu(None, ['홈', '군구분별', '모집구분별', '보고서'],
                          icons=['bi bi-brilliance', 'bi bi-graph-up-arrow', 'bi bi-book-half', 'bi bi-calendar-heart-fill'],
  menu_icon='cast', default_index=0, orientation='horizontal',
                          styles={
                          'container' : {
                                          'padding' : '0!important',
                                          'background-color' : '#FFD700'},
                          'icon' : {
                                      'color' : 'white',
                                      'font-size' : '25px'},
                          'nav-link' : {
                                          'font-size' : '15px',
                                          'text-align' : 'left',
                                          'margin' : '0px',
                                          '--hover-color' : '#eee'},
                          'nav-link-selected' : {
                                          'background' : 'black'}
                        })
                
  if selected == '홈' :
    home()
  elif selected == '군구분별' :
    predictType(total_df)
    pass
  elif selected == '모집구분별' :
    predictDistrict(total_df)
    pass
  elif selected == '보고서' :
    reportMain()
    pass
  else:
    st.warning('Wrong')