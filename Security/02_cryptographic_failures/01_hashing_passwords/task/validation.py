from dataclasses import dataclass, field


ERR_LENGTH = "length"
ERR_LETTER = "requires_letter"
ERR_DIGIT = "requires_digit"
ERR_SPECIAL = "requires_special"


@dataclass
class PasswordValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.is_valid


'''
Требуется проверить минимальную длину пароля (>= 12 символов) и
наличие в пароле хотя бы одной буквы, цифры и спецсимвола.
'''
def validate_password(password: str) -> PasswordValidationResult:
    return PasswordValidationResult(is_valid=True)
