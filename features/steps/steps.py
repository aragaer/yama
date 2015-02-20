from freezegun import freeze_time

@given('current date is "{date}"')
def freeze_date(context, date):
    context.freezer = freeze_time(date)
    context.freezer.start()
