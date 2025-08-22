Environment Requirements
Please ensure all required dependency packages and related plugins for the project are properly installed.

Usage Steps

1.Prepare the data:

    Place the existing dataset in the .\data\origin_data directory.

    Within the origin_data folder, ensure the corresponding mask and image files are placed in subfolders with matching names.

    Place the background images to be used for expansion in the .\data\background_data folder.（The author's self-built flood dataset augmentation library is located in the folder .\Flood_Dataset_Augmentation_Library. It can be used by copying it to .\data\background_data.）

2.Run the extraction script:

    Execute 1_Extract_flood_areas.py to extract flood areas and output the resulting images.

3.Run the expansion script:

    Execute 2_Expand_extracted_flow.py to perform reshape operations on the extracted flood areas.

4.Generate the final images:

    Execute 3_Paste_images.py to composite the processed flood areas with the background images. The final results will be saved in the .\data\finally_flow_data directory.


中文：
环境要求
请确保正常安装项目所需的依赖包及相关插件。

使用步骤
1.准备数据：

    将已有数据集放置于 .\data\origin_data 目录中。

    在 origin_data 文件夹内，请将对应的 mask 和 pic 图像分别放置于名称对应的子文件夹中。

    将需要用于扩充的背景图像放置于 .\data\background_data 文件夹中。(作者自建的洪水数据集扩充库在文件夹.\Flood_Dataset_Augmentation_Library中，将其复制在 .\data\background_data中即可使用)

2.运行提取脚本：

    python 1_Extract_flood_areas.py，提取洪水区域并输出结果图像。

3.运行扩展脚本：

    python 2_Expand_extracted_flow.py，对已提取的洪水区域进行形状调整（reshape）操作。

4.生成最终图像：

    python 3_Paste_images.py，将处理后的洪水区域与背景图像合成，最终结果将保存于 .\data\finally_flow_data 目录中。


