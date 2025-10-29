import validation

"""
Политика «набор символов»:
- хотя бы одна буква (a–zA–Z) -> ERR_LETTER
- хотя бы одна цифра (0–9)    -> ERR_DIGIT
- хотя бы один спецсимвол     -> ERR_SPECIAL
"""


def test_password_must_contain_letter_digit_special():
    res = validation.validate_password("OnlyLetters!")
    assert not res.is_valid
    assert validation.ERR_DIGIT in res.errors

    res = validation.validate_password("12345678123456!")
    assert not res.is_valid
    assert validation.ERR_LETTER in res.errors

    res = validation.validate_password("AbcdefgrtuerD1")
    assert not res.is_valid
    assert validation.ERR_SPECIAL in res.errors

    res = validation.validate_password("AbcdefghrtyeE1!")
    assert res.is_valid
    assert not res.errors
