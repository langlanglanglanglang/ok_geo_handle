## 声明
此脚本是处理全国省市区的ok_geo.csv，不想下对应的数据处理工具，因为我的需求很简单，把数据导入mysql即可，但是直接导入的无法转为Mysql的geo格式
## 使用方法
1. 修改里面的geo文件地址和输出文件地址
然后
2. 执行
```
python3 geo_handle.py 
```

执行结果可能会报错 
```
EMPTY
处理坐标失败: EMPTY，错误: 无效的坐标数据
```
此时查看output.csv的数据行数，与源文件一致就没问题

3. 然后将此文件导入到mysql中，对应polygon字段记得修改为longtext，其他的无所谓
4. 然后执行sql: select id, pid, deep, name, st_geomfromtext(concat('Point(', geo,')')), st_geomfromtext(polygon) from demos.output; 
你就能得到一个mysql geo格式的数据了，此时是insert into到另一张复制表还是直接去查询都由你
