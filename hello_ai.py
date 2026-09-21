#写一个函数，判断字符串是否回文，忽略大小写，空格和标点


def _normalize(text: str) -> str:
    """只保留字母与数字，并用 casefold 统一大小写。

    ``casefold()`` 比 ``lower()`` 更彻底（例如 "ß" -> "ss"）。

    Args:
        text: 原始字符串。

    Returns:
        归一化后的字符串。
    """
    return "".join(char.casefold() for char in text if char.isalnum())


def is_palindrome(text: str) -> bool:
    """判断字符串是否回文，忽略大小写、空格和标点。

    Args:
        text: 待判断的字符串。

    Returns:
        是回文返回 ``True``，否则返回 ``False``。空串或只含空格/标点的
        字符串，归一化后为空串，按惯例视为回文。

    Raises:
        TypeError: ``text`` 不是字符串时。
    """
    if not isinstance(text, str):
        raise TypeError(f"text 必须是 str，实际收到 {type(text).__name__}")

    normalized = _normalize(text)
    return normalized == normalized[::-1]


if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama"))  # True