import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()


def test_deepseek_api():
    # 从环境变量获取API Key
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        print("❌ 请在.env文件中设置DEEPSEEK_API_KEY")
        return

    print("正在初始化DeepSeek API客户端...")

    # 初始化客户端
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )

    print("正在测试美国队长对话...")

    try:
        # 测试调用
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system",
                 "content": "你是美国队长，用他标志性的正直勇敢的语气回答所有问题。你知道所有漫威宇宙的知识。"},
                {"role": "user", "content": "队长，巴基和钢铁侠谁更重要？"}
            ],
            temperature=0.7,
            max_tokens=500
        )

        print("🎉 API调用成功！")
        print("=" * 50)
        print("美国队长:", response.choices[0].message.content)
        print("=" * 50)
        print("本次消耗token:", response.usage.total_tokens)

    except Exception as e:
        print("❌ API调用失败:")
        print(f"错误信息: {e}")
        print("\n💡 排查步骤:")
        print("1. 检查.env文件中的API密钥是否正确")
        print("2. 检查网络连接")
        print("3. 确认DeepSeek账户有免费额度")


if __name__ == "__main__":
    test_deepseek_api()