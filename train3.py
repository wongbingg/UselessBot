from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import Trainer, TrainingArguments
from datasets import Dataset, load_dataset

# 데이터셋 준비
# train_data = {
#     "input_text": ["계정을 생성하세요.", "비밀번호를 입력하세요."],
#     "target_text": ["계정을 만들고 모험을 시작하세요!", "비밀번호를 입력하고 문을 여세요!"]
# }

# 더 많은 데이터 준비
train_data = {
    "input_text": [
        "계정을 생성하세요.",
        "비밀번호를 입력하세요.",
        "사용자 이름을 입력하세요.",
        "이메일 주소를 입력하세요.",
        "회원 가입을 완료하세요.",
        "계정 설정을 변경하세요.",
        "새로운 비밀번호를 설정하세요.",
        "로그인 버튼을 누르세요.",
        "계정을 삭제하세요.",
        "프로필 사진을 업로드하세요."
    ],
    "target_text": [
        "계정을 만들고 모험을 시작하세요!",
        "비밀번호를 입력하고 문을 여세요!",
        "사용자 이름을 입력하고 여정을 시작하세요!",
        "이메일 주소를 입력하고 확인하세요!",
        "회원 가입을 완료하고 즐기세요!",
        "계정 설정을 변경하고 개인화하세요!",
        "새로운 비밀번호를 설정하고 보안을 강화하세요!",
        "로그인 버튼을 누르고 시작하세요!",
        "계정을 삭제하고 떠나세요!",
        "프로필 사진을 업로드하고 꾸미세요!"
    ]
}
# train_data = load_dataset('kor_nli', 'multi_nli')

# Dataset 객체로 변환
train_dataset = Dataset.from_dict(train_data)

# 토크나이저와 모델 초기화
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

# 전처리 함수 정의
def preprocess(data):
    inputs = tokenizer(data['input_text'], max_length=32, truncation=True, padding="max_length")
    targets = tokenizer(data['target_text'], max_length=32, truncation=True, padding="max_length")
    inputs['labels'] = targets['input_ids']
    return inputs

# 데이터셋 전처리
train_dataset = train_dataset.map(preprocess, batched=True)

# 필요한 컬럼만 남기기
train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])

# 훈련 설정
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    save_steps=10_000,  # 모델 저장 주기 (필요에 맞게 조정)
    save_total_limit=2,  # 저장할 체크포인트 수 (필요에 맞게 조정)
    evaluation_strategy="steps",  # 평가 전략 설정
    eval_steps=500  # 평가 주기 설정
)

# Trainer 초기화 및 학습
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

trainer.train()

# 명시적으로 모델 저장
trainer.save_model('./results')
tokenizer.save_pretrained('./results')
