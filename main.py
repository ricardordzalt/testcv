import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
import cv2

GObject.threads_init()
Gst.init(None)

def on_new_sample(appsink):
    sample = appsink.emit("pull-sample")
    buffer = sample.get_buffer()
    result, info = buffer.map(Gst.MapFlags.READ)
    if result:
        data = info.data
        img = cv2.imdecode(np.frombuffer(data, np.uint8), -1)
        cv2.imshow("Video", img)
        cv2.waitKey(1)
        buffer.unmap(info)

pipeline = Gst.Pipeline()

# Agregamos el elemento libcamerasrc
camerasrc = Gst.ElementFactory.make("libcamerasrc")

# Agregamos el elemento appsink para recibir los frames del video
appsink = Gst.ElementFactory.make("appsink")
appsink.set_property("emit-signals", True)
appsink.set_property("sync", False)
appsink.connect("new-sample", on_new_sample)

# Agregamos los elementos al pipeline
pipeline.add(camerasrc)
pipeline.add(appsink)

# Conectamos los elementos
camerasrc.link(appsink)

# Iniciamos la reproducción
pipeline.set_state(Gst.State.PLAYING)

# Esperamos a que se cierre el pipeline
bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

# Paramos la reproducción y liberamos los recursos
pipeline.set_state(Gst.State.NULL)
cv2.destroyAllWindows()
