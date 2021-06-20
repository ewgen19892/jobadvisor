from tests.factories import QAFactory


def test_qa_name():
    qa = QAFactory.build()
    assert str(qa) == f"QA: {qa.pk}"
