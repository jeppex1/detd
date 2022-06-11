#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
# Copyright(C) 2020-2022 Intel Corporation
# Authors:
#   Hector Blanco Alcaine

import unittest
import subprocess
from unittest.mock import patch
from unittest import mock
from unittest.mock import mock_open
from subprocess import CalledProcessError

from detd import SystemInformation
from detd import CommandEthtool

import os

from .common import *


class TestSystemInformation(unittest.TestCase):


    def setUp(self):

        env_var = os.getenv("DETD_TESTENV")
        if env_var == "HOST":
            self.mode = TestMode.HOST
        elif env_var == "TARGET":
            self.mode = TestMode.TARGET
        else:
            self.mode = TestMode.HOST


    def test_getpcidbdf_success(self):

        sysinfo = SystemInformation()

        interface = "eth0"

        driver_information = [
            'driver: st_gmac',
            'version: 5.17.1-rt17',
            'firmware-version:',
            'expansion-rom-version:',
            'bus-info: 0000:00:1d.1',
            'supports-statistics: yes',
            'supports-test: no',
            'supports-eeprom-access: no',
            'supports-register-dump: yes',
            'supports-priv-flags: no'
        ]


        with mock.patch.object(CommandEthtool, 'get_driver_information', return_value=driver_information):
            domain, bus, device, function = sysinfo.get_pci_dbdf(interface)
            self.assertEqual(domain, "0000")
            self.assertEqual(bus, "00")
            self.assertEqual(device, "1d")
            self.assertEqual(function, "1")


    def test_gethex(self):

        vendor_or_product_id = '0x8086'
        mocked_open = mock.mock_open(read_data=vendor_or_product_id)
        with mock.patch('builtins.open', mocked_open):
            sysinfo = SystemInformation()
            filename = "da/file"
            value = sysinfo.get_hex(filename)
            self.assertEqual(value, '8086')


    def test_getpciid_parse_error(self):

        sysinfo = SystemInformation()

        interface = "eth0"

        uevent = """
DRIVER=stmmaceth
PCI_CLASS=20018
PCI_SUBSYS_ID=8086:7270
PCI_SLOT_NAME=0000:00:1d.1
MODALIAS=pci:v00008086d00004BA0sv00008086sd00007270bc02sc00i18"""

        mocked_open = mock.mock_open(read_data=uevent)
        with mock.patch('builtins.open', mocked_open):
            self.assertRaises(RuntimeError, sysinfo.get_pci_id, interface)


if __name__ == '__main__':
    unittest.main()
