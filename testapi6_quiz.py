import openai

OPENAI_API_KEY = "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"
if not OPENAI_API_KEY:
    print("NEED OPENAI API Key from https://platform.openai.com/account/api-keys")
openai.api_key = OPENAI_API_KEY

# Wrapper class

# from IPython.display import Markdown, HTML
import time

class Chat:
    def __init__(self, system_content='''경제 상식 퀴즈를 낼거야. 
    처음에 친절하게 인사하고 난이도(상/중/하)를 물어봐. 
    난이도에 맞춰서 다음 예시처럼 문제를 한개 출제해.
    [객관식 예시: 1. 문제 a. 정답선지 답변:], [주관식 예시: 1. 문제 답변 : ] ,
    문제는 경제상식, 채권, 외환 등 다양한 분야에서 금융 상식을 바탕으로  해. 
    문제는 매경퀴즈(https://exam.mk.co.kr/m/)와 한경 경제용어사전(https://dic.hankyung.com/economy/list)을 참고해.
    대답을 보고 문제를 맞추면 10점의 점수를 부여해줘.
    주관식 답변의 길이가 50글자를 넘으면 다시 작성해달라고 해. 
    문제를 풀면 답과 풀이를 제시하고 난이도에 맞춰서 예시처럼 문제를 한개 출제해.
    [정답입니다! 풀이는 다음과 같습니다. 이어서 다음 문제입니다.]
    총 점수는 문제 2개를 풀면 알려줘.
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
                
                    # frequency_penalty = 1.5
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

        st.write("안녕하세요, 반갑습니다.")
        st.write("도움이 필요하신가요?")
        st.write(""""경제상식퀴즈"라고 하시면 조언을 시작합니다.""")




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
