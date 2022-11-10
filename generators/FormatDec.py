## @file
# This file is used to check format of Dec file
#
# Copyright (c) 2022, Intel Corporation. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#


#
# Base Dec class
#
class Dec_Section(object):
    def __init__(self):
        self.tab_sp = "  "

    def __str__(self):
        pass

#
# Format Pcd
#
class DecSecPcds(object):
    def __init__(self, content, BasePcdName):
        self.Pcds = content
        self.BasePcdName = BasePcdName
        self.tab_sp = "  "

    def __str__(self):
        if self.Pcds:
            section_strlst = list()
            for arch in self.Pcds:
                if arch != "COMMON":
                    sec_head = "[%s.%s]" % (self.BasePcdName, arch)
                else:
                    sec_head = "[%s]" % self.BasePcdName

                section_strlst.append(sec_head)
                for pcd, pcd_value in self.Pcds[arch].items():
                    section_strlst.append(self.tab_sp + pcd + "|" + pcd_value)
                section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""

#
# Fotmat Defines
#
class DecSecDefines(Dec_Section):
    DEFINE_STR = "DEFINE"
    DESCRIPTION = '''
################################################################################
#
# Defines Section - statements that will be processed to create a Makefile.
#
################################################################################
'''

    def __init__(self, content):
        super(DecSecDefines, self).__init__()
        self.keywords = content
        self.macros = content.get("DEFINE", {})

    def __str__(self):
        section_strlst = []
        section_strlst.append(self.DESCRIPTION)
        section_strlst.append("[Defines]")
        def_len = len(self.DEFINE_STR) + 1

        key_str_width = self.stringMax()

        for key in self.keywords:
            if key in ["DEFINE", "EDK_GLOBAL"]:
                continue
            section_strlst.append(self.tab_sp + "{0:<{width}}".format(key,
                                                                      width=key_str_width) + " = " +
                                  self.keywords[key])

        section_strlst.append("")
        for key in self.macros:
            section_strlst.append(
                self.tab_sp + "DEFINE {0:<{width}}".format(key,
                                                           width=key_str_width - def_len) + " = " +
                self.macros[key])
        section_strlst.append("")
        return '\r\n'.join(section_strlst)

    def stringMax(self):
        def_len = len(self.DEFINE_STR) + 1

        key_str_width = []
        if self.keywords:
            key_str_width.append(max([len(k) for k in self.keywords]))

        if self.macros:
            key_str_width.append(max([len(k) for k in self.macros]) + def_len)
        else:
            key_str_width.append(def_len)

        return max(key_str_width)

#
# Format Includes
#
class DecSecIncludes(Dec_Section):
    def __init__(self, content):
        super(DecSecIncludes, self).__init__()
        self.Includes = content
        self.tab_sp = "  "

    def __str__(self):
        if self.Includes:
            section_strlst = []
            for arch in self.Includes:
                for private in self.Includes[arch]:
                    if private != "COMMON":
                        sec_head = "[Includes.%s.%s]" % (arch, private)
                    elif arch != "COMMON":
                        sec_head = "[Includes.%s]" % arch
                    else:
                        sec_head = "[Includes]"

                    section_strlst.append(sec_head)
                    section_strlst.extend([self.tab_sp + item for item in self.Includes[arch][private]])
                    section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""

#
# Format Guids, Protocols, Ppis
#
class DecSecHeader(Dec_Section):
    def __init__(self, content, BaseSecName):
        super(DecSecHeader, self).__init__()
        self.content = content
        self.BaseSecName = BaseSecName

    def __str__(self):
        if self.content:
            section_strlst = list()
            for arch in self.content:
                for private in self.content[arch]:
                    if private != "COMMON":
                        sec_head = "[%s.%s.%s]" % (self.BaseSecName, arch, private)
                    elif arch != "COMMON":
                        sec_head = "[%s.%s]" % (self.BaseSecName, arch)
                    else:
                        sec_head = "[%s]" % self.BaseSecName
                    section_strlst.append(sec_head)
                    for key, value in self.content[arch][private].items():
                        section_strlst.append(self.tab_sp + key.ljust(max([len(item) for item in self.content[arch][private].keys()])) + "  = " + value)
                    section_strlst.append("")
                section_strlst.append("")
                return "\r\n".join(section_strlst)
            return ""

