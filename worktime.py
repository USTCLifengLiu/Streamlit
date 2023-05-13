import streamlit as st
import base64
import random
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import time
from time import gmtime,strftime


st.set_page_config(page_title="丫丫学习时间汇总",page_icon = ':rainbow:')
st.title("丫丫学习时间")
st.write("学习时间汇总")

def get_audio_bytes(music):
    audio_file = open(f'/Users/apple/Desktop/worktime/music/{music}-郎朗.mflac', 'rb')
    audio_bytes = audio_file.read()
    audio_file.close()
    return audio_bytes

class MyRandom:
    def __init__(self,num):
        self.random_num=num


if 'first_visit' not in st.session_state:
        st.session_state.first_visit=True
else:
    st.session_state.first_visit=False
# 初始化全局配置
if st.session_state.first_visit:
    # 在这里可以定义任意多个全局变量，方便程序进行调用
    #st.session_state.date_time=datetime.datetime.now() + datetime.timedelta(hours=8) # Streamlit Cloud的时区是UTC，加8小时即北京时间
    #st.session_state.random_chart_index=random.choice(range(len(charts_mapping)))
    st.session_state.my_random=MyRandom(random.randint(1,1000000))
    #st.session_state.city_mapping,st.session_state.random_city_index=get_city_mapping()
    # st.session_state.random_city_index=random.choice(range(len(st.session_state.city_mapping)))
    st.balloons()
    st.snow()

# music=st.sidebar.radio('选择你喜欢的音乐',['圣诞快乐劳伦斯先生','春江花月夜'],index=random.choice(range(2)))
# st.sidebar.write(f'正在播放 {music}-郎朗:musical_note:')
# audio_bytes=get_audio_bytes(music)
# st.sidebar.audio(audio_bytes, format='audio/mp3/mflac')

# d=st.sidebar.date_input('日期',st.session_state.date_time.date())
# t=st.sidebar.time_input('时间',st.session_state.date_time.time())
# t=f'{t}'.split('.')[0]
# st.sidebar.write(f'xian{d} {t}')

data = pd.read_csv('worktime.csv')
day = data['日期'].unique().tolist()
Start = datetime.strptime(day[0],'%Y/%m/%d')
End = datetime.strptime(day[-1],'%Y/%m/%d')

start_date = st.sidebar.date_input("开始日期", datetime.date(Start))
end_date = st.sidebar.date_input("结束日期", datetime.date(End))

if start_date <= end_date:
    st.success("开始日期: `{}`\n\n结束日期:`{}`".format(start_date, end_date))
else:
    st.error("Error: 结束日期应该在开始日期之后")
pixture = st.sidebar.radio('功能图:',['折线图','饼状图'])

subject = st.multiselect("科目:",['法理学','刑法','英语'], default = ['法理学','刑法','英语'])

start_time = (pd.to_datetime(start_date)-pd.to_datetime(day[0])).days
end_time = (pd.to_datetime(end_date)-pd.to_datetime(day[0])).days

total_time_subject = np.sum(data.loc[range(start_time,end_time+1),subject])
total_time = np.sum(total_time_subject)
MinGet = total_time % (60)

HoursGet = total_time // 60

colordict = {'法理学':'#EAB364','刑法':'#A4CABC','英语':'#ACBD78','总时长':'#B2473E'}
st.write(f"总学习时间:{HoursGet}小时{MinGet}分钟")
#print(total_time)
colorchoice = []
for sub in subject:
    colorchoice.append(colordict[sub])
if pixture=='折线图':
    data['总时长'] = np.sum(data.loc[:,['法理学','刑法','英语']],axis=1)
    #print(data.loc[range(start_time,end_time+1),['日期']])
    data['日期'] = pd.to_datetime(data['日期'])
    #print(data.loc[range(start_time,end_time+1),['日期']])
    #print(np.array(data.loc[range(start_time,end_time+1),['日期']]), np.array(data.loc[range(start_time,end_time+1),['法理学']]/60))
    select = data.loc[range(start_time,end_time+1)]

    layout = go.Layout(title = '每日学习时间(单位:小时)',   #这里指出框架的标题
                    xaxis = {'title' : '日期'},              #x轴的标题
                    yaxis = {'title' : '时长'},              #y轴的标题
                    template = 'plotly_white'                #背景模版，这里是指背景为白色
                    )

    fig = go.Figure(layout=layout)
    if subject == ['法理学','刑法','英语']:
        fig.add_trace(go.Scatter(x=select['日期'], y=select['法理学']/60, name="法理学",
                                line_color=colordict['法理学']))
        fig.add_trace(go.Scatter(x=select['日期'], y=select['刑法']/60, name="刑法",
                                line_color=colordict['刑法']))
        fig.add_trace(go.Scatter(x=select['日期'], y=select['英语']/60, name="英语",
                                line_color=colordict['英语']))
        fig.add_trace(go.Scatter(x=select['日期'], y=select['总时长']/60, name="总时长",
                                line_color=colordict['总时长']))
    else:
        for sub in subject:
            fig.add_trace(go.Scatter(x=select['日期'], y=select[sub]/60, name=sub,
                                line_color=colordict[sub]))
    st.plotly_chart(fig)
    ##############################################
else:
    select2 = pd.DataFrame({'科目':subject,'时长':total_time_subject,'色彩':colorchoice})
    fig2 = px.pie(select2,names='科目',values='时长',color='科目',color_discrete_map=colordict,title='各科目学习占比')
    st.plotly_chart(fig2)
#fig.show()
#do_something()
####################################################
file_ = open("gogo.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)
####################################################
#st.balloons()
#print(colorchoice)
#print(subject,colordict['法理学'])

