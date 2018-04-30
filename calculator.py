import re
"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def args_string_to_int(*args):
    """ Convert args to ints
    args: a string that can be converted to int
    return: a list of int
    """
    operands = [int(i) for i in args]
    return operands


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    operands = args_string_to_int(*args)
    add_template = """<h2>Add</h2>
<p>The answer to {} + {} = {}</p>
"""
    body = add_template.format(*args, sum(operands))
    return body


def multiply(*args):
    operands = args_string_to_int(*args)
    product = 1
    for i in operands:
        product *= i
    multiply_template = """<h2>Multiply</h2>
<p>The answer to {} * {} = {}</p>
"""
    body = multiply_template.format(*args, product)
    return body


def subtract(*args):
    operands = args_string_to_int(*args)
    difference = 0
    loop_counter = 0
    for i in operands:
        if difference == 0:
            if loop_counter == 0:
                difference = i
                loop_counter += 1
        else:
            difference -= i
            loop_counter += 1
    subtract_template = """<h2>Subtract</h2>
<p>The answer to {} - {} = {}</p>
"""
    body = subtract_template.format(*args, difference)
    return body


def divide(*args):
    operands = args_string_to_int(*args)
    quotient = 1
    try:
        quotient = operands[0] / operands[1]
    except ZeroDivisionError:
        body = """<h1>Divide by zero</h1>

<p>The second number can not be 0, choose another.</p>
"""
        return body
    divide_template = """<h2>Divide</h2>
<p>The answer to {} / {} = {}</p>
"""
    body = divide_template.format(*args, quotient)
    return body


def home():
    body = '''<h2 style="margin-left: 80px;">HOW-TO-DOC FOR WSGI CALCULATOR</h2>

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
    return body


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    urls = [(r'^$', home),
            (r'^add/([\d]+)/([\d]+)$', add),
            (r'^multiply/([\d]+)/([\d]+)$', multiply),
            (r'^subtract/([\d]+)/([\d]+)$', subtract),
            (r'^divide/([\d]+)/([\d]+)$', divide), ]
    matchpath = path.lstrip('/')
    for regexp, func in urls:
        match = re.match(regexp, matchpath)
        if match is None:
            continue
        args = match.groups([])
        return func, args
    # we get here if no url matches
    raise NameError


def application(environ, start_response):

    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
