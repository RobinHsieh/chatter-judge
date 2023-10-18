# -*- coding: utf-8 -*-
'''
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
'''

from Chatter.Utils.Update import test

def background_listener(
        selected_question_name,
        test_word,
    ):
    selected_question_name.change(
            fn=test,
            inputs=selected_question_name,
            outputs=test_word,
        )
