# OLD VERSION (using print for errors):
# except Exception as e:
#     session.rollback()
#     print(f"Помилка збереження історії: {e}")

import logging
from services.db import SessionLocal
from models.user_result import UserResult

logger = logging.getLogger(__name__)


class HistoryService:
    def save_test_result(self, user_id, username, category, result):
        session = SessionLocal()
        try:
            db_result = UserResult(
                user_id=user_id,
                username=username,
                category=category,
                score=result.total_score,
            )
            session.add(db_result)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save test result: {e}")
        finally:
            session.close()

    def format_user_history(self, target_user_id):
        session = SessionLocal()
        try:
            results = (
                session.query(UserResult)
                .filter(UserResult.user_id == target_user_id)
                .order_by(UserResult.timestamp.desc())
                .all()
            )

            if not results:
                return "Історія тестів порожня."

            report = "Ваші результати за весь час:\n\n"
            for r in results:
                report += f" {r.timestamp.strftime('%d.%m.%Y %H:%M')} | {r.category} | Бал: {r.score}\n"  # noqa: E501

            return report
        finally:
            session.close()
