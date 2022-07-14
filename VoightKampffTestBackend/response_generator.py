import gpt_2_simple as gpt2
import os
import requests
import tensorflow as tf


class Response:
    def __init__(self):
        self.sess = None

    def get_model(self, model_name="124M"):
        if not os.path.isdir(os.path.join("models", model_name)):
            print(f"Downloading {model_name} model...")
            gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/

        tf.compat.v1.reset_default_graph()

        if self.sess == None:
            self.sess = gpt2.start_tf_sess()
        else:
            self.sess = gpt2.reset_session(self.sess)

        gpt2.load_gpt2(self.sess)
        return self.sess


    def train_model(self, sess, file, **kwargs):
        if kwargs.get("model_name"):
            model_name = kwargs.get("model_name")
        else:
            model_name = "124M"

        if kwargs.get("steps"):
            steps = kwargs.get("steps")
        else:
            steps = 5

        gpt2.finetune(sess,
              file,
              model_name=model_name,
              steps=steps,
              restore_from ='fresh',
              learning__rate = 1e-5,
              print_model = 1,
              sample_every = 1,
              save_every = 3,
              reuse=True)


        return sess

  def get_response(self, sess, prompt="How can you prove you aren't an android?", length=30, temperature=0.7):
        response = gpt2.generate(sess, prefix=prompt, nsamples=1, length=length, top_k=100, temperature=temperature

                                 return_as_list=True)[0]
        return response


if __name__ == '__main__':
    sess = Response().get_model()
    print(Response().get_response(sess=sess))
