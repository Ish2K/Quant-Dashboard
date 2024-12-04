from openai import OpenAI
import streamlit as st

st.title("Quantitative GPT-3 Chatbot")

# sidebar input for the OpenAI API key
api_key = st.sidebar.text_input("OpenAI API key", type="password")

#

with st.expander("GPT Bot Disclaimer"):
    st.markdown(
        '''
        ## GPT-3.5-turbo
        This chatbot is powered by OpenAI's GPT-3.5-turbo model. It is still in development and may not be perfect. Please provide feedback if you encounter any issues.
        It is yet to be fine tuned for quantitative finance questions. After which I will remove the 'API key' requirement.
        '''
    )


# add submit button

if (not (st.sidebar.button("Submit") or api_key)):
    st.stop()

client = OpenAI(api_key=api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
