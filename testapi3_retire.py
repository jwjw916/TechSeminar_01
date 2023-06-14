import openai

OPENAI_API_KEY = "sk-"
if not OPENAI_API_KEY:
    print("NEED OPENAI API Key from https://platform.openai.com/account/api-keys")
openai.api_key = OPENAI_API_KEY

# Wrapper class

# from IPython.display import Markdown, HTML
import time

class Chat:
    def __init__(self, system_content='''은퇴계획에 도움을 줄 수 있어.
     처음에는 은퇴를 위해 현재의 수입과 은퇴 희망 시기를 물어봐. 
     그 다음 대답을 듣고 생각하는 은퇴 후 필요한 금액을 물어봐.
     그 다음 대답을 듣고 모든 정보를 고려하여 은퇴 후 30년간 예상 비용을 계산하고, 
     해당 비용을 충당하기 위한 저축 금액을 제시해줘.'''):
        self.system_content = system_content
        self.init_messages()
        
    def init_messages(self):
        self.messages = []
        # if self.system_content:
        #     self.add_system_content(self.system_content)
        if self.system_content:
            self.add_system_content(self.system_content)



    def add_user_content(self, content):
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_content(self, content):
        self.messages.append({"role": "assistant", "content": content})
    
    def add_system_content(self, content):
        self.messages.append({"role": "system", "content": content})
        
    def _run_query(self):
        max_retries = 7
        wait_time = 1

        for i in range(max_retries):
            try:
                self.response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=self.messages,
                    temperature=0.6,
                    top_p=1.0,
                    max_tokens = 100,
                    frequency_penalty = 1.3
                )
                return
            except Exception as e:
                if i == max_retries - 1:
                    raise
                else:
                    print(f"Exception {e}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    wait_time *= 2
     

    def query(self, q, print_response=True):
        self.add_user_content(q)
        self._run_query()
        self.add_assistant_content(self.response['choices'][0]['message']['content'])
        # if print_response:
            # st.write(self.messages[-1]['content'])   



            


    

import streamlit as st
chat = Chat()


# session에 메시지 추가
def add_text(text):
    chat.query(text)
    result = chat.messages[-1]['content']
    #st.ssesion_stae는 세션상태를 저장하는 딕셔너리, 세션상태는 실행 중 유지하는 상태 
    state = st.session_state.get("state", []) #state값이 있으면 반환하고 없으면 []로 초기화
    state.append((text, result)) #text, result 쌍으로 리스트 저장
    st.session_state["state"] = state #state 변수를 ["state"] 키에 할당함 = 다음 실행시 이전값 유지

# def print_messages():
#     st.write(chat.messages[-1]['content'])     


# Streamlit 애플리케이션 구현
def main():
    with st.sidebar:
        st.title("Chatbot with Streamlit")

        chat.add_system_content("""안녕하세요! 은퇴 계획에 대해 도움을 드릴 수 있습니다.
    궁금한 점이 있으신가요? "네"라고 하시면 조언을 시작합니다.""")

        st.write("안녕하세요! 은퇴 계획 챗봇입니다.")
        st.write("궁금한 점이 있으신가요?")
        st.write(""""네"라고 하시면 조언을 시작합니다.""")




        text = st.text_input(label="Enter text and press Enter", key="text_input")

    if text.rstrip():
        add_text(text)

    state = st.session_state.get("state", [])


    st.write("")
    st.header("Chat History")
    st.write(state)
    # for input_text, output_text in state: #state 안에 있던 text=input_text, result=output_text 출력
    #     st.write(f'user: {input_text}')
    #     st.write(f'chatbot: {output_text}')


        # st.text_input("User:", value=input_text, disabled=True)
        # st.text_area("Chatbot:", value=output_text,height=10, disabled=True)
    


if __name__ == "__main__":
    main()
