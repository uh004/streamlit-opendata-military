import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from utils import load_data
from viz import showViz
from statistic import showStat
from camp import showCamp

total_df = load_data()

def home():
  st.markdown('### Graph 개요 \n'
              '- 군구분 모집병 지원 평균 지원율 추세 \n'
              '- 군구분 모집병 접수인원 추세 \n'
              '- 군구분 접수 선발 인원 과부족 \n')
  st.markdown('### Corr 개요 \n'
              ''
              '- 육군 두 집단간 차이 검정\n'
              '- 육군 상관관계 분석\n')
  st.markdown('### camp 개요 \n'
              '- 모집병 부대 인원 보기')

def run_eda_home(total_df):
  st.markdown('### 탐색적 자료 분석 개요 \n'
              '탐색적 자료 분석 페이지 입니다.'
              '여기에 포함하고 싶은 내용을 넣을 수 있습니다.')
  selected = option_menu(None, ['Home', 'Graph', 'Corr', 'camp'],
                        icons=['bi bi-brilliance', 'bi bi-graph-up-arrow', 'bi bi-book-half', 'bi bi-calendar-heart-fill'],
                        menu_icon = 'app-indicator', default_index=0, orientation='horizontal',
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
  
  if selected == 'Home':
    home()
  elif selected == 'Graph':
    showViz(total_df)
  elif selected == 'Corr':
    showStat(total_df)
    pass
  elif selected == 'camp':
    showCamp(total_df)
  else:
    st.warning('Wrong')