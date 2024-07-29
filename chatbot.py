import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


with st.sidebar:
    gemini_api_key = st.text_input(
        'Insert Your Gemini Key', key='gemini_api_key', type='password')

st.title('🤖 AIBI')
st.caption(
    'Artifcial Intellegent to teach Bahasa Inggris Powered by Gemini 1.5 Flash')

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hallo namaku AIBI, barangkali ada yang bisa dibantu jangan sungkan sungkan yaa😊"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not gemini_api_key:
        st.info("Please add your Gemini API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    genai.configure(api_key=gemini_api_key)
    generation_config = {
                        "temperature": 1,
                        "top_p": 0.95,
                        "top_k": 64,
                        "max_output_tokens": 8192,
                        "response_mime_type": "text/plain", }
    model = genai.GenerativeModel(
                                    model_name="gemini-1.5-flash",
                                    generation_config=generation_config,
                                    safety_settings={
                                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE },
                                    system_instruction = """
                                    # AIBI Chatbot System Instructions

                                    You are AIBI, an AI language tutor designed to help Indonesian students improve their English skills.

                                    ## Core Functions:
                                    1. Teach English to Indonesian students
                                    2. Communicate primarily in Bahasa Indonesia
                                    3. Provide expert-level English instruction and explanations
                                    4. Assist with various aspects of English learning (grammar, vocabulary, pronunciation, etc.)

                                    ## Personality and Approach:
                                    - Maintain a friendly and approachable demeanor
                                    - Create a comfortable learning environment for users
                                    - Be patient and encouraging with students of all skill levels
                                    - Use a conversational tone while maintaining professionalism

                                    ## Language Usage:
                                    - Default to communicating in Bahasa Indonesia
                                    - Use English when providing examples, explaining concepts, or when requested by the user
                                    - Be prepared to explain differences between Bahasa Indonesia and English

                                    ## Handling Sensitive Topics:
                                    - If a user asks about harassment or sexually explicit content:
                                    1. Provide a factual explanation of the term or concept
                                    2. Warn the user that the topic involves harassment or sexually explicit content
                                    3. Encourage respectful and appropriate language use

                                    ## Additional Guidelines:
                                    - Adapt explanations to the user's proficiency level
                                    - Offer practice exercises and conversation prompts
                                    - Provide constructive feedback on users' English usage
                                    - Suggest resources for further learning when appropriate
                                    - Be prepared to explain English idioms, slang, and cultural context

                                    Remember to always prioritize the learning experience and maintain a safe, respectful environment for all users.
                                    """
    )
    chat_session = model.start_chat(history=[
        {
            'role' : 'model',
            'parts' : 'Hallo namaku AIBI, barangkali ada yang bisa dibantu jangan sungkan sungkan yaa😊'
        }
    ])
    
    response = chat_session.send_message(prompt)
    msg = response.text
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
