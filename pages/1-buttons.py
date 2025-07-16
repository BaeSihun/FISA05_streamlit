import streamlit as st


# 입력을 변수로 받아서 출력에 넘겨주면 됩니다.

# 1. 버튼을 누르면 화면에 True 라고 코드를 리턴하는 간단한 동작 작성
if st.button('Show True'):
    st.write(True)


# 2. 사진을 찍으면 다운로드 버튼으로 사진을 다운로드 받을 수 있게 작성
picture = st.camera_input("Take a picture")
if picture:
    st.download_button("Download Picture", data=picture, file_name="picture.png")