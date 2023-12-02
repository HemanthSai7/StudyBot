import torch

from transformers import (
    BitsAndBytesConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    pipeline,
)

import warnings

warnings.filterwarnings("ignore")


class EmbeddingModel:
    def __init__(self, model_name, generation_config):
        self.model_name = model_name
        self.generation_config = generation_config
        self.tokenizer = self._initialize_tokenizer()
        self.model = self._initialize_model()

    def _initialize_tokenizer(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True)
        tokenizer.pad_token = tokenizer.eos_token
        return tokenizer

    def _initialize_model(self):
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            trust_remote_code=True,
            device_map="auto",
            quantization_config=quantization_config,
        )
        return model

    def _initialize_generation_config(self):
        generation_config = GenerationConfig.from_pretrained(self.model_name)
        generation_config.max_new_tokens = 1024
        generation_config.temperature = 0.0001
        generation_config.top_p = 0.95
        generation_config.do_sample = True
        generation_config.repetition_penalty = 1.15
        return generation_config

    def _initialize_pipeline(self):
        pipeline_obj = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            return_full_text=True,
            generation_config=self.generation_config,
        )
        return pipeline_obj


# if __name__ == "__main__":
#     MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

#     text_generator = MyTextGenerator(
#         MODEL_NAME, MyTextGenerator._initialize_generation_config()
#     )
#     generated_text = text_generator.generate_text()
#     print(generated_text)
