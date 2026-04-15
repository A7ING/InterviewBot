class Result:
    def __init__(self):
        self.correct_answers = 0
        self.wrong_answers = 0
        self.answer_details = []

    @property
    def total_score(self):
        return self.correct_answers * 10

    def add_answer_detail(self, question_text, user_answer, correct_answer, is_correct):
        self.answer_details.append(
            {
                "question_text": question_text,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
            }
        )

    def show_result(self):
        return (
            f"Тест завершено.\n\n"
            f"Правильних відповідей: {self.correct_answers}\n"
            f"Неправильних відповідей: {self.wrong_answers}\n"
            f"Підсумковий бал: {self.total_score}"
        )

    def show_detailed_result(self):
        lines = [self.show_result(), "", "Правильні відповіді:"]

        for index, item in enumerate(self.answer_details, start=1):
            mark = "✓" if item["is_correct"] else "✗"
            lines.append(
                f"{index}. {mark} {item['question_text']}\n"
                f"   Ваша відповідь: {item['user_answer']}\n"
                f"   Правильна відповідь: {item['correct_answer']}"
            )

        return "\n\n".join(lines)