import sys
from io import StringIO
from unittest import TestCase

from opendoors.utils import generate_email, print_progress


class Test(TestCase):
    def test_generate_email(self):
        result = generate_email("R!@andom~. nàØm", "", "Løng name of archive")
        self.assertEqual("RAndomNaomLongNameOfArchiveArchive@ao3.org", result)

    def test_print_progress(self):
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        for cur in range(0, 3):
            print_progress(cur, 3, "text")
        self.assertEqual("\r1/3 text\r2/3 text\r3/3 text\n", sys.stdout.getvalue(),
                         "should print out all the stages of progress separated by carriage returns without line feed.")
        sys.stdout = old_stdout  # Reset redirect.
