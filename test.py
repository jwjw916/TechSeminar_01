# 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

import logging
import random

import streamlit
from revChatGPT.V1 import Chatbot
from streamlit.commands.page_config import RANDOM_EMOJIS

streamlit.set_page_config(page_title="Raynor ChatGPT", page_icon=random.choice(RANDOM_EMOJIS), menu_items={})
streamlit.title("Demo ChatGPT with Streamlit")
streamlit.sidebar.header("Chatting")
streamlit.sidebar.info("Chat")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
element = streamlit.empty()


# https://chat.openai.com/api/auth/session
chat_log= []
def request_to_rev_openai(query):
    chatbot = Chatbot(config={
        "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ3amVkaXRvcjkxNkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1wOUkwT0ozcnlZMzNHZnFURlBxNFFmRlkifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTExMDAxMzQ0MDkwNzIyNTk1NDU2IiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4NTA2Njk4NiwiZXhwIjoxNjg2Mjc2NTg2LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSJ9.WqIuLz1-CVj6LRpzjRd_qHb_sjlV0zYfdagsP8dL8sdy2-W845CaujKwtMMmmOP-QFZvK0YwGJ_KUmvje-zHAV7mAkyQRncpWFw4xEkvFOiucPYSZ7kJZ-eKlMfFkcU2pvYyJOv9USMdVLqHHBGmMDwMHeqMdVeC_-FvMvJJwXkNMtlDnCfWOUeX2g5tbt0tyml4h7kSTtGXn7uzNfYA0_hWBrD6SdFLbviy0Tr1CrKCD0KGAELkj2E0iGF2Kk9BsQ1qYPQuulMOoLQw18t2-HjNAcnsQ_rOjZY16jyzWnnPKZO5JhdymEJ59y3VK0Wp1G6HGvj9jCc-1aoFBuhPzw"
    })

    prev_text = ""
    # for data in chatbot.ask(prompt=query):
    #     prev_text = data["message"]
    #     element.write(prev_text, unsafe_allow_html=True)
    for data in chatbot.ask(prompt=query, chat_log=chat_log):
        chat_log.append(data)

    return chat_log


def app_main():
    user_query = streamlit.text_input("Enter").strip()
    if user_query is not None and user_query and user_query != "":
        request_to_rev_openai(user_query)
# 대화 기록 출력
    for data in chat_log:
        element.write(data["message"], unsafe_allow_html=True)


app_main()