import os
import json
import desmos_polygon_gen

def load_desmos_polygons(frames_path):

    all_points = []
    all_colors = []

    frames = len(os.listdir(frames_path)) + 1

    for i in range(1, frames):
        with open(f"{frames_path}/frame{i}.jpg.json", "r") as frame:
            frame_data = json.loads(frame.read())
            polygon_EQ_points = []
            polygon_EQ_colors = []
            for data in frame_data:
                points = [[round(data['data'][0]),-round(data['data'][1])],[round(data['data'][2]),-round(data['data'][3])],[round(data['data'][4]),-round(data['data'][5])]]
                colors = [data['color'][0],data['color'][1], data['color'][2]]

                polygon_EQ_points.append(points)
                polygon_EQ_colors.append(colors)
                
            all_points.append(polygon_EQ_points)
            all_colors.append(polygon_EQ_colors)

    frame_ticker = f'window.Calc.controller.listModel.ticker.open=true;window.Calc.controller.listModel.ticker.handlerLatex="F";window.Calc.controller.listModel.ticker.minStepLatex="{1000//24}";'
    frame_increment = f'window.Calc.setExpression({{latex: "F=\\\\left\\\\{{f<{frames-2}:f{{\\\\to}}f+1, f={frames-2}:f{{\\\\to}}0\\\\right\\\\}}"}});'

    frame_slider = f'window.Calc.setExpression({{latex: "f=0", sliderBounds: {{ min: 0, max: {frames-2}, step: 1 }}}});'
    expression = frame_ticker + frame_increment + frame_slider + desmos_polygon_gen.multiple_set_to_polygons(all_points, all_colors, "f", 0)
    desmos_polygon_gen.hostExpression(expression, 8081)