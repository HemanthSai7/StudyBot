import tiktoken

def make_texts_tokenisation_safe(func):
    encoding = tiktoken.get_encoding("cl100k_base")
    special_tokens_set = encoding.special_tokens_set

    def remove_special_tokens(text):
        for token in special_tokens_set:
            text = text.replace(token, "")
        return text

    def wrapper(*args, **kwargs):
        documents = func(*args, **kwargs)
        for document in documents:
            document.page_content = remove_special_tokens(document.page_content)
        return documents

    return wrapper


# def remove_whitespace(func):
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         if isinstance(result, str):
#             return result.replace(" ", "").replace("\t", "").replace("\n", "")
#         elif isinstance(result, bytes):
#             return (
#                 result.decode("utf-8")
#                 .replace(" ", "")
#                 .replace("\t", "")
#                 .replace("\n", "")
#             )
#         return result

#     return wrapper
