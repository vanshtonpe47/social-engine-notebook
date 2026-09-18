from pathlib import Path
import html,re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline,FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score,f1_score
ROOT=Path(__file__).resolve().parents[2]; DATA=ROOT/'round2/data/raw/Labeled_Social_NLP_Training_Data.csv'
def clean(v):
 t=html.unescape(str(v)); t=re.sub(r'https?://\S+|www\.\S+',' URLTOKEN ',t); t=re.sub(r'@\w+',' USERTOKEN ',t); return re.sub(r'\s+',' ',t).strip().lower()
def sc(y,p): return {'accuracy':accuracy_score(y,p),'macro_f1':f1_score(y,p,average='macro',zero_division=0),'weighted_f1':f1_score(y,p,average='weighted',zero_division=0)}
def make(kind,ng,C,weight,clf):
 if kind=='char': f=TfidfVectorizer(analyzer='char',ngram_range=ng,min_df=2,max_features=300000,sublinear_tf=True)
 elif kind=='word': f=TfidfVectorizer(ngram_range=ng,min_df=1,max_features=300000,sublinear_tf=True)
 else: f=FeatureUnion([('w',TfidfVectorizer(ngram_range=(1,2),min_df=1,max_features=200000,sublinear_tf=True)),('c',TfidfVectorizer(analyzer='char',ngram_range=ng,min_df=2,max_features=200000,sublinear_tf=True))])
 if clf=='svm': c=LinearSVC(C=C,class_weight=weight)
 else: c=LogisticRegression(C=C,class_weight=weight,max_iter=3000,solver='lbfgs')
 return Pipeline([('features',f),('classifier',c)])
d=pd.read_csv(DATA,encoding='utf-8-sig'); d['clean']=d.post_text.map(clean); g=d.post_text.astype(str); a,b=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(d,groups=g)); tmp,test=d.iloc[a],d.iloc[b]; a,b=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=42).split(tmp,groups=tmp.post_text.astype(str))); tr,va=tmp.iloc[a],tmp.iloc[b]
configs=[]
for clf in ['logreg','svm']:
 for kind in ['char','combined']:
  for ng in [(2,5),(3,5),(3,6),(3,7),(2,6)]:
   for C in ([0.1,0.25,0.5,1.0] if clf=='svm' else [0.25,0.5,1.0]): configs.append((clf,kind,ng,C,'balanced'))
for target in ['sentiment_label','topic_category']:
 best=None; print('\nTARGET',target)
 for clf,kind,ng,C,w in configs:
  m=make(kind,ng,C,w,clf).fit(tr.clean,tr[target]); p=m.predict(va.clean); s=sc(va[target],p)
  print(clf,kind,ng,C,s)
  if best is None or s['macro_f1']>best[0]: best=(s['macro_f1'],clf,kind,ng,C,w,s)
 _,clf,kind,ng,C,w,vs=best; m=make(kind,ng,C,w,clf).fit(pd.concat([tr.clean,va.clean]),pd.concat([tr[target],va[target]])); p=m.predict(test.clean); ts=sc(test[target],p)
 print('BEST',{'classifier':clf,'kind':kind,'ngram':ng,'C':C,'validation':vs,'test':ts})
