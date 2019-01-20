import os

from datasource import CsvDatasource, SlackDatasource
from usecase import NotifyToSlack


def hello(event, context):
    try:
        # get outside data
        index_history_csv_file = os.environ['INDEX_HISTORY_CSV_FILE']
        settings_csv_file = os.environ['SETTINGS_CSV_FILE']

        # create datasource
        csv_datasource = CsvDatasource(
            settings_file=settings_csv_file,
            index_history_file=index_history_csv_file)
        slack_datasource = SlackDatasource()

        # create usecase
        notify_to_slack = NotifyToSlack(
            csv_datasource=csv_datasource, slack_datasource=slack_datasource)

        # run usecase
        notify_to_slack.run()

    except Exception as e:
        raise e


if __name__ == '__main__':
    for i in range(10):
        hello('', '')
