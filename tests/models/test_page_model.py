from tests.factories import PageFactory


def test_page_name():
    job = PageFactory.build()
    assert job.title == str(job)
