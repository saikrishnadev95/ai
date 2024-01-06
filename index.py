# pip install streamlit streamlit_chat google-generativeai pybase64
import streamlit as st
from streamlit_chat import message
import os
import base64

# google gemini pro configuration

import google.generativeai as genai
GOOGLE_API_KEY=base64.b64decode(os.getenv('GOOGLE_API_KEY')).decode('utf-8').strip()
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def api_calling(prompt):
	response = model.generate_content(prompt)
	return response.text


# STREAMLIT configuration

st.title("ChatBot With Streamlit and gemini-pro")
if 'user_input' not in st.session_state:
	st.session_state['user_input'] = []

if 'openai_response' not in st.session_state:
	st.session_state['openai_response'] = []

def get_text():
	input_text = st.text_input("write here", key="input")
	return input_text

user_input = get_text()

if user_input:
	output = api_calling(user_input)
	output = output.lstrip("\n")

	# Store the output
	st.session_state.openai_response.append(user_input)
	st.session_state.user_input.append(output)

message_history = st.empty()

if st.session_state['user_input']:
	for i in range(len(st.session_state['user_input']) - 1, -1, -1):
		# This function displays user input
		message(st.session_state["user_input"][i], 
				key=str(i),avatar_style="icons")
		# This function displays OpenAI response
		message(st.session_state['openai_response'][i], 
				avatar_style="miniavs",is_user=True,
				key=str(i) + 'data_by_user')
