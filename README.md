# edk2-parser
The edk2 metadata files parsers including dsc parser, fdf parser, dec parser, and inf parser.

In addition, edk2-parser provides utilities to :
1. Parse source files and generate filtered new files
2. The filtered content generates a json file
3. The filtered content generates a yaml file
# Github link
For detailed code, see [edk2-parser code](https://github.com/mingyueliang/edk2-parser/tree/mingyue).

# Input 
1. Meta file(dsc, dec, inf, fdf)
#### From
1. From yaml
2. From json

Read files of the above types for other operations.

# Output
#### Meta File  Parser Type
1. Dsc parser
2. Dec parser
3. Inf parser
4. Fdf parser

Save the parsed content in the dictionary.

#### Format
1. Format yaml
2. Format json
3. Format metafile(dsc, dec, inf, fdf)

Read the data in the dictionary and generate files according to different standards.


# Parser Test
1. Test dsc
2. Test dec
3. Test inf
4. Test fdf



# Edk2 spec links
- [Edk2 Specifications](https://github.com/tianocore/tianocore.github.io/wiki/EDK-II-Documentation#specifications)
- [DSC Specifications](https://tianocore-docs.github.io/edk2-DscSpecification/release-1.28/)
- [DEC Specifications](https://tianocore-docs.github.io/edk2-DecSpecification/release-1.27/)
- [INF Specifications](https://tianocore-docs.github.io/edk2-InfSpecification/release-1.27/)
- [FDF Specifications](https://tianocore-docs.github.io/edk2-FdfSpecification/release-1.28.01/)



