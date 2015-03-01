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


@when('I go to "{path}"')
def go_hello(context, path):
    context.page = context.client.get(path)


@then('I get the response "{response}"')
def get_hello(context, response):
    assert context.page.data == bytes(response, 'utf-8'), \
        "Expected %s, got %s" % (response, str(context.page.data))
