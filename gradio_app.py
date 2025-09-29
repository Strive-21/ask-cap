import gradio as gr
import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI


# 环境加载代码 - 调整为Railway兼容
def load_environment():
    # 优先使用Railway的环境变量
    if os.getenv("RAILWAY_ENVIRONMENT"):
        print("🚄 运行在Railway环境中")
        # Railway会自动设置环境变量，不需要.env文件
        return os.getenv("DEEPSEEK_API_KEY")
    else:
        # 本地开发时使用.env文件
        env_path = find_dotenv()
        if env_path:
            load_dotenv(env_path)
            print(f"✅ 成功加载 .env 文件：{env_path}")
            return os.getenv("DEEPSEEK_API_KEY")
        else:
            raise FileNotFoundError("⚠️ 未找到 .env 文件")


DEEPSEEK_API_KEY = load_environment()
if not DEEPSEEK_API_KEY:
    raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")


def get_deepseek_client():
    return OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com/v1"
    )


def chat_with_captain(message, history):
    try:
        client = get_deepseek_client()

        messages = [
            {
                "role": "system",
                "content": "你是美国队长，用他标志性的正直勇敢的语气回答所有问题。你知道所有漫威宇宙的知识。"
            }
        ]

        messages.extend(history)
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        bot_reply = response.choices[0].message.content

        updated_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": bot_reply}
        ]

        return updated_history

    except Exception as e:
        error_msg = f"❌ 通讯故障，请检查API密钥和网络连接\n错误详情: {str(e)}"
        updated_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": error_msg}
        ]
        return updated_history


# 创建界面
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# US Ask Captain America")
    gr.Markdown("与漫威超级英雄美国队长对话")

    chatbot = gr.Chatbot(
        type="messages",
        height=400,
        label="对话记录",
        show_copy_button=True
    )

    with gr.Row():
        msg = gr.Textbox(
            label="输入问题",
            placeholder="例如：队长，你最好的朋友是谁？",
            scale=4
        )
        submit_btn = gr.Button("发送", variant="primary", scale=1)

    with gr.Row():
        clear_btn = gr.Button("清除对话")

    examples = gr.Examples(
        examples=[
            "队长，你最好的朋友是谁？",
            "在巴基和钢铁侠之间你选谁？",
            "全复联的人都知道你在找巴基吗？你那两年有什么任务？跟托尼等人联系吗？猎鹰是不是跟你一起找人？"
        ],
        inputs=msg
    )


    def respond(message, history):
        if not message.strip():
            return history
        return chat_with_captain(message, history)


    msg.submit(respond, [msg, chatbot], [chatbot])
    submit_btn.click(respond, [msg, chatbot], [chatbot])
    clear_btn.click(lambda: [], None, chatbot)

# Railway部署适配 - 关键修改！
if __name__ == "__main__":
    # 获取Railway提供的端口，如果没有则使用默认7860
    port = int(os.environ.get("PORT", 7860))

    # 启动应用
    demo.launch(
        server_name="0.0.0.0",  # 允许外部访问
        server_port=port,  # 使用Railway的端口
        share=False  # 不在Railway上生成公开链接
    )