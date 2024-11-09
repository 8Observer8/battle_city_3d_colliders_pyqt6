from OpenGL import GL as gl
from panda3d.bullet import BulletWorld
from panda3d.core import Vec3
from PyQt6.QtCore import QElapsedTimer, Qt, QTimer
from PyQt6.QtGui import QImage, QKeyEvent, QMatrix4x4, QQuaternion, QVector3D
from PyQt6.QtOpenGL import QOpenGLShader, QOpenGLShaderProgram, QOpenGLTexture
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from collider import Collider, ColliderType
from object3d import Object3D
from vertex_buffers import Locations, initVertexBuffers


class OpenGLWidget(QOpenGLWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("panda3d.bullet, OpenGL3, PyQt6")
        self.resize(400, 400)
        self.drawColliders = True
        self.drawObjects = True

    def initializeGL(self):
        gl.glClearColor(0.2, 0.2, 0.2, 1)
        gl.glEnable(gl.GL_DEPTH_TEST)
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.ShaderTypeBit.Vertex, "assets/shaders/default.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.ShaderTypeBit.Fragment, "assets/shaders/default.frag")
        self.program.link()
        self.program.bind()
        self.program.bindAttributeLocation("aPosition", 0)
        self.program.bindAttributeLocation("aNormal", 1)
        self.program.bindAttributeLocation("aTexCoord", 2)
        locations = Locations()
        self.program.bind()
        locations.uMvpMatrixLocation = self.program.uniformLocation("uMvpMatrix")
        locations.uModelMatrixLocation = self.program.uniformLocation("uModelMatrix")
        locations.uNormalMatrixLocation = self.program.uniformLocation("uNormalMatrix")

        self.groundVertBuffers = initVertexBuffers("assets/models/ground.dae")
        self.cubeVertBuffers = initVertexBuffers("assets/models/cube.dae")
        self.playerVertBuffers = initVertexBuffers("assets/models/tank/TexturedTank.dae")

        self.projViewMatrix = QMatrix4x4()
        self.projMatrix = QMatrix4x4()
        self.viewMatrix = QMatrix4x4()
        self.viewMatrix.lookAt(
            QVector3D(0, 5, -5),
            QVector3D(0, 0, 0),
            QVector3D(0, 1, 0))

        self.groundTexture = QOpenGLTexture(QOpenGLTexture.Target.Target2D)
        self.groundTexture.create()
        self.groundTexture.setData(QImage("assets/models/ground.png").mirrored())
        self.groundTexture.setMinMagFilters(QOpenGLTexture.Filter.Linear, QOpenGLTexture.Filter.Linear)
        self.groundTexture.setWrapMode(QOpenGLTexture.WrapMode.ClampToEdge)

        self.colliderTexture = QOpenGLTexture(QOpenGLTexture.Target.Target2D)
        self.colliderTexture.create()
        self.colliderTexture.setData(QImage("assets/models/box_collider2.png").mirrored())
        self.colliderTexture.setMinMagFilters(QOpenGLTexture.Filter.Linear, QOpenGLTexture.Filter.Linear)
        self.colliderTexture.setWrapMode(QOpenGLTexture.WrapMode.ClampToEdge)

        self.playerTexture01 = QOpenGLTexture(QOpenGLTexture.Target.Target2D)
        self.playerTexture01.create()
        # self.texture.setData(QImage("assets/models/cube.png").mirrored())
        # self.texture.setData(QImage("assets/models/box_collider2.png").mirrored())
        self.playerTexture01.setData(QImage("assets/models/tank/PlayerTextureFrame01.png").mirrored())
        self.playerTexture01.setMinMagFilters(QOpenGLTexture.Filter.Linear, QOpenGLTexture.Filter.Linear)
        self.playerTexture01.setWrapMode(QOpenGLTexture.WrapMode.ClampToEdge)

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, -9.81, 0))

        pos = [
            [0.0, -0.1, -0.0],
        ]

        rot = [
            [0.0, 0.0, -0.0, 1.0],
        ]

        scale = [
            [2.5, 0.1, 2.5],
        ]

        self.ground = Object3D(QVector3D(0, 0, 0), QQuaternion(1, 0, 0, 0), QVector3D(1, 1, 1), self.groundVertBuffers, locations, self.groundTexture)
        self.player = Object3D(QVector3D(0, 0, 0), QQuaternion(1, 0, 0, 0), QVector3D(1, 1, 1), self.playerVertBuffers, locations, self.playerTexture01)

        self.groundCollider = Collider(ColliderType.Box, QVector3D(pos[0][0], pos[0][1], pos[0][2]), QVector3D(scale[0][0], scale[0][1], scale[0][2]), self.cubeVertBuffers, locations, self.colliderTexture, self.world, mass=0)
        self.playerCollider = Collider(ColliderType.Box, QVector3D(0.8, 3, 0), QVector3D(2.2, 1, 2.5), self.cubeVertBuffers, locations, self.colliderTexture, self.world, mass=1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animationLoop)
        self.elapsedTimer = QElapsedTimer()
        self.elapsedTimer.start()
        self.deltaTime = 0
        self.timer.start(1000//60)

    def animationLoop(self):
        self.deltaTime = self.elapsedTimer.elapsed()
        self.elapsedTimer.restart()
        self.world.doPhysics(self.deltaTime / 1000)
        self.update()
        
    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.projViewMatrix = self.projMatrix * self.viewMatrix

        if self.drawObjects:
            self.player.position.setX(self.playerCollider.position.x())
            self.player.position.setY(self.playerCollider.position.y() - 0.5)
            self.player.position.setZ(self.playerCollider.position.z())
            self.ground.draw(self.program, self.projViewMatrix)
            self.player.draw(self.program, self.projViewMatrix)

        if self.drawColliders:
            self.groundCollider.draw(self.program, self.projViewMatrix)
            self.playerCollider.draw(self.program, self.projViewMatrix)

    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        self.projMatrix.setToIdentity()
        self.projMatrix.perspective(50, float(w) / float(h), 0.1, 100)
    
    def closeEvent(self, event):
        self.groundTexture.destroy()
        self.colliderTexture.destroy()
        self.playerTexture01.destroy()

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key.Key_B:
            self.drawObjects = not self.drawObjects

        if event.key() == Qt.Key.Key_C:
            self.drawColliders = not self.drawColliders
