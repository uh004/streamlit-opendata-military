import streamlit as st
from streamlit_option_menu import option_menu
from utils import load_data
from home import run_home
from eda import run_eda_home
from ml import run_ml_home

def main():
  total_df = load_data()

  with st.sidebar:
    selected = option_menu('데시보드 메뉴', ['홈','탐색적 자료분석', '모집병 예측'],
                          icons=['bi bi-brilliance', 'bi bi-clipboard-data', 'bi bi-palette2'], menu_icon='app-indicator', default_index=0,
                          styles={
                          'container' : {
                                          'padding' : '0!important',
                                          'background-color' : '#FFFFFF'},
                          'icon' : {
                                      'color' : 'white',
                                      'font-size' : '25px'},
                          'nav-link' : {
                                          'font-size' : '15px',
                                          'text-align' : 'left',
                                          'margin' : '0px',
                                          },
                          'nav-link-selected' : {
                                          'background' : 'black'}
                        })
    
  if selected == '홈':
    run_home(total_df)
  elif selected == '탐색적 자료분석':
    run_eda_home(total_df)
  elif selected == '모집병 예측':
    run_ml_home(total_df)
  else:
    print('error')

if __name__ == '__main__':
  main()