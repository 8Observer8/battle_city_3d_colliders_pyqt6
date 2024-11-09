from OpenGL import GL as gl
from PyQt6.QtGui import QMatrix4x4, QQuaternion, QVector3D
from PyQt6.QtOpenGL import QOpenGLTexture
from vertex_buffers import VertexBuffers, Locations

class Object3D:

    def __init__(self, position: QVector3D, quat: QQuaternion, scale: QVector3D, vertBuffers: VertexBuffers, locations: Locations, texture: QOpenGLTexture):

        self.position = position
        self.quat = quat
        self.scale = scale

        self.mvpMatrix = QMatrix4x4()
        self.modelMatrix = QMatrix4x4()
        self.normalMatrix = QMatrix4x4()

        self.vertPosBuffer = vertBuffers.vertPosBuffer
        self.normalBuffer = vertBuffers.normalBuffer
        self.texCoordBuffer = vertBuffers.texCoordBuffer
        self.amountOfVertices = vertBuffers.amountOfVertices

        self.uMvpMatrixLocation = locations.uMvpMatrixLocation
        self.uModelMatrixLocation = locations.uModelMatrixLocation
        self.uNormalMatrixLocation = locations.uNormalMatrixLocation
        
        self.texture = texture

    def draw(self, program, projViewMatrix):
        program.bind()

        self.vertPosBuffer.bind()
        program.setAttributeBuffer(0, gl.GL_FLOAT, 0, 3)
        program.enableAttributeArray(0)

        self.normalBuffer.bind()
        program.setAttributeBuffer(1, gl.GL_FLOAT, 0, 3)
        program.enableAttributeArray(1)

        self.texCoordBuffer.bind()
        program.setAttributeBuffer(2, gl.GL_FLOAT, 0, 2)
        program.enableAttributeArray(2)
      
        self.modelMatrix.setToIdentity()
        self.modelMatrix.translate(self.position)
        self.modelMatrix.rotate(self.quat)
        self.modelMatrix.scale(self.scale)
        self.mvpMatrix = projViewMatrix * self.modelMatrix
        
        self.normalMatrix = self.modelMatrix.inverted()
        self.normalMatrix = self.normalMatrix[0].transposed()
        
        program.bind()
        program.setUniformValue(self.uMvpMatrixLocation, self.mvpMatrix)
        program.setUniformValue(self.uModelMatrixLocation, self.modelMatrix)
        program.setUniformValue(self.uNormalMatrixLocation, self.normalMatrix)
        
        self.texture.bind()

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.amountOfVertices)
