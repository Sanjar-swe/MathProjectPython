import pytest
from apps.models import BotUser, Question, TestAttempt as ModelTestAttempt, AttemptDetail, BotState
from django.db.utils import IntegrityError

@pytest.mark.django_db
class TestBotUserModel:
    def test_create_bot_user(self):
        user = BotUser.objects.create(
            telegram_id=123456789,
            full_name="Test User",
            username="testuser"
        )
        assert user.telegram_id == 123456789
        assert user.full_name == "Test User"
        assert user.username == "testuser"
        assert str(user) == "Test User"

    def test_duplicate_telegram_id(self):
        BotUser.objects.create(telegram_id=123, full_name="User 1")
        with pytest.raises(IntegrityError):
            BotUser.objects.create(telegram_id=123, full_name="User 2")

@pytest.mark.django_db
class TestQuestionModel:
    def test_create_question(self):
        question = Question.objects.create(
            text="What is 2+2?",
            option_a="3",
            option_b="4",
            option_c="5",
            option_d="6",
            correct_answer="b"
        )
        assert question.text == "What is 2+2?"
        assert question.correct_answer == "b"
        assert question.is_active is True
        assert str(question) == "What is 2+2?"

@pytest.mark.django_db
class TestTestAttemptModel:
    def test_create_attempt(self):
        user = BotUser.objects.create(telegram_id=1, full_name="U")
        attempt = ModelTestAttempt.objects.create(
            user=user,
            score=8,
            total_questions=10
        )
        assert attempt.user == user
        assert attempt.score == 8
        assert str(attempt) == "U - 8/10"

@pytest.mark.django_db
class TestAttemptDetailModel:
    def test_create_detail(self):
        user = BotUser.objects.create(telegram_id=1, full_name="U")
        attempt = ModelTestAttempt.objects.create(user=user)
        question = Question.objects.create(
            text="Q", option_a="a", option_b="b", option_c="c", option_d="d", correct_answer="a"
        )
        detail = AttemptDetail.objects.create(
            attempt=attempt,
            question=question,
            user_answer="a",
            is_correct=True
        )
        assert detail.is_correct is True
        assert str(detail) == f"U - {question.id} (True)"

@pytest.mark.django_db
class TestBotStateModel:
    def test_create_state(self):
        state = BotState.objects.create(
            user_id=111,
            chat_id=222,
            state="some_state",
            data={"key": "value"}
        )
        assert state.user_id == 111
        assert state.state == "some_state"
        assert state.data["key"] == "value"
