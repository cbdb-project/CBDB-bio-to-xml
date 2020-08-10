# CBDB-BIO-to-xml
This file is a python package that converts BIO tagged files(in txt format) into xml files. The output files will be uploaded to the website Markus(https://dh.chinese-empires.eu/markus/beta/index.html) for further investigation conducted by experts.

STEP1:

The tagged txt files should be saved in a document folder named "tag_results". At the same time, the folder shall be put under the same directory with bio2markus.py

STEP2:

you could directly run the code in the package or import this module into your own script. In both ways, this python package will read the txt files and output xml files

STEP3:

The output files are of .html format. All output files generated by this package will be saved in a document folder named "markus" which is also placed in the same directory.

PS.

Please make sure that the txt files you would like to parse are of .txt format

My Python version is 3.7.4

#Chinese Version

第一步：

这一Python模块接收的BIO标注文件必须是txt格式。与此同时，这些txt格式文件应当被保存在文件夹"tag_results"中，并且该文件夹需要与bio2markus.py位于同一目录下

第二步：

你可以直接运行脚本中的代码，你也可以使用import命令将这一模块导入你自己的Python脚本中。

第三步：

程序输出的文件格式为 .html。所有输出的文件都被存放于相同目录内名为”markus“的文件夹内。

PS.

请确保所有的输入文件为BIO格式

我的Python版本为3.7.4
