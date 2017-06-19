#! /usr/bin/env python3
"""
pcom.py test cases
"""

import os
import unittest
import shutil
import pcom

class TestGenCfg(unittest.TestCase):
    """test case class for gen_cfg function"""
    def setUp(self):
        self.tmp_cfg1_file = "/tmp/test_pcom1.cfg"
        self.tmp_cfg2_file = "/tmp/test_pcom2.cfg"
        cfg1_str = """\
[section1]
key1 = val1, val2
key2 = val3,
       val4
[section2]
key3 = val5
       val6
key4 = val7=val8
[section3]
key5 = 
# key6
key7
"""
        cfg2_str = """\
[section3]
key7 = val9
key8
[section4]
key9 = `~!@#$%%^&*()-_=+[{]}|;:'",<.>/?
"""
        with open(self.tmp_cfg1_file, "w") as tc1f:
            tc1f.write(cfg1_str)
        with open(self.tmp_cfg2_file, "w") as tc2f:
            tc2f.write(cfg2_str)
    def test_gen_cfg(self):
        """test case"""
        cfg = pcom.gen_cfg([self.tmp_cfg1_file, self.tmp_cfg2_file])
        self.assertEqual(cfg["section1"]["key1"], "val1, val2")
        self.assertEqual(cfg["section1"]["key2"], f"val3,{os.linesep}val4")
        self.assertEqual(cfg["section2"]["key3"], f"val5{os.linesep}val6")
        self.assertEqual(cfg["section2"]["key4"], "val7=val8")
        self.assertEqual(cfg["section3"]["key5"], "")
        self.assertNotIn("key6", cfg["section3"])
        self.assertEqual(cfg["section3"]["key7"], "val9")
        self.assertEqual(cfg["section3"]["key8"], None)
        self.assertEqual(cfg["section4"]["key9"], """`~!@#$%^&*()-_=+[{]}|;:'",<.>/?""")
    def tearDown(self):
        os.remove(self.tmp_cfg1_file)
        os.remove(self.tmp_cfg2_file)
        del self.tmp_cfg1_file
        del self.tmp_cfg2_file

class TestFindIter(unittest.TestCase):
    """test case for find_iter function"""
    def setUp(self):
        self.base_dir = "/tmp/test_pcom"
        os.makedirs(self.base_dir)
    def test_find_iter(self):
        """test case"""
        test_dir_tup = (
            f"{self.base_dir}{os.sep}test1",
            f"{self.base_dir}{os.sep}test2",
            f"{self.base_dir}{os.sep}test3")
        test_tup = (
            f"{self.base_dir}{os.sep}test.log",
            f"{self.base_dir}{os.sep}test.txt",
            f"{self.base_dir}{os.sep}test.cfg")
        test1_tup = (
            f"{test_dir_tup[0]}{os.sep}test1.log",
            f"{test_dir_tup[0]}{os.sep}test1.txt",
            f"{test_dir_tup[0]}{os.sep}test1.cfg")
        test2_tup = (
            f"{test_dir_tup[1]}{os.sep}test2.log",
            f"{test_dir_tup[1]}{os.sep}test2.txt",
            f"{test_dir_tup[1]}{os.sep}test2.cfg")
        test3_tup = (
            f"{test_dir_tup[2]}{os.sep}test3.log",
            f"{test_dir_tup[2]}{os.sep}test3.txt",
            f"{test_dir_tup[2]}{os.sep}test3.cfg")
        test_test_dir_tup = (f"{cc}{os.sep}test" for cc in test_dir_tup)
        for test_dir in test_dir_tup+test_test_dir_tup:
            os.makedirs(test_dir)
        for test_file in test_tup+test1_tup+test2_tup+test3_tup:
            open(test_file, "w").close()
        self.assertEqual(
            set(pcom.find_iter(self.base_dir, "*.log")),
            {test_tup[0], test1_tup[0], test2_tup[0], test3_tup[0]})
        self.assertEqual(
            set(pcom.find_iter(self.base_dir, "*test1*")),
            set(test1_tup))
        self.assertEqual(
            set(pcom.find_iter(self.base_dir, "*.log", True)),
            set())
        self.assertEqual(
            set(pcom.find_iter(self.base_dir, "*test*", True)),
            set(test_dir_tup+test_test_dir_tup))
        self.assertEqual(
            set(pcom.find_iter(self.base_dir, "*.log", cur_flg=True)),
            {test_tup[0]})
        self.assertEqual(
            set(pcom.find_iter(test_dir_tup[0], "*.log", cur_flg=True)),
            {test1_tup[0]})
        self.assertEqual(
            set(pcom.find_iter(self.base_dir, "*test*", True, True)),
            set(test_dir_tup))
    def tearDown(self):
        shutil.rmtree(self.base_dir)
        del self.base_dir

if __name__ == "__main__":
    unittest.main()
