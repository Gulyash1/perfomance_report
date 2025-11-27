# import os
# import pytest
#
# import performance_report as pr
#
#
# # Behaviors covered:
# # 1) parse_args should error when a file path does not exist
# # 2) parse_args should error when a file does not have .csv extension
# # 3) parse_args should error when report type is not in allowed choices
# # 4) read_rows_from_files should read and merge rows from multiple CSV files
# # 5) build_performance_data should compute averages per position and sort desc
# # 6) display_report should print a GitHub table with two-decimal formatting
# # 7) main should integrate all steps and print the full table for provided CSVs
#
#
# def test_parse_args_errors_on_missing_file(capsys, tmp_path):
#     args = ["--files", str(tmp_path / "missing.csv"), "--report", "performance"]
#     with pytest.raises(SystemExit) as ex:
#         pr.parse_args(args)
#     assert ex.value.code == 2
#     err = capsys.readouterr().err
#     assert "Path doesn't exist" in err
#
#
# def test_parse_args_errors_on_incorrect_extension(capsys, tmp_path):
#     bad = tmp_path / "data.txt"
#     bad.write_text("name,position,performance\nA,Dev,4.0\n", encoding="utf-8")
#     args = ["--files", str(bad), "--report", "performance"]
#     with pytest.raises(SystemExit) as ex:
#         pr.parse_args(args)
#     assert ex.value.code == 2
#     err = capsys.readouterr().err
#     assert "Incorrect file format" in err
#
#
# def test_parse_args_errors_on_invalid_report(capsys, tmp_path):
#     good = tmp_path / "data.csv"
#     good.write_text("name,position,performance\nA,Dev,4.0\n", encoding="utf-8")
#     args = ["--files", str(good), "--report", "perfomance"]  # misspelled on purpose
#     with pytest.raises(SystemExit) as ex:
#         pr.parse_args(args)
#     assert ex.value.code == 2
#     err = capsys.readouterr().err
#     assert "invalid choice" in err
#
#
# def test_read_rows_from_files_merges_two_files(tmp_path):
#     f1 = tmp_path / "a.csv"
#     f2 = tmp_path / "b.csv"
#     content = (
#         "name,position,performance\n"
#         "Ann,Dev,4.0\n"
#         "Bob,QA,3.5\n"
#     )
#     f1.write_text(content, encoding="utf-8")
#     f2.write_text(
#         "name,position,performance\nCarl,DevOps,4.5\n", encoding="utf-8"
#     )
#     rows = pr.read_rows_from_files([str(f1), str(f2)])
#     assert len(rows) == 3
#     assert rows[0]["name"] == "Ann"
#     assert rows[-1]["position"] == "DevOps"
#
#
# def test_build_performance_data_averages_and_sorts():
#     rows = [
#         {"position": "Dev", "performance": "4.0"},
#         {"position": "Dev", "performance": "5.0"},
#         {"position": "QA", "performance": "3.0"},
#         {"position": "QA", "performance": "5.0"},
#         {"position": "Ops", "performance": "4.5"},
#     ]
#     data = pr.build_performance_data(rows)
#     # Expected averages: Dev=4.5, QA=4.0, Ops=4.5
#     assert data[0][1] >= data[1][1] >= data[2][1]
#     as_dict = {k: v for k, v in data}
#     assert pytest.approx(as_dict["Dev"], rel=1e-6) == 4.5
#     assert pytest.approx(as_dict["QA"], rel=1e-6) == 4.0
#     assert pytest.approx(as_dict["Ops"], rel=1e-6) == 4.5
#
#
# def test_display_report_prints_table(capsys):
#     pr.display_report([("Dev", 4.555), ("QA", 3.0)])
#     out = capsys.readouterr().out
#     # Headers present
#     assert "| Position" in out and "| Avg Performance |" in out
#     # Rows contain values with 2-decimal formatting
#     dev_line = next((ln for ln in out.splitlines() if "| Dev" in ln), "")
#     qa_line = next((ln for ln in out.splitlines() if "| QA" in ln), "")
#     assert "4.56" in dev_line
#     assert "3.00" in qa_line
#
#
# def test_main_integration_with_sample_csvs(capsys):
#     # Use the repository's sample CSVs
#     repo_root = os.path.dirname(__file__)
#     employees1 = os.path.join(repo_root, "employees1.csv")
#     employees2 = os.path.join(repo_root, "employees2.csv")
#
#     assert os.path.exists(employees1)
#     assert os.path.exists(employees2)
#
#     argv = [
#         "--files",
#         employees1,
#         employees2,
#         "--report",
#         "performance",
#     ]
#
#     pr.main(argv)
#     out = capsys.readouterr().out
#
#     # Headers exist
#     assert "| Position" in out and "| Avg Performance |" in out
#
#     # Backend Developer should be above DevOps Engineer
#     assert "Backend Developer" in out and "4.83" in out
#     assert "DevOps Engineer" in out and "4.80" in out
#     assert out.find("Backend Developer") < out.find("DevOps Engineer")
