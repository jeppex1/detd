#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
# Copyright(C) 2020-2022 Intel Corporation
# Authors:
#   Hector Blanco Alcaine

import inspect
import re
import unittest

from detd import CommandStringIpLinkSetVlan
from detd import CommandStringIpLinkUnsetVlan
from detd import CommandStringEthtoolFeatures
from detd import CommandStringEthtoolGetChannelsInformation
from detd import CommandStringEthtoolSetCombinedChannels
from detd import CommandStringEthtoolSetSplitChannels
from detd import CommandStringEthtoolSetRing
from detd import CommandStringEthtoolGetDriverInformation
from detd import CommandStringTcTaprioOffloadSet
from detd import CommandStringTcTaprioSoftwareSet
from detd import CommandStringTcTaprioTxassistSet
from detd import CommandStringTcEtfInstall




class TestCommandString(unittest.TestCase):


    def assert_commandstring_equal(self, one, another):

        harmonized_one = re.sub('\s+', ' ', str(one).strip())
        harmonized_another = re.sub('\s+', ' ', str(another).strip())

        self.assertEqual(harmonized_one, harmonized_another)




    def test_iplinksetvlan(self):

        interface_name = "eth0"
        stream_vid = 3
        soprio_to_pcp = "0:7 1:6 2:5 3:4 4:3 5:2 6:1 7:0"

        cmd = CommandStringIpLinkSetVlan(interface_name, stream_vid, soprio_to_pcp)
        expected = """
            ip link add
                    link     eth0
                    name     eth0.3
                    type     vlan
                    protocol 802.1Q
                    id       3
                    egress   0:7 1:6 2:5 3:4 4:3 5:2 6:1 7:0"""

        self.assert_commandstring_equal(cmd, expected)




    def test_iplinkunsetvlan(self):

        interface_name = "eth0"
        stream_vid = 3

        cmd = CommandStringIpLinkUnsetVlan(interface_name, stream_vid)
        expected = "ip link delete eth0.3"

        self.assert_commandstring_equal(cmd, expected)




    def test_ethtoolfeatures(self):

        interface_name = "eth0"
        features = {'rxvlan': 'off', 'hw-tc-offload': 'on'}

        cmd = CommandStringEthtoolFeatures(interface_name, features)
        expected = 'ethtool --features eth0 rxvlan off hw-tc-offload on'

        self.assert_commandstring_equal(cmd, expected)


    def test_ethtoolgetchannelsinformation(self):

        interface_name = "eth0"

        cmd = CommandStringEthtoolGetChannelsInformation(interface_name)
        expected = 'ethtool --show-channels eth0'

        self.assert_commandstring_equal(cmd, expected)



    def test_ethtoolsetsplitchannels(self):

        interface_name = "eth0"
        num_tx_queues = 4
        num_rx_queues = 6

        cmd = CommandStringEthtoolSetSplitChannels(interface_name, num_tx_queues, num_rx_queues)
        expected = 'ethtool --set-channels eth0 tx 4 rx 6'

        self.assert_commandstring_equal(cmd, expected)




    def test_ethtoolsetcombinedchannels(self):

        interface_name = "eth0"
        num_queues = 4

        cmd = CommandStringEthtoolSetCombinedChannels(interface_name, num_queues)
        expected = 'ethtool --set-channels eth0 combined 4'

        self.assert_commandstring_equal(cmd, expected)




    def test_ethtoolsetring(self):

        interface_name = "eth0"
        num_tx_rings = 1024
        num_rx_rings = 256

        cmd = CommandStringEthtoolSetRing(interface_name, num_tx_rings, num_rx_rings)
        expected = 'ethtool --set-ring eth0 tx 1024 rx 256'

        self.assert_commandstring_equal(cmd, expected)




    def test_ethtoolgetdriverinformation(self):

        interface_name = "eth0"

        cmd = CommandStringEthtoolGetDriverInformation(interface_name)
        expected = 'ethtool --driver eth0'

        self.assert_commandstring_equal(cmd, expected)




    def test_tcsettapriooffload(self):

        interface_name = "eth0"
        soprio_to_tc   = "0 0 0 0 0 0 1 0 0 0 0 0"
        num_tc         = 2
        tc_to_hwq      = "1@0 1@1 1@2 1@3 1@4 1@5 1@6 1@7"
        base_time      = "165858970408520000"
        sched_entries  = """sched-entry S 01 250000
                            sched-entry S 02 12176
                            sched-entry S 01 19737824"""

        cmd = CommandStringTcTaprioOffloadSet(interface_name, num_tc, soprio_to_tc, tc_to_hwq, base_time, sched_entries)
        expected = '''
           tc qdisc replace
                    dev       eth0
                    parent    root
                    taprio
                    num_tc    2
                    map       0 0 0 0 0 0 1 0 0 0 0 0
                    queues    1@0 1@1 1@2 1@3 1@4 1@5 1@6 1@7
                    base-time 165858970408520000
                    sched-entry S 01 250000
                    sched-entry S 02 12176
                    sched-entry S 01 19737824
                    flags     0x2'''


        self.assert_commandstring_equal(cmd, expected)




    def test_tcsettapriosoftware(self):

        interface_name = "eth0"
        soprio_to_tc   = "0 0 0 0 0 0 1 0 0 0 0 0"
        num_tc         = 2
        tc_to_hwq      = "1@0 1@1 1@2 1@3 1@4 1@5 1@6 1@7"
        base_time      = "165858970408520000"
        sched_entries  = """sched-entry S 01 250000
                            sched-entry S 02 12176
                            sched-entry S 01 19737824"""

        cmd = CommandStringTcTaprioSoftwareSet(interface_name, num_tc, soprio_to_tc, tc_to_hwq, base_time, sched_entries)
        expected = '''
           tc qdisc replace
                    dev       eth0
                    parent    root
                    taprio
                    num_tc    2
                    map       0 0 0 0 0 0 1 0 0 0 0 0
                    queues    1@0 1@1 1@2 1@3 1@4 1@5 1@6 1@7
                    base-time 165858970408520000
                    sched-entry S 01 250000
                    sched-entry S 02 12176
                    sched-entry S 01 19737824
                    flags     0x0
                    clockid CLOCK_TAI'''


        self.assert_commandstring_equal(cmd, expected)


    def test_tcsettapriotxassist(self):

        interface_name = "eth0"
        soprio_to_tc   = "0 0 0 0 0 0 1 0 0 0 0 0"
        num_tc         = 2
        tc_to_hwq      = "1@0 1@1 1@2 1@3 1@4 1@5 1@6 1@7"
        base_time      = "165858970408520000"
        sched_entries  = """sched-entry S 01 250000
                            sched-entry S 02 12176
                            sched-entry S 01 19737824"""
        handle         = "100"
        txtime_delay   = "500000"

        cmd = CommandStringTcTaprioTxassistSet(interface_name, num_tc, soprio_to_tc, tc_to_hwq, base_time, sched_entries, handle, txtime_delay)
        expected = '''
           tc qdisc replace
                    dev       eth0
                    parent    root
                    handle    100
                    taprio
                    num_tc    2
                    map       0 0 0 0 0 0 1 0 0 0 0 0
                    queues    1@0 1@1 1@2 1@3 1@4 1@5 1@6 1@7
                    base-time 165858970408520000
                    sched-entry S 01 250000
                    sched-entry S 02 12176
                    sched-entry S 01 19737824
                    flags     0x1
                    txtime-delay 500000
                    clockid CLOCK_TAI'''


        self.assert_commandstring_equal(cmd, expected)


    def test_tcetfinstall(self):

        interface_name = "eth0"
        parent         = "100:1"
        delta          = "500000"

        cmd = CommandStringTcEtfInstall(interface_name, parent, delta)
        expected = '''
           tc qdisc replace
                    dev       eth0
                    parent    100:1
                    etf
                    clockid CLOCK_TAI
                    delta 500000
                    offload
                    skip_sock_check'''


        self.assert_commandstring_equal(cmd, expected)
        
        
        
if __name__ == '__main__':
    unittest.main()
