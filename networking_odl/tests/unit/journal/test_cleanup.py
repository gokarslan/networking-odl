#
# Copyright (C) 2017 Red Hat, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#

import mock

from networking_odl.db import db
from networking_odl.journal.cleanup import JournalCleanup
from networking_odl.tests.unit import test_base_db


class JournalCleanupTestCase(test_base_db.ODLBaseDbTestCase):
    def _journal_cleanup_object(self, retention):
        self.cfg.config(completed_rows_retention=retention, group='ml2_odl')
        return JournalCleanup()

    def test_delete_completed_rows_retries_exceptions(self):
        journal_cleanup = self._journal_cleanup_object(1)
        with mock.patch.object(db, 'delete_rows_by_state_and_time') as m:
            self._test_retry_exceptions(
                journal_cleanup.delete_completed_rows, m, True)

    def test_cleanup_processsing_rows_retries_exceptions(self):
        journal_cleanup = self._journal_cleanup_object(1)
        with mock.patch.object(db, 'reset_processing_rows') as m:
            self._test_retry_exceptions(
                journal_cleanup.cleanup_processing_rows, m, True)