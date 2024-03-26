# # -*- coding: utf-8 -*-
# """
# Create Date: 2023/10/18
# Author: @1chooo (Hugo ChunHo Lin)
# Version: v0.0.1
# """
import google.generativeai as genai
import os
import csv


# 從環境變數讀取 API 金鑰
API_KEY = os.environ.get("GEMINI_API_KEY")


if not API_KEY:
    raise ValueError("GEMINI_API_KEY 環境變數未設置")

async def save_to_csv(prompt_parts, response_category):
    # import csv
    current_working_directory = os.getcwd()
    with open('chatbot.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Category'])
        writer.writerow([prompt_parts, response_category])    
        
    return current_working_directory


async def call_chat_api(
    message,
    chat_history,
    *args,
    **kwargs,
    ):

    prompt_parts = [
        "在教授有關於電腦工程、資訊科學的課程中，我們開放同學問問題，請幫我擷取這個問題的核心大綱，例如：「語法說明, 運算子」、「程式語法錯誤, 除以零」。",
        "問題主體 (2 + 2) * 2 和 2 + 2 * 2 有什麼不一樣？",
        "問題分類 程式語法說明, 運算子",
        "問題主體 下列的程式哪裡錯誤：\n```\ndef get_code(txt, selected_homework_name,\n        selected_question_name, *args, **kwargs):\n    with open(\"tmp.py\", \"w\") as file:\n        file.write(txt)\n\n    try:\n        output = subprocess.check_output[\n            [\"python\", \"tmp.py\"], \n            stderr=subprocess.STDOUT, \n            universal_newlines=True,\n        )\n        print(\"Script output:\")\n        print(output)\n\n        result = judge_question_1(output)\n        return result\n    except subprocess.CalledProcessError as e:\n        print(\"Error:\", e.output)\n        return e.output\n    finally:\n        os.remove(\"tmp.py\")\n```",
        "問題分類 程式語法錯誤, 函數調用",
        "問題主體 __init__ 在 python 中是做什麼用的？ 和 C++ 的 constructor 有什麼差別？",
        "問題分類 程式語法說明, 建構子",
        "問題主體 from a import * 和 import a 有什麼差別？",
        "問題分類 程式語法說明, 模組導入",
        "問題主體 下面的程式碼中，safety_settings 的 type 是什麼：\n\n```\nsafety_settings = [    {        \"category\": \"HARM_CATEGORY_HARASSMENT\",        \"threshold\": \"BLOCK_NONE\"    },    {        \"category\": \"HARM_CATEGORY_HATE_SPEECH\",        \"threshold\": \"BLOCK_NONE\"    },    {        \"category\": \"HARM_CATEGORY_SEXUALLY_EXPLICIT\",        \"threshold\": \"BLOCK_NONE\"    },    {        \"category\": \"HARM_CATEGORY_DANGEROUS_CONTENT\",        \"threshold\": \"BLOCK_NONE\"    },    ]\n```",
        "問題分類 程式語言, 資料型態",
        "問題主體 __init__.py 的用處是什麼？",
        "問題分類 檔案結構, 模組導入",
        f"問題主體 {message}",
        "問題分類 ",
        ]
    
    # 呼叫 gemini API, 並回傳問題的回應
    response_text = await respond(message, chat_history)

    # 呼叫 gemini API, 並回傳問題的分類結果
    response_category = await respond(prompt_parts, chat_history)

    # 將提問的問題與問題的分類結果存入 csv 檔案
    current_working_directory = await save_to_csv(message, response_category)

    return f"{response_text}\n{response_category}"

    

async def respond(
    message,
    chat_history,
    *args,
    **kwargs,
):
    genai.configure(api_key=API_KEY)

    generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
    ]
    prompt = []
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    
    # 模型回應函式 (model_response)
    def model_response(text):
        data = {
            "role": "model",  # 指定角色為模型 (model)
            "parts": [{"text": f"{text}"}],  # 文字內容包含在 "text" 欄位
        }
        return data

    # 使用者輸入函式 (user_word)
    def user_word(text):
        data = {
            "role": "user",  # 指定角色為使用者 (user)
            "parts": [{"text": f"{text}"}],  # 文字內容包含在 "text" 欄位
        }
        return data
    
    # 對話歷史初始化
    def init_dialog(sentence):
        for i in sentence:
            user_input = user_word(i[0])
            model_output = model_response(i[1])
            prompt.append(user_input)
            prompt.append(model_output)

    init_dialog(chat_history)

    user_input = user_word(message)
    prompt.append(user_input)
    print(prompt)
    try:
        response = model.generate_content(prompt)
    except:
        raise ValueError(f"API response error: {response}")
    model_output = model_response(response.text)
    prompt.append(model_output)
    
    return response.text