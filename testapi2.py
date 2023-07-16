import openai
import streamlit as st
from streamlit_chat import message
from IPython.display import display, Markdown, HTML
import time

OPENAI_API_KEY = ""
if not OPENAI_API_KEY:
    print("NEED OPENAI API Key from https://platform.openai.com/account/api-keys")
openai.api_key = OPENAI_API_KEY

class Chat:
    def __init__(self):
      self.initialize_chat()

    def initialize_chat(self):
      self.messages = []
      self.instruction_index = 0
      self.add_system_content("안녕! 은퇴 계획에 대해 도움을 드릴 수 있습니다. 예상 비용과 생활 수준, 저축 목표, 투자 전략 등 은퇴와 관련된 다양한 정보와 조언을 제공할 수 있어요. 어떤 도움이 필요하신가요?")

    def get_instruction_message(self):
      instruction_message_list = [
    "은퇴 계획을 상상하는 사용자의 말을 듣고 은퇴 계획이 적절한지 조언해줍니다.",
    "은퇴를 위해 현재의 수입과 목표한 은퇴 금액을 고려하여 적절한 저축 목표를 제시해드립니다.",
    "은퇴에 필요한 자금을 목표에 맞게 모으는 데 도움을 드리기 위해 투자 전략을 제시해드립니다.",
    "은퇴 후의 생활 수준을 고려하여 예상 비용을 계산하고, 해당 비용을 충당하기 위한 방법을 제시해드립니다.",
    "은퇴 시기에 따라 고려해야 할 요소와 관련된 질문에 대한 조언을 제공해드립니다."
]

      instruction_index = self.instruction_index % len(instruction_message_list)
      self.instruction_index += 1
      return instruction_message_list[instruction_index]

    def query(self, print_response=True):
      user_input = input("사용자: ")
      self.add_user_content(user_input)
      self.add_assistant_content(self.get_instruction_message())
      self._run_query()
      self.add_assistant_content(self.response.choices[0].text)
      if print_response:
          self.print_messages()

    def _get_prompt(self):
      prompt = ""
      for message in self.messages:
          role = message["role"]
          content = message["content"]
          prompt += f"{role}: {content}\n"
      return prompt

    def _run_query(self):
      max_retries = 7
      wait_time = 1

      for i in range(max_retries):
          try:
              self.response = openai.Completion.create(
                  engine="gpt-3.5 turbo",
                  prompt=self._get_prompt(),
                  temperature=0.7,
                  max_tokens=50
              )
              return
          except Exception as e:
              if i == max_retries - 1:
                  raise
              else:
                  print(f"Exception {e}. Retrying in {wait_time} seconds...")
                  time.sleep(wait_time)
                  wait_time *= 2
            
    def add_user_content(self, content):
        self.messages.append({"role": "user", "content": content})
        
    def add_assistant_content(self, content):
        self.messages.append({"role": "assistant", "content": content})
        
    def add_system_content(self, content):
        self.messages.append({"role": "system", "content": content})
        
    def print_messages(self):
        for d in self.messages:
            role = d['role']
            content = d['content']
            if role == 'assistant':
                print(content)
            else:
                color = '#080' if role == 'system' else '#008'
                print(f"\033[38;5;{color}m{role}: {content}\033[0m")

chat = Chat()



st.header("ChatGPT-3 (Demo)")

def add_text(state, text):
    chat.query(text)
    result = chat.messages[-1]['content']
    state = state + [(text, result)]
    return state, state

# def add_text(state, text):
#     # 챗봇과의 대화를 진행하는 로직
#     result = chatbot.generate_response(text)
#     state.append((text, result))
#     return state

def run_chatbot():
    state = []
    
    # 사용자 입력 받기
    user_input = st.text_input("User:")
    
    # 사용자 입력이 있는 경우 대화 진행
    if user_input:
        state = add_text(state, user_input)
    
    # 대화 내용 출력
    for user, response in state:
        st.markdown(f"**User:** {user}")
        st.markdown(f"**Chatbot:** {response}")
        st.markdown("---")



# 스트림릿 앱 실행
run_chatbot()

