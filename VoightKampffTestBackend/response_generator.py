import gpt_2_simple as gpt2
import os
import requests
import tensorflow as tf


class Response:
    def __init__(self):
        self.model = None

    def get_model(self, model_name="124M"):
        if not os.path.isdir(os.path.join("models", model_name)):
            print(f"Downloading {model_name} model...")
            gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/

        tf.compat.v1.reset_default_graph()
        sess = gpt2.start_tf_sess()

        gpt2.load_gpt2(sess)

        return sess

    def train_model(self):
        pass

    def get_response(self, sess, prompt="How can you prove you aren't an android?"):
        response = gpt2.generate(sess, prefix=prompt, nsamples=1, length=30, top_k=100,
                                 return_as_list=True)[0]
        return response


# if __name__ == '__main.py__':
sess = Response().get_model()
print(Response().get_response(sess=sess))
