import openai

OPENAI_API_KEY = "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"
if not OPENAI_API_KEY:
    print("NEED OPENAI API Key from https://platform.openai.com/account/api-keys")
openai.api_key = OPENAI_API_KEY

# Wrapper class

# from IPython.display import Markdown, HTML
import time

class Chat:
    def __init__(self, system_content='''투자 자문에 도움을 드리는 역할입니다.
    처음 질문은 목표 수익률을 물어봅니다. 
    대답을 듣고 10개의 질문으로 구성된 위험 허용도 평가를 보여줍니다. 
    - style: questions for deep engagement written by marketing expert 
    - easy to answer - output table - columns: Number, Question Type(주관식), Question, Answer(Empty)
    -질문은 한글로 줍니다 그 다음 사용자의 평가 답변을 듣고 포트폴리오를 전달해줍니다.
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
    state = st.session_state.get("state", []) 
    state.append((text, result))
    st.session_state["state"] = state 




# Streamlit 애플리케이션 구현
def main():
    with st.sidebar:
        st.title("Chatbot with Streamlit")

        st.write("안녕하세요, 반갑습니다.")
        st.write("도움이 필요하신가요?")
        st.write(""""투자 자문"이라고 하시면 조언을 시작합니다.""")

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
