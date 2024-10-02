def fromArabicNumeralsToChineseNumerals(number: int):
    digits = "零一二三四五六七八九"
    tens = "十"

    if number < 10:
        return digits[number]

    unitDigit = number % 10
    if number < 20:
        if unitDigit == 0:
            return tens
        return tens + digits[unitDigit]

    tenDigit = number // 10
    if unitDigit == 0:
        return digits[tenDigit] + tens

    return digits[tenDigit] + tens + digits[unitDigit]
