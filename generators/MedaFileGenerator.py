## @file
# This file is used to check format of comments
#
# Copyright (c) 2012, Intel Corporation. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#
from collections import OrderedDict
import CommonDataClass.DataClass as DC
import Common.DataType as DT


class DscGen(object):
    def __init__(self):
        self.content = OrderedDict()
        self.txt = ""
        self.tab_sp = "  "
        self.arch_lst = set()

    def from_parser(self, dsc_parser):
        ''' Process the parser database and store the data in dict '''
        dsc_parser_dict = dict()
        if isinstance(dsc_parser,dict):
            dsc_parser_dict.update(dsc_parser)
        else:
            dsc_parser_dict[dsc_parser._Arch] = dsc_parser
        self.Set_Defines(dsc_parser_dict)
        self.Set_SkuIds(dsc_parser_dict)
        self.Set_DefaultStores(dsc_parser_dict)
        self.Set_Packages(dsc_parser_dict)
        self.Set_BuildOptions(dsc_parser_dict)
        self.Set_LibraryClasses(dsc_parser_dict)
        self.Set_Components(dsc_parser_dict)
        self.Set_PcdsFeatureFlag(dsc_parser_dict)
        self.Set_PcdsFixedAtBuild(dsc_parser_dict)
        self.Set_PcdsPatchableInModule(dsc_parser_dict)
        self.Set_PcdsDynamicDefault(dsc_parser_dict)
        self.Set_PcdsDynamicHii(dsc_parser_dict)
        self.Set_PcdsDynamicVpd(dsc_parser_dict)
        self.Set_PcdsDynamicExDefault(dsc_parser_dict)
        self.Set_PcdsDynamicExVpd(dsc_parser_dict)
        # ...
        self.Set_Libraries(dsc_parser_dict)
        # self.Set_UserExtensions(dsc_parser_dict)
        # ...
    
    def from_yaml(self, yaml_content):
        ''' Import the yaml_content into dict'''
        import yaml
        self.content = yaml.load(yaml_content)
    
    def from_json(self, json_content):
        ''' Import the json_content into dict'''
        import json
        self.content = json.loads(json_content)

    def FormatDsc(self):
        self.txt += str(Sec_Defines(self.content.get("Defines", {})))
        self.txt += str(Sec_SkuIds(self.content.get("SkuIds", {})))
        self.txt += str(Sec_DefaultStores(self.content.get("DefaultStores", {})))
        self.txt += str(Sec_Packages(self.content.get("Packages", {})))
        self.txt += str(Sec_PcdsFeatureFlag(self.content.get("PcdsFeatureFlag", {})))
        self.txt += str(Sec_PcdsFixedAtBuild(self.content.get("PcdsFixedAtBuild", {})))
        self.txt += str(Sec_BuildOptions(self.content.get("BuildOptions", {})))
        self.txt += str(Sec_Components(self.content.get("Components", {})))
        self.txt += str(Sec_LibraryClasses(self.content.get("LibraryClasses", {})))
        self.txt += str(Sec_PcdsPatchableInModule(self.content.get("PcdspatchableInModule", {})))
        self.txt += str(Sec_PcdsDynamicDefault(self.content.get("PcdsDynamicDefault", {})))
        self.txt += str(Sec_PcdsDynamicExDefault(self.content.get("PcdsDynamicExDefault", {})))
        self.txt += str(Sec_PcdsDynamicHii(self.content.get("PcdsDynamicHii", {})))
        self.txt += str(Sec_PcdsDynamicExHii(self.content.get("PcdsDynamicExHii", {})))
        self.txt += str(Sec_PcdsDynamicVpd(self.content.get("PcdsDynamicVpd", {})))
        self.txt += str(Sec_PcdsDynamicExVpd(self.content.get("PcdsDynamicExVpd", {})))
        self.txt += str(Sec_Libraries(self.content.get("Libraries", {})))
        self.txt += str(Sec_UserExtensions(self.content.get("UserExtensions", {})))
        return self.txt

    def FormatYaml(self):
        import yaml
        self.txt = yaml.dump(self.content, default_flow_style=False)
        return self.txt

    def FormatJson(self):
        import json
        self.txt = json.dumps(self.content,indent=2)
        with open("OvmfPkgX64.dsc.json", "w") as f:
            f.write(self.txt)
        return self.txt

    def ParserPcd(self, dsc_parser_dict, PcdsDict, ItemType, PcdTypeName):
        '''
        {
            PcdsFeatureFlag:
                {
                    arch: {
                        platform: {
                            PcdName: PcdValue
                        }
                    }
                }
        }
        '''

        for arch in dsc_parser_dict:
            dsc_parser = dsc_parser_dict[arch]
            model_dict = OrderedDict()
            for item in dsc_parser[ItemType, arch]:
                platform = item.Scope2
                PcdName = item.Value1 + "." + item.Value2
                PcdValue = item.Value3.replace("|", "")
                if platform not in model_dict.keys():
                    model_dict[platform] = OrderedDict()
                model_dict[platform].update({PcdName:PcdValue})
            PcdsDict.setdefault(arch, OrderedDict()).update(model_dict)
        if PcdsDict:
            for arch, dic in PcdsDict.items():
                if dic:
                    self.content.update({PcdTypeName: PcdsDict})
                    break

    def Set_Defines(self,dsc_parser_dict):
        dsc_parser = dsc_parser_dict.get("COMMON", list(dsc_parser_dict.values())[0])
        defines_section = OrderedDict()
        keywords = OrderedDict()
        macros = OrderedDict()
        edk_globals = OrderedDict()
        for item in dsc_parser[DC.MODEL_META_DATA_HEADER]:
            keywords[item.Value2] = item.Value3
        for item in dsc_parser[DC.MODEL_META_DATA_DEFINE,"COMMON","COMMON"]:
            macros[item.Value2] = item.Value3
        for item in dsc_parser[DC.MODEL_META_DATA_GLOBAL_DEFINE,"COMMON","COMMON"]:
            edk_globals[item.Value1] = item.Value2
        
        defines_section["Defines"] = keywords
        defines_section["Defines"]['DEFINE'] = macros 
        defines_section["Defines"]['EDK_GLOBAL'] = edk_globals
        if defines_section:
            self.content.update(defines_section)

    def Set_SkuIds(self, dsc_parser_dict):
        dsc_parser = dsc_parser_dict.get("COMMON", list(dsc_parser_dict.values())[0])
        skuids = OrderedDict()
        for item in dsc_parser[DC.MODEL_EFI_SKU_ID]:
            skuids[item.Value1] = " | ".join((item.Value2, item.Value3)) if item.Value3 else item.Value2
        if skuids:
            self.content.update({"SkuIds":skuids})

    def Set_DefaultStores(self, dsc_parser_dict):
        dsc_parser = dsc_parser_dict.get("COMMON", list(dsc_parser_dict.values())[0])
        defaultstores = OrderedDict()
        for item in dsc_parser[DC.MODEL_EFI_DEFAULT_STORES]:
            defaultstores[item.Value1] = " | ".join((item.Value2, item.Value3)) if item.Value3 else item.Value2

        if defaultstores:
            self.content.update({"DefaultStores":defaultstores})

    def Set_Packages(self, dsc_parser_dict):
        dsc_parser = dsc_parser_dict.get("COMMON", list(dsc_parser_dict.values())[0])
        packages = []
        for item in dsc_parser[DC.MODEL_META_DATA_PACKAGE]:
            packages.append(item.Value1)
        if packages:
            self.content.update({"Packages":packages})

    def Set_BuildOptions(self,dsc_parser_dict):
        '''
        row = [
            ToolChain,
            FLAGS,
            FLAGSValue,
            Arch,
            CodeBase, # EDKII
            ModuleType,
            ID,
            LineNum
        ]
        '''
        build_opts = OrderedDict()
        '''
        build_opts:
            Arch1:
                ModuleType1:
                    ToolChain1:
                        FLAG_1:
                            Value_1
                        FLAG_2:
                            Value_2
                    ToolChain2:
                        FLAG_3:
                            Value_3
                ModuleType2:
                    ...
            Arch2:
                ...
        '''
        for arch in dsc_parser_dict:
            dsc_parser = dsc_parser_dict[arch]
            l_build_opts = OrderedDict()
            for item in dsc_parser[DC.MODEL_META_DATA_BUILD_OPTION, arch]:
                if not item.Value1:
                    toolchain = "COMMON"
                else:
                    toolchain = item.Value1
                module_type = item.Scope2
                flag = item.Value2
                flagvalue = item.Value3

                if module_type not in l_build_opts:
                    l_build_opts[module_type] = OrderedDict()
                if toolchain not in l_build_opts[module_type]:
                    l_build_opts[module_type][toolchain] = OrderedDict()
                l_build_opts[module_type][toolchain][flag] = flagvalue

            build_opts[arch] = l_build_opts
        if build_opts:
            self.content.update({"BuildOptions":build_opts})

    def Set_LibraryClasses(self, dsc_parser_dict):
        '''
        row = [
            LibraryClass,
            LibraryInstance,
            "",
            Arch,
            ModuleType,
            COMMON,
            ID,
            LineNo
        ]
        '''
        lib_classes = OrderedDict()
        '''
            {
                Arch:{
                    ModuleType:{
                        LibClass: LibInstance
                    }
                }
            }
        '''

        for arch in dsc_parser_dict:
            dsc_parser = dsc_parser_dict[arch]
            l_lib_class = OrderedDict()
            for item in dsc_parser[DC.MODEL_EFI_LIBRARY_CLASS,arch]:
                m_arch = item.Scope1
                module_t = item.Scope2
                libclass = item.Value1
                libIns = item.Value2
                if module_t not in l_lib_class:
                    l_lib_class[module_t] = OrderedDict()
                l_lib_class[module_t][libclass] = libIns

                lib_classes.setdefault(m_arch,OrderedDict()).update(l_lib_class)
        if libclass:
            self.content.update({"LibraryClasses":lib_classes})

    def Set_Components(self, dsc_parser_dict):
        components = OrderedDict()
        dsc_sub_section_name_and_type = {
            # PCD*
            (DT.TAB_PCDS + DT.TAB_PCDS_FIXED_AT_BUILD).upper(): DC.MODEL_PCD_FIXED_AT_BUILD,
            (DT.TAB_PCDS + DT.TAB_PCDS_PATCHABLE_IN_MODULE).upper(): DC.MODEL_PCD_PATCHABLE_IN_MODULE,
            (DT.TAB_PCDS + DT.TAB_PCDS_FEATURE_FLAG).upper(): DC.MODEL_PCD_FEATURE_FLAG,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_DEFAULT).upper(): DC.MODEL_PCD_DYNAMIC_EX_DEFAULT,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_VPD).upper(): DC.MODEL_PCD_DYNAMIC_EX_VPD,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_HII).upper(): DC.MODEL_PCD_DYNAMIC_EX_HII,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_DEFAULT).upper(): DC.MODEL_PCD_DYNAMIC_DEFAULT,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_VPD).upper(): DC.MODEL_PCD_DYNAMIC_VPD,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_HII).upper(): DC.MODEL_PCD_DYNAMIC_HII,
            # LibraryClasses
            (DT.TAB_LIBRARY_CLASSES).upper(): DC.MODEL_EFI_LIBRARY_CLASS,
            # BuildOptions
            (DT.TAB_BUILD_OPTIONS).upper(): DC.MODEL_META_DATA_BUILD_OPTION
        }
        '''
        {
            components: {
                arch: {
                    model1: {
                        libraryclassName: libins,
                        PcdType: Pcds,
                        Buildoptions: optValues
                    },
                    model2,
                    ...
                    }
                }
            }
        }
        '''
        for arch in dsc_parser_dict:
            dsc_parser = dsc_parser_dict[arch]
            components[arch] = OrderedDict()
            for model in dsc_parser[DC.MODEL_META_DATA_COMPONENT, arch]:
                if dsc_parser[DC.MODEL_META_DATA_SUBSECTION_HEADER, arch, "COMMON", model.ID]:
                    model_dict = OrderedDict()
                    for sub_section in dsc_parser[DC.MODEL_META_DATA_SUBSECTION_HEADER, arch, "COMMON", model.ID]:
                        section_name = sub_section.Value1
                        #
                        # <LibraryClasses>
                        #
                        if section_name == (DT.TAB_LIBRARY_CLASSES).upper():
                            if dsc_parser[DC.MODEL_EFI_LIBRARY_CLASS, arch, "COMMON", model.ID]:
                                libs = list()
                                for lib in dsc_parser[DC.MODEL_EFI_LIBRARY_CLASS, arch, "COMMON", model.ID]:
                                    libs.append(lib.Value1 + "|" + lib.Value2)
                                model_dict[section_name] = libs
                        #
                        # <Pcd*>
                        #
                        elif "PCDS" in section_name:
                            if dsc_parser[dsc_sub_section_name_and_type[section_name], arch, "COMMON", model.ID]:
                                pcds = OrderedDict()
                                for item in dsc_parser[dsc_sub_section_name_and_type[section_name], arch, "COMMON", model.ID]:
                                    PcdName = item.Value1 + "." + item.Value2
                                    PcdValue = item.Value3.replace("|", "")
                                    pcds[PcdName] = PcdValue
                                model_dict[section_name] = pcds
                        #
                        # <BuildOptions>
                        #
                        elif section_name == (DT.TAB_BUILD_OPTIONS).upper():
                            if dsc_parser[dsc_sub_section_name_and_type[section_name], arch, "COMMON", model.ID]:
                                buildoptions_dcit = OrderedDict()
                                for opt in dsc_parser[dsc_sub_section_name_and_type[section_name], arch, "COMMON", model.ID]:
                                    if not opt.Value1:
                                        toolchain = "COMMON"
                                    else:
                                        toolchain = opt.Value1
                                    if toolchain not in buildoptions_dcit:
                                        buildoptions_dcit[toolchain] = OrderedDict()

                                    flag = opt.Value2
                                    flagValue = opt.Value3
                                    buildoptions_dcit[toolchain][flag] = flagValue
                                model_dict[section_name] = buildoptions_dcit
                    components[arch][model.Value1] = model_dict
                    continue
                components[arch][model.Value1] = ""
        self.content.update({"Components": components})

    def Set_PcdsFeatureFlag(self, dsc_parser_dict):
        PcdsFeatureFlag = OrderedDict()
        ItemType = DC.MODEL_PCD_FEATURE_FLAG

        self.ParserPcd(dsc_parser_dict,PcdsFeatureFlag, ItemType, "PcdsFeatureFlag")

    def Set_PcdsFixedAtBuild(self, dsc_parser_dict):
        PcdsFixedAtBuild = OrderedDict()

        ItemType = DC.MODEL_PCD_FIXED_AT_BUILD

        self.ParserPcd(dsc_parser_dict, PcdsFixedAtBuild, ItemType, "PcdsFixedAtBuild")

    def Set_PcdsPatchableInModule(self, dsc_parser_dict):
        PcdsPatchableInModule = OrderedDict()

        ItemType = DC.MODEL_PCD_PATCHABLE_IN_MODULE

        self.ParserPcd(dsc_parser_dict, PcdsPatchableInModule, ItemType, "PcdsPatchableInModule")

    def Set_PcdsDynamicDefault(self, dsc_parser_dict):
        PcdsDynamicDefault = OrderedDict()
        ItemType = DC.MODEL_PCD_DYNAMIC_DEFAULT

        self.ParserPcd(dsc_parser_dict, PcdsDynamicDefault, ItemType, "PcdsDynamicDefault")

    def Set_PcdsDynamicHii(self, dsc_parser_dict):
        PcdsDynamicHii = OrderedDict()

        ItemType = DC.MODEL_PCD_DYNAMIC_HII

        self.ParserPcd(dsc_parser_dict, PcdsDynamicHii, ItemType, "PcdsDynamicHii")

    def Set_PcdsDynamicVpd(self, dsc_parser_dict):
        PcdsDynamicVpd = OrderedDict()

        ItemType= DC.MODEL_PCD_DYNAMIC_VPD

        self.ParserPcd(dsc_parser_dict, PcdsDynamicVpd, ItemType, "PcdsDynamicVpd")

    def Set_PcdsDynamicExDefault(self, dsc_parser_dict):
        PcdsDynamicExDefault = OrderedDict()

        ItemType = DC.MODEL_PCD_DYNAMIC_EX_DEFAULT

        self.ParserPcd(dsc_parser_dict, PcdsDynamicExDefault, ItemType, "PcdsDynamicExDefault")

    def Set_PcdsDynamicExHii(self, dsc_parser_dict):
        PcdsDynamicExHii = OrderedDict()

        ItemType = DC.MODEL_PCD_DYNAMIC_EX_HII

        self.ParserPcd(dsc_parser_dict, PcdsDynamicExHii, ItemType, "PcdsDynamicExHii")

    def Set_PcdsDynamicExVpd(self, dsc_parser_dict):
        PcdsDynamicExVpd = OrderedDict()

        ItemType = DC.MODEL_PCD_DYNAMIC_EX_VPD

        self.ParserPcd(dsc_parser_dict, PcdsDynamicExVpd, ItemType, "PcdsDynamicExVpd")

    def Set_Libraries(self, dsc_parser_dict):
        Libraries = OrderedDict()

        for arch in dsc_parser_dict:
            Libraries[arch] = list()
            dsc_parser = dsc_parser_dict[arch]
            for item in dsc_parser[DC.MODEL_EFI_LIBRARY_INSTANCE, arch]:
                Libraries[arch].append(item.Value1)
        self.content.update({"Libraries": Libraries})

    def Set_UserExtensions(self, dsc_parser_dict):
        pass

