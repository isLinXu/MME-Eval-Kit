import numpy as np
import pandas as pd
from matplotlib import rcParams, pyplot as plt

from utils.colors import colors_common_private
from utils.fonts import font_new_roman


def plot_evaluation_chart(csv_path, sort_column, output_path='evaluation_chart.png', font_size=25, figsize=(16, 16)):
    # 设置全局字体为Times New Roman
    rcParams['font.family'] = 'Times New Roman'

    # 读取CSV文件并提取数据
    data_frame = pd.read_csv(csv_path)
    data_frame = data_frame.sort_values(sort_column, ascending=False)  # 对DataFrame进行排序
    categories = list(data_frame.columns[1:])
    values = data_frame.values[:, 1:]
    model_labels = data_frame.values[:, 0]

    # 计算角度并闭合多边形
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    # 创建极坐标图并设置大小
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))

    # 设置坐标标签字体大小
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)

    # 隐藏最外圈的圆
    ax.spines['polar'].set_visible(False)

    # 绘制每一行数据的多边形
    for i, row in enumerate(values):
        cr = colors_common_private[i]
        data = np.concatenate((row, [row[0]]))  # 闭合多边形
        label_name = model_labels[i]
        ax.fill(angles, data, alpha=0.25,color=cr)  # 填充多边形
        ax.plot(angles, data, label=label_name, linewidth=2.0,color=cr)  # 绘制多边形

        # 设置图例属性
        num_models = len(values)
        legend = ax.legend(bbox_to_anchor=(0.5, -0.15), loc='lower center', ncol=num_models, prop=font_new_roman)
        for line in legend.get_lines():
            line.set_linewidth(5)

    # 设置刻度、标签和标题
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # 显示并保存图形
    # plt.show()
    fig.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)

    return data_frame, output_path  # 返回排序后的DataFrame和雷达图路径

def plot_histogram(data_frame, column, output_path='histogram.png'):
    sorted_data_frame = data_frame.sort_values(column, ascending=False)
    if type(sorted_data_frame[column].values[0]) != str:
        # 获取模型名称和数据
        model_names = sorted_data_frame['Model'].values
        data = sorted_data_frame[column].values

        # 为每个模型分配一个颜色
        colors = plt.get_cmap('tab20', len(model_names)).colors

        # 创建一个新的图形
        fig, ax = plt.subplots(figsize=(12, 6))

        # 使用bar函数绘制直方图
        bar_plot = ax.bar(model_names, data, color=colors)

        # 在直方图上显示数据
        for i, rect in enumerate(bar_plot):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., height, f'{data[i]:.2f}', ha='center', va='bottom')

        # 保存并关闭图形
        plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
        plt.close()
        return output_path