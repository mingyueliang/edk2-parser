## @file
# This file is used to check format of Meta file
#
# Copyright (c) 2022, Intel Corporation. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

# from collections import dict

from .FormatDsc import *
from .FormatDec import *
from .FormatInf import *

import CommonDataClass.DataClass as DC
import Common.DataType as DT
import json
import yaml


class MetaGenerator(object):
    """
    Meta file generator
    """
    def __init__(self):
        self.content = dict()
        self.txt = ""
        self.tab_sp = "  "
        self.arch_lst = set()

    def from_yaml(self, yaml_content):
        ''' Import the yaml_content into dict'''
        self.content = yaml.load(yaml_content)

    def from_json(self, json_content):
        ''' Import the json_content into dict'''
        self.content = json.loads(json_content)

    def FormatYaml(self):
        # with open("dsc.yml", "wt") as f:
        #     yaml.dump(self.content, f, default_flow_style=False, allow_unicode=True)

        self.txt = yaml.dump(self.content, default_flow_style=False)
        with open("dsc.yml", "w") as f:
            f.write(self.txt)
        return self.txt

    def FormatJson(self, file_name):
        self.txt = json.dumps(self.content,indent=2)
        with open(file_name, "w") as f:
            f.write(self.txt)
        return self.txt


class DscGen(MetaGenerator):
    def from_parser(self, dsc_parser):
        ''' Process the parser database and store the data in dict '''
        dsc_parser_dict = dict()
        if isinstance(dsc_parser,dict):
            dsc_parser_dict.update(dsc_parser)
        else:
            self.arch_lst.add(dsc_parser._Arch)
            dsc_parser_dict[dsc_parser._Arch] = dsc_parser
        self.Set_Defines(dsc_parser_dict)
        self.Set_SkuIds(dsc_parser_dict)
        self.Set_DefaultStores(dsc_parser_dict)
        self.Set_Packages(dsc_parser_dict)
        self.Set_BuildOptions(dsc_parser_dict)
        self.Set_LibraryClasses(dsc_parser_dict)
        self.Set_Components(dsc_parser_dict)
        #
        self.Set_PcdsFeatureFlag(dsc_parser_dict)
        self.Set_PcdsFixedAtBuild(dsc_parser_dict)
        self.Set_PcdsPatchableInModule(dsc_parser_dict)
        self.Set_PcdsDynamicDefault(dsc_parser_dict)
        self.Set_PcdsDynamicHii(dsc_parser_dict)
        self.Set_PcdsDynamicVpd(dsc_parser_dict)
        self.Set_PcdsDynamicExDefault(dsc_parser_dict)
        self.Set_PcdsDynamicExVpd(dsc_parser_dict)
        # # ...
        self.Set_Libraries(dsc_parser_dict)
        self.Set_UserExtensions(dsc_parser_dict)
        # ...

    def FormatDsc(self, filename):
        self.txt += str(Sec_Defines(self.content.get("Defines", {})))
        self.txt += str(Sec_SkuIds(self.content.get("SkuIds", {})))
        self.txt += str(Sec_DefaultStores(self.content.get("DefaultStores", {})))
        self.txt += str(Sec_Packages(self.content.get("Packages", {})))
        self.txt += str(Sec_BuildOptions(self.content.get("BuildOptions", {})))
        self.txt += str(Sec_Components(self.content.get("Components", {})))
        self.txt += str(Sec_LibraryClasses(self.content.get("LibraryClasses", {})))
        self.txt += str(Sec_PcdsFeatureFlag(self.content.get("PcdsFeatureFlag", {})))
        self.txt += str(Sec_PcdsFixedAtBuild(self.content.get("PcdsFixedAtBuild", {})))
        self.txt += str(Sec_PcdsPatchableInModule(self.content.get("PcdspatchableInModule", {})))
        self.txt += str(Sec_PcdsDynamicDefault(self.content.get("PcdsDynamicDefault", {})))
        self.txt += str(Sec_PcdsDynamicExDefault(self.content.get("PcdsDynamicExDefault", {})))
        self.txt += str(Sec_PcdsDynamicHii(self.content.get("PcdsDynamicHii", {})))
        self.txt += str(Sec_PcdsDynamicExHii(self.content.get("PcdsDynamicExHii", {})))
        self.txt += str(Sec_PcdsDynamicVpd(self.content.get("PcdsDynamicVpd", {})))
        self.txt += str(Sec_PcdsDynamicExVpd(self.content.get("PcdsDynamicExVpd", {})))
        self.txt += str(Sec_Libraries(self.content.get("Libraries", {})))
        self.txt += str(Sec_UserExtensions(self.content.get("UserExtensions", {})))
        with open(filename, "w") as f:
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
            model_dict = dict()
            for item in dsc_parser[ItemType, arch]:
                platform = item.Scope2
                PcdName = item.Value1 + "." + item.Value2
                PcdValue = item.Value3.replace("|", "")
                if platform not in model_dict.keys():
                    model_dict[platform] = dict()
                model_dict[platform].update({PcdName:PcdValue})
            PcdsDict.setdefault(arch, dict()).update(model_dict)
        if PcdsDict:
            for arch, dic in PcdsDict.items():
                if dic:
                    self.content.update({PcdTypeName: PcdsDict})
                    break

    def Set_Defines(self,dsc_parser_dict):
        dsc_parser = dsc_parser_dict.get("COMMON", list(dsc_parser_dict.values())[0])
        defines_section = dict()
        keywords = dict()
        macros = dict()
        edk_globals = dict()
        for item in dsc_parser[DC.MODEL_META_DATA_HEADER]:
            keywords[item.Value2] = item.Value3
        for item in dsc_parser[DC.MODEL_META_DATA_DEFINE,"COMMON","COMMON"]:
            macros[item.Value2] = item.Value3
        for item in dsc_parser[DC.MODEL_META_DATA_GLOBAL_DEFINE,"COMMON","COMMON"]:
            edk_globals[item.Value1] = item.Value2
        # Get all arch
        [self.arch_lst.add(arch) for arch in keywords["SUPPORTED_ARCHITECTURES"].split("|")]
        defines_section["Defines"] = keywords
        defines_section["Defines"]['DEFINE'] = macros
        defines_section["Defines"]['EDK_GLOBAL'] = edk_globals
        if defines_section:
            self.content.update(defines_section)

    def Set_SkuIds(self, dsc_parser_dict):
        dsc_parser = dsc_parser_dict.get("COMMON", list(dsc_parser_dict.values())[0])
        skuids = dict()
        for item in dsc_parser[DC.MODEL_EFI_SKU_ID]:
            skuids[item.Value1] = " | ".join((item.Value2, item.Value3)) if item.Value3 else item.Value2
        if skuids:
            self.content.update({"SkuIds":dict(skuids)})

    def Set_DefaultStores(self, dsc_parser_dict):
        dsc_parser = dsc_parser_dict.get("COMMON", list(dsc_parser_dict.values())[0])
        defaultstores = dict()
        for item in dsc_parser[DC.MODEL_EFI_DEFAULT_STORES]:
            defaultstores[item.Value1] = " | ".join((item.Value2, item.Value3)) if item.Value3 else item.Value2

        if defaultstores:
            self.content.update({"DefaultStores":dict(defaultstores)})

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
        build_opts = dict()
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
            l_build_opts = dict()
            for item in dsc_parser[DC.MODEL_META_DATA_BUILD_OPTION, arch]:
                if not item.Value1:
                    toolchain = "COMMON"
                else:
                    toolchain = item.Value1
                module_type = item.Scope2
                flag = item.Value2
                flagvalue = item.Value3

                if module_type not in l_build_opts:
                    l_build_opts[module_type] = dict()
                if toolchain not in l_build_opts[module_type]:
                    l_build_opts[module_type][toolchain] = dict()
                l_build_opts[module_type][toolchain][flag] = flagvalue

            build_opts[arch] = dict(l_build_opts)
        if build_opts:
            self.content.update({"BuildOptions":dict(build_opts)})

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
        lib_classes = dict()
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
            l_lib_class = dict()
            for item in dsc_parser[DC.MODEL_EFI_LIBRARY_CLASS,arch]:
                m_arch = item.Scope1
                module_t = item.Scope2
                libclass = item.Value1
                libIns = item.Value2
                if module_t not in l_lib_class:
                    l_lib_class[module_t] = dict()
                l_lib_class[module_t][libclass] = libIns

                lib_classes.setdefault(m_arch,dict()).update(dict(l_lib_class))
        if lib_classes:
            self.content.update({"LibraryClasses": dict(lib_classes)})

    def Set_Components(self, dsc_parser_dict):
        components = dict()
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
            components[arch] = dict()
            for model in dsc_parser[DC.MODEL_META_DATA_COMPONENT, arch]:
                if dsc_parser[DC.MODEL_META_DATA_SUBSECTION_HEADER, arch, "COMMON", model.ID]:
                    model_dict = dict()
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
                                pcds = dict()
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
                                buildoptions_dcit = dict()
                                for opt in dsc_parser[dsc_sub_section_name_and_type[section_name], arch, "COMMON", model.ID]:
                                    if not opt.Value1:
                                        toolchain = "COMMON"
                                    else:
                                        toolchain = opt.Value1
                                    if toolchain not in buildoptions_dcit:
                                        buildoptions_dcit[toolchain] = dict()

                                    flag = opt.Value2
                                    flagValue = opt.Value3
                                    buildoptions_dcit[toolchain][flag] = flagValue
                                model_dict[section_name] = buildoptions_dcit
                    components[arch][model.Value1] = model_dict
                    continue
                components[arch][model.Value1] = ""
        self.content.update({"Components": components})

    def Set_PcdsFeatureFlag(self, dsc_parser_dict):
        PcdsFeatureFlag = dict()
        ItemType = DC.MODEL_PCD_FEATURE_FLAG

        self.ParserPcd(dsc_parser_dict,PcdsFeatureFlag, ItemType, "PcdsFeatureFlag")

    def Set_PcdsFixedAtBuild(self, dsc_parser_dict):
        PcdsFixedAtBuild = dict()

        ItemType = DC.MODEL_PCD_FIXED_AT_BUILD

        self.ParserPcd(dsc_parser_dict, PcdsFixedAtBuild, ItemType, "PcdsFixedAtBuild")

    def Set_PcdsPatchableInModule(self, dsc_parser_dict):
        PcdsPatchableInModule = dict()

        ItemType = DC.MODEL_PCD_PATCHABLE_IN_MODULE

        self.ParserPcd(dsc_parser_dict, PcdsPatchableInModule, ItemType, "PcdsPatchableInModule")

    def Set_PcdsDynamicDefault(self, dsc_parser_dict):
        PcdsDynamicDefault = dict()
        ItemType = DC.MODEL_PCD_DYNAMIC_DEFAULT

        self.ParserPcd(dsc_parser_dict, PcdsDynamicDefault, ItemType, "PcdsDynamicDefault")

    def Set_PcdsDynamicHii(self, dsc_parser_dict):
        PcdsDynamicHii = dict()

        ItemType = DC.MODEL_PCD_DYNAMIC_HII

        self.ParserPcd(dsc_parser_dict, PcdsDynamicHii, ItemType, "PcdsDynamicHii")

    def Set_PcdsDynamicVpd(self, dsc_parser_dict):
        PcdsDynamicVpd = dict()

        ItemType= DC.MODEL_PCD_DYNAMIC_VPD

        self.ParserPcd(dsc_parser_dict, PcdsDynamicVpd, ItemType, "PcdsDynamicVpd")

    def Set_PcdsDynamicExDefault(self, dsc_parser_dict):
        PcdsDynamicExDefault = dict()

        ItemType = DC.MODEL_PCD_DYNAMIC_EX_DEFAULT

        self.ParserPcd(dsc_parser_dict, PcdsDynamicExDefault, ItemType, "PcdsDynamicExDefault")

    def Set_PcdsDynamicExHii(self, dsc_parser_dict):
        PcdsDynamicExHii = dict()

        ItemType = DC.MODEL_PCD_DYNAMIC_EX_HII

        self.ParserPcd(dsc_parser_dict, PcdsDynamicExHii, ItemType, "PcdsDynamicExHii")

    def Set_PcdsDynamicExVpd(self, dsc_parser_dict):
        PcdsDynamicExVpd = dict()

        ItemType = DC.MODEL_PCD_DYNAMIC_EX_VPD

        self.ParserPcd(dsc_parser_dict, PcdsDynamicExVpd, ItemType, "PcdsDynamicExVpd")

    def Set_Libraries(self, dsc_parser_dict):
        Libraries = dict()

        for arch in dsc_parser_dict:
            Libraries[arch] = list()
            dsc_parser = dsc_parser_dict[arch]
            for item in dsc_parser[DC.MODEL_EFI_LIBRARY_INSTANCE, arch]:
                Libraries[arch].append(item.Value1)
            # Check current arch or not value
            if not Libraries[arch]:
                Libraries.pop(arch)
        if Libraries:
            self.content.update({"Libraries": Libraries})

    def Set_UserExtensions(self, dsc_parser_dict):
        pass

