# -*- coding: utf-8 -*-
'''
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
'''

import gradio as gr

def test(selected_question_name):

    output_components = []

    if selected_question_name == "Q1":

        test_word = gr.Markdown(
            """\
            ### Q1
            
            print("Hello World")
            """,  
            visible=True,
        )
    elif selected_question_name == "Q2":
        test_word = gr.Markdown(
            "### Q2", 
            visible=True,
        )

    output_components.append(test_word)
    
    return test_word
