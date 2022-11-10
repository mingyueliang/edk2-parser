## @file
# This file is used to check format of Inf file
#
# Copyright (c) 2022, Intel Corporation. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

class InfSection(object):
    def __init__(self):
        self.tab_sp = "  "

    def __str__(self):
        pass

class InfSecDefines(InfSection):
    DEFINE_STR = "DEFINE"
    DESCRIPTION = '''
################################################################################
#
# Defines Section - statements that will be processed to create a Makefile.
#
################################################################################
    '''

    def __init__(self, content):
        super(InfSecDefines, self).__init__()
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


class InfSecBuildOptions(InfSection):
    def __init__(self, content):
        super(InfSecBuildOptions, self).__init__()
        self.BuildOptions = content

    def __str__(self):
        if self.BuildOptions:
            section_strlst = list()
            for arch in self.BuildOptions:
                if arch != "COMMON":
                    sec_head = "[BuildOptions.%s]" % arch
                else:
                    sec_head = "[BuildOptions]"

                section_strlst.append(sec_head)

                for toolchain in self.BuildOptions[arch]:
                    for flag, flag_value in self.BuildOptions[arch][toolchain].items():
                        section_strlst.append(self.tab_sp + toolchain + ":" + flag + " = " + flag_value)
                section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""

#
# Format Sources, LibraryClasses, Protocols, Ppis, Packages
#
class InfSecOther(InfSection):
    def __init__(self, content, BaseSecName):
        super(InfSecOther, self).__init__()
        self.content = content
        self.BaseScename = BaseSecName

    def __str__(self):
        if self.content:
            section_strlst = list()
            for arch in self.content:
                if arch != "COMMON":
                    sec_head = "[%s.%s]" % (self.BaseScename, arch)
                else:
                    sec_head = "[%s]" % self.BaseScename
                section_strlst.append(sec_head)

                section_strlst.extend([self.tab_sp + item for item in self.content[arch]])
                section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""


class InfSecDepex(InfSection):
    def __init__(self, content):
        super(InfSecDepex, self).__init__()
        self.Depex = content

    def __str__(self):
        if self.Depex:
            section_strlst = list()
            for arch in self.Depex:
                for model_type in self.Depex[arch]:
                    if model_type != "COMMON":
                        sec_head = "[Depex.%s.%s]" % (arch, model_type)
                    elif arch != "COMMON":
                        sec_head = "[Depex.%s]" % arch
                    else:
                        sec_head = "[Depex]"
                    section_strlst.append(sec_head)
                    section_strlst.extend([self.tab_sp + item for item in self.Depex[arch][model_type]])
                    section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""


class InfSecBinaries(InfSection):
    def __init__(self, content):
        super(InfSecBinaries, self).__init__()
        self.Binaries = content

    def __str__(self):
        if self.Binaries:
            section_strlst = list()
            for arch in self.Binaries:
                if arch != "COMMON":
                    sec_head = "[Binaries.%s]" % arch
                else:
                    sec_head = "[Binaries]"

                section_strlst.append(sec_head)
                for tag, tag_value in self.Binaries[arch].items():
                    section_strlst.append(self.tab_sp + tag + "|" + tag_value)
                section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""

#
# format FixedPcd, Pcd, FeaturePcd, PatchPcd
#
class InfSecPcd(InfSection):
    def __init__(self, content, pcd_name):
        super(InfSecPcd, self).__init__()
        self.pcds = content
        self.pcd_name = pcd_name

    def __str__(self):
        if self.pcds:
            section_strlst = list()
            for arch in self.pcds:
                if arch != "COMMON":
                    sec_head = "[%s.%s]" % (self.pcd_name, arch)
                else:
                    sec_head = "[%s]" % self.pcd_name
                section_strlst.append(sec_head)
                for pcd, pcdValue in self.pcds[arch].items():
                    if pcdValue:
                        section_strlst.append(self.tab_sp + pcd + "|" + pcdValue)
                    else:
                        section_strlst.append(self.tab_sp + pcd)
                section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""


class InfSecUserExtensions(InfSection):
    def __init__(self, content):
        super(InfSecUserExtensions, self).__init__()
        self.UserExtensions = content

    def __str__(self):
        return ""

#
# Need change
#
class InfSecPackages(InfSection):
    def __init__(self, content):
        super(InfSecPackages, self).__init__()
        self.Packages = content

    def __str__(self):
        if self.Packages:
            section_strlst = list()
            for arch in self.Packages:
                if arch != "COMMON":
                    sec_head = "[Packages.%s]" % arch
                else:
                    sec_head = "[Packages]"
                section_strlst.append(sec_head)
                section_strlst.extend([self.tab_sp + item for item in self.Packages[arch]])
                section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""


class InfSecProtocols(InfSection):
    def __init__(self, content):
        super(InfSecProtocols, self).__init__()
        self.Protocols = content

    def __str__(self):
        pass


class InfSecSources(InfSection):
    def __init__(self, content):
        super(InfSecSources, self).__init__()
        self.Sources = content

    def __str__(self):
        if self.Sources:
            section_strlst = list()
            for arch in self.Sources:
                if arch != "COMMON":
                    sec_head = "[Sources.%s]" % arch
                else:
                    sec_head = "[Sources]"
                section_strlst.append(sec_head)
                for source in self.Sources[arch]:
                    section_strlst.append(self.tab_sp + source)

                section_strlst.append("")
            section_strlst.append("")
            return "\r\n".join(section_strlst)
        return ""

