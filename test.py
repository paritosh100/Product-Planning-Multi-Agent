from openai import OpenAI
import os; from dotenv import load_dotenv; load_dotenv()
c = OpenAI()
c.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":"hello"}])
