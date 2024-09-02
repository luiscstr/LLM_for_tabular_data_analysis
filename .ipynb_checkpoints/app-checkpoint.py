import gradio as gr
from sqlchain import agent_executor



def ask_bot(text):
    output=agent_executor.invoke(text)
    return output


def main():
    with gr.Blocks() as querydb:
        gr.Markdown("Langchain SQL Agent App")
        #First row:chat interface
        with gr.Row() as row_one:
            chatbot=gr.Chatbot(
                [],
                element_id='chatbot',
                bubble_full_width=False,
                height=500,
                avatar_images=("images/user.png","images/chatbot.jpg")
            )
             # **Adding like/dislike icons
                #chatbot.like(UISettings.feedback, None, None)
        #Second row:text input
        with gr.Row as row_two:():
            input_text=gr.Textbox(
                lines=4,
                scale=8,
                placeholder="Enter text and click enter or press submit",
                container=False,
            )
        #Third row:button
        with gr.Row as row_three:():
            submit_btn=gr.Button(value='Submit text')
            clear_btn=gr.ClearButton([input_text,chatbot])
        #Process (can be submitted with enter or with click button)
        output=input_text.submit(fn=Chatbot.respond,
                                 inputs=[chatbot,input_text],
                                 outputs=[input_text,
                                          chatbot],
                                 queue=False).then(lambda gr: gr.Textbox(interactive=True),
                                                   None,[input_text],queue=False)
        output=submit_btn.click(fn=Chatbot.respond,
                                 inputs=[chatbot,input_text],
                                 outputs=[input_text,
                                          chatbot],
                                 queue=False).then(lambda gr: gr.Textbox(interactive=True),
                                                   None,[input_text],queue=False)
        
        
        
        
      
    
    querydb.launch()

if __name__=="__main__":
    main()