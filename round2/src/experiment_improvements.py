from pathlib import Path
import html
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score, f1_score

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'round2' / 'data' / 'raw' / 'Labeled_Social_NLP_Training_Data.csv'

def clean_text(value):
    text = html.unescape(str(value))
    if '\\u' in text or '\\x' in text:
        try: text = text.encode('utf-8').decode('unicode_escape')
        except UnicodeDecodeError: pass
    text = re.sub(r'https?://\S+|www\.\S+', ' URLTOKEN ', text)
    text = re.sub(r'@\w+', ' USERTOKEN ', text)
    return re.sub(r'\s+', ' ', text).strip().lower()

def scores(y, p):
    return {'accuracy': accuracy_score(y,p), 'macro_f1': f1_score(y,p,average='macro',zero_division=0), 'weighted_f1': f1_score(y,p,average='weighted',zero_division=0)}

def make_model(kind, C, class_weight):
    if kind == 'word':
        features = TfidfVectorizer(ngram_range=(1,2), min_df=1, sublinear_tf=True, max_features=200000)
    elif kind == 'char':
        features = TfidfVectorizer(analyzer='char', ngram_range=(3,5), min_df=2, sublinear_tf=True, max_features=200000)
    else:
        features = FeatureUnion([
            ('word', TfidfVectorizer(ngram_range=(1,2), min_df=1, sublinear_tf=True, max_features=150000)),
            ('char', TfidfVectorizer(analyzer='char', ngram_range=(3,5), min_df=2, sublinear_tf=True, max_features=150000)),
        ])
    return Pipeline([('features', features), ('classifier', LogisticRegression(C=C, max_iter=2500, class_weight=class_weight, solver='lbfgs'))])

data = pd.read_csv(DATA, encoding='utf-8-sig')
data['clean_text'] = data['post_text'].map(clean_text)
groups = data['post_text'].astype(str)
a,b = next(GroupShuffleSplit(n_splits=1,test_size=.20,random_state=42).split(data,groups=groups))
tmp, test = data.iloc[a].copy(), data.iloc[b].copy()
a,b = next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=42).split(tmp,groups=tmp['post_text'].astype(str)))
train, val = tmp.iloc[a].copy(), tmp.iloc[b].copy()
print(f'split train={len(train)} val={len(val)} test={len(test)}')
results = {}
for target in ['sentiment_label','topic_category']:
    print(f'\nTARGET {target}')
    candidates=[]
    for kind in ['word','char','combined']:
        for C in [0.5, 1.0, 2.0, 4.0]:
            for cw in ['balanced', None]:
                candidates.append((kind,C,cw))
    best = None
    for kind,C,cw in candidates:
        m=make_model(kind,C,cw)
        m.fit(train.clean_text, train[target])
        pv=m.predict(val.clean_text)
        sv=scores(val[target],pv)
        print(f'VAL kind={kind:8} C={C:<3} cw={str(cw):8} acc={sv["accuracy"]:.4f} macro_f1={sv["macro_f1"]:.4f}')
        if best is None or sv['macro_f1'] > best[0]: best=(sv['macro_f1'],kind,C,cw,sv)
    _,kind,C,cw,sv=best
    final=make_model(kind,C,cw).fit(pd.concat([train.clean_text,val.clean_text]), pd.concat([train[target],val[target]]))
    pt=final.predict(test.clean_text)
    st=scores(test[target],pt)
    print(f'BEST {kind} C={C} cw={cw} validation={sv} TEST={st}')
    results[target]={'best_kind':kind,'C':C,'class_weight':cw,'validation':sv,'test':st}
print('\nSUMMARY')
print(results)
