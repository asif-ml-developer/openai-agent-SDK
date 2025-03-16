import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # Our custom logic goes here...
    
    await cl.Message(content="Welcome to the AI Assistant! How can I help you today?").send()# it is send one time and not updated
    # await cl.Message(content=f"Received: {message.content}").send() # it is when send updated
    mes= cl.Message(content=f"Received: {message.content}") 
    await mes.send() # it is when s