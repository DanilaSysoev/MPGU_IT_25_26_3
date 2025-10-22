import validation


def test_password_min_length_enforced():
    res_short = validation.validate_password("short")
    assert isinstance(res_short, validation.PasswordValidationResult)
    assert not res_short.is_valid
    assert validation.ERR_LENGTH in res_short.errors

    res_ok = validation.validate_password("longenough1!")
    assert isinstance(res_ok, validation.PasswordValidationResult)
    assert res_ok.is_valid
    assert not res_ok.errors
