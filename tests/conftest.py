import pytest

TEST_DATA_1 = """name,position,performance
Ann,DevOps,4.0
Bob,QA,3.5
Mike,Backend,4.0
Jason,Frontend,3.8
Molly,QA,3.6"""

TEST_DATA_2 = """name,position,performance
Carl,DevOps,4.5
Jake,Backend,4.2
Lily,Frontend,4.0
Morgan,QA,3.7"""

@pytest.fixture(scope="session")
def session_test_data(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test_data")
    (temp_dir / 'test_data_1.csv').write_text(TEST_DATA_1)
    (temp_dir / 'test_data_2.csv').write_text(TEST_DATA_2)
    return temp_dir


@pytest.fixture(scope="session")
def session_test_files(session_test_data):
    return [str(session_test_data / 'test_data_1.csv'), str(session_test_data / 'test_data_2.csv')]


