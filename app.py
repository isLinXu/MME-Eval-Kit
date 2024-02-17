

import gradio as gr
from utils.plots import plot_evaluation_chart, plot_histogram

def create_interface():
    with gr.Blocks() as demo:
        data_frame, output_path = plot_evaluation_chart("/Users/gatilin/PycharmProjects/MME-Eval-Kit/data/mllm_acc_eval-csv_private_0128.csv","Existence")
        with gr.TabItem('🔍 About', elem_id='about', id=1):
            gr.Markdown("## About")
            gr.Image(output_path, label="Evaluation Chart")

        with gr.Tabs(elem_classes='tab-buttons') as tabs:
            # 创建标签页
            for column in data_frame.columns:
                if type(data_frame[column].values[0]) != str:
                    with gr.TabItem(f'📊 {column} Leaderboard', elem_id=column):
                        # 在每个标签页中展示对应列的数据
                        gr.Markdown(f"## {column} Leaderboard")
                        sorted_data_frame = data_frame.sort_values(column, ascending=False)
                        gr.components.DataFrame(value=sorted_data_frame, type="pandas", interactive=False, visible=True)

                        # 在每个标签页中显示对应排序的直方图
                        histogram_path = f"histogram_{column}.png"
                        plot_histogram(data_frame, column, output_path=histogram_path)
                        gr.Image(histogram_path, label=f"{column} Histogram")
    demo.launch()

if __name__ == '__main__':
    create_interface()