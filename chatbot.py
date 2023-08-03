import torch
from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM
from Shared.constants import MODEL_NAME
import os

class PetalsModel:
    def __init__(self):
        os.environ["TOKENIZERS_PARALLELISM"] = "true"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.fake_token = self.tokenizer("^")["input_ids"][0]  # Workaround to make tokenizer.decode() keep leading spaces
        self.model = self._model

    @property
    def _model(self):
        m = AutoDistributedModelForCausalLM.from_pretrained(MODEL_NAME)
        return m.cuda()

    def text_session(self):
        with self.model.inference_session(max_length=512) as sess:
            while True:
                prompt = input('Human: ')
                if prompt == "":
                    break
                prefix = f"Human: {prompt}\nFriendly AI:"
                prefix = self.tokenizer(prefix, return_tensors="pt")["input_ids"].cuda()
                print("Friendly AI:", end="", flush=True)

                while True:
                    outputs = self.model.generate(prefix, max_new_tokens=1, session=sess,
                                             do_sample=True, temperature=0.1, top_p=0.6)
                    outputs = self.tokenizer.decode([self.fake_token, outputs[0, -1].item()])[1:]

                    # Now, let's print one new token at a time
                    print(outputs, end="", flush=True)

                    if "<\n>" in outputs:
                        break
                    prefix = None  # Prefix is passed only for the 1st token of the bot's response
