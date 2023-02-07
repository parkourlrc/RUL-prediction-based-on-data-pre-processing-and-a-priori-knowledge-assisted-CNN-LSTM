新建一个output.txt在文件夹内，将处理好的B18rongliang.xls文件放在文件夹内。
该B18rongliang.xls文件是在原数据基础上使用=OFFSET($A$2,(ROW(A2)-1)*20,0)得到的
具体操作在B18rongliang处理用中有详细教程

打开quzao.py然后把导入文件的部分改成该文件夹中所用电池数据的名字如：B05rongliang.xls
然后直接运行应该就可以了

运行完以后，把生成的图片保存在文件夹中

生成的文件中，output.txt中记录了残差RES的值；example.xls中记录了模态分量IMF的值，每一列是一个IMF的值
example.xls中，从左到右分别为IMF1、IMF2···

新建一个XLS文件，名为B··各种组合，在该文件中，按照B18各种组合中每一列的提示，从第一列开始依次往后填
该文件中IMF1到res的意思是将IMF1、IMF2一直到res全部加在一起，然后填到这一列，即原始数据
IMF2到res的意思是将IMF2一直到res全部加在一起，然后填到这一列
以此类推···
每个电池的数据分解出的IMF数量可能不一样，根据具体情况进行调整。
