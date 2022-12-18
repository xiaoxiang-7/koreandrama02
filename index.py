import firebase_admin
from firebase_admin import credentials, firestore

import requests
from bs4 import BeautifulSoup

def update_data():
  # 初始化 Firebase
  cred = credentials.Certificate("serviceAccountKey.json")
  firebase_admin.initialize_app(cred)
  db = firestore.client()

  # 爬取網頁資料
  url = "https://jumi.tv/show/23.html"
  data = requests.get(url)
  data.encoding = "utf-8"
  sp = BeautifulSoup(data.text, "html.parser")

  # 列出 "最新韓劇" 集合中的所有文件
  docs = db.collection("最新韓劇").list_documents()

  # 個別刪除每筆文件
  for doc in docs:
    doc.delete()

  h4_titles = sp.find_all("h4", class_="title")
  for h4_title in h4_titles[:10]:
    text = h4_title.text # 取出 h4 標題的文字內容
    link = "https://jumi.tv/" + h4_title.find("a").get("href") # 取出 h4 標題的文字超連結

    # 使用韓劇名稱作為文件 ID
    movie_id = text

    doc = {
      "text": text, #最新韓劇名稱
      "link": link  #最新韓劇網址
    }
    doc_ref = db.collection("最新韓劇").document(movie_id)
    doc_ref.set(doc)

# 設定 Vercel Worker
exports.handler = update_data