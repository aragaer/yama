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


@given('I have the following memos for date {date}')
def insert_memos_for_date(context, date):
    raise NotImplementedError('STEP: Given I have the following memos for date {date}')


@when('I access the resource \'{path}\'')
def access_resource(context, path):
    raise NotImplementedError('STEP: When I access the resource \'{path}\'')


@then('I get the following list of memos')
def check_memos_result(context):
    raise NotImplementedError('STEP: Then I get the following list of memos')
