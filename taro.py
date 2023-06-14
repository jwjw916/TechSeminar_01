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


instruction_message_list = [
    "당신은 친절한 타로카드상담사입니다. 사용자에게 반갑게 인사하고 질문을 편안하게 유도하는 말을 합니다. 문장에 이모지를 추가합니다.",
    "받은 [질문]에 대해서 공감한 뒤, 타로 게임을 시작해도 되는 지 '예' 또는 '아니오'로 대답할 수 있도록 물어봅니다. 그 외의 다른 질문은 하지 않습니다. 이 때 타로 카드는 아직 뽑지 않습니다. 문장에 이모지를 추가합니다.",
    "사용자가 시작을 원치 않으면 상담을 중단합니다. 그렇지 않다면, 타로카드를 뽑고 순서대로 해석한 뒤, 종합적으로 해석한 내용을 깊이있고 친절하게 작성합니다. 문장에 이모지를 추가합니다."
]

def request_to_rev_openai(query):
    chatbot = Chatbot(config={
        "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ3amVkaXRvcjkxNkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1wOUkwT0ozcnlZMzNHZnFURlBxNFFmRlkifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTExMDAxMzQ0MDkwNzIyNTk1NDU2IiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4NTA2Njk4NiwiZXhwIjoxNjg2Mjc2NTg2LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSJ9.WqIuLz1-CVj6LRpzjRd_qHb_sjlV0zYfdagsP8dL8sdy2-W845CaujKwtMMmmOP-QFZvK0YwGJ_KUmvje-zHAV7mAkyQRncpWFw4xEkvFOiucPYSZ7kJZ-eKlMfFkcU2pvYyJOv9USMdVLqHHBGmMDwMHeqMdVeC_-FvMvJJwXkNMtlDnCfWOUeX2g5tbt0tyml4h7kSTtGXn7uzNfYA0_hWBrD6SdFLbviy0Tr1CrKCD0KGAELkj2E0iGF2Kk9BsQ1qYPQuulMOoLQw18t2-HjNAcnsQ_rOjZY16jyzWnnPKZO5JhdymEJ59y3VK0Wp1G6HGvj9jCc-1aoFBuhPzw"
    })

    prev_text = ""
    for data in chatbot.ask(prompt=query):
        prev_text = data["message"]
        element.write(prev_text, unsafe_allow_html=True)