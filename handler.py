import os

from datasource import CsvDatasource
from datasource import SlackDatasource
from usecase import NotifyToSlack


def hello(event, context):
    try:
        # create datasource
        csv_datasource = CsvDatasource()
        slack_datasource = SlackDatasource()

        # get outside data
        read_csv_file = os.environ['READ_CSV_FILE']
        write_csv_file = os.environ['WRITE_CSV_FILE']

        # create usecase
        notify_to_slack = NotifyToSlack(
                csv_datasource=csv_datasource,
                slack_datasource=slack_datasource,
                read_csv_file=read_csv_file,
                write_csv_file=write_csv_file
                )

        # run usecase
        notify_to_slack.run()

    except Exception as e:
        raise e
