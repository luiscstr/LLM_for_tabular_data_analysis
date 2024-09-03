import gradio as gr
from  chatbot import ChatBot
from dotenv import load_dotenv
from upload_file import load_and_save_file
load_dotenv()


def main():
    with gr.Blocks() as querydb:
        gr.Markdown("Langchain SQL Agent App")
        #First row:chat interface
        with gr.Row() as row_one:
            chatbot=gr.Chatbot(
                [],
                elem_id='chatbot',
                bubble_full_width=False,
                height=500,
                avatar_images=("images/user.png","images/chatbot.jpg")
            )
             # **Adding like/dislike icons
                #chatbot.like(UISettings.feedback, None, None)
        #Second row:text input
        with gr.Row() as row_two:
            input_text=gr.Textbox(
                lines=4,
                scale=8,
                placeholder="Enter text and click enter or press submit",
                container=False,
            )
        #Third row:button
        with gr.Row() as row_three:
            submit_btn=gr.Button(value='Submit text')
            file_input=gr.UploadButton(
                 label="📁 Upload CSV or XLSX files",
                file_types=['.csv','.xls','.xlsx'])
            clear_btn=gr.ClearButton([input_text,chatbot])
        output_message = gr.Textbox(label="Message", interactive=False)
        output_table = gr.DataFrame(label="Preview of the Data")
   
        #Process (can be submitted with enter or with click button)
        file_input.upload(fn=load_and_save_file,inputs=[file_input],outputs=[output_message,output_table])
    
        output=input_text.submit(fn=ChatBot.respond,
                                 inputs=[chatbot,input_text],
                                 outputs=[input_text,chatbot],
                                 queue=False).then(lambda: gr.Textbox(interactive=True),
                                                   None,[input_text],queue=False)
        output=submit_btn.click(fn=ChatBot.respond,
                                 inputs=[chatbot,input_text],
                                 outputs=[input_text,
                                          chatbot],
                                 queue=False).then(lambda: gr.Textbox(interactive=True),
                                                   None,[input_text],queue=False)
        
    
    querydb.launch()

if __name__=="__main__":
    main()