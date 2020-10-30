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
import seaborn as sns

from konlpy.tag import Okt
okt = Okt()
import hanja
# st.write(hanja.translate('大韓民國은 民主共和國이다.', 'substitution'))
# '대한민국은 민주공화국이다.'

import matplotlib
from IPython.display import set_matplotlib_formats
matplotlib.rc('font',family = 'Malgun Gothic')
set_matplotlib_formats('retina')
matplotlib.rc('axes',unicode_minus = False)
import matplotlib.pyplot as plt

@st.cache
def load_data():
    df_total=pd.read_excel('C:/Users/fordi/df_ ndsl_5129.xlsx')
    return df_total

df = pd.read_excel('paper_ffill.xlsx')

def clean_str(sentence):
    sentence1 = re.sub(r"&.*?;", " ", str(sentence))
    sentence2 = re.findall(r"[a-zA-Z가-힣0-9]*", sentence1)
    res = ' '.join(sentence2)
    result = re.sub(r"\s{2,}", " ", str(res))
    return result.strip()


df_total = load_data()
st.subheader("미술치료가 키워드로 포함된 NDSL 전체 논문 수{} , 데이터 수 {} 개".format(df_total.shape[0],df_total.shape))
st.subheader("")
st.dataframe(df_total.head(10))

#st.pyplot(df_total['발행기관_대학_short'][df_total['발행기관_대학_short']!=""].value_counts()[0:20].plot(kind='bar'))

year_slider = st.sidebar.slider('원하는 기간를 선택하세요(2020-이전)', 1999, 2020,(1999,2020))
input_pi=st.sidebar.text_input("대상", "")
input_pe=st.sidebar.text_input("증상 키워드", "")

input_1=st.sidebar.text_input("측정 방법 키워드", "")
input_2=st.sidebar.text_input("측정 지표 키워드", "")

#df_short = df[df['year_short'].between(year_slider[0], year_slider[1])]

df_paper=df[['year_short', '제목', '대학']].drop_duplicates()
df_table=pd.pivot_table(df_paper, index='대학', columns='year_short', values='제목', aggfunc=len, margins=True).fillna(0)
df_table=df_table.reset_index()
df_table=df_table.sort_values(by='All',ascending=False).reset_index()
df_table=df_table.drop(df_table[df_table['대학']=='All'].index[0])
df_table=df_table.drop(['index'], axis=1)



df_year_insitite=pd.pivot_table(df_total, index='발행년', columns='발행기관_구분',values='논문명', aggfunc=len).fillna(0).reset_index()
df_year_insitite=pd.melt(df_year_insitite, id_vars='발행년',value_vars=['기타','대학','학회'], value_name='발행건')
sns.barplot(x='발행년', y='발행건', hue='발행기관_구분', data=df_year_insitite,

           dodge=False) # stacked bar chart
plt.xticks(rotation=45)
plt.title('발행년도별 기관별 현황', fontsize='20')

st.pyplot()

st.subheader("미술치료가 키워드로 포함된 논문중 사전사후 데이터가 있는 전체 논문 수{} , 데이터 수 {} 개".format(df_paper.shape[0],df.shape))
st.dataframe(df_table)

df_table_plot=df_table.sort_values(by='All',ascending=False)
df_table_plot=df_table_plot.drop('All', axis=1)
df_table_plot=pd.melt(df_table_plot, id_vars=['대학'])
df1 = df_table_plot.groupby(by='대학').sum().sort_values(by='value',ascending=False).reset_index()
trace3 = go.Bar(x=df1['대학'][:20], y=df1['value'], name='대학별 구성')
figure_3 = go.Figure(data=[trace3])
#figure_3.update_layout(title="대학별 논문 제출 수", barmode='stack')
figure_3.update_layout(title="상위 20개 대학별 논문 누계 순위(1999-2020)")
st.plotly_chart(figure_3)

st.subheader('년도별 대학교 논문 제출 결과')
figure_ex=px.bar(df_table_plot, x='year_short', y='value', color='대학')
st.plotly_chart(figure_ex)

st.subheader("전체 논문의 증상 분포")
df_phenom=df[['year_short', '제목', '대학','증상']].drop_duplicates()
df_table_phenom=pd.pivot_table(df_phenom, index='증상', columns='year_short', values='제목', aggfunc=len, margins=True).fillna(0)
df_table_phenom=df_table_phenom.sort_values(by='All',ascending=False)
st.dataframe(df_table_phenom)

trace4 = go.Bar(x=df1['대학'][:20], y=df1['value'], name='대학별 구성')
figure_3 = go.Figure(data=[trace3])
#figure_3.update_layout(title="대학별 논문 제출 수", barmode='stack')
figure_3.update_layout(title="상위 20개 대학별 논문 수(1999-2020)")
st.plotly_chart(figure_3)


st.subheader("전체 논문의 대상 분포")
df_phenom=df[['year_short', '제목', '대학','증상']].drop_duplicates()
df_table_phenom=pd.pivot_table(df_phenom, index='증상', columns='year_short', values='제목', aggfunc=len, margins=True).fillna(0)
st.dataframe(df_table_phenom.sort_values(by='All',ascending=False))

st.subheader("전체 논문의 학교 분포")
st.subheader("전체 논문의 측정방법 분포")
st.subheader("전체 논문의 측정방법별 전후 비교")


st.subheader("선택 범위의 증상 분포")


st.subheader("전체 논문의 대상 분포")

if st.sidebar.button('Submit'):
    df_short = df[df['year_short'].between(year_slider[0], year_slider[1])]
    if len(str(input_pi)) > 1:
        df_short = df_short[df_short['증상'].str.contains(str(input_pi))]
    else:
        df_short = df_short
    if len(str(input_pi)) > 1:
        df_short = df_short[df_short['증상'].str.contains(str(input_pi))]
    else:
        df_short = df_short
        
    st.write(f"선택 몬문 수{df_short.shape}")
    st.dataframe(df_short)

st.markdown("## Party time!")
st.write("Yay! You're done with this tutorial of Streamlit. Click below to celebrate.")
btn = st.button("Celebrate!")
if btn:
    st.balloons()