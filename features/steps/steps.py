from datetime import date
import json
from os import path
from time import sleep

from freezegun import freeze_time


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


@given('I have the following memos for date {date}')
def insert_memos_for_date(context, date):
    container = context.storage.get_container(date)
    for line in context.text.splitlines():
        container.post(line)
        if context.debug:
            print("Posted '%s' to container %s" % (line, date))


@when('I access the resource \'{path}\'')
def access_resource(context, path):
    context.response = context.app.get(path)


@then('I get the following list of memos')
def check_memos_result(context):
    if context.debug:
        print(context.response.json)
    result = context.response.json
    expected = context.text.splitlines()

    assert result == expected, \
        "Expected:\n%s\ngot:\n%s" % (expected, result)


@when('I wait for 1 second')
def wait(context):
    sleep(1)


@given('the date is \'{date}\'')
def freeze_date(context, date):
    context.freezer = freeze_time(date)
    context.freezer.start()


@when('I post to \'{resource}\' the following text')
def post_data_to_resource(context, resource):
    context.response = context.app.post(resource, context.text)


@then('I have the following memos for date {date}')
def check_memos(context, date):
    container = context.storage.get_container(date)
    existing = list(container.messages)
    expected = context.text.splitlines()
    assert existing == expected, \
        "Expected %s, got %s" % (expected, existing)
