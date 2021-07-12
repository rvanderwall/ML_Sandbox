import os
import json

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds
import tensorflow_text as text  # A dependency of the preprocessing model
import tensorflow_addons as tfa
# from official.nlp import optimization
import matplotlib.pyplot as plt
import numpy as np

from official.modeling import tf_utils
from official import nlp
from official.nlp import bert

# Load the required submodules
import official.nlp.optimization
import official.nlp.bert.bert_models
import official.nlp.bert.configs
import official.nlp.bert.run_classifier
import official.nlp.bert.tokenization
import official.nlp.data.classifier_data_lib
import official.nlp.modeling.losses
import official.nlp.modeling.models
import official.nlp.modeling.networks


tf.get_logger().setLevel('ERROR')

if 'COLAB_TPU_ADDR' in os.environ and os.environ['COLAB_TPU_ADDR']:
    cluster_resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu='')
    tf.config.experimental_connect_to_cluster(cluster_resolver)
    tf.tpu.experimental.initialize_tpu_system(cluster_resolver)
    strategy = tf.distribute.TPUStrategy(cluster_resolver)
    print('Using TPU')
elif tf.test.is_gpu_available():
    strategy = tf.distribute.MirroredStrategy()
    print('Using GPU')
else:
    # raise ValueError('Running on CPU is not recommended.')
    print('Using CPU.  NOT RECOMMENDED')


def get_bert_folder():
    BERT_MODEL = "uncased_L-12_H-768_A-12"
    BERT_VERS = 3
    LCA_DIR = "/Users/rvanderwall/projects/AI_Team/construction-AI/Services/LCA/"
    local_bert = f"{LCA_DIR}/DescriptionProcessing/models/bert_en_{BERT_MODEL}_{BERT_VERS}"

    gs_folder_bert = f"gs://cloud-tpu-checkpoints/bert/v{BERT_VERS}/{BERT_MODEL}"
    print(tf.io.gfile.listdir(gs_folder_bert))
    hub_url_bert = f"https://tfhub.dev/tensorflow/bert_en_{BERT_MODEL}/{BERT_VERS}"
    return local_bert, gs_folder_bert


def get_bert_model(bert_dir):
    pass


def download_dataset():
    # Download a dataset
    glue, info = tfds.load('glue/mrpc', with_info=True,
                           # It's small, load the whole dataset
                           batch_size=-1)
    print("Downloaded to ~/tensorflow_datasets/glue/mrpc/1.0.0")
    return glue, info


def show_dataset(glue, info):
    print(list(glue.keys()))
    print(info.features)
    print(info.features['label'].names)
    glue_train = glue['train']
    for key, value in glue_train.items():
      print(f"{key:9s}: {value[0].numpy()}")


def get_tokenizer(path):
    tokenizer = bert.tokenization.FullTokenizer(
        vocab_file=os.path.join(path, "vocab.txt"),
         do_lower_case=True)
    print("Vocab size:", len(tokenizer.vocab))
    tokens = tokenizer.tokenize("Hello TensorFlow!")
    print(tokens)
    ids = tokenizer.convert_tokens_to_ids(tokens)
    print(ids)
    # The model expects its two input sentences concatonated with these separator tokens
    tokenizer.convert_tokens_to_ids(['[CLS]', '[SEP]'])
    return tokenizer


def encode_sentence(tokenizer, s):
    tokens = list(tokenizer.tokenize(s))
    tokens.append('[SEP]')
    return tokenizer.convert_tokens_to_ids(tokens)


def show_bert_info(s1, s2, inputs):
    print("Sentence1 shape:", s1.shape.as_list())
    print("Sentence2 shape:", s2.shape.as_list())

    input_word_ids = inputs['input_word_ids']
    plt.pcolormesh(input_word_ids)
    plt.show()

    input_mask = inputs['input_mask']
    plt.pcolormesh(input_mask)
    plt.show()

    input_type_ids = inputs['input_type_ids']
    plt.pcolormesh(input_type_ids)
    plt.show()


