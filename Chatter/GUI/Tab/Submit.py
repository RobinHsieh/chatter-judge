# -*- coding: utf-8 -*-
'''
Create Date: 2024/01/14
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
'''

import gradio as gr
from typing import Any
from Chatter.Judge.Judge import get_code
from Chatter.ChatBot.Chat import respond
from Chatter.Utils.Listener import background_listener
from Chatter.GUI.Information import Header as heaader
from Chatter.GUI.Information import Question as question
from Chatter.GUI.Information import Header as heaader

def init_submit_tab():

    with gr.Tab("Submit Your Code") as submit_tab:
        gr.Markdown(
            heaader.submit_page_header
        )

        with gr.Row():
            with gr.Column("Question part"):

                with gr.Row():
                    selected_homework_name = gr.Dropdown(
                        label="⛳️ Select Homework", 
                        value=question.homework_sessions[0],
                        choices=question.homework_sessions,
                        interactive=True,
                    )

                    selected_question_name = gr.Dropdown(
                        label="📸 Select Question", 
                        value=question.question_sessions[0],
                        choices=question.question_sessions,
                        interactive=True,
                    )

                gr.Markdown(
                    heaader.question_descriptions_header
                )

                question_description = gr.Markdown(
                    question.homework_one_content_sessions[0], 
                    visible=True,
                )
            with gr.Column():
                chatbot = gr.Chatbot(
                    label="EE Chat",
                    show_label=True,
                )
                msg = gr.Textbox(
                    label="Tell me something..."
                )
                clear = gr.ClearButton(
                    [msg, chatbot]
                )
                msg.submit(
                    respond, 
                    [msg, chatbot], 
                    [msg, chatbot],
                )

        with gr.Row():

            answer_code = gr.Code(
                label="Write Your code here", 
                language="python",
                # info="Initial text",
            )

        with gr.Row():
            txt_3 = gr.Textbox(
                label="Your code results",
                info="Initial text",
            )

        with gr.Row():
            btn = gr.Button(
                value="Submit",
            )
            btn.click(
                get_code, 
                inputs=[answer_code], 
                outputs=[txt_3],
            )

    background_listener(
        selected_homework_name,
        selected_question_name,
        question_description
    )

    # the next try listener and update in the background

    return submit_tab
