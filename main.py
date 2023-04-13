import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

GObject.threads_init()
Gst.init(None)

pipeline = Gst.Pipeline()

# Agregamos el elemento libcamerasrc
camerasrc = Gst.ElementFactory.make("libcamerasrc")

# Agregamos el elemento autovideosink para mostrar el video
videosink = Gst.ElementFactory.make("autovideosink")

# Agregamos los elementos al pipeline
pipeline.add(camerasrc)
pipeline.add(videosink)

# Conectamos los elementos
camerasrc.link(videosink)

# Iniciamos la reproducción
pipeline.set_state(Gst.State.PLAYING)

# Esperamos a que se cierre el pipeline
bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

# Paramos la reproducción y liberamos los recursos
pipeline.set_state(Gst.State.NULL)
