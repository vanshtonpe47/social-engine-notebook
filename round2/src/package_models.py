from pathlib import Path
import pickle

root = Path(__file__).resolve().parents[2]
models = root / 'round2' / 'models'
with (models / 'sentiment_model.pkl').open('rb') as f:
    sentiment = pickle.load(f)
with (models / 'topic_model.pkl').open('rb') as f:
    topic = pickle.load(f)
with (models / 'trained_models.pkl').open('wb') as f:
    pickle.dump({'sentiment_model': sentiment, 'topic_model': topic}, f, protocol=pickle.HIGHEST_PROTOCOL)
print(models / 'trained_models.pkl')
