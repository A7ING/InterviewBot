import html


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
            f"<b>Тест завершено.</b>\n\n"
            f"Правильних відповідей: {self.correct_answers}\n"
            f"Неправильних відповідей: {self.wrong_answers}\n"
            f"Підсумковий бал: <b>{self.total_score}</b>"
        )

    def show_detailed_result(self):
        lines = [self.show_result(), "", "<b>Детальна статистика:</b>"]

        for index, item in enumerate(self.answer_details, start=1):
            mark = "✓" if item["is_correct"] else "✗"
            safe_question = html.escape(str(item["question_text"]))
            safe_user_answer = html.escape(str(item["user_answer"]))
            safe_correct_answer = html.escape(str(item["correct_answer"]))

            lines.append(
                f"<b>{index}.</b> {mark} {safe_question}\n"
                f"   Ваша відповідь: <i>{safe_user_answer}</i>\n"
                f"   Правильна відповідь: <i>{safe_correct_answer}</i>"
            )
        return "\n\n".join(lines)
