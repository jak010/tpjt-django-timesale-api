import os
import sys

import pytest
#
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#
# sys.path.append(PROJECT_ROOT)
# sys.path.append(PROJECT_ROOT + "/src")
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
#
# import django
#
# django.setup()


@pytest.fixture
def django_db_setup():
    """ 테스트용 DB를 생성하지 않도록 처리 """
    pass