def bert_encode(tokenizer, glue_dict):
    sentence1 = tf.ragged.constant([encode_sentence(tokenizer, s) for s in np.array(glue_dict["sentence1"])])
    sentence2 = tf.ragged.constant([encode_sentence(tokenizer, s) for s in np.array(glue_dict["sentence2"])])

    # Prepend the classifier token
    cls = [tokenizer.convert_tokens_to_ids(['[CLS]'])] * sentence1.shape[0]
    input_word_ids = tf.concat([cls, sentence1, sentence2], axis=-1)

    # Differentiate between content and padding
    input_mask = tf.ones_like(input_word_ids).to_tensor()

    # Differentiate between sentence 1 and sentence 2
    type_cls = tf.zeros_like(cls)
    type_s1 = tf.zeros_like(sentence1)
    type_s2 = tf.ones_like(sentence2)
    input_type_ids = tf.concat([type_cls, type_s1, type_s2], axis=-1).to_tensor()

    inputs = {
          'input_word_ids': input_word_ids.to_tensor(),
          'input_mask': input_mask,
          'input_type_ids': input_type_ids}

    # show_bert_info(sentence1, sentence2, inputs)
    return inputs


def main2():
    local_bert, gs_bert = get_bert_folder()
    glue, info = download_dataset()
    # show_dataset(glue, info)
    tokenizer = get_tokenizer(f"{local_bert}/assets")

    glue_train = bert_encode(tokenizer, glue['train'])
    glue_train_labels = glue['train']['label']

    glue_validation = bert_encode(tokenizer, glue['validation'])
    glue_validation_labels = glue['validation']['label']

    # glue_test = bert_encode(tokenizer, glue['test'])
    # glue_test_labels  = glue['test']['label']

    bert_config_file = f"{local_bert}/bert_config.json"
    config_dict = json.loads(tf.io.gfile.GFile(bert_config_file).read())

    bert_config = bert.configs.BertConfig.from_dict(config_dict)
    bert_classifier, bert_encoder = bert.bert_models.classifier_model(bert_config, num_labels=2)
    tf.keras.utils.plot_model(bert_classifier, show_shapes=True, dpi=48)
    tf.keras.utils.plot_model(bert_encoder, show_shapes=True, dpi=48)

    checkpoint = tf.train.Checkpoint(encoder=bert_encoder)
    checkpoint.read(
        os.path.join(gs_bert, 'bert_model.ckpt')).assert_consumed()

    # Set up epochs and steps
    epochs = 1
    batch_size = 32
    eval_batch_size = 32

    train_data_size = len(glue_train_labels)
    steps_per_epoch = int(train_data_size / batch_size)
    num_train_steps = steps_per_epoch * epochs
    warmup_steps = int(epochs * train_data_size * 0.1 / batch_size)

    # creates an optimizer with learning rate schedule
    optimizer = nlp.optimization.create_optimizer(
        2e-5, num_train_steps=num_train_steps, num_warmup_steps=warmup_steps)

    metrics = [tf.keras.metrics.SparseCategoricalAccuracy('accuracy', dtype=tf.float32)]
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    bert_classifier.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=metrics)

    bert_classifier.fit(
        glue_train, glue_train_labels,
        validation_data=(glue_validation, glue_validation_labels),
        batch_size=32,
        epochs=epochs)

    my_examples = bert_encode(
        glue_dict={
            'sentence1': [
                'The rain in Spain falls mainly on the plain.',
                'Look I fine tuned BERT.'],
            'sentence2': [
                'It mostly rains on the flat lands of Spain.',
                'Is it working? This does not match.']
        },
        tokenizer=tokenizer)

    result = bert_classifier(my_examples, training=False)

    result = tf.argmax(result).numpy()
    print(result)

    export_dir = './saved_models'
    tf.saved_model.save(bert_classifier, export_dir=export_dir)

    glue_batch = {key: val[:10] for key, val in glue_train.items()}

    res = bert_classifier(glue_batch, training=True).numpy()
    print(res)

    result = bert_classifier(my_examples, training=False)

    result = tf.argmax(result).numpy()
    print(result)


if __name__ == "__main__":
    main2()
    # preprocessor = build_model()
    # sample(preprocessor)
    pass
