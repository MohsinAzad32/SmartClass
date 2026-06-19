import streamlit as st
from src.ui.style_base_layout import style_background_dashboard
from src.ui.style_base_layout import style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipeline.face_pipeline import predict_attendence
from src.database.db import get_all_students

import time 


def student_screen():

    style_background_dashboard()
    style_base_layout()


def student_dashboard():
    st.header("Student Dashboard")

    if 'student_data' in st.session_state:
        student_dashboard()
        return



    c1,c2 =st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",type="secondary",key="registerbackbtn",shortcut="control+backspace"):
            st.session_state["login_type"]=None
            st.rerun()
    
    st.header("Login using Password",text_alignment="center")
    st.space()
    st.space()

    st.header("Login using FaceID",text_alignment='center')


    show_registration_type=False
    image_source=st.camera_input("Position your face in the center")
    if image_source:
        img=np.array(Image.open(image_source))

        with st.spinner("AI is scanning...."):
            detected,all_ids,num_faces=predict_attendence(img)

            if num_faces==0:
                st.warning("Face not found")
            elif num_faces>1:
                st.warning("Multiple Faces found")
            else:
                if detected:
                    student_id=list(detected.keys[0])
                    all_students=get_all_students()
                    student=next((s for s in all_students if s['student_id']==student_id),None)

                    if student:
                        st.session_state.is_logged_in=True
                        st.session_state.user_role='student'
                        st.session_state.student_data=student
                        st.toast(f"Wellcome Back! {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not Recognized!. You might be a new student")
                    show_registration_type=True
    if show_registration_type:
        with st.container(border=True):
            st.header('Register new profile')
            new_name=st.text_input("Enter your name",placeholder="E.g Mohsin Azad")
            st.subheader("Optional :Voice Enrollment")
            st.info("Enroll you for voice only attendence")


            audio_data=None
            try:
                audio_data=st.audio_input("Record short phrase like i am present, My name is Mohsin")
            except Exception:
                st.error("Audio Data Failed")
            if st.button('Create Account',type="primary"):
                if new_name:
                    with st.spinner('Creating profile'):
                        
                else:
                    st.warning('Please Enter your name!')

    footer_dashboard()