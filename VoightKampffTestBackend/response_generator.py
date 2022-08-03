import gpt_2_simple as gpt2
import os
import tensorflow as tf

class Response:
    def __init__(self):
        self.sess = None

    def get_model(self, model_name="124M", run_name="run1"):

        # checks if model is already saved and if not downloads it

        if not os.path.isdir(os.path.join("models", model_name)):
            print(f"Downloading {model_name} model...")
            gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/


        # checks if there is an existing checkpoint, and if not creates one with the base model

        if not os.path.isdir(os.path.join("checkpoint", run_name)):
            print(f"Creating checkpoint files")
            gpt2.download_gpt2(model_name=model_name, model_dir=os.path.join("checkpoint", run_name)) #base checkpoint is saved under the name of run_name

        tf.compat.v1.reset_default_graph()

        if self.sess == None:
            self.sess = gpt2.start_tf_sess()
            reuse = False
        else:
            self.sess = gpt2.reset_session(self.sess)
            reuse = True


        gpt2.load_gpt2(self.sess, run_name=run_name, reuse=reuse)
        return self.sess


    def train_model(self, sess, file, run_name='run3', **kwargs):
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
              restore_from ='latest',
              reuse=True,
              run_name=run_name)


        return sess

    def get_response(self, sess, prompt="How can you prove you aren't an android?", length=50, temperature=0.8, top_k=40, run_name='run1'):

        response = gpt2.generate(sess, prefix=prompt, nsamples=1, length=length, temperature=temperature, top_k=top_k, run_name=run_name,
                                 return_as_list=True,include_prefix=False,truncate="<|endoftext|>")[0]
        return response


if __name__ == '__main__':
    sess = Response().get_model(run_name='run3')
    # sess = Response().train_model(sess=sess, file='raw_data/preprozcessed_data/training_text.csv', steps=10000)
    print(Response().get_response(sess=sess, prompt="What improved your quality of life so much, you wish you did it sooner?", top_k=5000, run_name='run3'))
