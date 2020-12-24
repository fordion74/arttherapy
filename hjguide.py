# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 18:28:16 2020

@author: fordi
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re

@st.cache
def load_data():
    df = pd.read_excel('df_analysis_final_m.xlsx')
    return df


def clean_str(sentence):
    sentence1 = re.sub(r"&.*?;", " ", str(sentence))
    sentence2 = re.findall(r"[a-zA-Z가-힣0-9]*", sentence1)
    res = ' '.join(sentence2)
    result = re.sub(r"\s{2,}", " ", str(res))
    return result.strip()
st.beta_set_page_config(layout="wide")
df_sex=['전체(구분없음)','남성','여성']

df = load_data()

st.sidebar.title('성별, 장애, 연령, 증상 선택')
select_sex=st.sidebar.selectbox('성별 선택',df_sex)
select_disable=st.sidebar.selectbox("장애여부 선택",("전체(구분없음)","정상","장애"))
age_gorup=st.sidebar.radio("연령대 선택",("전체","영유아기","청소년기","성인","노인"))


select_ph=st.sidebar.multiselect("증상 선택(다중선택 가능)",("우울","스트레스","창의성","표현","불안","분노조절","자아존중감","공격성","중독","자아존중"))
input_pi=st.sidebar.text_input("추가 조건(주부, 군인 등)", "")


st.title("힐링아트 심리치료 가이드")
st.title("(Healing Art Therapy  Clinic Guide)")
st.title(" ")


#st.write("성별:", select_sex," ","장애여부:",select_disable," ","연령대 선택:",age_gorup)

#for w in select_ph:
#    st.write(w)
#st.sidebar.write('증상선택')
#select_ph=st.sidebar.checkbox('스트레스')
#select_w=st.sidebar.checkbox('우울')

if select_sex=='전체(구분없음)':
    df_select = df
elif select_sex=='남성':
    df_select=df[df['남여구분']=='남']
elif select_sex=='여성':
    df_select=df[df['남여구분']=='여']

#st.write("성별뒤",df_select.shape)
# select_age_group=st.sidebar.radio("연령그룹 선택",df['연령그룹'].unique())
#df_select=df_select[df_select['연령그룹']==select_age_group]

if select_disable=='전체(구분없음)':
    df_select = df_select
elif select_disable=="정상":
    df_select=df_select[df_select['장애여부']=="정상"]
elif select_sex=='여성':
    df_select=df_select[df_select['장애여부']=="장애"]

#st.write("장애뒤",df_select.shape)



if age_gorup=="영유아기":
    age_gorup_sub = st.sidebar.selectbox("세부 선택", ("전체","영아기", "유아기"))
    df_select = df_select[df_select['연령대구분']=='아동']
elif age_gorup=="청소년기":
    age_gorup_sub = st.sidebar.selectbox("세부 선택", ("전체","초등학생","중학생", "고등학생"))
    df_select = df_select[df_select['연령대구분'] == '청소년']
elif age_gorup=="성인":
    age_gorup_sub = st.sidebar.selectbox("세부 선택", ("전체","대학생","20대","30대","40대","50대"))
    df_select = df_select[df_select['연령대구분'] == '성인']
elif age_gorup=="노인":
    age_gorup_sub = st.sidebar.selectbox("세부 선택", ("전체","60대","70대이상"))
    df_select = df_select[df_select['연령대구분'] == '노인']
else :
    age_gorup_sub= "전체"
df_select_temp=pd.DataFrame()
#st.write(select_ph)
for w in select_ph:
    df_select_temp=df_select_temp.append(df_select[df_select['제목'].str.contains(w)])

df_select=df_select_temp.drop_duplicates()

st.write("사례수",df_select.shape[0])
#st.dataframe(df_select)


