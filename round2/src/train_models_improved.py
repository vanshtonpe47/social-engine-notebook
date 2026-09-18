from pathlib import Path
import html, json, pickle, re
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score

ROOT=Path(__file__).resolve().parents[2]; R=ROOT/'round2'; DATA=R/'data/raw/Labeled_Social_NLP_Training_Data.csv'; MODELS=R/'models'; FIGS=R/'figures'; REPORTS=R/'reports'
for p in (MODELS,FIGS,REPORTS): p.mkdir(parents=True,exist_ok=True)

def clean_text(v):
    t=html.unescape(str(v))
    if '\\u' in t or '\\x' in t:
        try:t=t.encode('utf-8').decode('unicode_escape')
        except UnicodeDecodeError:pass
    t=re.sub(r'https?://\S+|www\.\S+',' URLTOKEN ',t); t=re.sub(r'@\w+',' USERTOKEN ',t)
    return re.sub(r'\s+',' ',t).strip().lower()

def scores(y,p):
    return {'accuracy':accuracy_score(y,p),'macro_precision':precision_score(y,p,average='macro',zero_division=0),'macro_recall':recall_score(y,p,average='macro',zero_division=0),'macro_f1':f1_score(y,p,average='macro',zero_division=0),'weighted_f1':f1_score(y,p,average='weighted',zero_division=0)}

def model(kind,C,weight):
    if kind=='char': feats=TfidfVectorizer(analyzer='char',ngram_range=(3,5),min_df=2,sublinear_tf=True,max_features=200000)
    else: feats=FeatureUnion([('word',TfidfVectorizer(ngram_range=(1,2),min_df=1,sublinear_tf=True,max_features=150000)),('char',TfidfVectorizer(analyzer='char',ngram_range=(3,5),min_df=2,sublinear_tf=True,max_features=150000))])
    return Pipeline([('features',feats),('classifier',LogisticRegression(C=C,max_iter=2500,class_weight=weight,solver='lbfgs'))])

data=pd.read_csv(DATA,encoding='utf-8-sig'); data['clean_text']=data.post_text.map(clean_text); groups=data.post_text.astype(str)
a,b=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(data,groups=groups)); tmp,test=data.iloc[a].copy(),data.iloc[b].copy(); a,b=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=42).split(tmp,groups=tmp.post_text.astype(str))); train,val=tmp.iloc[a].copy(),tmp.iloc[b].copy()
results={}
configs={'sentiment_label':{'kind':'combined','C':1.0,'weight':None,'prefix':'sentiment'},'topic_category':{'kind':'char','C':0.5,'weight':'balanced','prefix':'topic'}}
for target,cfg in configs.items():
    candidates={}
    for kind,C,weight in ([('word',1.0,None),('word',2.0,'balanced'),('char',1.0,'balanced'),('combined',0.5,None),('combined',1.0,None),('combined',2.0,None)] if target=='sentiment_label' else [('word',1.0,'balanced'),('char',0.5,'balanced'),('char',1.0,'balanced'),('combined',1.0,'balanced'),('combined',2.0,'balanced')]):
        m=model(kind,C,weight).fit(train.clean_text,train[target]); pv=m.predict(val.clean_text); candidates[f'{kind}_C{C}_cw{weight}']=scores(val[target],pv)
    final=model(cfg['kind'],cfg['C'],cfg['weight']).fit(pd.concat([train.clean_text,val.clean_text]),pd.concat([train[target],val[target]])); pred=final.predict(test.clean_text); sc=scores(test[target],pred); labels=sorted(test[target].unique()); report=classification_report(test[target],pred,labels=labels,output_dict=True,zero_division=0); cm=confusion_matrix(test[target],pred,labels=labels)
    with open(MODELS/f"{cfg['prefix']}_model.pkl",'wb') as f: pickle.dump(final,f)
    plt.figure(figsize=(8,6)); plt.imshow(cm,cmap='Blues'); plt.title(f"{cfg['prefix'].title()} Confusion Matrix\nModel: {cfg['kind']}"); plt.colorbar(); plt.xticks(range(len(labels)),labels,rotation=45,ha='right'); plt.yticks(range(len(labels)),labels); plt.xlabel('Predicted label'); plt.ylabel('True label')
    for i in range(len(labels)):
        for j in range(len(labels)): plt.text(j,i,cm[i,j],ha='center',va='center')
    plt.tight_layout(); plt.savefig(FIGS/f"{cfg['prefix']}_confusion_matrix.png",dpi=180,bbox_inches='tight'); plt.close()
    err=test.loc[test[target].to_numpy()!=pred,['text_id','post_text',target]].copy(); err['predicted_label']=pred[test[target].to_numpy()!=pred]; err.to_csv(REPORTS/f"{cfg['prefix']}_errors.csv",index=False)
    results[cfg['prefix']]={'target':target,'selected_model':f"{cfg['kind']}_tfidf_logistic_regression",'training_records':len(train),'validation_records':len(val),'testing_records':len(test),'train_validation_text_overlap':len(set(train.post_text)&set(val.post_text)),'train_test_text_overlap':len(set(train.post_text)&set(test.post_text)),'validation_model_comparison':candidates,'final_test_scores':sc,'classification_report':report,'confusion_matrix_labels':labels,'confusion_matrix':cm.tolist(),'model_file':str(MODELS/f"{cfg['prefix']}_model.pkl"),'confusion_matrix_file':str(FIGS/f"{cfg['prefix']}_confusion_matrix.png"),'error_file':str(REPORTS/f"{cfg['prefix']}_errors.csv")}
    print(cfg['prefix'],sc)
with open(REPORTS/'metrics.json','w',encoding='utf-8') as f: json.dump(results,f,indent=2)
print('Wrote improved models, metrics, figures, and error reports.')
