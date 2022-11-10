# -*- coding: utf-8 -*-
# @Time : 10/28/2022 9:12 AM
# @Author : mliang2x
# @Email : mingyuex.liang@intel.com
# @File : FormatDsc.py
# @Project : edk2-parser

from collections import OrderedDict
from CommonDataClass import DataClass as DC
from Common import DataType as DT


'''
    Format DSC Class
'''
class Sec_Pcds(object):
    def JoinPcd(self, PcdName, content, tab_sp, sp, description=""):
        if content:
            Pcd_StrList = []
            Pcd_StrList.append(description)
            for arch in content:
                for platform in content[arch]:
                    sectionName = "[%s]" % PcdName
                    if platform != "COMMON":
                        sectionName = "[%s.%s.%s]" % (PcdName, arch, platform)
                    elif arch != "COMMON":
                        sectionName = "[%s.%s]" % (PcdName, arch)
                    Pcd_StrList.append(sectionName)
                    for pcd, pcdValue in content[arch][platform].items():
                        pcd_str = tab_sp + pcd + sp + pcdValue
                        Pcd_StrList.append(pcd_str)
                    Pcd_StrList.append("")
            Pcd_StrList.append("")
            return "\r\n".join(Pcd_StrList)
        return ""


class Sec_Defines(object):
    DEFINE_STR = "DEFINE"
    EDK_GLOBAL_STR = "EDK_GLOBAL"
    DESCRIPTION = '''
################################################################################
#
# Defines Section - statements that will be processed to create a Makefile.
#
################################################################################
'''

    def __init__(self, content):
        self.keywords = content
        self.macros = content.get("DEFINE", {})
        self.edk_globals = content.get("EDK_GLOBAL", {})
        self.tab_sp = "  "

    def __str__(self):
        section_strlst = []
        section_strlst.append(self.DESCRIPTION)
        section_strlst.append("[Defines]")
        def_len = len(self.DEFINE_STR) + 1
        glo_len = len(self.EDK_GLOBAL_STR) + 1

        key_str_width = self.stringMax()

        for key in self.keywords:
            if key in ["DEFINE", "EDK_GLOBAL"]:
                continue
            section_strlst.append(self.tab_sp + "{0:<{width}}".format(key,
                                                                      width=key_str_width) + " = " +
                                  self.keywords[key])

        section_strlst.append("")
        if self.macros:
            for key in self.macros:
                section_strlst.append(
                    self.tab_sp + "DEFINE {0:<{width}}".format(key,
                                                               width=key_str_width - def_len) + " = " +
                    self.macros[key])

            section_strlst.append("")
        if self.edk_globals:
            for key in self.edk_globals:
                section_strlst.append(
                    self.tab_sp + "EDK_GLOBAL {0:<{width}}".format(key,
                                                                   width=key_str_width - glo_len) + " = " +
                    self.edk_globals[key])

            section_strlst.append("")
        return '\r\n'.join(section_strlst)

    def stringMax(self):
        def_len = len(self.DEFINE_STR) + 1
        glo_len = len(self.EDK_GLOBAL_STR) + 1

        key_str_width = []
        if self.keywords:
            key_str_width.append(max([len(k) for k in self.keywords]))

        if self.macros:
            key_str_width.append(max([len(k) for k in self.macros]) + def_len)
        else:
            key_str_width.append(def_len)

        if self.edk_globals:
            key_str_width.append(
                max([len(k) for k in self.edk_globals]) + glo_len)
        else:
            key_str_width.append(glo_len)
        return max(key_str_width)


class Sec_SkuIds(object):
    DESCRIPTION = '''
################################################################################
#
# SKU Identification section - list of all SKU IDs supported by this Platform.
#
################################################################################
'''

    def __init__(self, content):
        self.skuids = content
        self.tab_sp = "  "

    def __str__(self):
        if self.skuids:
            section_strlst = []
            section_strlst.append(self.DESCRIPTION)
            section_strlst.append("[SkuIds]")
            for key, value in self.skuids.items():
                section_strlst.append(self.tab_sp + " | ".join((key, value)))

            section_strlst.append('\r\n')
            return '\r\n'.join(section_strlst)
        return ""


class Sec_DefaultStores(object):

    def __init__(self, content):
        self.defaultstores = content
        self.tab_sp = "  "

    def __str__(self):
        if self.defaultstores:
            section_strlst = []
            section_strlst.append("[DefaultStores]")
            for key, value in self.defaultstores.items():
                section_strlst.append(self.tab_sp + " | ".join((key, value)))

            section_strlst.append('\r\n')
            return '\r\n'.join(section_strlst)
        return ""


class Sec_Packages(object):

    def __init__(self, content):
        self.packages = content
        self.tab_sp = "  "

    def __str__(self):
        if self.packages:
            section_strlst = []
            section_strlst.append("[Packages]")
            for item in self.packages:
                section_strlst.append(self.tab_sp + item)

            section_strlst.append('\r\n')
            return '\r\n'.join(section_strlst)
        return ""


