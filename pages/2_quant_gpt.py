from openai import OpenAI
import streamlit as st

st.title("Quantitative GPT-3 Chatbot")

# sidebar input for the OpenAI API key
api_key = st.sidebar.text_input("OpenAI API key", type="password")

#

with st.expander("GPT Bot Guide"):
    st.markdown(
        '''
        ## GPT-3.5-turbo
        
        ### Disclaimer: 
        This chatbot is powered by OpenAI's GPT-3.5-turbo model. It is still in development and may not be perfect. Please provide feedback if you encounter any issues.
        It is yet to be fine tuned for quantitative finance questions. After which I will remove the 'API key' requirement.

        ## How to Get Your OpenAI API Key

        Follow these steps to generate an API key for accessing OpenAI's services:

        ---

        ## Step 1: Log In to OpenAI
        1. Go to the [OpenAI website](https://platform.openai.com/).
        2. Click on the **Log In** button in the top-right corner.
        3. Enter your credentials to log in. If you don’t have an account, click **Sign Up** and create one.

        ---

        ## Step 2: Access the API Dashboard
        1. After logging in, navigate to the [API dashboard](https://platform.openai.com/account/api-keys).
        2. This page is where you can manage your API keys.

        ---

        ## Step 3: Create a New API Key
        1. Click the **+ Create new secret key** button.
        2. A pop-up will appear displaying your new API key.

            > **Note:** You will only see this key once. Make sure to copy and save it in a secure location, such as a password manager or a secure file.

        ---

        ## Step 4: Secure Your API Key
        - Treat your API key like a password. Do not share it publicly or store it in publicly accessible code repositories.
        - If you suspect that your API key has been exposed or compromised, immediately delete it and generate a new one.

        ---

        ## Step 5: Use the API Key
        - Use your API key in your application to enable the chatbot.

        ---

        ## Troubleshooting
        - If you encounter issues, visit the [OpenAI Help Center](https://help.openai.com/) for support.
        - Ensure your account has the necessary subscription or credits to access the API.

        ---

        ## Additional Tips
        - Regularly review your API key usage in the [Usage Dashboard](https://platform.openai.com/account/usage).
        - Follow best practices for securely managing your API keys.

        ---

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
