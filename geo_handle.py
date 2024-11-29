# -*- coding: utf-8 -*-

import csv
import sys

# 增大 CSV 字段大小限制
csv.field_size_limit(sys.maxsize) 
def process_coordinates_to_mysql(coord_string):
    """
    将坐标字符串处理为 MySQL 格式的 MultiPolygon 或 Polygon，并确保每个多边形收尾相连。

    Args:
        coord_string (str): 原始坐标字符串，多多边形用分号隔开。

    Returns:
        str: MySQL 格式的 MultiPolygon 或 Polygon 数据。
    """
    try:
        # 判断是否为 MultiPolygon（有分号）
        if ';' in coord_string:
            polygons = []
            for part in coord_string.split(';'):
                points = [
                    tuple(map(float, coord.split())) for coord in part.split(',')
                    if len(coord.split()) == 2
                ]

                # 如果点集有效，确保首尾相连
                if points and points[0] != points[-1]:
                    points.append(points[0])

                # 将单个多边形加入集合
                if points:
                    polygons.append(f"(({','.join(f'{x} {y}' for x, y in points)}))")

            # 如果有多个有效的多边形，返回 MultiPolygon
            if polygons:
                return f"MULTIPOLYGON ({','.join(polygons)})"
            else:
                raise ValueError("无有效多边形数据")

        else:  # 单个多边形
            points = [
                tuple(map(float, coord.split())) for coord in coord_string.split(',')
                if len(coord.split()) == 2
            ]

            # 如果点集有效，确保首尾相连
            if points and points[0] != points[-1]:
                points.append(points[0])

            # 返回单个 Polygon
            if points:
                polygon = f"(({','.join(f'{x} {y}' for x, y in points)}))"
                return f"POLYGON {polygon}"
            else:
                print(coord_string)
                raise ValueError("无效的坐标数据")

    except Exception as e:
        print(f"处理坐标失败: {coord_string}，错误: {e}")
        return "INVALID_GEOMETRY"

def process_csv(input_file, output_file):
    """
    处理 CSV 文件，将最后一列坐标数据转换为 MySQL 格式，其他字段保持原样。

    Args:
        input_file (str): 输入 CSV 文件路径。
        output_file (str): 输出 CSV 文件路径。
    """
    processed_rows = []

    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # 读取表头
        processed_rows = [header]
        for i, row in enumerate(reader):
            if len(row) < 7:
                print(f"输入数据格式错误，跳过该行：{row}")
                continue

            raw_coords = row[6]  # 假设第7列是坐标数据
            mysql_geometry = process_coordinates_to_mysql(raw_coords)

            # 更新最后一列为 MySQL 格式的几何数据
            row[6] = mysql_geometry
            processed_rows.append(row)

    # 写入新的 CSV 文件
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(processed_rows)

if __name__ == "__main__":
    input_csv = "ok_geo.csv"  # 输入文件名
    output_csv = "output.csv"  # 输出文件名

    process_csv(input_csv, output_csv)
    print(f"处理完成，结果已保存到 {output_csv}")