class Sec_BuildOptions(object):

    def __init__(self, content):
        self.buildoptions = content
        self.tab_sp = "  "

    def __str__(self):
        section_strlst = []
        sections = OrderedDict()
        for arch in self.buildoptions:
            for module_type in self.buildoptions[arch]:
                for toolchain in self.buildoptions[arch][module_type]:
                    for flag in self.buildoptions[arch][module_type][toolchain]:
                        flag_value = \
                        self.buildoptions[arch][module_type][toolchain][flag]
                        if module_type == "COMMON":
                            section_head = "[" + ".".join(
                                ("BuildOptions", arch)) + "]"
                        else:
                            section_head = "[" + ".".join(("BuildOptions", arch,
                                                           "EDKII",
                                                           module_type)) + "]"
                        if section_head not in sections:
                            sections[section_head] = OrderedDict()
                        if toolchain not in sections[section_head]:
                            sections[section_head][toolchain] = OrderedDict()
                        sections[section_head][toolchain].update(
                            {flag: flag_value})
        for sec_head in sections:
            section_strlst.append(sec_head)
            for toolchain in sections[sec_head]:
                for flag in sections[sec_head][toolchain]:
                    flag_value = sections[sec_head][toolchain][flag]
                    if toolchain == "COMMON":
                        if flag_value.startswith("="):
                            section_strlst.append(
                                self.tab_sp + flag + " =" + flag_value)
                        else:
                            section_strlst.append(
                                self.tab_sp + flag + " = " + flag_value)
                    else:
                        if flag_value.startswith("="):
                            section_strlst.append(
                                self.tab_sp + toolchain + ":" + flag + " =" + flag_value)
                        else:
                            section_strlst.append(
                                self.tab_sp + toolchain + ":" + flag + " = " + flag_value)
            section_strlst.append("\n")

        return '\r\n'.join(section_strlst)


class Sec_LibraryClasses(object):
    DESCRIPTION = '''
################################################################################
#
# Library Class section - list of all Library Classes needed by this Platform.
#
################################################################################
    '''

    def __init__(self, content):
        self.libraryclasses = content
        self.tab_sp = "  "

    def __str__(self):
        section_strlst = []
        section_strlst.append(self.DESCRIPTION)
        sections = OrderedDict()

        for arch in self.libraryclasses:
            for module_t in self.libraryclasses[arch]:
                for lib_class in self.libraryclasses[arch][module_t]:
                    lib_inst = self.libraryclasses[arch][module_t][lib_class]
                    if module_t.upper() == "COMMON":
                        if arch.upper() == "COMMON":
                            sec_head = "[LibraryClasses]"
                        else:
                            sec_head = "[LibraryClasses.COMMON.%s]" % module_t
                    else:
                        sec_head = "[LibraryClasses.%s.%s]" % (arch, module_t)
                    sections.setdefault(sec_head, OrderedDict())[
                        lib_class] = lib_inst

        for sec_head in sections:
            section_strlst.append(sec_head)
            for lib_class, lib_ins in sections[sec_head].items():
                section_strlst.append(
                    "%s%s|%s" % (self.tab_sp, lib_class, lib_ins))
            section_strlst.append("")

        section_strlst.append("")
        return '\r\n'.join(section_strlst)


class Sec_Components(object):
    DESCRIPTION = '''
################################################################################
#
# Components Section - list of all EDK II Modules needed by this Platform.
#
################################################################################
 '''

    def __init__(self, content):
        self.Components = content
        self.tab_sp = "  "
        self.PcdType = {
            (
                        DT.TAB_PCDS + DT.TAB_PCDS_FIXED_AT_BUILD).upper(): DT.TAB_PCDS + DT.TAB_PCDS_FIXED_AT_BUILD,
            (
                        DT.TAB_PCDS + DT.TAB_PCDS_PATCHABLE_IN_MODULE).upper(): DT.TAB_PCDS + DT.TAB_PCDS_PATCHABLE_IN_MODULE,
            (
                        DT.TAB_PCDS + DT.TAB_PCDS_FEATURE_FLAG).upper(): DT.TAB_PCDS + DT.TAB_PCDS_FEATURE_FLAG,
            (
                        DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_DEFAULT).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_DEFAULT,
            (
                        DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_VPD).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_VPD,
            (
                        DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_HII).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_HII,
            (
                        DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_DEFAULT).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_DEFAULT,
            (
                        DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_VPD).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_VPD,
            (
                        DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_HII).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_HII,
        }

    def __str__(self):
        if self.Components:
            components_strlsit = list()
            components_strlsit.append(self.DESCRIPTION)
            for arch in self.Components:
                section_name = "[Components.%s]" % arch
                if arch == "COMMON":
                    section_name = "[Components]"
                components_strlsit.append(section_name)
                for model, sub_sections in self.Components[arch].items():
                    if sub_sections:
                        components_strlsit.append(self.tab_sp + model + " {")
                        for secName, value in sub_sections.items():
                            if secName == (DT.TAB_LIBRARY_CLASSES).upper():
                                components_strlsit.append(
                                    "%s%s<LibararyClasses>" % (
                                    self.tab_sp, self.tab_sp))
                                for lib in value:
                                    components_strlsit.append("%s%s%s%s" % (
                                    self.tab_sp, self.tab_sp, self.tab_sp, lib))
                            elif "PCDS" in secName:
                                components_strlsit.append("%s%s<%s>" % (
                                self.tab_sp, self.tab_sp,
                                self.PcdType[secName]))
                                for PcdName, PcdValue in value.items():
                                    components_strlsit.append("%s%s%s%s|%s" % (
                                    self.tab_sp, self.tab_sp, self.tab_sp,
                                    PcdName, PcdValue))
                            elif secName == (DT.TAB_BUILD_OPTIONS).upper():
                                components_strlsit.append(
                                    "%s%s<BuildOptions>" % (
                                    self.tab_sp, self.tab_sp))
                                for toolchain, flag_fvalue_dict in value.items():
                                    for flag, flagValue in flag_fvalue_dict.items():
                                        components_strlsit.append(
                                            "%s%s%s%s:%s = %s" % (
                                            self.tab_sp, self.tab_sp,
                                            self.tab_sp, toolchain, flag,
                                            flagValue))
                        components_strlsit.append(self.tab_sp + "}")

                    else:
                        components_strlsit.append(self.tab_sp + model)
                components_strlsit.append("\n")
            return "\r\n".join(components_strlsit)
        return ""


