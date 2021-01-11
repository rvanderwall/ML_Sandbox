from GPT2.scrape import scrape_guten
import gpt_2_simple as gpt2
import os

from GPT2.Chat import chat

model_name = "124M"
training_text = "trainingtext.txt"
# Download from https://github.com/minimaxir/gpt-2-simple


def prep():
    if not os.path.isdir(os.path.join("models", model_name)):
        print(f"Downloading {model_name} model...")
        gpt2.download_gpt2(model_name=model_name)
    if not os.path.isfile(training_text):
        scrape_guten(training_text)


def tune_from_scratch():
    pass
    # Find gpt2.py in Python37/Lib/site-packages/gpt-2-simple
    # Around line 136, def finetune()
    # change restore_from='latest'
    # to     restore_from='fresh'


def generate():
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, model_name='124M')
    gpt2.generate(sess, model_name='124M')


def tune():
    sess = gpt2.start_tf_sess()
    gpt2.finetune(sess,
                  training_text,
                  model_name=model_name,
                  steps=50)


def main():
    print("Starting GPT")
    prep()
    # tune()
    # generate()
    chat(model_name=model_name)

if __name__ == "__main__":
    main()