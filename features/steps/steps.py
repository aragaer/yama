from datetime import date
from os import path


@then('a file for today date should exist in "{directory}" with')
def verify_today_file(context, directory):
    filename = date.today().isoformat()+".txt"
    filepath = path.join(directory, filename)
    context.execute_steps('''
    Then a file named "{path}" should exist
    And the file "{path}" should contain:
    """
    {text}
    """'''.format(path=filepath, text=context.text))


@when(u'I go to "{path}"')
def go_to_hello(context, path):
    context.response = context.app.get(path)


@then(u'I get the response "{text}"')
def step_impl(context, text):
    assert context.response.html.text == text, \
        "Expected '%s', got '%s'" % (text, context.response.html)
