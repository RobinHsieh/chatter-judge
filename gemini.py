# 導入模組 (import)
import json
import requests
import time

# 定義 Google Cloud Generative Language API 的 API 金鑰 (API_KEY)
API_KEY = ""

# 定義對話狀態 (conversation_state)
conversation_state = {
  "contents": [],
  "safety_settings" : [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
}

# 生成回應函式 (generate_response)
def generate_response(data):
  """
  此函式利用 Google Cloud Generative Language API 生成對提示的回應，
  並考量對話狀態。

  參數:
    data: 要傳送至 API 的資料，包含提示內容及對話歷史.

  回傳值:
    來自 API 的回應內容 (JSON 格式).
  """

  # 建構 API 請求 URL
  url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}'

  # 設定 JSON 內容的標頭 (headers)
  headers = {'Content-Type': 'application/json'}

  # 使用 requests 函式送出 POST 請求至 API
  response = requests.post(url, headers=headers, json=data)

  # 解析來自 API 的 JSON 回應，並格式化以方便閱讀
  json_response = json.dumps(response.json(), indent=4, ensure_ascii=False)

  return json_response

# 模型回應函式 (model_response)
def model_response(text):
  """
  此函式將文字轉換成符合模型輸入格式的資料結構.

  參數:
    text: 要轉換的文字.

  回傳值:
    符合模型輸入格式的資料結構 (字典).
  """

  data = {
    "role": "model",  # 指定角色為模型 (model)
    "parts": [{"text": f"{text}"}]  # 文字內容包含在 "text" 欄位
  }
  return data

# 使用者輸入函式 (user_word)
def user_word(text):
  """
  此函式將文字轉換成符合使用者輸入格式的資料結構.

  參數:
    text: 要轉換的文字.

  回傳值:
    符合使用者輸入格式的資料結構 (字典).
  """

  data = {
    "role": "user",  # 指定角色為使用者 (user)
    "parts": [{"text": f"{text}"}]  # 文字內容包含在 "text" 欄位
  }
  return data

# 開始對話迴圈 (while loop)
while True:
  # 獲取使用者輸入 (user_input)
  user_input = input("請問您想說什麼？輸入 'end' 結束對話\n")
  if user_input.lower() == "end":  # 不分大小寫比較輸入是否為 "end"
    print("對話結束")
    break  # 退出迴圈

  # 將使用者輸入轉換成符合格式的資料 (user_word)
  user_input = user_word(user_input)

  # 更新對話狀態 (conversation_state)
  conversation_state['contents'].append(user_input)

  # 生成對使用者輸入的回應 (generate_response)
  response = generate_response(conversation_state)
  print(response)
  # 解析來自 API 的 JSON 回應 (response_data)
  response_data = json.loads(response)
  # 解析來自 API 的 JSON 回應 (response_data)
  generated_text = response_data["candidates"][0]['content']['parts'][0]['text']

  # 將生成的文字轉換成符合模型輸入格式的資料 (model_response)
  model_output = model_response(generated_text)

  # 更新對話狀態 (conversation_state)
  conversation_state['contents'].append(model_output)

  # 顯示生成的文字 (print)
  print(f"Gemini：{generated_text}")

# 添加延遲以方便閱讀
  time.sleep(1)
