"""``hello_ai.is_palindrome`` 的 pytest 测试。

重点覆盖边界情况：空串、单字符、只含空格/标点、大小写混用、
非字母数字字符、Unicode（中文/全角/casefold 展开）、超长字符串、
以及非字符串入参。
"""

import pytest

from hello_ai import is_palindrome

# 超长字符串用的构造片段
_LONG_HALF = "abcdefghij" * 100


# --------------------------------------------------------------------------- #
# 常规回文 / 非回文
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "text",
    [
        "racecar",
        "Level",
        "A man, a plan, a canal: Panama",
        "No 'x' in Nixon",
        "Was it a car or a cat I saw?",
        "Madam, I'm Adam.",
        "12321",
        "1 2 3 2 1",
        "A1b2b1a",
        "上海自来水来自海上",
        "人人为我我为人人",
        "a",
        "A",
        "7",
    ],
)
def test_palindrome_returns_true(text):
    """回文（含需忽略的大小写/空格/标点）应返回 True。"""
    assert is_palindrome(text) is True


@pytest.mark.parametrize(
    "text",
    [
        "hello",
        "abcdef",
        "ab",
        "Palindrome",  # 归一化成 "palindrome"，倒序不同
        "A man, a plan, a canal: Panamas",
        "1 2 3 4",
        "上海自来水来自海下",
        "!!hello?!",
    ],
)
def test_non_palindrome_returns_false(text):
    """非回文应返回 False。"""
    assert is_palindrome(text) is False


# --------------------------------------------------------------------------- #
# 边界情况：空与“空归一化”
# --------------------------------------------------------------------------- #
def test_empty_string_is_palindrome():
    """空串：递归定义下空序列是回文（没有需要比较的字符）。"""
    assert is_palindrome("") is True


@pytest.mark.parametrize(
    "text",
    [
        " ",
        "   ",
        "\t",
        "\n",
        "\r\n",
        "\u3000",  # 全角空格
        "!",
        "!!!",
        ",.;:",
        "... --- ...",
        "，。！？",  # 中文标点
        " \t\n!?，。 ",
    ],
)
def test_only_ignorable_characters_is_palindrome(text):
    """只含空格/标点时归一化为空串，按惯例视为回文。"""
    assert is_palindrome(text) is True


@pytest.mark.parametrize(
    "text",
    [
        "a",
        "Z",
        "  x  ",
        "\t中\n",
        "，a，",
        "€a€",  # 非字母数字符号被忽略
        "１",  # 全角数字，isalnum() 为 True
    ],
)
def test_single_meaningful_character_is_palindrome(text):
    """归一化后只剩一个字符 -> 必然是回文。"""
    assert is_palindrome(text) is True


# --------------------------------------------------------------------------- #
# 边界情况：大小写
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("AbBa", True),
        ("ABBA", True),
        ("abba", True),
        ("RaceCar", True),
        ("AbAb", False),
        ("aAbB", False),
    ],
)
def test_case_is_ignored(text, expected):
    """大小写差异不应影响判定结果。"""
    assert is_palindrome(text) is expected


def test_casefold_is_used_not_lower():
    """ß / ẞ 经 casefold 展开为 "ss"，因此是回文（仅用 lower() 会判错）。"""
    assert is_palindrome("ß") is True
    assert is_palindrome("ẞ") is True
    assert is_palindrome("Aaß") is False  # 归一化为 "aass"，倒序 "ssaa"


# --------------------------------------------------------------------------- #
# 边界情况：标点/空格只影响归一化，不改变原本的判定结果
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("clean", "noisy"),
    [
        ("abba", " a!b,b a "),
        ("racecar", "--race:car--"),
        ("12321", "1,2 3;2 1"),
        ("hello", "h_e_l_l_o"),
        ("hello", "  h.e.l.l.o  "),
    ],
)
def test_punctuation_does_not_change_result(clean, noisy):
    """同一字符串插入任意标点/空格后，判定结果应保持一致。"""
    assert is_palindrome(noisy) is is_palindrome(clean)

    # 下划线不是字母数字，会被忽略：判定结果应与去掉后一致
    if "_" in noisy:
        assert is_palindrome(noisy) is is_palindrome(noisy.replace("_", ""))


# --------------------------------------------------------------------------- #
# 边界情况：超长字符串
# --------------------------------------------------------------------------- #
def test_long_even_palindrome():
    """长度为 2000 的偶数长度回文。"""
    text = _LONG_HALF + _LONG_HALF[::-1]
    assert len(text) == 2000
    assert is_palindrome(text) is True


def test_long_palindrome_with_one_char_off():
    """超长回文里改动一个字符后应判定为非回文。"""
    text = _LONG_HALF + "Z" + _LONG_HALF[::-1]
    assert is_palindrome(text) is True
    # 追加一个字母会破坏对称性；追加标点则不会（标点被忽略）
    assert is_palindrome(text + "x") is False
    assert is_palindrome(text + "!") is True


def test_long_non_palindrome():
    """超长且不对称的字符串。"""
    assert is_palindrome(_LONG_HALF + _LONG_HALF) is False


# --------------------------------------------------------------------------- #
# 边界情况：入参类型与返回值类型
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "value",
    [
        None,
        123,
        12.5,
        ["a", "b"],
        ("a",),
        b"abab",
        {"a": 1},
        {1, 2},
    ],
)
def test_non_string_input_raises_type_error(value):
    """非字符串入参应抛出 TypeError，而不是静默返回错误结果。"""
    with pytest.raises(TypeError):
        is_palindrome(value)


def test_return_type_is_bool():
    """返回值必须是真正的 bool，而不是真值/假值对象。"""
    assert type(is_palindrome("abba")) is bool
    assert type(is_palindrome("abab")) is bool


def test_input_is_not_modified():
    """函数不应修改调用方传入的字符串。"""
    original = "A man, a plan, a canal: Panama"
    before = str(original)
    is_palindrome(original)
    assert original == before