btn = st.sidebar.button("선택하기")
if btn:
    left_column_3, right_column_4 = st.beta_columns(2)
    if len(df_select[df_select['지표구분'] == '긍정']) > 0:
        df_select_melt=pd.melt(df_select[['Unnamed: 0','제목','처음측정방법','초기측정결과', '나중 측정 결과']][df_select['지표구분'] == '긍정'], id_vars=['Unnamed: 0','제목','처음측정방법'], value_vars=['초기측정결과', '나중 측정 결과'])
        fig_3 = px.bar(df_select_melt, x="variable", y="value", color='처음측정방법')
        with left_column_3:
            st.header("긍정지표변화")
            st.plotly_chart(fig_3)

    if len(df_select[df_select['지표구분'] == '부정']) > 0:
        df_select_melt=pd.melt(df_select[['Unnamed: 0','제목','처음측정방법','초기측정결과', '나중 측정 결과']][df_select['지표구분'] == '부정'], id_vars=['Unnamed: 0','제목','처음측정방법'], value_vars=['초기측정결과', '나중 측정 결과'])
        fig_4 = px.bar(df_select_melt, x="variable", y="value", color='처음측정방법')
        with right_column_4:
            st.header("부정지표변화")
            st.plotly_chart(fig_4)


    left_column_far, left_column_time, right_column_time = st.beta_columns(3)

    with left_column_far:
        if len(df_select)>0:
            st.write("전체 회기 수 분포")
            df_select_time=df_select[df_select['총_횟수_clean']!="자료없음"]
            fig_time = px.pie(df_select_time, values=df_select_time['총_횟수_clean'].value_counts()[0:10].values,
                 names=df_select_time['총_횟수_clean'].value_counts()[0:10].index)
            fig_time.update_traces(hoverinfo='label+percent', textinfo='value')
            fig_time.update_layout(legend=dict(
                yanchor="top",
                y=0.9,
                xanchor="left",
                x=0.0
            ))
            st.plotly_chart(fig_time)


    with left_column_time:
        if len(df_select)>0:
            st.write("주당 횟수 분포")
            df_select_time=df_select[df_select['주횟수_clean']!="자료없음"]
            fig_time = px.pie(df_select_time, values=df_select_time['주횟수_clean'].value_counts()[0:10].values,
                 names=df_select_time['주횟수_clean'].value_counts()[0:10].index)
            fig_time.update_traces(hoverinfo='label+percent', textinfo='value')
            fig_time.update_layout(legend=dict(
                yanchor="top",
                y=0.9,
                xanchor="left",
                x=0.0
            ))
            st.plotly_chart(fig_time)

    with right_column_time:
        if len(df_select)>0:
            st.write("1회기당 시간 분포")
            df_select_time=df_select[df_select['시간_clean']!="자료없음"]
            fig_time = px.pie(df_select_time, values=df_select_time['시간_clean'].value_counts()[0:10].values,
                     names=df_select_time['시간_clean'].value_counts()[0:10].index)
            fig_time.update_traces(hoverinfo='label+percent', textinfo='value')
            fig_time.update_layout(legend=dict(
                yanchor="top",
                y=0.9,
                xanchor="left",
                x=0.0
            ))
            st.plotly_chart(fig_time)
    df_temp_p = df_select[['초기측정결과', '나중 측정 결과']][df_select['지표구분'] == '긍정']
    df_temp_p.set_index('초기측정결과', inplace=True)

    df_temp_n = df_select[['초기측정결과', '나중 측정 결과']][df_select['지표구분'] == '부정']
    df_temp_n.set_index('초기측정결과', inplace=True)

    left_column, right_column = st.beta_columns(2)
    # You can use a column just like st.sidebar:
    with left_column:
        st.write('긍정지표변화')
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df_temp_p.index, y=df_temp_p['나중 측정 결과'],
                                  mode='markers', name='사전사후결과'))
        fig2.add_trace(go.Scatter(x=df_temp_p.index, y=df_temp_p.index,
                                  mode='lines', name='기준선'))
        st.plotly_chart(fig2)
    # Or even better, call Streamlit functions inside a "with" block:
    with right_column:
        st.write('부정지표변화')
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_temp_n.index, y=df_temp_n['나중 측정 결과'],
                                  mode='markers', name='사전사후결과'))
        fig3.add_trace(go.Scatter(x=df_temp_n.index, y=df_temp_n.index,
                                  mode='lines', name='기준선'))
        st.plotly_chart(fig3)

    left_column_1, right_column_2 = st.beta_columns(2)
    if len(df_select[df_select['지표구분'] == '긍정']) > 0:
        fig_p = px.scatter(df_select[df_select['지표구분'] == '긍정'], x='초기측정결과', y='나중 측정 결과', color='증상_구분',
                           marginal_y="violin",
                           marginal_x="box", trendline="ols", template="simple_white")
        with left_column_1:
            st.write("긍정지표변화")
            st.plotly_chart(fig_p)
    else:
        with left_column_1:
            st.write('긍정지표 자료없음')

    if len(df_select[df_select['지표구분'] == '부정']) > 0:
        fig_n = px.scatter(df_select[df_select['지표구분'] == '부정'], x='초기측정결과', y='나중 측정 결과', color='증상_구분',
                           marginal_y="violin",
                           marginal_x="box", trendline="ols", template="simple_white")
        with right_column_2:
            st.write("부정지표변화")
            st.plotly_chart(fig_n)
    else:
        with right_column_2:
            st.write('부정지표 자료없음')

