import torch.cuda

from ChatGPT.Batching import Batcher
from ChatGPT.Config import v1_config, Config
from ChatGPT.Bigram import BigramLanguageModel
from ChatGPT.Encoders import Encoder
from ChatGPT.Preprocess import PreProc
from ChatGPT.Trainer import Trainer


cfg = Config(v1_config)
cfg.device = 'cuda' if torch.cuda.is_available() else 'cpu'

pp = PreProc("ssp", cfg.train_data_file, verbose=False)
e = Encoder(pp.chars)
assert e.vocab_size == cfg.vocab_size
m = BigramLanguageModel(cfg)
b = Batcher(cfg)
t = Trainer(cfg, e, m, b)

train_data, val_data = t.get_train_test_data(pp.text)
print(f'training data:{train_data.shape}')
print(f'testing data:{val_data.shape}')
# b.show_one_batch(train_data)

seq = m.gen_from_scratch(100)
print(e.decode(seq[0].tolist()))

t.train(train_data, val_data)

seq = m.gen_from_scratch(300)
print(e.decode(seq[0].tolist()))
