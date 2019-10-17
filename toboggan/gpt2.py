import torch
import torch.nn.functional as F
import numpy as np

from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer


_MODEL_NAME = "gpt2-large" # other options: "gpt2", "gpt2-large", etc.
_SEED = 3189


class _GPT2:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        np.random.seed(_SEED)
        torch.manual_seed(_SEED)
        
        self.tokenizer = GPT2Tokenizer.from_pretrained(_MODEL_NAME)
        self.model = GPT2LMHeadModel.from_pretrained(_MODEL_NAME)
        self.model.to(self.device)
        self.model.eval()

    def sample_sequence(self, input_text: str):
        num_samples = 1
        repetition_penalty = 1
        top_k = 40
        top_p = 1

        context_tokens = self.tokenizer.encode(input_text)
        context = torch.tensor(context_tokens, dtype=torch.long, device=self.device)
        context = context.unsqueeze(0).repeat(num_samples, 1)
        generated = context

        with torch.no_grad():
            while 1:
                inputs = {'input_ids': generated}
                outputs = self.model(**inputs)
                next_token_logits = outputs[0][0, -1, :] / 1.

                # reptition penalty from CTRL (https://arxiv.org/abs/1909.05858)
                for _ in set(generated):
                    next_token_logits[_] /= repetition_penalty
                
                filtered_logits = _top_k_top_p_filtering(next_token_logits, top_k=top_k, top_p=top_p)
                next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)

                generated = torch.cat((generated, next_token.unsqueeze(0)), dim=1)

                yield self.tokenizer.decode(generated[0,
                    len(context_tokens):].tolist()[-1], True, True)



def _top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float('Inf')):
    """ Filter a distribution of logits using top-k and/or nucleus (top-p) filtering
        Args:
            logits: logits distribution shape (vocabulary size)
            top_k > 0: keep only top k tokens with highest probability (top-k filtering).
            top_p > 0.0: keep the top tokens with cumulative probability >= top_p (nucleus filtering).
                Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
        From: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
    """
    assert logits.dim() == 1  # batch size 1 for now - could be updated for more but the code would be less clear
    top_k = min(top_k, logits.size(-1))  # Safety check
    if top_k > 0:
        # Remove all tokens with a probability less than the last token of the top-k
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = filter_value
    return logits


GPT2 = _GPT2()