class Sec_PcdsFeatureFlag(Sec_Pcds):
    DESCRIPTION = '''
################################################################################
#
# Pcd Section - list of all EDK II PCD Entries defined by this Platform.
#
################################################################################
'''

    def __init__(self, content):
        self.PcdsFeatureFlag = content
        self.sp = "|"
        self.tab_sp = "  "
        self.PcdName = "PcdsFeatureFlag"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsFeatureFlag, self.tab_sp,
                            self.sp, self.DESCRIPTION)


class Sec_PcdsFixedAtBuild(Sec_Pcds):
    def __init__(self, content):
        self.PcdsFixedAtBuild = content
        self.sp = "|"
        self.tab_sp = "  "
        self.PcdName = "PcdsFixedAtBuild"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsFixedAtBuild, self.tab_sp,
                            self.sp)


class Sec_PcdsPatchableInModule(Sec_Pcds):
    def __init__(self, content):
        self.PcdsPatchableInModule = content
        self.sp = "|"
        self.tab_sp = "  "
        self.PcdName = "PcdsPatchableInModule"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsPatchableInModule,
                            self.tab_sp, self.sp)


class Sec_PcdsDynamicDefault(Sec_Pcds):
    DESCRIPTION = '''
################################################################################
#
# Pcd Dynamic Section - list of all EDK II PCD Entries defined by this Platform
#
################################################################################
    '''

    def __init__(self, content):
        self.PcdsDynamicDefault = content
        self.tab_sp = "  "
        self.sp = "|"
        self.PcdName = "PcdsDynamicDefault"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicDefault, self.tab_sp,
                            self.sp, self.DESCRIPTION)


class Sec_PcdsDynamicHii(Sec_Pcds):
    def __init__(self, content):
        self.PcdsDynamicHii = content
        self.tab_sp = "  "
        self.sp = '|'
        self.PcdName = "PcdsDynamicHii"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicHii, self.tab_sp,
                            self.sp)


class Sec_PcdsDynamicVpd(Sec_Pcds):
    def __init__(self, content):
        self.PcdsDynamicVpd = content
        self.tab_sp = "  "
        self.sp = '|'
        self.PcdName = "PcdsDynamicVpd"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicVpd, self.tab_sp,
                            self.sp)


class Sec_PcdsDynamicExDefault(Sec_Pcds):
    def __init__(self, content):
        self.PcdsDynamicExDefault = content
        self.tab_sp = "  "
        self.sp = '|'
        self.PcdName = "PcdsDynamicExDefault"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicExDefault,
                            self.tab_sp, self.sp)


class Sec_PcdsDynamicExHii(Sec_Pcds):
    def __init__(self, content):
        self.PcdsDynamicExHii = content
        self.tab_sp = "  "
        self.sp = '|'
        self.PcdName = "PcdsDynamicExHii"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicExHii, self.tab_sp,
                            self.sp)


class Sec_PcdsDynamicExVpd(Sec_Pcds):
    def __init__(self, content):
        self.PcdsDynamicExVpd = content
        self.tab_sp = "  "
        self.sp = '|'
        self.PcdName = "PcdsDynamicExVpd"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicExVpd, self.tab_sp,
                            self.sp)


class Sec_Libraries(object):
    def __init__(self, content):
        self.Libraries = content
        self.tab_sp = "  "

    def __str__(self):
        if self.Libraries:
            Libraries_StrList = []
            for arch in self.Libraries:
                section_name = "[Libraries.%s]" % arch
                if arch == "COMMON":
                    section_name = "[Libraries]"
                Libraries_StrList.append(section_name)
                Libraries_StrList.extend(
                    [self.tab_sp + item for item in self.Libraries[arch]])
                Libraries_StrList.append("")
            return "\r\n".join(Libraries_StrList)
        return ""


class Sec_UserExtensions(object):
    def __init__(self, content):
        pass

    def __str__(self):
        return ""

