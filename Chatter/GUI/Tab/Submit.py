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
from Chatter.Utils.Listener import submit_background_listener
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
                chat_history = gr.Chatbot(
                    label="EE Chat",
                    show_label=True,
                )
                msg = gr.Textbox(
                    label="Tell me something..."
                )
                gr.ClearButton(
                    components=[
                        msg, 
                        chat_history,
                    ],
                )
                msg.submit(
                    fn=respond, 
                    inputs=[
                        msg, 
                        chat_history,
                    ], 
                    outputs=[
                        msg, 
                        chat_history,
                    ],
                )

        with gr.Row():

            with gr.Column():
                answer_code = gr.Code(
                    label="Write Your code here", 
                    language="python",
                    lines=10,
                    # info="Initial text",
                )

            with gr.Column():
                judged_result = gr.Markdown(
                    f"### Your code results: "
                )

                submit_code_btn = gr.Button(
                    value="Submit",
                )

                submit_code_btn.click(
                    get_code, 
                    inputs=[
                        answer_code,
                        selected_homework_name,
                        selected_question_name,
                    ], 
                    outputs=[
                        judged_result
                    ],
                )

    submit_background_listener(
        selected_homework_name,
        selected_question_name,
        question_description
    )

    

    return submit_tab
