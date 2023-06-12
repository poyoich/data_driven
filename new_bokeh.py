from bokeh.plotting import figure, show,output_file
from bokeh.models import CustomJS, Select, ColumnDataSource
from bokeh.layouts import column, row
from bokeh.models.widgets import TextInput
from bokeh.models.tickers import SingleIntervalTicker
from bokeh.models.widgets import Slider



# Create the data for the lines
x = [1, 2, 3, 4, 5]
y1 = [1, 4, 3, 2, 5]
y2 = [5, 2, 3, 1, 4]
y3 = [3, 1, 2, 4, 5]

# Create a ColumnDataSource to store the data
source = ColumnDataSource(data=dict(x=x, y1=y1, y2=y2, y3=y3))

# Create a figure
p = figure(width=400, height=300)

# Plot the lines with initial colors
line1 = p.line('x', 'y1', source=source, color='blue')
line2 = p.line('x', 'y2', source=source, color='green')
line3 = p.line('x', 'y3', source=source, color='red')

# Create dropdown menu for label name
label_select = Select(title="Label Name:", options=["Line 1", "Line 2", "Line 3"])
label_select.value = "Line 1"
# Create selection pull-down menu for line color
color_select = Select(title="Line Color:", options=["blue", "red", "green", "orange"])

# Create callback for color select change event
callback = CustomJS(args=dict(line1=line1, line2=line2, line3=line3, label_select=label_select, color_select=color_select), code="""
    var lineMap = { 'Line 1': line1, 'Line 2': line2, 'Line 3': line3 };
    var line = lineMap[label_select.value];
    line.glyph.line_color = color_select.value;
    line.glyph.legend_label = label_select.value;
    line.glyph.visible = true;
""")
color_select.js_on_change('value', callback)

# Set initial color for the selected line
initial_color_callback = CustomJS(args=dict(line1=line1, line2=line2, line3=line3, label_select=label_select, color_select=color_select), code="""
    var lineMap = { 'Line 1': line1, 'Line 2': line2, 'Line 3': line3 };
    var selectedLine = lineMap[label_select.value];
    var selectedColor = color_select.value;
    selectedLine.glyph.line_color = selectedColor;
""")
label_select.js_on_change('value', initial_color_callback)

# Create callback for range select change event
rangex_callback = CustomJS(args=dict(p=p), code="""
    var range_value = cb_obj.value;
    var range_values = range_value.split(",");
    p.x_range.start = parseFloat(range_values[0]);
    p.x_range.end = parseFloat(range_values[1]);
""")

# Create callback for range select change event
rangey_callback = CustomJS(args=dict(p=p), code="""
    var range_value = cb_obj.value;
    var range_values = range_value.split(",");
    p.y_range.start = parseFloat(range_values[0]);
    p.y_range.end = parseFloat(range_values[1]);
""")




# Create range input widgets
x_range_select = TextInput(title="X Range (start,end)", value="1,5")
y_range_select = TextInput(title="Y Range (start,end)", value="1,5")

# Attach range callback to input widgets
x_range_select.js_on_change('value', rangex_callback)
y_range_select.js_on_change('value', rangey_callback)




p.xaxis.ticker = SingleIntervalTicker(interval=1.0)

# Create layout with inputs and plot
inputs = column(label_select, color_select, x_range_select, y_range_select)
layout = row(inputs, p)

# Show the plot
show(layout)
output_file("plot.html")
