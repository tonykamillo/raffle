#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, click, unittest, importlib
from app import create_app


env = 'testing'
os.environ.setdefault('FLASK_ENV', env)
app = create_app(__name__)


@app.cli.command()
@click.option('--package', '-p', default=None, help='Package path to your test suite. Ex: python runtests.py -p path/to/my/test/suite/package')
@click.option('--module', '-m', default=None, help='''
    Module to your test cases. It\'s needed to be a import path style. Ex: python runtests.py -m test.test_module
    ''')
@click.option('--case', '-c', multiple=True, default=[], help='''
    Especify the test cases you want to test. Ex: python runtests.py -c some.path.TestCase -c another.path.TestCase
    ''')
def main(package, module, case):
    with app.app_context():
        print('* Environment: %s' % app.config.get('ENV'))
        test_suite = None
        if module:
            module_obj = importlib.import_module(module)
            test_suite = unittest.defaultTestLoader.loadTestsFromModule(module_obj)
        elif case:
            test_suite = unittest.defaultTestLoader.loadTestsFromNames(case)
        elif package:
            package = package.replace('.', '/')
            test_suite = unittest.defaultTestLoader.discover(package)
        else:
            test_suite = unittest.defaultTestLoader.discover(app.root_path)

        unittest.TextTestRunner().run(test_suite)


if __name__ == '__main__':
    main()