class Sec_Pcds(object):
    def JoinPcd(self, PcdName, content, tab_sp, sp, description=""):
        if content:
            Pcd_StrList = []
            Pcd_StrList.append(description)
            for arch in content:
                for platform in content[arch]:
                    sectionName = "[%s.%s]" % (PcdName, arch)
                    if platform != "COMMON":
                        sectionName = "[%s.%s.%s]" % (PcdName, arch, platform)
                    Pcd_StrList.append(sectionName)
                    for pcd, pcdValue in content[arch][platform].items():
                        pcd_str = tab_sp + pcd + sp + pcdValue
                        Pcd_StrList.append(pcd_str)
                    Pcd_StrList.append("\n")
            return "\r\n".join(Pcd_StrList)
        return ""

class Sec_Defines(object):
    DEFINE_STR = "DEFINE"
    EDK_GLOBAL_STR     = "EDK_GLOBAL"
    DESCRIPTION = '''
################################################################################
#
# Defines Section - statements that will be processed to create a Makefile.
#
################################################################################
'''
    def __init__(self, content):
        self.keywords = content
        self.macros = content.get("DEFINE",{})
        self.edk_globals = content.get("EDK_GLOBAL", {})
        self.tab_sp = "  "

    def __str__(self):
        section_strlst = []
        section_strlst.append(self.DESCRIPTION)
        section_strlst.append("[Defines]")
        def_len = len(self.DEFINE_STR) + 1
        glo_len = len(self.EDK_GLOBAL_STR) + 1

        # key_str_width = max(
        #     [
        #         max([len(k) for k in self.keywords]),
        #         max([len(k) for k in self.macros]) + def_len,
        #         max([len(k) for k in self.edk_globals]) + glo_len,
        #     ])
        key_str_width = self.stringMax()

        for key in self.keywords:
            if key in ["DEFINE","EDK_GLOBAL"]:
                continue
            section_strlst.append(self.tab_sp + "{0:<{width}}".format(key,width=key_str_width) + " = " + self.keywords[key])

        section_strlst.append("")
        for key in self.macros:
            section_strlst.append(self.tab_sp + "DEFINE {0:<{width}}".format(key,width = key_str_width - def_len) + " = " + self.macros[key])

        section_strlst.append("")
        for key in self.edk_globals:
            section_strlst.append(self.tab_sp + "EDK_GLOBAL {0:<{width}}".format(key,width = key_str_width - glo_len) + " = " + self.edk_globals[key])

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
            key_str_width.append(max([len(k) for k in self.edk_globals]) + glo_len)
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
                section_strlst.append(self.tab_sp + " | ".join((key,value)))

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
    
    def __init__(self,content):
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
                        flag_value = self.buildoptions[arch][module_type][toolchain][flag]
                        if module_type == "COMMON":
                            section_head = "[" + ".".join(("BuildOptions",arch)) + "]"
                        else:
                            section_head = "[" + ".".join(("BuildOptions",arch,"EDKII",module_type)) + "]"
                        if section_head not in sections:
                            sections[section_head] = OrderedDict()
                        if toolchain not in sections[section_head]:
                            sections[section_head][toolchain] = OrderedDict()
                        sections[section_head][toolchain].update({flag:flag_value})
        for sec_head in sections:
            section_strlst.append(sec_head)
            for toolchain in sections[sec_head]:
                for flag in sections[sec_head][toolchain]:
                    flag_value = sections[sec_head][toolchain][flag]
                    if toolchain == "COMMON":
                        if flag_value.startswith("="):
                            section_strlst.append(self.tab_sp + flag + " =" + flag_value)
                        else:
                            section_strlst.append(self.tab_sp + flag + " = " + flag_value)
                    else:
                        if flag_value.startswith("="):
                            section_strlst.append(self.tab_sp + toolchain + ":" + flag + " =" + flag_value)
                        else:
                            section_strlst.append(self.tab_sp + toolchain + ":" + flag + " = " + flag_value)
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
                        sec_head = "[LibraryClasses.%s.%s]" % (arch,module_t)
                    sections.setdefault(sec_head, OrderedDict())[lib_class] = lib_inst
        
        for sec_head in sections:
            section_strlst.append(sec_head)
            for lib_class, lib_ins in sections[sec_head].items():
                section_strlst.append("%s%s|%s" % (self.tab_sp, lib_class, lib_ins))
            section_strlst.append("")

        section_strlst.append("\n")
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
            (DT.TAB_PCDS + DT.TAB_PCDS_FIXED_AT_BUILD).upper(): DT.TAB_PCDS + DT.TAB_PCDS_FIXED_AT_BUILD,
            (DT.TAB_PCDS + DT.TAB_PCDS_PATCHABLE_IN_MODULE).upper(): DT.TAB_PCDS + DT.TAB_PCDS_PATCHABLE_IN_MODULE,
            (DT.TAB_PCDS + DT.TAB_PCDS_FEATURE_FLAG).upper(): DT.TAB_PCDS + DT.TAB_PCDS_FEATURE_FLAG,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_DEFAULT).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_DEFAULT,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_VPD).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_VPD,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_HII).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_EX_HII,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_DEFAULT).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_DEFAULT,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_VPD).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_VPD,
            (DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_HII).upper(): DT.TAB_PCDS + DT.TAB_PCDS_DYNAMIC_HII,
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
                                components_strlsit.append("%s%s<LibararyClasses>" % (self.tab_sp, self.tab_sp))
                                for lib in value:
                                    components_strlsit.append("%s%s%s%s" % (self.tab_sp, self.tab_sp, self.tab_sp, lib))
                            elif "PCDS" in secName:
                                components_strlsit.append("%s%s<%s>" %(self.tab_sp, self.tab_sp, self.PcdType[secName]))
                                for PcdName, PcdValue in value.items():
                                    components_strlsit.append("%s%s%s%s|%s" % (self.tab_sp, self.tab_sp, self.tab_sp, PcdName, PcdValue))
                            elif secName == (DT.TAB_BUILD_OPTIONS).upper():
                                components_strlsit.append("%s%s<BuildOptions>" %(self.tab_sp, self.tab_sp))
                                for toolchain, flag_fvalue_dict in value.items():
                                    for flag, flagValue in flag_fvalue_dict.items():
                                        components_strlsit.append("%s%s%s%s:%s = %s" % (self.tab_sp, self.tab_sp, self.tab_sp, toolchain, flag, flagValue))
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
        return self.JoinPcd(self.PcdName, self.PcdsFeatureFlag, self.tab_sp, self.sp, self.DESCRIPTION)

