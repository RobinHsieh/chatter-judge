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
        title='EE-Judge',
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
                    gr.Markdown(
                        heaader.question_descriptions_header
                    )

                    selected_question_name = gr.Dropdown(
                        label="Select Question", 
                        value=question.question_sessions[0],
                        choices=question.question_sessions,
                        interactive=True,
                    )

                    question_description = gr.Markdown(
                        question.question_one_description, 
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
                txt = gr.Textbox(
                    label="Paste Your code here", 
                    info="Initial text",
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
                    inputs=[txt], 
                    outputs=[txt_3],
                )

        with gr.Tab("Submitted History"):
            gr.Markdown(
                "We will record the submitted history in the future..."
            )

        with gr.Tab("Race Bar"):
            gr.Markdown(
                "We will record the Race Bar in the future..."
            )

        with gr.Tab("Judge Mechanism"):
            gr.Markdown(
                "We will record the judge mechanism in the future..."
            )

        background_listener(
            selected_question_name,
            question_description
        )

    return demo
