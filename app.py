import gradio as gr

from utils.files import save_image_to_base64
from utils.plots import plot_evaluation_chart, plot_histogram
import base64

def calculate_perception(row):
    columns = ['Existence','Count','Position','Color','Poster','Celebrity','Scene','Landmark','Artwork','OCR']
    count = sum(row[column] for column in columns)
    return round(count,2)

def calculate_cognition(row):
    columns = ['Commensense Reasoning','Numerical Calculation','Text Translation','Code Reasoning']
    count = sum(row[column] for column in columns)
    return round(count,2)

def create_interface():
    with gr.Blocks() as demo:
        data_frame, output_path = plot_evaluation_chart("/Users/gatilin/PycharmProjects/MME-Eval-Kit/data/mllm_acc_eval-csv_private_0128.csv", "Existence")
        data_frame['Perception'] = data_frame.apply(calculate_perception, axis=1)
        data_frame['Cognition'] = data_frame.apply(calculate_cognition, axis=1)
        with gr.TabItem('🔍 About', elem_id='about', id=1):
            gr.Markdown("## MME-Eval-Kit")
            gr.Markdown("MME-Eval-Kit is a toolkit for model metrics evaluation.")

            # 将图像转换为base64编码
            encoded_leida_string = save_image_to_base64(output_path)
            gr.Markdown(f'<center><img src="data:image/png;base64,{encoded_leida_string}" alt="Evaluation Chart" width=480 height=480></center>')
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
                        encoded_histogram_string = save_image_to_base64(histogram_path)
                        gr.Markdown(f'<center><img src="data:image/png;base64,{encoded_histogram_string}" alt="f"{column} Histogram" width=640 height=480></center>')
    demo.launch()


if __name__ == '__main__':
    create_interface()