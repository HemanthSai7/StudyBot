# class A:
#     def __init__(self):
#         self._bill = 1

#     @property
#     def bill(self):
#         return self._bill

#     @bill.setter
#     def bill(self,value):
#         self._bill = value
#         # raise PermissionError("You can't change the bill")

# class B(A):
#     def __init__(self):
#         super().__init__()
#         self._bill = 2

# # b = B()
# # print(b.bill)
# a=A()
# a.bill=3
# print(a.bill)

# if "uploaded_pdf" in st.session_state.keys():
#     # chatbot
#     st.subheader("Ask Studybot a question! 🤖")

#     if "messages" not in st.session_state.keys():
#         st.session_state.messages = [
#             {
#                 "role": "assistant",
#                 "content": "What's troubling you? Ask me a question right away!",
#             }
#         ]

#     # Display or clear chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     def clear_chat_history():
#         st.session_state.messages = [
#             {
#                 "role": "assistant",
#                 "content": "What's troubling you? Ask me a question right away!",
#             }
#         ]

#     st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

#     def generate_mistral_response(question: str):
#         for dict_message in st.session_state.messages:
#             if dict_message["role"] == "user":
#                 question = dict_message["content"]

#         answer = requests.post(
#             "https://hemanthsai7-studybotapi.hf.space/api/inference",
#             json={"promptMessage": question},
#         ).json()

#         return answer

# User-provided prompt
# if prompt := st.chat_input(
#     disabled=not st.session_state.messages[-1]["role"] == "assistant",
#     placeholder="Hello, please ask me a question! 🤖"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.write(prompt)

# # ask question
# st.write(st.session_state)

# # Generate a new response if last message is not from assistant
# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             response = generate_mistral_response(prompt)
#             placeholder = st.empty()
#             full_response = ""
#             for item in response:
#                 full_response += item
#                 placeholder.markdown(full_response)
#             placeholder.markdown(full_response)
#     message = {"role": "assistant", "content": full_response}
#     st.session_state.messages.append(message)