# 홈 버튼을 선택할 경우 실행

import pandas as pd
import streamlit as st
from millify import prettify

import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def run_home(total_df):
  st.markdown('## 대시보드 개요 \n'
              '본 프로젝트는 **2024년 병무청_모집병 군지원 접수현황**을 제공하는 대시보드 입니다.\n'
              '본 데이터는 **실시간**으로 계속 변동되는 데이터를 기반으로 하며, 프로젝트는 **5월 24일 기준** totalCount: 964건의 데이터를 CSV 파일에 저장하여 분석하였습니다. 이후 6월 6일 기준으로 totalCount: 755건으로 감소한 것을 확인할 수 있었습니다. 이는 접수기간이 만료된 것이 있는것을 확인할 수 있습니다. 이러한 분석을 통해 실시간으로 변화하는 데이터를 반영하여 **유의미한 예측과 분석**을 제공합니다.\n')
  st.markdown('**공공 데이터 포털 :** <a href="https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15031295" style="text-decoration:none">병무청_모집병 군지원 접수현황</a>', unsafe_allow_html=True)

  image_path = 'rotc.jpeg'
  base64_image = get_base64_image(image_path)

  html_code = f'''
      <div style="width: 100%; height: 300px; overflow: hidden;">
          <img src="data:image/jpeg;base64,{base64_image}" style="width: 100%; height: auto;">
      </div>
  '''

  st.markdown(html_code, unsafe_allow_html=True)

  
  # DEAL_YMD:계약일
  total_df['iyyjsijakYm'] = pd.to_datetime(total_df['iyyjsijakYm'], format=('%Y%m'))
  total_df['month'] = total_df['iyyjsijakYm'].dt.month
  
  selected_month = st.sidebar.selectbox('확인하고 싶은 월을 선택하시오 ', list(set(total_df['month'])))
  sgg_nm = st.sidebar.selectbox('군구분', total_df['gunGbnm'].unique()) # 중복된 값을 제거하고 고유한 값만 반환

  st.markdown('<hr>', unsafe_allow_html=True)
  st.subheader(f'{sgg_nm} {2024}년 {selected_month}월 접수인원 수')
  st.markdown('군구분과 월을 클릭하면 자동으로 각 군구분의 접수인원 수를 알 수 있습니다.')

  filtered_month = total_df[total_df['month'] == selected_month]
  filtered_month = filtered_month[filtered_month['gunGbnm'] == sgg_nm]

  people = filtered_month['jeopsuPcnt'].sum() # 접수 인원
  count = filtered_month['seonbalPcnt'].sum() # 선발 인원

  cols = filtered_month[['iybudaeCdm', 'mojipGbnm','gsteukgiNm', 'rate']] # 입영부대명, 모집구분명, 군사특기명,지원율

  top = cols.sort_values(by='rate', ascending=False).head(3) # 내림차순 높은거 -> 낮은거
  bottom = cols.sort_values(by='rate').head(3) # 내림차순 높은거 -> 낮은거

  col1, col2 = st.columns(2)

  with col1:
    st.metric(label= f'{sgg_nm} 접수인원', value= prettify(people))
  with col2:
    st.metric(label= f'{sgg_nm} 선발인원', value= prettify(count))

  st.markdown(f'## {sgg_nm} 지원율 상위 3위')
  st.dataframe(top,use_container_width=True)

  st.markdown(f'## {sgg_nm} 지원율 하위 3위')
  st.dataframe(bottom,use_container_width=True)
