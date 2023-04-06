v1_config = {
    "train_data_file": "/Users/rvanderwall/Downloads/tiny_shakespear/train.txt",

    # Model characteristics
    "vocab_size": 66,
    "embedding_dims": 36,   # (384),
    "head_size": 36,        # Keep same as embedding
    "num_heads": 6,         # each head will end up being head_size // num_heads
    "block_size": 32,       # (256) context length (Time steps)
    "num_layers": 6,        # Number of attention blocks

    # Training parameters
    "split": 0.9,
    "epochs": 10000,
    "batch_size": 64,
    "eval_iters": 200,
    "learning_rate": 3e-4,
    "dropout": 0.2
}


class Config:
    def __init__(self, cfg_json):
        self.json = cfg_json
        self.train_data_file = cfg_json["train_data_file"]

        self.vocab_size = cfg_json["vocab_size"]
        self.embedding_dims = cfg_json["embedding_dims"]
        self.head_size = cfg_json["head_size"]
        self.num_heads = cfg_json["num_heads"]
        self.block_size = cfg_json["block_size"]
        self.num_layers = cfg_json["num_layers"]

        self.device = None
        self.split = cfg_json["split"]
        self.epochs = cfg_json["epochs"]
        self.batch_size = cfg_json["batch_size"]
        self.eval_iters = cfg_json["eval_iters"]
        self.learning_rate = cfg_json["learning_rate"]
        self.dropout = cfg_json["dropout"]

    def clone(self):
        return Config(dict(self.json))
