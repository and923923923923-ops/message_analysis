import os
import openai
from youtube_transcript_api import YouTubeTranscriptApi

client = openai.OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

def get_content(input_text):
    if "youtube.com" in input_text or "youtu.be" in input_text:
        video_id = input_text.split("v=")[-1].split("&")[0] if "v=" in input_text else input_text.split("/")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-TW', 'zh-HK', 'zh-Hans'])
        return " ".join([i['text'] for i in transcript])
    return input_text

def get_reflection(content):
    prompt = "你是一位深耕教會三十年的資深基督徒，請對以下內容進行深度反思（包含磨練的價值與行動決心），直接以第一人稱寫出內在對話："
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}]
    )
    return response.choices[0].message.content

with open("input.txt", "r", encoding="utf-8") as f:
    user_input = f.read().strip()

if user_input:
    content = get_content(user_input)
    reflection = get_reflection(content)
    with open("reflection.md", "a", encoding="utf-8") as f:
        f.write(f"\n\n## 靈修反思紀錄\n{reflection}\n\n---\n")