from tests.factories import QuestionFactory


def test_question_name():
    question = QuestionFactory.build()
    assert str(question) == f"{question.category.name}: {question.text}"
