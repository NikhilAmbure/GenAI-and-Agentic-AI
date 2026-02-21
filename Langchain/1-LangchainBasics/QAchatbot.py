"""
    Simple Langchain Streamlit App with Groq
"""

import streamlit as st
import os 

from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

## Page config
st.set_page_config(page_title="Simple Langchain Chatbot with Groq", page_icon="🚀")

## Title
st.title("Simple Langchain Chat with Groq")
st.markdown("Learn Langchain with Groq")

with st.sidebar:
    st.header("Settings")

    ## Api Key
    api_key = st.text_input("GROQ API Key", type="password", help="GET Free API key at console.groq.com")

    ## Model Selection
    model_name = st.selectbox(
        "Model",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
        index=0 # By default it will select first one
    )

    ## clear button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

## Initialize LLM
@st.cache_resource
def get_chain(api_key, model_name):
    if not api_key:
        return None
    
    ## Initialize the Groq model
    llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.7, streaming=True)

    ## Create prompt template
    prompt = ChatPromptTemplate.from_messages({
        ("system", "You're a helpful assistant powered by Groq. Answer questions clearly and concisely."),
        ("user", "{question}")
    })

    ## create chain
    chain = prompt| llm| StrOutputParser()

    return chain

chain = get_chain(api_key, model_name)

if not chain:
    st.warning("Please enter your Groq API Key in the sidebar to start chatting!")
    st.markdown("Don't have an API key? [Get one for free at console.groq.com]")
else:
    ## Display the Chat Messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    ## chat input
    if question:= st.chat_input("Ask me anything"):
        ## Add user message to session_state
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        ## Generate Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try: 
                ## Stream response from Groq
                for chunk in chain.stream({"question": question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "|")

                message_placeholder.markdown(full_response)

                ## Add to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

## Examples
st.markdown("---")
st.markdown("### 🚀 Try these example questions:")
col1, col2 = st.columns(2)

with col1:
    st.markdown("- What is Langchain?")
    st.markdown("- How do I use Groq with Langchain?")

with col2:
    st.markdown("- What are the best practices for prompt engineering?")
    st.markdown("- Can you explain the difference between LLM and traditional ML models?")

## Footer
st.markdown("---")
st.markdown("Made with ❤️ using Langchain and Groq")