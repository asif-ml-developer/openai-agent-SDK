# only  chainlit without aget
# uv run chainlit run main1.py
import chainlit as cl
@cl.on_message

async def handle_message(message: cl.Message):
    await cl.Message(content=f"Hello {message.content}").send()