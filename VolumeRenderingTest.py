import vtk

data_dir = "Input-Folder"

reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(data_dir)
reader.Update()

print(f"Extent: {reader.GetDataExtent()}")
print(f"Spacing: {reader.GetDataSpacing()}")

image_data = reader.GetOutput()
print(f"Dimensions: {image_data.GetDimensions()}")

mapper = vtk.vtkSmartVolumeMapper()
mapper.SetInputConnection(reader.GetOutputPort())

color = vtk.vtkColorTransferFunction()
color.AddRGBPoint(0, 0, 0, 0)
color.AddRGBPoint(100, 1, 1, 1)

opacity = vtk.vtkPiecewiseFunction()
opacity.AddPoint(0, 0)
opacity.AddPoint(100, 1)

volume = vtk.vtkVolume()
volume.SetMapper(mapper)
volume.GetProperty().SetColor(color)
volume.GetProperty().SetScalarOpacity(opacity)

renderer = vtk.vtkRenderer()
renderer.AddActor(volume)
renderer.SetBackground(0.1,0.2,0.4)

window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)

inter = vtk.vtkRenderWindowInteractor()
inter.SetRenderWindow(window)

# Text kısmı
text_actor = vtk.vtkTextActor()
text_actor.SetInput("Color: (0, 100), Zoom: 1.0")
text_actor.GetTextProperty().SetFontSize(24)
text_actor.GetTextProperty().SetColor(1.0, 1.0, 1.0)

text_actor.SetDisplayPosition(10, 10)

renderer.AddActor2D(text_actor)

points = []
points.append(0)
points.append(100)

def func(obj, event):
    key = obj.GetKeySym()
    if key == "a":
        points[0] -= 1
    if key == "d":
        points[0] += 1

    if key == "Right":
        points[1] += 1
    if key == "Left":
        points[1] -= 1

    color.RemoveAllPoints()
    color.AddRGBPoint(points[0], 0.0, 0.0, 0.0)
    color.AddRGBPoint(points[1], 1.0, 1.0, 1.0)
    opacity.RemoveAllPoints()
    opacity.AddPoint(points[0], 0.0)
    opacity.AddPoint(points[1], 1.0)
    text_actor.SetInput(f"Color: ({points[0]}, {points[1]})")
    
    window.Render()

def zoom_callback(obj, event):
    zoom_factor = 1.1 if event == "MouseWheelForwardEvent" else 0.9
    renderer.GetActiveCamera().Zoom(zoom_factor)
    text_actor.SetInput(f"Color: ({points[0]}, {points[1]})")
    window.Render()

inter.AddObserver("MouseWheelForwardEvent", zoom_callback)
inter.AddObserver("MouseWheelBackwardEvent", zoom_callback)

inter.AddObserver("KeyPressEvent", func)

window.Render()
inter.Start()