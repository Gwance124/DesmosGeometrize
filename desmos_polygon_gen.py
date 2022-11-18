import http.server
import socketserver
from os import path

"""
    A simple http request handler to serve a javascript file named "serve.js" in the current dir.
"""
class _JSDesmosTableServer(http.server.SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/javascript')
        self.end_headers()

    def getPath(self):
        return "./serve.js"

    def getContent(self, content_path):
        with open(content_path, mode='r') as f:
            content = f.read()
        return content.encode('utf-8')

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self.getContent(self.getPath()))

# Start of table functions

"""
    Makes an expression that adds one polygon equation with many faces to desmos. 

    poly_points - 3D list of floats or ints. Determines the points in the polygon.
       3rd dim are [x,y] pairs to define points. 2nd dim comprises the many points of a single polygon. 
        The 1st dim defines the many polygons that exist in this equation. *where 1st dim is the outermost dimension*.
        Must have a regular shape.
    colors - 2D array definining polygon color. 2nd dim holds RGB values for each face [0,255]. 1st dimention is the collection
        of RGB values across polygons.
    id - String to define id of the equation. This can be any unique string.
    frame - integer frame to display this polygon.
    opacity - opacity for all faces in this polygon [0,1].
"""
def single_set_to_polygons(poly_points, colors, id, frame=0, opacity=0.5):
    # Process points
    split_points = []
    for point_pair in range(len(poly_points[0])):
        for dim in range(2):
            vals = []
            for polygon_point in range(len(poly_points)):
                vals.append(poly_points[polygon_point][point_pair][dim])
            split_points.append(vals)

    polygon_expression = f"\\operatorname{{polygon}}(("
    for i in range(int(len(split_points)/2)):
        polygon_expression += (str(split_points[2*i]) + "," + str(split_points[2*i+1]) + f")\\left\\{{f={frame}\\right\\}},(").replace(" ", "")
    
    polygon_expression = polygon_expression[:-2] + ")"
    polygon_set_expression = f"window.Calc.setExpression({{id:'{id}', latex: {repr(polygon_expression)}, fillOpacity: '{opacity}', lines: false}});"

    # Process colors
    split_colors = []
    for color_componant in range(3):
        color_componantSet = []
        for color in colors:
            color_componantSet.append(color[color_componant])
        split_colors.append(color_componantSet)

    color_expression = f"\\operatorname{{rgb}}({str(split_colors[0])},{str(split_colors[1])},{str(split_colors[2])})".replace(" ", "")
    color_set_expression = f"window.Calc.controller.listModel.__itemIdToModel['{id}'].colorLatex={repr(color_expression)};"

    full_polygon_expression = polygon_set_expression + color_set_expression
    return full_polygon_expression

"""
    Makes an expression that adds many polygon equations each with many faces to desmos. 

    poly_points - 4D list of floats or ints. Determines the points in the polygon.
       4th dim are [x,y] pairs to define points. 3rd dim comprises the many points of a single polygon. 
        The 2nd dim defines the many polygons that exist in one equation. 1st dim holds many such equations (each should be 1 frame).
        *where 1st dim is the outermost dimension*. Must have a regular shape.
    colors - 3D array of ints [0,255] definining polygon color. 3rd dim holds RGB values for each face [0,255]. 2nd dim is the collection
        of RGB values across polygons of a single equation. 1st dim holds collections of RGB values across many equations.
    id_prefix- String to define id prefix of the equations. This can be any unique string.
    starting_frame - integer value of the first frame
    opacity - opacity for all faces in all equations [0,1].
"""
def multiple_set_to_polygons(poly_points, colors, id_prefix, starting_frame, opacity=0.5):
    expression = ""
    for i in range(len(poly_points)):
        expression += single_set_to_polygons(poly_points[i], colors[i], id_prefix + str(i), i + starting_frame, opacity)

    return expression


"""
    Saves a js expression as a file.

    expression - string, javascript expression to be saved.
    fileName - string, the name of the file to save as without extension. 
"""
def saveExpression(expression, fileName):
    fout = open(fileName + ".js", "w")
    fout.write(expression)
    fout.close()

"""
    Indefinitally hosts an expression on a webserver for easy upload to desmos. This function never returns.

    expression - string, javascript expression to host.
    port - int, port to host the server.
"""
def hostExpression(expression, port):
    saveExpression(expression, "serve")
    server = _JSDesmosTableServer

    with socketserver.TCPServer(("", port), server) as httpd:
        print("\nServing javascript expression. Type in the script below into a console with desmos to create the graph:\n")
        print(f"var script = document.createElement('script');script.type = 'text/javascript';script.src = 'http://localhost:{port}';document.head.appendChild(script);")
        httpd.serve_forever()