class Sec_PcdsFixedAtBuild(Sec_Pcds):
    def __init__(self, content):
        self.PcdsFixedAtBuild = content
        self.sp = "|"
        self.tab_sp = "  "
        self.PcdName = "PcdsFixedAtBuild"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsFixedAtBuild, self.tab_sp, self.sp)

class Sec_PcdsPatchableInModule(Sec_Pcds):
    def __init__(self, content):
        self.PcdsPatchableInModule = content
        self.sp = "|"
        self.tab_sp = "  "
        self.PcdName = "PcdsPatchableInModule"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsPatchableInModule, self.tab_sp, self.sp)

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
        return self.JoinPcd(self.PcdName, self.PcdsDynamicDefault, self.tab_sp, self.sp, self.DESCRIPTION)

class Sec_PcdsDynamicHii(Sec_Pcds):
    def __init__(self, content):
        self.PcdsDynamicHii = content
        self.tab_sp = "  "
        self.sp = '|'
        self.PcdName = "PcdsDynamicHii"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicHii, self.tab_sp, self.sp)

class Sec_PcdsDynamicVpd(Sec_Pcds):
    def __init__(self, content):
        self.PcdsDynamicVpd = content
        self.tab_sp = "  "
        self.sp = '|'
        self.PcdName = "PcdsDynamicVpd"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicVpd, self.tab_sp, self.sp)

