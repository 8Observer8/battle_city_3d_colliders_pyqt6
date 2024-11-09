import sys

from OpenGL import GL as gl
from PyQt6.QtCore import QElapsedTimer, QFile, QIODevice, Qt, QTimer
from PyQt6.QtGui import (QImage, QMatrix4x4, QQuaternion, QSurfaceFormat,
                         QVector3D)
from PyQt6.QtOpenGL import (QOpenGLBuffer, QOpenGLShader, QOpenGLShaderProgram,
                            QOpenGLTexture)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QApplication
from opengl_widget import OpenGLWidget

# Assets:
# Cube Texture: https://dl.dropboxusercontent.com/s/tply9ubx3n3ycvv/cube.png
# Cube Model: https://dl.dropboxusercontent.com/s/0aktc37c3nx9iq3/cube.dae
# Plane Texture: https://dl.dropboxusercontent.com/s/3iibsnvyw0vupby/plane.png
# Plane Model: https://dl.dropboxusercontent.com/s/e0wktg69ec3w8pq/plane.dae


def main():
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL)
    app = QApplication(sys.argv)

    format = QSurfaceFormat()
    format.setSamples(8)
    
    w = OpenGLWidget()
    w.setFormat(format)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
