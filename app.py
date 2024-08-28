import gradio as gr
from sqlchain import agent_executor

def ask_bot(text):
    output=agent_executor.invoke(text)
    return output


def main():
    with gr.Blocks() as querydb:
        gr.Markdown("Langchain SQL Agent App")
        name=gr.Textbox(
            lines=1,
            placeholder="Ask your question here...",
            label="Ask your question here...",
            )
        output=gr.Textbox(label="Answer",lines=4)
        greet_btn=gr.Button(label='Ask Model')

        greet_btn.click(ask_bot,input=[name],output=[output])
    
    querydb.launch()

if __name__=="__main__":
    main()