class DecGen(MetaGenerator):
    def from_parser(self, dec_parser):
        ''' Process the parser database and store the data in dict '''
        dec_parser_dict = dict()
        if isinstance(dec_parser,dict):
            dec_parser_dict.update(dec_parser)
        else:
            dec_parser_dict[dec_parser._Arch] = dec_parser

        self.Set_Defines(dec_parser_dict)
        self.Set_Includes(dec_parser_dict)
        self.Set_Guids(dec_parser_dict)
        self.Set_Protocols(dec_parser_dict)
        self.Set_Ppis(dec_parser_dict)
        self.Set_LibraryClasses(dec_parser_dict)
        self.Set_PcdsFeatureFlag(dec_parser_dict)
        self.Set_PcdsFixedAtBuild(dec_parser_dict)
        self.Set_PcdsDynamic(dec_parser_dict)
        self.Set_PcdsDynamicEx(dec_parser_dict)
        self.Set_UserExtensions(dec_parser_dict)

    def FormatDec(self):
        self.txt += str(DecSecDefines(self.content.get("Defines", {})))
        self.txt += str(DecSecIncludes(self.content.get("Includes", {})))
        # Format Guids, Protocols, Ppis
        self.txt += str(DecSecHeader(self.content.get("Guids", {}), "Guids"))
        self.txt += str(DecSecHeader(self.content.get("Protocols", {}), "Protocols"))
        self.txt += str(DecSecHeader(self.content.get("Ppis", {}), "Ppis"))
        # Format LibraryClasses
        self.txt += str(DecSecLibraryClasses(self.content.get("LibraryClasses", {})))
        # Format Pcd
        self.txt += str(DecSecPcds(self.content.get("PcdsFixedAtBuild", {}), "PcdsFixedAtBuild"))
        self.txt += str(DecSecPcds(self.content.get("PcdsFeatureFlag", {}), "PcdsFeatureFlag"))
        self.txt += str(DecSecPcds(self.content.get("PcdsDynamic", {}), "PcdsDynamic"))
        self.txt += str(DecSecPcds(self.content.get("PcdsDynamicEx", {}), "PcdsDynamicEx"))
        self.txt += str(DecSecPcds(self.content.get("PcdsPatchableInModule", {}), "PcdsPatchableInModule"))

        # Format UserExtensions
        self.txt += str(DecSecUserExtensions(self.content.get("UserExtensions", {})))


        return self.txt

    def Set_Defines(self, dec_parser_dict):
        dec_parser = dec_parser_dict.get("COMMON", list(dec_parser_dict.values())[0])
        defines_section = dict()
        keywords = dict()
        macros = dict()
        for item in dec_parser[DC.MODEL_META_DATA_HEADER]:
            keywords[item.Value2] = item.Value3

        for item in dec_parser[DC.MODEL_META_DATA_DEFINE]:
            macros[item.Value2] = item.Value3

        defines_section["Defines"] = keywords
        defines_section["Defines"]["DEFINE"] = macros

        if defines_section:
            self.content.update(defines_section)

    def Set_Includes(self, dec_parser_dict):
        '''
            Includes:
                arch:
                    Private:
                        list
        '''
        IncludesDict = dict()
        for arch in dec_parser_dict.keys():
            dec_parser = dec_parser_dict[arch]
            arch_dict = dict()
            for item in dec_parser[DC.MODEL_EFI_INCLUDE, arch]:
                private = item.Scope2
                ins = item.Value1
                if private not in arch_dict:
                    arch_dict[private] = list()
                arch_dict[private].append(ins)
            IncludesDict.setdefault(arch, dict()).update(arch_dict)
        if IncludesDict:
            self.content.update({"Includes": IncludesDict})

    def Set_Guids(self, dec_parser_dict):
        GuidsDict = dict()

        for arch in dec_parser_dict.keys():
            dec_parser = dec_parser_dict[arch]
            arch_dict = dict()
            for item in dec_parser[DC.MODEL_EFI_GUID, arch]:
                private = item.Scope2
                if private not in arch_dict:
                    arch_dict[private] = dict()
                arch_dict[private][item.Value1] = item.Value2
            GuidsDict.setdefault(arch, dict()).update(arch_dict)
        if GuidsDict:
            self.content.update({"Guids": GuidsDict})

    def Set_Protocols(self, dec_parser_dict):
        '''
            Protocols:
                arch:
                    private:
                        key:value
        '''
        ProtocolsDict = dict()
        for arch in dec_parser_dict.keys():
            dec_parser = dec_parser_dict[arch]
            arch_dict = dict()
            for item in dec_parser[DC.MODEL_EFI_PROTOCOL, arch]:
                my_arch = item.Scope1
                private = item.Scope2
                key = item.Value1
                value = item.Value2
                if private not in arch_dict:
                    arch_dict[private] = dict()
                arch_dict[private][key] = value
            ProtocolsDict.setdefault(arch, dict()).update(arch_dict)
        if ProtocolsDict:
            self.content.update({"Protocols": ProtocolsDict})

    def Set_Ppis(self, dec_parser_dict):
        PpisDict = dict()
        for arch in dec_parser_dict.keys():
            dec_parser = dec_parser_dict[arch]
            arch_dict = dict()
            for item in dec_parser[DC.MODEL_EFI_PPI, arch]:
                private = item.Scope2
                key = item.Value1
                value = item.Value2
                if private not in arch_dict:
                    arch_dict[private] = dict()
                arch_dict[private][key] = value
            PpisDict.setdefault(arch, dict()).update(arch_dict)
        if PpisDict:
            self.content.update({"Ppis": PpisDict})

    def Set_LibraryClasses(self, dec_parser_dict):
        LibraryClassesDict = dict()
        for arch in dec_parser_dict.keys():
            dec_parser = dec_parser_dict[arch]
            lib_dict = dict()
            for item in dec_parser[DC.MODEL_EFI_LIBRARY_CLASS, arch]:
                ModelType = item.Scope2
                key = item.Value1
                value = item.Value2
                if ModelType not in lib_dict:
                    lib_dict[ModelType] = dict()
                lib_dict[ModelType][key] = value
            LibraryClassesDict.setdefault(arch, dict()).update(lib_dict)
        if LibraryClassesDict:
            self.content.update({"LibraryClasses": LibraryClassesDict})

    def SetPcd(self, ItemType, dec_parser_dict, PcdSecName):
        PcdsDict = dict()
        for arch in dec_parser_dict.keys():
            dec_parser = dec_parser_dict[arch]
            InPcds = dict()
            for item in dec_parser[ItemType, arch]:
                PcdName = item.Value1 + "." + item.Value2
                PcdValue = item.Value3
                InPcds[PcdName] = PcdValue
            PcdsDict[arch] = InPcds
        if PcdsDict:
            self.content.update({PcdSecName: PcdsDict})

    def Set_PcdsFeatureFlag(self, dec_parser_dict):
        PcdSecName = "PcdsFeatureFlag"
        ItemType = DC.MODEL_PCD_FEATURE_FLAG
        self.SetPcd(ItemType, dec_parser_dict, PcdSecName)

    def Set_PcdsFixedAtBuild(self, dec_parser_dict):
        PcdSecName = "PcdsFixedAtBuild"
        ItemType = DC.MODEL_PCD_FIXED_AT_BUILD
        self.SetPcd(ItemType, dec_parser_dict, PcdSecName)

    def Set_PcdsDynamic(self, dec_parser_dict):
        PcdSecName = "PcdsDynamic"
        ItemType = DC.MODEL_PCD_DYNAMIC
        self.SetPcd(ItemType, dec_parser_dict, PcdSecName)

    def Set_PcdsDynamicEx(self, dec_parser_dict):
        PcdSecName = "PcdsDynamicEx"
        ItemType = DC.MODEL_PCD_DYNAMIC_EX
        self.SetPcd(ItemType, dec_parser_dict, PcdSecName)

    def Set_PcdsPatchableInModule(self, dec_parser_dict):
        PcdSecName = "PcdsPatchableInModule"
        ItemType = DC.MODEL_PCD_PATCHABLE_IN_MODULE
        self.SetPcd(ItemType, dec_parser_dict, PcdSecName)

    def Set_UserExtensions(self, dec_parser_dict):
        UserExtensionsDict = dict()
        for arch in dec_parser_dict.keys():
            dec_parser = dec_parser_dict[arch]
            extFiles = list()
            for item in dec_parser[DC.MODEL_META_DATA_USER_EXTENSION]:
                pass


