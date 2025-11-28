import os
import sys
import pytest
from tabulate import tabulate

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import performance_report as pr
def test_args_multiple_files(session_test_files):
    args = pr.parse_args(['--files', *session_test_files, '--report', 'performance'])

    assert args.report == 'performance'
    assert args.files == session_test_files

def test_args_no_files(capsys):
    with pytest.raises(SystemExit):
        pr.parse_args(['--report', 'performance'])
    assert 'the following arguments are required: --files' in capsys.readouterr().err

def test_args_no_report_name(capsys, session_test_files):
    with pytest.raises(SystemExit):
        pr.parse_args(['--files', *session_test_files])
    assert 'the following arguments are required: --report' in capsys.readouterr().err

def test_no_args(capsys):
    with pytest.raises(SystemExit):
        pr.parse_args([])
    assert "the following arguments are required: --files, --report" in capsys.readouterr().err

def test_file_not_exists(capsys, session_test_files, session_test_data):
    paths = session_test_files + ([str(session_test_data / 'non_existent.csv')])
    with pytest.raises(SystemExit):
        pr.parse_args(['--files', *paths, '--report', 'performance'])
    assert "Path doesn't exist" in capsys.readouterr().err

def test_incorrect_file_format(capsys, session_test_files, session_test_data):
    bad = session_test_data / 'bad.txt'
    bad.write_text('dummy', encoding='utf-8')
    paths = session_test_files + ([str(bad)])
    with pytest.raises(SystemExit):
        pr.parse_args(['--files', *paths, '--report', 'performance'])
    err = capsys.readouterr().err
    assert "Incorrect file format (.txt):" in err

def test_read_rows_from_files_merges_two_files(session_test_files):
    rows = pr.read_rows_from_files(session_test_files)
    assert len(rows) == 9
    assert rows[0]["name"] == "Ann"
    assert rows[-1]["position"] == "QA"

def test_build_performance_data_averages_and_sorts(session_test_files):
    rows = pr.read_rows_from_files(session_test_files)
    data = pr.build_data(rows)
    assert data[0][1] >= data[1][1] >= data[2][1]
    print(data)
    as_dict = {k: v for k, v in data}
    assert pytest.approx(as_dict["DevOps"], rel=1e-6) == 4.25
    assert pytest.approx(as_dict["Backend"], rel=1e-6) == 4.1
    assert pytest.approx(as_dict["Frontend"], rel=1e-6) == 3.9
    assert pytest.approx(as_dict["QA"], rel=1e-6) == 3.6

def test_display_report(capsys, session_test_files):
    rows = pr.read_rows_from_files(session_test_files)
    data = pr.build_data(rows)
    expected_table = tabulate(
        [
            ("DevOps", "4.25"),
            ("Backend", "4.1"),
            ("Frontend", "3.9"),
            ("QA", "3.6")
        ],
        headers=["Position", "Avg Performance"],
        tablefmt="github"
    )
    pr.display_report(data)
    capt = capsys.readouterr().out
    assert capt.strip() == expected_table.strip()