class Sec_PcdsDynamicExDefault(Sec_Pcds):
    def __init__(self, content):
        self.PcdsDynamicExDefault = content
        self.tab_sp = "  "
        self.sp = '|'
        self.PcdName = "PcdsDynamicExDefault"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicExDefault, self.tab_sp, self.sp)

class Sec_PcdsDynamicExHii(Sec_Pcds):
    def __init__(self, content):
        self.PcdsDynamicExHii = content
        self.tab_sp = "  "
        self.sp = '|'
        self.PcdName = "PcdsDynamicExHii"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicExHii, self.tab_sp, self.sp)

class Sec_PcdsDynamicExVpd(Sec_Pcds):
    def __init__(self, content):
        self.PcdsDynamicExVpd = content
        self.tab_sp = "  "
        self.sp = '|'
        self.PcdName = "PcdsDynamicExVpd"

    def __str__(self):
        return self.JoinPcd(self.PcdName, self.PcdsDynamicExVpd, self.tab_sp, self.sp)

class Sec_Libraries(object):
    def __init__(self, content):
        self.Libraries = content
        self.tab_sp = "  "
    def __str__(self):
        if self.Libraries:
            Libraries_StrList = []
            for arch in self.Libraries:
                Libraries_StrList.append("[Libraries.%s]" % arch)
                Libraries_StrList.extend([self.tab_sp + item for item in self.Libraries[arch]])
            return "\r\n".join(Libraries_StrList)
        return ""
class Sec_UserExtensions(object):
    def __init__(self, content):
        pass

    def __str__(self):
        return ""

