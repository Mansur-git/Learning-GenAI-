import tiktoken

def tokenizer_for_openAI_models(text,model):
    encoder = tiktoken.encoding_for_model(model)
    #print(f'Total number of tokens in {model} : {encoder.n_token}')
    tokens = encoder.encode(text)
    return tokens

print(tokenizer_for_openAI_models('Hello world!','gpt-4o'))

