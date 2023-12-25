# -*- coding: utf-8 -*-
'''
Create Date: 2023/10/18
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

def build_chatter_judge(
        *args: Any, 
        **kwargs: Any,
    ) -> None:

    demo = gr.Blocks(
        title='Chatter Judge',
    )

    with demo:
        gr.Markdown(
            heaader.ee_judge_header
        )

        with gr.Tab("Submit Your Code"):
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

        with gr.Tab("Submitted History"):
            gr.Markdown(
                heaader.submitted_history_page_header
            )

        with gr.Tab("Race Bar"):
            gr.Markdown(
                heaader.race_bar_page_header
            )

        with gr.Tab("Judge Mechanism"):
            gr.Markdown(
                heaader.judge_mechanism_page_header
            )

        with gr.Tab("Judge Developers"):
            gr.Markdown(
                heaader.judger_developer_page_header
            )

        background_listener(
            selected_homework_name,
            selected_question_name,
            question_description
        )

    return demo
