import pandas as pd
import jieba
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report

# 1. 读取数据并分词
df = pd.read_csv('cleaned_contracts.csv')
df['words'] = df['text_content'].apply(lambda x: " ".join(jieba.cut(x)))

# 2. 划分数据集 (8:1:1)
X_train, X_test, y_train, y_test = train_test_split(df['words'], df['risk_level'], test_size=0.2, random_state=42)

# 3. TF-IDF 向量化
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 4. 训练 SVM 基线模型
svm = SVC(kernel='linear', class_weight='balanced')
svm.fit(X_train_vec, y_train)

# 5. 预测与评估
y_pred = svm.predict(X_test_vec)
print("====== 基线模型评估结果 ======")
print(classification_report(y_test, y_pred))