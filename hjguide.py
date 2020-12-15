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

df_sex=['전체(구분없음)','남성','여성']

#df = load_data()
df = pd.read_excel('df_analysis_final_m.xlsx')
st.write(df.shape)
st.sidebar.title('성별, 장애, 연령, 증상 선택')
select_sex=st.sidebar.selectbox('성별 선택',df_sex)
select_disable=st.sidebar.selectbox("장애여부 선택",("전체(구분없음)","정상","장애"))
age_gorup=st.sidebar.radio("연령대 선택",("전체","영유아기","청소년기","성인","노인"))


select_ph=st.sidebar.multiselect("증상 선택(다중선택 가능)",("우울","스트레스","창의성","표현","불안","분노조절","자아존중감","공격성","중독","자아존중"))
input_pi=st.sidebar.text_input("추가 조건(주부, 군인 등)", "")


st.title("HJ 미술치료 클리닉 가이드")
st.title("(HJ Art Therapy  Clinic Guide)")
st.title(" ")


st.write("성별:", select_sex," ","장애여부:",select_disable," ","연령대 선택:",age_gorup)

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

st.write("성별뒤",df_select.shape)
# select_age_group=st.sidebar.radio("연령그룹 선택",df['연령그룹'].unique())
#df_select=df_select[df_select['연령그룹']==select_age_group]

if select_disable=='전체(구분없음)':
    df_select = df_select
elif select_disable=="정상":
    df_select=df_select[df_select['장애여부']=="정상"]
elif select_sex=='여성':
    df_select=df_select[df_select['장애여부']=="장애"]

st.write("장애뒤",df_select.shape)



if age_gorup=="영유아기":
    age_gorup_sub = st.sidebar.radio("세부 선택", ("영아기", "유아기"))
    df_select = df_select[df_select['연령대구분']=='아동']
elif age_gorup=="청소년기":
    age_gorup_sub = st.sidebar.radio("세부 선택", ("초등학생","중학생", "고등학생"))
    df_select = df_select[df_select['연령대구분'] == '청소년']
elif age_gorup=="성인":
    age_gorup_sub = st.sidebar.radio("세부 선택", ("대학생","20대","30대","40대","50대"))
    df_select = df_select[df_select['연령대구분'] == '성인']
elif age_gorup=="노인":
    age_gorup_sub = st.sidebar.radio("세부 선택", ("60대","70대이상"))
    df_select = df_select[df_select['연령대구분'] == '노인']
else :
    age_gorup_sub= "전체"
st.write(df_select.shape)
df_select_temp=pd.DataFrame()
#st.write(select_ph)

for w in select_ph:
    df_select_temp=df_select_temp.append(df_select[df_select['제목'].str.contains(w)])
    st.write(df_select_temp.shape)

df_select=df_select_temp.drop_duplicates()

st.write("사례수",df_select.shape[0])
#st.dataframe(df_select)


btn = st.sidebar.button("선택하기")
if btn:
    #if len(df_select[df_select['지표구분'] == '긍정'])>0:
    try:
        fig_p = px.scatter(df_select[df_select['지표구분'] == '긍정'], x='초기측정결과', y='나중 측정 결과', color='증상_구분',
                           marginal_y="violin",
                           marginal_x="box", trendline="ols", template="simple_white")
        st.write("긍정지표변화")
        st.plotly_chart(fig_p)
    except:
        st.write("자료없음")
    #else: st.write('긍정지표 자료없음')

    #if len(df_select[df_select['지표구분'] == '부정']) > 0:
    try:
        fig_n = px.scatter(df_select[df_select['지표구분'] == '부정'], x='초기측정결과', y='나중 측정 결과', color='증상_구분',
                           marginal_y="violin",
                           marginal_x="box", trendline="ols", template="simple_white")
        st.write("부정지표변화")
        st.plotly_chart(fig_n)
    #else : st.write('부정지표 자료없음')
    except:
        st.write("자료없음")

    try:

        df_temp_p=df_select[['초기측정결과','나중 측정 결과']][df_select['지표구분'] == '긍정']
        df_temp_p.set_index('초기측정결과', inplace=True)


        df_temp_n=df_select[['초기측정결과','나중 측정 결과']][df_select['지표구분'] == '부정']
        df_temp_n.set_index('초기측정결과', inplace=True)

        st.write('긍정지표변화')
        fig2=go.Figure()
        fig2.add_trace(go.Scatter(x=df_temp_p.index, y=df_temp_p['나중 측정 결과'],
                              mode='markers', name='사전사후결과'))
        fig2.add_trace(go.Scatter(x=df_temp_p.index, y=df_temp_p.index,
                              mode='lines', name='기준선'))
        st.plotly_chart(fig2)


        st.write('부정지표변화')
        fig3=go.Figure()
        fig3.add_trace(go.Scatter(x=df_temp_n.index, y=df_temp_n['나중 측정 결과'],
                          mode='markers', name='사전사후결과'))
        fig3.add_trace(go.Scatter(x=df_temp_n.index, y=df_temp_n.index,
                          mode='lines', name='기준선'))
        st.plotly_chart(fig3)
    except: st.write("자료없음")