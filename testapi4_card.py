import openai

OPENAI_API_KEY = "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"
if not OPENAI_API_KEY:
    print("NEED OPENAI API Key from https://platform.openai.com/account/api-keys")
openai.api_key = OPENAI_API_KEY

# Wrapper class

# from IPython.display import Markdown, HTML
import time

class Chat:
    def __init__(self, system_content='''너는 사용자에게 최적의 신용카드를 추천해주는 역할이야. 
    친절하게 존댓말 사용해서 대답해.
    먼저 신용카드를 추천해주기 위해 연령, 소득수준, 주로 소비하는 카테고리에 대해서 물어봐.
    두번째 대답을 듣고 나서 주로 소비하는 카테고리에 혜택이 좋은 카드를 최대 2개 추천해줘.
    사용자가 자세하게 설명해달라고 하면 
    해당 카드의 연회비와 금리, 혜택, 제공되는 서비스에 관해서 자세하게 설명해줘.
    사용자가 이 카드 이외에 비슷한 다른 카드도 추천해달라고 하면 비슷한 카드를 2개 더 추천해줘.
    다음으로 이때까지 추천해준 각 카드 별로 총 혜택을 비교하고 1개만 결정해줘.
    '''):
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

        # chat.add_system_content("""안녕하세요! 신용카드와 관련하여 도움을 드릴게요. 어떤 도움이 필요하신가요?""")

        st.write("안녕하세요! 신용카드와 관련하여 도움을 드릴게요.")
        st.write("도움이 필요하신가요?")
        st.write(""""카드 추천"이라고 하시면 조언을 시작합니다.""")




        text = st.text_input(label="Enter text and press Enter", key="text_input")

    if text.rstrip():
        add_text(text)

    state = st.session_state.get("state", [])


    st.write("")
    st.header("Chat History")
    # st.write(state)
    for input_text, output_text in state: #state 안에 있던 text=input_text, result=output_text 출력
        st.write(f'user: {input_text}')
        st.write(f'chatbot: {output_text}')


        # st.text_input("User:", value=input_text, disabled=True)
        # st.text_area("Chatbot:", value=output_text,height=10, disabled=True)
    


if __name__ == "__main__":
    main()
