import os
import openai
import gradio as gr

from dotenv import load_dotenv

load_dotenv()

#if you have OpenAI API key as a string, enable the below
openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nAI: I am an AI created by OpenAI. How can I help you today?"

def openai_create(prompt):

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )

    return response.choices[0].text

# ... (previous code)

def customize_response(response_text):
    # Add your customizations here
    if "AI:" in response_text:
        response_text = response_text.replace("AI:", "ChatGPT:")
    return response_text

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    output_text = customize_response(output)
    return history, history, output_text

'''
# ... (remaining code)


def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history

'''

block = gr.Blocks()

with block:
    gr.Markdown("""<h1><center>My-GPT 1.0</center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

block.launch(debug = True, share=True)