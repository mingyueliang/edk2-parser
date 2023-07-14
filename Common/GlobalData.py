## @file
# This file is used to define common static strings used by INF/DEC/DSC files
#
# Copyright (c) 2007 - 2018, Intel Corporation. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent

import re

gActivePlatform = None
gIsWindows = None
gWorkspace = "."
gOptions = None
gCaseInsensitive = False
gAllFiles = None

gGlobalDefines = {}
gPlatformDefines = {}
# PCD name and value pair for fixed at build and feature flag
gPlatformPcds = {}
# PCDs with type that are not fixed at build and feature flag
gPlatformOtherPcds = {}
gCommandLineDefines = {}
gEdkGlobal = {}

# definition for a MACRO name.  used to create regular expressions below.
_MacroNamePattern = "[A-Z][A-Z0-9_]*"

## Regular expression for matching macro used in DSC/DEC/INF file inclusion
gMacroRefPattern = re.compile("\$\(({})\)".format(_MacroNamePattern), re.UNICODE)
gMacroDefPattern = re.compile("^(DEFINE|EDK_GLOBAL)[ \t]+")
gMacroNamePattern = re.compile("^{}$".format(_MacroNamePattern))
# definition for a GUID.  used to create regular expressions below.
_HexChar = r"[0-9a-fA-F]"
_GuidPattern = r"{Hex}{{8}}-{Hex}{{4}}-{Hex}{{4}}-{Hex}{{4}}-{Hex}{{12}}".format(Hex=_HexChar)

## Regular expressions for GUID matching
gGuidPattern = re.compile(r'{}'.format(_GuidPattern))
gGuidPatternEnd = re.compile(r'{}$'.format(_GuidPattern))

## Regular expressions for HEX matching
g4HexChar = re.compile(r'{}{{4}}'.format(_HexChar))
gHexPattern = re.compile(r'0[xX]{}+'.format(_HexChar))
gHexPatternAll = re.compile(r'0[xX]{}+$'.format(_HexChar))

## Regular expression for GUID c structure format
_GuidCFormatPattern = r"{{\s*0[xX]{Hex}{{1,8}}\s*,\s*0[xX]{Hex}{{1,4}}\s*,\s*0[xX]{Hex}{{1,4}}" \
                      r"\s*,\s*{{\s*0[xX]{Hex}{{1,2}}\s*,\s*0[xX]{Hex}{{1,2}}" \
                      r"\s*,\s*0[xX]{Hex}{{1,2}}\s*,\s*0[xX]{Hex}{{1,2}}" \
                      r"\s*,\s*0[xX]{Hex}{{1,2}}\s*,\s*0[xX]{Hex}{{1,2}}" \
                      r"\s*,\s*0[xX]{Hex}{{1,2}}\s*,\s*0[xX]{Hex}{{1,2}}\s*}}\s*}}".format(Hex=_HexChar)
gGuidCFormatPattern = re.compile(r"{}".format(_GuidCFormatPattern))


#
# The Conf dir outside the workspace dir
#
gConfDirectory = ''
gCmdConfDir = ''
gBuildDirectory = ''

BuildOptionPcd = []

# Pcd name for the Pcd which used in the Conditional directives
gConditionalPcds = []


# Test GetFv
gGuidDict = {}
