from attention.Attention import subsequent_mask, try_attention
from attention.Plot import plot_mask, plot_encoding, plot_rates, plot_label_smoothing, plot_loss_smooth
from attention.Copier import train_copier
from attention.EN2DE import load_data
from attention.NN import make_model
# http://nlp.seas.harvard.edu/2018/04/03/attention.html


# plot_mask(subsequent_mask(20)[0])
# try_attention()
# plot_encoding()

#plot_rates()
#plot_label_smoothing()
#plot_loss_smooth()
#train_copier()

if __name__ == "__main__":
    from attention.Attention import MultiHeadedAttention
    from attention.Embedding import Embeddings, PositionalEncoding, greedy_decode
    from attention.EncoderDecoder import EncoderDecoder, Encoder, EncoderLayer, Decoder, DecoderLayer
    from attention.EncoderDecoder import SublayerConnection, LayerNorm
    from attention.NN import PositionwiseFeedForward, Generator
    load_data()
