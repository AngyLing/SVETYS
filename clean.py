import joblib

data = joblib.load('shved_vocab.pkl')

for k in range(len(data)):
    if '&&' in data[k]:
        print(data[k])
        data[k] = data[k].replace('&&', '&')
joblib.dump(data, 'shved_vocab.pkl')
