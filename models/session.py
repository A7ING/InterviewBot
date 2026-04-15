from models.result import Result


class InterviewSession:
    def __init__(self, user_id, direction, questions):
        self.user_id = user_id
        self.direction = direction
        self.questions = questions
        self.current_index = 0
        self.result = Result()
        self.finished = False

    def get_current_question(self):
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def submit_answer(self, option_index):
        question = self.get_current_question()
        if question is None:
            return None

        is_correct = question.is_correct(option_index)
        user_answer = question.options[option_index]
        correct_answer = question.options[question.correct_option]

        if is_correct:
            self.result.correct_answers += 1
        else:
            self.result.wrong_answers += 1

        self.result.add_answer_detail(
            question_text=question.text,
            user_answer=user_answer,
            correct_answer=correct_answer,
            is_correct=is_correct,
        )

        self.current_index += 1

        if self.current_index >= len(self.questions):
            self.finished = True

        return is_correct