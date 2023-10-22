import openai


class OpenAICompletor:
    # user: question
    # assistant: answer
    def __init__(self):
        self.messages = []

    def answer(self, question):
        self._add_questoin(question)
        ans = self._get_completion()
        self._add_answer(ans)
        return self._last_message()

    def _last_message(self):
        return self.messages[-1]['content']

    def _add_questoin(self, question):
        self.messages.append({'role':'user', 'content':question})

    def _add_answer(self, answer):
        self.messages.append({'role':'assistant', 'content':answer})

    def _get_completion(self):
        response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        # model = 'gpt-4',
        messages = self.messages,
        temperature = 0,
        )
        return response.choices[0].message['content']