#
# Format LibraryClasses
class DecSecLibraryClasses(Dec_Section):
    def __init__(self, content):
        super(DecSecLibraryClasses, self).__init__()
        self.LibraryClasses = content

    def __str__(self):
        if self.LibraryClasses:
            section_strlst = list()
            for arch in self.LibraryClasses:
                for model_type in self.LibraryClasses[arch]:
                    if model_type != "COMMON":
                        sec_head = "[LibraryClasses.%s.%s]" % (arch, model_type)
                    elif arch != "COMMON":
                        sec_head = "[LibraryClasses.%s]" % arch
                    else:
                        sec_head = "[LibraryClasses]"

                    section_strlst.append(sec_head)
                    for lib, lib_value in self.LibraryClasses[arch][model_type].items():
                        section_strlst.append(self.tab_sp + lib + "|" + lib_value)
                    section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""

class DecSecUserExtensions(Dec_Section):
    def __init__(self, content):
        pass

    def __str__(self):
        return ""


# Need change
class Sec_Guids(Dec_Section):
    def __init__(self, content):
        super(Sec_Guids, self).__init__()
        self.Guids = content

    def __str__(self):
        if self.Guids:
            section_strlst = list()
            for arch in self.Guids:
                for private in self.Guids[arch]:
                    if private != "COMMON":
                        sec_head = "[Guids.%s.%s]" % (arch, private)
                    elif arch != "COMMON":
                        sec_head = "[Guids.%s]" % arch
                    else:
                        sec_head = "[Guids]"

                    section_strlst.append(sec_head)
                    for guid, guid_value in self.Guids[arch][private].items():
                        section_strlst.append(self.tab_sp + guid.ljust(max([len(item) for item in self.Guids[arch][private].keys()])) + "  = " + guid_value)
                    section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""

class Sec_Protocols(Dec_Section):
    def __init__(self, content):
        super(Sec_Protocols, self).__init__()
        self.Protocols = content

    def __str__(self):
        if self.Protocols:
            section_strlst = list()
            for arch in self.Protocols:
                for private in self.Protocols[arch]:
                    if private != "COMMON":
                        sec_head = "[Protocols.%s.%s]" % (arch, private)
                    elif arch != "COMMON":
                        sec_head = "[Protocols.%s]" % arch
                    else:
                        sec_head = "[Protocols]"

                    section_strlst.append(sec_head)
                    for Protocols, ProtocolsValue in self.Protocols[arch][private].items():
                        section_strlst.append(self.tab_sp + Protocols.ljust(max([len(item) for item in self.Protocols[arch][private].keys()])) + "  = " + ProtocolsValue)
                    section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)

        return ""

class Sec_Ppis(Dec_Section):
    def __init__(self, content):
        super(Sec_Ppis, self).__init__()
        self.Ppis = content

    def __str__(self):
        if self.Ppis:
            section_strlst = list()
            for arch in self.Ppis:
                for private in self.Ppis[arch]:
                    if private != "COMMON":
                        sec_head = "[Ppis.%s.%s]" % (arch, private)
                    elif arch != "COMMON":
                        sec_head = "[Ppis.%s]" % arch
                    else:
                        sec_head = "[Ppis]"

                    section_strlst.append(sec_head)
                    for ppis, ppis_value in self.Ppis[arch][private].items():
                        section_strlst.append(self.tab_sp + ppis.ljust(max([len(item) for item in self.Ppis[arch][private].keys()])) + "  = " + ppis_value)
                    section_strlst.append("")
                section_strlst.append("")
            return "\r\n".join(section_strlst)

        return ""




