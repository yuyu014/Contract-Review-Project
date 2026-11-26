import pandas as pd
import re

def clean_text(text):
    # 去除HTML标签和特殊符号
    text = re.sub(r'<.*?>', '', text)
    return text.strip()

# 读取原始数据
df = pd.read_csv('raw_contracts.csv')
initial_len = len(df)

# 清洗与过滤
df['text_content'] = df['text_content'].apply(clean_text)
# 过滤短文本
df = df[df['text_content'].str.len() > 10]
# 去重
df = df.drop_duplicates(subset=['text_content'])
final_len = len(df)

# 保存清洗后的数据
df.to_csv('cleaned_contracts.csv', index=False, encoding='utf-8-sig')
print(f"清洗完成，样本量从 {initial_len} 降至 {final_len}")