import pandas as pd
import numpy as np
import random

# 设置随机种子保证每次生成结果一致
np.random.seed(42)
random.seed(42)

# 1. 构建真实的条款模板库
# 无风险（法律套话）
no_risk = [
    "本合同一式肆份，甲乙双方各执贰份，具有同等法律效力。",
    "本合同自双方法定代表人或授权代表签字并加盖公章之日起生效。",
    "本合同未尽事宜，双方可另行签订补充协议，补充协议与本合同具有同等效力。",
    "甲乙双方在履行本合同过程中如发生争议，应首先通过友好协商解决。",
    "本合同的附件与本合同正文具有同等法律效力。"
]

# 低风险（常规商业条款）
low_risk = [
    "乙方应于每月5日前向甲方提供上个月的服务总结报告。",
    "甲方在收到乙方开具的合法有效增值税专用发票后15个工作日内付款。",
    "如因不可抗力导致合同无法继续履行，双方均不承担违约责任。",
    "未经对方书面同意，任何一方不得将本合同项下的权利义务转让给第三方。",
    "乙方应对在合作期间获知的甲方商业秘密承担永久保密义务。"
]

# 中风险（需注意的条款）
medium_risk = [
    "若乙方未能按期交付成果，每逾期一日，应向甲方支付合同总额千分之五的违约金。",
    "甲方有权根据业务需要单方面调整服务范围，但应提前7天通知乙方。",
    "乙方需保证其提供的产品不侵犯任何第三方的知识产权，否则承担全部赔偿责任。",
    "合同期满后，如需续约，双方应提前30天书面通知对方。",
    "如甲方逾期付款，应按中国人民银行同期贷款利率向乙方支付滞纳金。"
]

# 高风险（霸王条款）
high_risk = [
    "本活动的最终解释权归甲方单方所有，乙方不得提出任何异议。",
    "若乙方违约，需按合同总额的每日百分之十支付违约金，并赔偿甲方所有间接损失。",
    "甲方有权随时单方面解除本合同，且无需承担任何违约或赔偿责任。",
    "乙方需对本合同项下的所有连带责任承担无限担保，且放弃一切抗辩权。",
    "因本合同引起的任何争议，均排他性地由甲方所在地法院管辖。"
]

# 2. 生成基础数据
n_samples = 1000
data = []

for i in range(n_samples):
    # 随机分配风险等级 (65%无, 25%低, 8%中, 2%高)
    risk_level = np.random.choice(['无', '低', '中', '高'], p=[0.65, 0.25, 0.08, 0.02])

    if risk_level == '无':
        text = random.choice(no_risk)
        c_type = random.choice(['效力条款', '争议解决', '其他'])
    elif risk_level == '低':
        text = random.choice(low_risk)
        c_type = random.choice(['付款条件', '保密义务', '其他'])
    elif risk_level == '中':
        text = random.choice(medium_risk)
        c_type = random.choice(['违约责任', '合同变更', '知识产权'])
    else:
        text = random.choice(high_risk)
        c_type = random.choice(['违约责任', '争议解决', '免责条款'])

    # 随机拼接额外套话，模拟不同长度的长文本
    if random.random() > 0.8:
        text = text + " " + random.choice(no_risk)

    contract_id = f"HT-2023-{i + 1:04d}"

    data.append({
        'contract_id': contract_id,
        'clause_id': f"C-{i + 1:04d}",
        'text_content': text,
        'clause_type': c_type,
        'risk_level': risk_level,
        'is_trap': True if risk_level == '高' else False
    })

df = pd.DataFrame(data)

# ==========================================
# 3. 故意注入“脏数据”，完美契合你的报告
# ==========================================

# 1. 注入约 1.2% 的缺失值 (clause_type)
missing_idx = np.random.choice(df.index, size=int(len(df) * 0.012), replace=False)
df.loc[missing_idx, 'clause_type'] = np.nan

# 2. 注入网页标签与多余换行 (格式噪声，约5%)
noise_idx = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
df.loc[noise_idx, 'text_content'] = df.loc[noise_idx, 'text_content'] + "<br>\n\n 附件内容请见下页。"

# 3. 注入异常短文本 (约0.5%)
short_idx = np.random.choice(df.index, size=int(len(df) * 0.005), replace=False)
df.loc[short_idx, 'text_content'] = "签字页"

# 4. 注入完全重复的行 (约3%)
duplicate_rows = df.sample(frac=0.03)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# 打乱顺序
df = df.sample(frac=1).reset_index(drop=True)

# 保存为 CSV
df.to_csv('contract_dataset.csv', index=False, encoding='utf-8-sig')
print(f"高仿真数据集已生成！总行数：{len(df)}。文件保存在当前目录下的 contract_dataset.csv")