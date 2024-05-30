import os
from transformers import pipeline, set_seed
from huggingface_hub import login
from dotenv import load_dotenv

# Hugging Face 토큰 가져오기
load_dotenv()
hugging_face_token = os.getenv("HUGGINGFACE_TOKEN")

# Hugging Face 로그인 (필요한 경우)
login(token=hugging_face_token)

def apply_ux_writing_principles(input_text):
    # GPT-2 모델을 사용하여 텍스트 생성 파이프라인 설정
    generator = pipeline('text-generation', model='gpt2')
    set_seed(42)
    
    # 텍스트 생성 (max_length와 num_return_sequences는 필요에 맞게 조정)
    outputs = generator(input_text, max_length=50, num_return_sequences=1)
    
    # 생성된 텍스트 반환
    return outputs[0]['generated_text']

if __name__ == "__main__":
    while True:
        user_input = input("문장을 입력하세요 (종료하려면 'exit' 입력): ")
        if user_input.lower() == "exit":
            break
        transformed_text = apply_ux_writing_principles(user_input)
        print("변환된 문장:", transformed_text)

