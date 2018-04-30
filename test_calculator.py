''' Run this test using pytest '''
import calculator
from pytest import raises


def test_resolve_path_home():
    '''  Ensure input of ('/') returns home func and no args'''
    result = calculator.resolve_path('/')
    assert 'function home' in str(result)
    assert '()' in str(result)


def test_resolve_path_add():
    '''Ensure that input of ('/add/2/5') returns a function = 'add' and
    args of (2, 5)
    '''
    result = calculator.resolve_path('/add/2/5')
    assert 'function add' in str(result)
    assert "('2', '5')" in str(result)


def test_resolve_path_no_match():
    with raises(NameError):
        calculator.resolve_path('/Python/Rocks/really')


def test_add():
    """ Test that add() returns the sum of the arguments"""
    result = calculator.add(2, 3)
    print("result is ", result)
    assert result == """<h2>Add</h2>
<p>The answer to 2 + 3 = 5</p>
"""


def test_add_with_zeros():
    result = calculator.add(0, 0)
    assert result == """<h2>Add</h2>
<p>The answer to 0 + 0 = 0</p>
"""


def test_multiply():
    result = calculator.multiply(2, 3)
    assert result == """<h2>Multiply</h2>
<p>The answer to 2 * 3 = 6</p>
"""


def test_add_with_negs():
    result = calculator.add(-3, -4)
    assert result == """<h2>Add</h2>
<p>The answer to -3 + -4 = -7</p>
"""


def test_add_with_mixed_pos_negs():
    result = calculator.add(-3, 2)
    assert result == """<h2>Add</h2>
<p>The answer to -3 + 2 = -1</p>
"""


def test_subtract_with_mixed_pos_negs():
    result = calculator.subtract(-3, 2)
    assert result == """<h2>Subtract</h2>
<p>The answer to -3 - 2 = -5</p>
"""


def test_divide_by_zero():
    result = calculator.divide(1, 0)
    assert result.startswith("<h1>Divide by zero</h1>")
    assert result.endswith(
        "<p>The second number can not be 0, choose another.</p>\n")


def test_divide_numerator_zero():
    result = calculator.divide(0, 1)
    assert '<h2>Divide</h2>' in result
    assert '<p>The answer to 0 / 1 = 0.0</p>' in result


def test_home():
    result = calculator.home()
    assert result == '''<h2 style="margin-left: 80px;">HOW-TO-DOC FOR WSGI CALCULATOR</h2>

<ul>
    <li>To add 2 + 3, navigate to:
    <ul>
        <li>/add/2/3</li>
    </ul>
    </li>
    <li>To multiply 3 * 4, navigate to:
    <ul>
        <li>/multiply/3/4</li>
    </ul>
    </li>
    <li>To subtract 3 - 4, navigate to:
    <ul>
        <li>/subtract/3/4</li>
        <li>/subtract/-3/4</li>
    </ul>
    </li>
    <li>To divide 3/4 navigate to:
    <ul>
        <li>/divide/3/4</li>
        <li>/divide/-3/4</li>
    </ul>
    </li>
</ul>
'''
