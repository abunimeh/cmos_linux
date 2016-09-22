#! /usr/bin/env python3

import pcom
import unittest
import os
import shutil

class TestGenCfg(unittest.TestCase):
    def setUp(self):
        self.tmp_cfg1_file = '/tmp/test_pcom1.cfg'
        self.tmp_cfg2_file = '/tmp/test_pcom2.cfg'
        cfg1_str = '''\
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
'''
        cfg2_str = '''\
[section3]
key7 = val9
key8
[section4]
key9 = `~!@#$%%^&*()-_=+[{]}\|;:'",<.>/?
'''
        with open(self.tmp_cfg1_file, 'w') as f:
            f.write(cfg1_str)
        with open(self.tmp_cfg2_file, 'w') as f:
            f.write(cfg2_str)
    def test_gen_cfg(self):
        cfg = pcom.gen_cfg([self.tmp_cfg1_file, self.tmp_cfg2_file])
        self.assertEqual(cfg['section1']['key1'], 'val1, val2')
        self.assertEqual(cfg['section1']['key2'], 'val3,'+os.linesep+'val4')
        self.assertEqual(cfg['section2']['key3'], 'val5'+os.linesep+'val6')
        self.assertEqual(cfg['section2']['key4'], 'val7=val8')
        self.assertEqual(cfg['section3']['key5'], '')
        self.assertNotIn('key6', cfg['section3'])
        self.assertEqual(cfg['section3']['key7'], 'val9')
        self.assertEqual(cfg['section3']['key8'], None)
        self.assertEqual(cfg['section4']['key9'],
                         '''`~!@#$%^&*()-_=+[{]}\|;:'",<.>/?''')
    def tearDown(self):
        os.remove(self.tmp_cfg1_file)
        os.remove(self.tmp_cfg2_file)
        del self.tmp_cfg1_file
        del self.tmp_cfg2_file

class TestFindIter(unittest.TestCase):
    def setUp(self):
        self.base_dir = '/tmp/test_pcom'
        os.makedirs(self.base_dir)
    def test_find_iter(self):
        test_log = self.base_dir+os.sep+'test.log'
        test_txt = self.base_dir+os.sep+'test.txt'
        test_cfg = self.base_dir+os.sep+'test.cfg'
        test1_dir = self.base_dir+os.sep+'test1'
        test2_dir = self.base_dir+os.sep+'test2'
        test3_dir = self.base_dir+os.sep+'test3'
        test1_log = test1_dir+os.sep+'test1.log'
        test1_txt = test1_dir+os.sep+'test1.txt'
        test1_cfg = test1_dir+os.sep+'test1.cfg'
        test2_log = test2_dir+os.sep+'test2.log'
        test2_txt = test2_dir+os.sep+'test2.txt'
        test2_cfg = test2_dir+os.sep+'test2.cfg'
        test3_log = test3_dir+os.sep+'test3.log'
        test3_txt = test3_dir+os.sep+'test3.txt'
        test3_cfg = test3_dir+os.sep+'test3.cfg'
        test1_test_dir = test1_dir+os.sep+'test'
        test2_test_dir = test2_dir+os.sep+'test'
        test3_test_dir = test3_dir+os.sep+'test'
        os.makedirs(test1_dir)
        os.makedirs(test2_dir)
        os.makedirs(test3_dir)
        os.makedirs(test1_test_dir)
        os.makedirs(test2_test_dir)
        os.makedirs(test3_test_dir)
        open(test_log, 'w').close()
        open(test_txt, 'w').close()
        open(test_cfg, 'w').close()
        open(test1_log, 'w').close()
        open(test1_txt, 'w').close()
        open(test1_cfg, 'w').close()
        open(test2_log, 'w').close()
        open(test2_txt, 'w').close()
        open(test2_cfg, 'w').close()
        open(test3_log, 'w').close()
        open(test3_txt, 'w').close()
        open(test3_cfg, 'w').close()
        self.assertEqual(set(pcom.find_iter(self.base_dir, '*.log')),
                         {test_log, test1_log, test2_log, test3_log})
        self.assertEqual(set(pcom.find_iter(self.base_dir, '*test1*')),
                         {test1_log, test1_txt, test1_cfg})
        self.assertEqual(set(pcom.find_iter(self.base_dir, '*.log', True)),
                         set())
        self.assertEqual(set(pcom.find_iter(self.base_dir, '*test*', True)),
                         {test1_dir, test2_dir, test3_dir,
                          test1_test_dir, test2_test_dir, test3_test_dir})
        self.assertEqual(
            set(pcom.find_iter(self.base_dir, '*.log', cur_flg=True)),
            {test_log})
        self.assertEqual(
            set(pcom.find_iter(test1_dir, '*.log', cur_flg=True)),
            {test1_log})
        self.assertEqual(
            set(pcom.find_iter(self.base_dir, '*test*', True, True)),
            {test1_dir, test2_dir, test3_dir})
    def tearDown(self):
        shutil.rmtree(self.base_dir)
        del self.base_dir

class TestNestedDict(unittest.TestCase):
    def test_nested_dict(self):
        nor_dic = {}
        nst_dic = pcom.NestedDict()
        with self.assertRaises(KeyError):
            nor_dic['a']['b'] = 'c'
        nst_dic['a']['b'] = 'c'
        self.assertIsInstance(nst_dic, dict)
        self.assertIsInstance(nst_dic['a'], dict)
        self.assertEqual(nst_dic['a']['b'], 'c')

if __name__ == '__main__':
    unittest.main()
