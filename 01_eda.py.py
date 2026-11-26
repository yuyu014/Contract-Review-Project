import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import random

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)
random.seed(42)

# ==========================================
# 1. 构建真实的法律合同条款语料库
# ==========================================
no_risk_texts = [
    "本合同一式两份，甲乙双方各执一份，具有同等法律效力。",
    "本合同自双方签字或盖章之日起生效。",
    "双方在履行本合同过程中发生争议，应友好协商解决。",
    "本合同未尽事宜，由双方另行协商签订补充协议。",
    "附件为本合同不可分割的组成部分。"
]

low_risk_texts = [
    "乙方应当在收到货物后的七个工作日内完成验收。",
    "甲方应在每月的五号前结清上个月的服务费用。",
    "因不可抗力导致合同无法履行的，双方均不承担违约责任。",
    "未经对方书面同意，任何一方不得将本合同的权利义务转让给第三方。",
    "乙方需对在合作期间获知的甲方商业机密严格保密。"
]

medium_risk_texts = [
    "若乙方逾期交货，每逾期一日，需按合同总额的千分之五支付违约金。",
    "甲方有权根据实际业务需要对合同条款进行合理变更，并提前通知乙方。",
    "乙方保证其提供的产品不存在任何权利瑕疵，否则需赔偿甲方全部损失。",
    "如因乙方原因导致项目延期，甲方有权要求乙方退还部分已支付款项。"
]

high_risk_texts = [
    "最终解释权归甲方所有，乙方不得提出任何异议。",
    "若乙方逾期交货，需按合同总额的每日百分之十支付违约金。",
    "甲方有权随时单方面解除本合同且无需承担任何赔偿责任。",
    "乙方需承担无限连带责任，并放弃一切抗辩权。",
    "发生任何争议，均由甲方所在地法院管辖，乙方不得提出异议。"
]

# ==========================================
# 2. 模拟生成包含1000条记录的数据集
# ==========================================
# 设定比例：无风险65%，低风险25%，中风险8%，高风险2%
n_samples = 1000
risk_levels = ['无', '低', '中', '高']
risk_probs = [0.65, 0.25, 0.08, 0.02]
risk_data = np.random.choice(risk_levels, size=n_samples, p=risk_probs)

texts = []
for risk in risk_data:
    if risk == '无':
        base_text = random.choice(no_risk_texts)
    elif risk == '低':
        base_text = random.choice(low_risk_texts)
    elif risk == '中':
        base_text = random.choice(medium_risk_texts)
    else:
        base_text = random.choice(high_risk_texts)

    # 随机拼接1-3句话，模拟不同长度的段落
    repeat_times = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
    final_text = "".join(random.choices([base_text] + no_risk_texts, k=repeat_times))
    texts.append(final_text)

text_lengths = [len(t) for t in texts]

# 组装 DataFrame
df = pd.DataFrame({'text_content': texts, 'risk_level': risk_data, 'text_length': text_lengths})

# 保存为 CSV 文件 (utf-8-sig 防止 Excel 打开乱码)
df.to_csv('raw_contracts.csv', index=False, encoding='utf-8-sig')
print("真实感模拟数据已生成：raw_contracts.csv，共1000条。")

# ==========================================
# 3. 绘制 EDA 图表
# ==========================================
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='risk_level', order=['无', '低', '中', '高'], palette='Blues_r')
plt.title('图4-1 不同风险等级条款的数量分布', fontsize=14, pad=15)
plt.xlabel('风险等级', fontsize=12)
plt.ylabel('条款数量', fontsize=12)
plt.savefig('eda_bar.png', dpi=300, bbox_inches='tight')

plt.figure(figsize=(8, 5))
sns.boxplot(x=df['text_length'], color='skyblue')
plt.title('图4-2 条款文本长度分布箱线图', fontsize=14, pad=15)
plt.xlabel('条款文本长度（字数）', fontsize=12)
plt.savefig('eda_box.png', dpi=300, bbox_inches='tight')

print("EDA图表已生成：eda_bar.png, eda_box.png")