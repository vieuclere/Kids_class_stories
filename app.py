import streamlit as st
import openai
from pypinyin import lazy_pinyin, Style
from zhconv import convert

st.title("🧒 中文識字故事生成器")
st.write("輸入一些常用字，生成一篇適合孩子閱讀的小故事。")

openai.api_key = st.secrets["openai_api_key"]

char_input = st.text_input("請輸入可使用的中文字（例如：我你他小山水火）")
story_theme = st.text_input("故事主題或角色（可選）", placeholder="小龍、山、香蕉⋯")

if st.button("生成故事") and char_input:
    with st.spinner("正在寫故事，請稍候⋯"):
        prompt = (
            f"請用以下中文字創作一篇適合學齡兒童閱讀的小故事：{char_input}。"
            f"主題：{story_theme if story_theme else '自由發揮'}。"
            "字數約150字，內容有趣、友善，適合台灣孩子閱讀。"
        )
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        story = response["choices"][0]["message"]["content"]

        st.subheader("📝 繁體中文")
        st.write(story)

        def add_zhuyin(text):
            from pypinyin import pinyin, BOPOMOFO
            zhuyin_text = ""
            for word, py in zip(text, pinyin(text, style=BOPOMOFO, errors='ignore')):
                zhuyin_text += f"<ruby>{word}<rt>{py[0]}</rt></ruby>" if py else word
            return zhuyin_text

        st.subheader("🔤 注音")
        st.markdown(f"<div style='font-size: 1.5em; line-height: 2.2;'>{add_zhuyin(story)}</div>", unsafe_allow_html=True)

        st.subheader("🇨🇳 简体中文")
        st.write(convert(story, 'zh-cn'))

        pinyin_text = ' '.join(lazy_pinyin(story, style=Style.TONE))
        st.subheader("📣 拼音")
        st.markdown(f"<div style='font-size: 1.3em;'>{pinyin_text}</div>", unsafe_allow_html=True)
