from app import ParseResult
import pytest

def test_parse_result_valid():
    obj = ParseResult(skills=["python","fastapi"], score=88, reasons="solid match")
    assert obj.score == 88
    assert "python" in obj.skills

def test_parse_result_score_bounds():
    with pytest.raises(Exception):
        ParseResult(skills=["python"], score=101, reasons="nope")
