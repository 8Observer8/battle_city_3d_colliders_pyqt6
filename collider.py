from enum import Enum
from OpenGL import GL as gl
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode, BulletWorld
from panda3d.core import Point3, Quat, TransformState, Vec3
from PyQt6.QtGui import QMatrix4x4, QQuaternion, QVector3D
from PyQt6.QtOpenGL import QOpenGLTexture
from vertex_buffers import VertexBuffers, Locations

class ColliderType(Enum):
    Box = 1
    Sphere = 2

class Collider:

    def __init__(self, type: ColliderType, position: QVector3D, scale: QVector3D, vertBuffers: VertexBuffers, locations: Locations, texture: QOpenGLTexture, world: BulletWorld, mass: float):

        self.position = position
        self.rotation = QVector3D(0, 0, 0)
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

        self.shape = BulletBoxShape(Vec3(scale.x(), scale.y(), scale.z()))
        self.node = BulletRigidBodyNode("Box")

        self.mass = mass
        self.node.setMass(self.mass)

        p = Point3(self.position.x(), self.position.y(), self.position.z())
        q = Quat.identQuat()
        s = Vec3(1, 1, 1)

        self.transform = TransformState.make_pos_quat_scale(p, q, s)
        self.node.setTransform(self.transform)

        self.node.addShape(self.shape)
        self.world = world
        self.world.attachRigidBody(self.node)

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

        self.position.setX(self.node.getTransform().pos.x)
        self.position.setY(self.node.getTransform().pos.y)
        self.position.setZ(self.node.getTransform().pos.z)
        hpr = self.node.getTransform().getHpr()
        pandaQuat = Quat()
        pandaQuat.setHpr(hpr)
        quat = QQuaternion(pandaQuat.getX(), pandaQuat.getY(), pandaQuat.getZ(), pandaQuat.getW())
        
        self.modelMatrix.setToIdentity()
        self.modelMatrix.translate(self.position)
        self.modelMatrix.rotate(quat)
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
