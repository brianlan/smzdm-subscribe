import sys
sys.path.append('..')

from ..message_mail import sendmail


def test_send_mail():
    sendmail('hello rlan', 'rongyilan@126.com', ['brianlan@163.com'], 'hello rlan')
