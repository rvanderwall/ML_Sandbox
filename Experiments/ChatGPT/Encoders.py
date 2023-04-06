import torch


class Encoder:
    def __init__(self, char_set, verbose=False):
        self.char_set = char_set

        stoi = {ch: i for i, ch in enumerate(char_set)}
        itos = {i: ch for i, ch in enumerate(char_set)}
        self.encode = lambda s: [stoi[c] for c in s]
        self.decode = lambda l: ''.join([itos[i] for i in l])

        if verbose:
            e = self.encode("hello world ABC")
            print(e)
            print(self.decode(e))

    @property
    def vocab_size(self):
        return len(self.char_set)

    def get_encoded_data(self, text):
        data = torch.tensor(self.encode(text), dtype=torch.long)
        return data

    def show_decoded_text(self, tokens):
        new_text = self.decode(tokens[0].tolist())
        print(new_text)
