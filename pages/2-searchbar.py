import streamlit as st
import pandas as pd
import numpy as np  

ani_list = ['짱구는못말려', '몬스터','릭앤모티']
img_list = ['https://i.imgur.com/t2ewhfH.png', 
            'https://i.imgur.com/ECROFMC.png', 
            'https://i.imgur.com/MDKQoDc.jpg']


#텍스트를 입력받아서 해당 텍스트와 일치하는 이미지를 화면에 줄력하는 검색창 생성 

search_text = st.text_input("Search for an anime")
if search_text:
    if search_text in ani_list:
        index = ani_list.index(search_text)
        st.image(img_list[index])
    else:
        st.write("No matching anime found.")
