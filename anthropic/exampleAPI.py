import anthropic
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def get_claude_response(user_message, model_name="claude-3-5-sonnet-20241022"):  # 모델 이름만 수정
    """
    Claude API를 호출하여 응답을 받는 함수
    """
    try:
        message = client.messages.create(
            model=model_name,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"API 호출 중 오류 발생: {e}"

if __name__ == "__main__":
    print("Claude와 대화해보세요! (종료하려면 'exit' 입력)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        response = get_claude_response(user_input)
        print(f"Claude: {response}")