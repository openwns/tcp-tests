#! /usr/bin/env python2.4

# this is needed, so that the script can be called from everywhere
import os
import sys
base, tail = os.path.split(sys.argv[0])
os.chdir(base)

# Append the python sub-dir of WNS--main--x.y ...
sys.path.append(os.path.join('..', '..', '..', 'sandbox', 'default', 'lib', 'python2.4', 'site-packages'))

# ... because the module WNS unit test framework is located there.
import pywns.WNSUnit

# create a system test
testSuite1 = pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                           executeable = "wns-core",
                                           configFile = 'tcpTestsConstanze.py',
                                           shortDescription = 'Constanze traffic sent over TCP',
                                           requireReferenceOutput = False,
                                           disabled = False,
                                           disabledReason = '')

testSuite2 = pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                           executeable = "wns-core",
                                           configFile = 'udpTestsConstanze.py',
                                           shortDescription = 'Two station communicate via TCP',
                                           requireReferenceOutput = False,
                                           disabled = False,
                                           disabledReason = "")

testSuite3 = pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                           executeable = "wns-core",
                                           configFile = 'tcpTestsApplication.py',
                                           shortDescription = 'Traffic of different applications sent over TCP and UDP',
                                           requireReferenceOutput = False,
                                           disabled = True,
                                           disabledReason = 'Currently no applications available')

# create a system test
testSuite = pywns.WNSUnit.TestSuite()
testSuite.addTest(testSuite1)
testSuite.addTest(testSuite2)
testSuite.addTest(testSuite3)

if __name__ == '__main__':
    # This is only evaluated if the script is called by hand

    # if you need to change the verbosity do it here
    verbosity = 2

    pywns.WNSUnit.verbosity = verbosity

    # Create test runner
    testRunner = pywns.WNSUnit.TextTestRunner(verbosity=verbosity)

    # Finally, run the tests.
    testRunner.run(testSuite)
