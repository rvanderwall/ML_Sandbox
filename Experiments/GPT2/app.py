from scrape import scrape_guten
import gpt_2_simple as gpt2
import os

from Chat import Chatbot

model_name = "124M"
# training_text = "trainingtext.txt"
training_text = "GuideToTesting.txt"

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


def tune():
    sess = gpt2.start_tf_sess()
    gpt2.finetune(sess,
                  training_text,
                  model_name=model_name,
                  steps=10000)


def generate():
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name="run1", checkpoint_dir="./checkpoint")
    gpt2.generate(sess, length=200, run_name="run1", checkpoint_dir="./checkpoint")


def chat():
    bot = Chatbot("./checkpoint", "run1")
    bot.chat()


def main():
    print("Starting GPT")
    #prep()
    # tune()
    # generate()
    chat()

if __name__ == "__main__":
    main()