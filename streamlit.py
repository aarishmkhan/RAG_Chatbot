from main import ChatBot
import streamlit as st

bot = ChatBot()

st.set_page_config(page_title="Customer Service Bot")
with st.sidebar:
    st.title('Customer Service Bot')


# Function for generating LLM response
def generate_response(input):
    # result = bot.rag_chain.invoke(input)
    result = bot.ask(input)
    return result


# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Welcome, How May I Help You?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Getting your answer from the archives.."):
            response = generate_response(input)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)