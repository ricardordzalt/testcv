import numpy as np
import cv2
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib

# Inicializamos GStreamer y GObject
Gst.init(None)
GObject.threads_init()

# Creamos el pipeline de GStreamer
pipeline = Gst.Pipeline()

# Creamos los elementos necesarios
camerasrc = Gst.ElementFactory.make('libcamerasrc', 'camera-source')
# camerasrc.set_property('sensor-id', 0)
videoscale = Gst.ElementFactory.make('videoscale', 'video-scaler')
capsfilter = Gst.ElementFactory.make('capsfilter', 'capsfilter')
caps = Gst.Caps.from_string('video/x-raw,width=640,height=480')
capsfilter.set_property('caps', caps)
videoconvert = Gst.ElementFactory.make('videoconvert', 'video-converter')
appsink = Gst.ElementFactory.make('appsink', 'app-sink')
appsink.set_property('emit-signals', True)
appsink.set_property('sync', False)

# Añadimos los elementos al pipeline
pipeline.add(camerasrc)
pipeline.add(videoscale)
pipeline.add(capsfilter)
pipeline.add(videoconvert)
pipeline.add(appsink)

# Conectamos los elementos
camerasrc.link(videoscale)
videoscale.link(capsfilter)
capsfilter.link(videoconvert)
videoconvert.link(appsink)

# Creamos la función para manejar los nuevos frames del AppSink
def on_new_sample(appsink):
    sample = appsink.emit('pull-sample')
    buffer = sample.get_buffer()
    caps = sample.get_caps()
    width = caps.get_structure(0).get_value('width')
    height = caps.get_structure(0).get_value('height')
    nparr = buffer.extract_dup(0, buffer.get_size())
    frame = np.frombuffer(nparr, np.uint8).reshape((height, width, 3))
    return frame

# Conectamos la señal "new-sample" del AppSink a la función "on_new_sample"
appsink.connect('new-sample', on_new_sample)

# Iniciamos el pipeline
pipeline.set_state(Gst.State.PLAYING)

# Creamos la ventana de OpenCV
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

# Bucle principal
while True:
    # Obtenemos un frame del AppSink
    frame = on_new_sample(appsink)

    # Mostramos el frame en la ventana de OpenCV
    cv2.imshow('Video', frame)
    # Si se presiona la tecla 'q', salimos del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

