class StatisticsService:
    def __init__(self):
        self.user_stats = {}

    def save_result(self, user_id, result):
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                "tests_passed": 0,
                "total_correct": 0,
                "total_wrong": 0,
                "total_score": 0,
            }

        self.user_stats[user_id]["tests_passed"] += 1
        self.user_stats[user_id]["total_correct"] += result.correct_answers
        self.user_stats[user_id]["total_wrong"] += result.wrong_answers
        self.user_stats[user_id]["total_score"] += result.total_score

    def get_user_statistics(self, user_id):
        return self.user_stats.get(
            user_id,
            {
                "tests_passed": 0,
                "total_correct": 0,
                "total_wrong": 0,
                "total_score": 0,
            },
        )

    def format_user_statistics(self, user_id):
        stats = self.get_user_statistics(user_id)
        return (
            f"Ваші результати за весь час:\n\n"
            f"Пройдено тестів: {stats['tests_passed']}\n"
            f"Усього правильних відповідей: {stats['total_correct']}\n"
            f"Усього неправильних відповідей: {stats['total_wrong']}\n"
            f"Сумарний бал: {stats['total_score']}"
        )