class InfGen(MetaGenerator):
    def from_parser(self, inf_parser):
        ''' Process the parser database and store the data in dict '''
        inf_parser_dict = dict()
        if isinstance(inf_parser, dict):
            inf_parser_dict.update(inf_parser)
        else:
            inf_parser_dict[inf_parser._Arch] = inf_parser

        self.Set_Defines(inf_parser_dict)
        self.Set_Sources(inf_parser_dict)
        self.Set_BuildOptions(inf_parser_dict)
        self.Set_LibraryClasses(inf_parser_dict)
        self.Set_Packages(inf_parser_dict)
        self.Set_Protocols(inf_parser_dict)
        self.Set_Ppis(inf_parser_dict)
        self.Set_Guids(inf_parser_dict)
        self.Set_Depex(inf_parser_dict)
        self.Set_Binaries(inf_parser_dict)
        self.Set_FixedPcd(inf_parser_dict)
        self.Set_Pcd(inf_parser_dict)
        self.Set_FeaturePcd(inf_parser_dict)
        self.Set_PatchPcd(inf_parser_dict)

    def FormatInf(self):
        self.txt += str(InfSecDefines(self.content.get("Defines", {})))
        self.txt += str(InfSecSources(self.content.get("Sources", {})))
        self.txt += str(InfSecBuildOptions(self.content.get("BuildOptions", {})))
        self.txt += str(InfSecOther(self.content.get("LibraryClasses", {}), "LibraryClasses"))
        self.txt += str(InfSecOther(self.content.get("Packages", {}), "Packages"))
        self.txt += str(InfSecOther(self.content.get("Protocols", {}), "Protocols"))
        self.txt += str(InfSecOther(self.content.get("Ppis", {}), "Ppis"))
        self.txt += str(InfSecOther(self.content.get("GUids", {}), "GUids"))
        self.txt += str(InfSecDepex(self.content.get("Depex", {})))
        self.txt += str(InfSecBinaries(self.content.get("Binaries", {})))
        self.txt += str(InfSecPcd(self.content.get("FixedPcd", {}), "FixedPcd"))
        self.txt += str(InfSecPcd(self.content.get("Pcd", {}), "Pcd"))
        self.txt += str(InfSecPcd(self.content.get("FeaturePcd", {}), "FeaturePcd"))
        self.txt += str(InfSecPcd(self.content.get("PatchPcd", {}), "PatchPcd"))
        self.txt += str(InfSecUserExtensions(self.content.get("UserExtensions", {})))


        return self.txt

    def Set_Defines(self, inf_parser_dict):
        inf_parser = inf_parser_dict.get("COMMON", list(inf_parser_dict.values())[0])
        defines_section = dict()
        keywords = dict()
        macros = dict()
        for item in inf_parser[DC.MODEL_META_DATA_HEADER]:
            keywords[item.Value2] = item.Value3

        for item in inf_parser[DC.MODEL_META_DATA_DEFINE]:
            macros[item.Value2] = item.Value3
        defines_section["Defines"] = keywords
        defines_section["Defines"]["DEFINE"] = macros
        if defines_section:
            self.content.update(defines_section)

    def Set_Sources(self, inf_parser_dict):
        SourcesDict = dict()
        for arch in inf_parser_dict.keys():
            inf_parser = inf_parser_dict[arch]
            sources = list()
            for item in inf_parser[DC.MODEL_EFI_SOURCE_FILE, arch]:
                sources.append(item.Value1)
            SourcesDict[arch] = sources
        if SourcesDict:
            self.content.update({"Sources": SourcesDict})

    def Set_BuildOptions(self, inf_parser_dict):
        BuildOptionsDict = dict()
        for arch in inf_parser_dict.keys():
            inf_parser = inf_parser_dict[arch]
            arch_dict = dict()
            for item in inf_parser[DC.MODEL_META_DATA_BUILD_OPTION, arch]:
                if not item.Value1:
                    toolchain = "COMMON"
                else:
                    toolchain = item.Value1
                module_type = item.Scope2
                flag = item.Value2
                flagvalue = item.Value3

                # if module_type not in arch_dict:
                #     arch_dict[module_type] = dict()
                if toolchain not in arch_dict:
                    arch_dict[toolchain] = dict()
                arch_dict[toolchain][flag] = flagvalue
            BuildOptionsDict[arch] = arch_dict
        if BuildOptionsDict:
             self.content.update({"BuildOptions": BuildOptionsDict})

    def Set_LibraryClasses(self, inf_parser_dict):
        LibraryClassesDict = dict()
        for arch in inf_parser_dict.keys():
            inf_parser = inf_parser_dict[arch]
            arch_list = list()
            for item in inf_parser[DC.MODEL_EFI_LIBRARY_CLASS, arch]:
                arch_list.append(item.Value1)
            LibraryClassesDict[arch] = arch_list
        if LibraryClassesDict:
            self.content.update({"LibraryClasses": LibraryClassesDict})

    def Set_Packages(self, inf_parser_dict):
        PackagesDict = dict()
        for arch in inf_parser_dict.keys():
            inf_parser = inf_parser_dict[arch]
            packages = list()
            for item in inf_parser[DC.MODEL_META_DATA_PACKAGE, arch]:
                packages.append(item.Value1)
            PackagesDict[arch] = packages
        if PackagesDict:
            self.content.update({"Packages": PackagesDict})

    def Set_Protocols(self, inf_parser_dict):
        ProtocolsDict = dict()
        for arch in inf_parser_dict.keys():
            inf_parser = inf_parser_dict[arch]
            Protocols = list()
            for item in inf_parser[DC.MODEL_EFI_PROTOCOL, arch]:
                Protocols.append(item.Value1)
            ProtocolsDict[arch] = Protocols
        if ProtocolsDict:
             self.content.update({"Protocols": ProtocolsDict})

    def Set_Ppis(self, inf_parser_dict):
        PpisDict = dict()
        for arch in inf_parser_dict.keys():
            inf_parser = inf_parser_dict[arch]
            Ppis = list()
            for item in inf_parser[DC.MODEL_EFI_PPI, arch]:
                Ppis.append(item.Value1 + "." + item.Value2)
            PpisDict[arch] = Ppis
        if PpisDict:
            self.content.update({"Ppis": PpisDict})

    def Set_Guids(self, inf_parser_dict):
        GuidsDict = dict()
        for arch in inf_parser_dict.keys():
            inf_parser = inf_parser_dict[arch]
            Guids = list()
            for item in inf_parser[DC.MODEL_EFI_GUID, arch]:
                Guids.append(item.Value1)
            GuidsDict[arch] = Guids
        if GuidsDict:
            self.content.update({"GUids": GuidsDict})

    def Set_Depex(self, inf_parser_dict):
        DepexDict = dict()
        for arch in inf_parser_dict.keys():
            inf_parser = inf_parser_dict[arch]
            InDepex = dict()
            for item in inf_parser[DC.MODEL_EFI_DEPEX, arch]:
                myarch = item.Scope1
                model_type = item.Scope2
                value = item.Value1
                if model_type not in InDepex:
                    InDepex[model_type] = list()
                InDepex[model_type].append(value)
            DepexDict[arch] = InDepex
        if DepexDict:
            self.content.update({"Depex": DepexDict})

    def Set_Binaries(self, inf_parser_dict):
        BinariesDict = dict()
        for arch in inf_parser_dict.keys():
            inf_parser = inf_parser_dict[arch]
            archs = dict()
            for item in inf_parser[DC.MODEL_EFI_BINARY_FILE, arch]:
                archs[item.Value1] = item.Value2
            BinariesDict[arch] = archs
        if BinariesDict:
            self.content.update({"Binaries": BinariesDict})

    def Set_UserExtensions(self, inf_parser_dict):
        pass

    def ParserPcd(self, ItemType, inf_parser_dict, PcdSecName):
        PcdDict = dict()
        for arch in inf_parser_dict.keys():
            inf_parser = inf_parser_dict[arch]
            InPcds = dict()
            for item in inf_parser[ItemType, arch]:
                PcdName = item.Value1 + "." + item.Value2
                PcdValue = item.Value3
                InPcds[PcdName] = PcdValue
            PcdDict[arch] = InPcds
        if PcdDict:
            self.content.update({PcdSecName: PcdDict})

    def Set_FixedPcd(self, inf_parser_dict):
        PcdSecName = "FixedPcd"
        ItemType = DC.MODEL_PCD_FIXED_AT_BUILD
        self.ParserPcd(ItemType, inf_parser_dict, PcdSecName)

    def Set_FeaturePcd(self, inf_parser_dict):
        ItemType = DC.MODEL_PCD_FEATURE_FLAG
        pcdSectionName = "FeaturePcd"
        self.ParserPcd(ItemType, inf_parser_dict, pcdSectionName)

    def Set_Pcd(self, inf_parser_dict):
        PcdSecName = "Pcd"
        ItemType = DC.MODEL_PCD_DYNAMIC
        self.ParserPcd(ItemType, inf_parser_dict, PcdSecName)

    def Set_PatchPcd(self, inf_parser_dict):
        PcdSecname = "PatchPcd"
        Itemtype = DC.MODEL_PCD_PATCHABLE_IN_MODULE
        self.ParserPcd(Itemtype, inf_parser_dict, PcdSecname)

    def Set_PcdEx(self, inf_parser_dict):
        PcdSecname = "PcdEx"
        ItemType = DC.MODEL_PCD_DYNAMIC_EX
        self.ParserPcd(ItemType, inf_parser_dict, PcdSecname)


#
# Fdf file generator
#
class FdfGen(MetaGenerator):
    def __init__(self):
        pass





