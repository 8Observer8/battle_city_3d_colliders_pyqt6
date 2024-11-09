import numpy as np
from PyQt6.QtCore import QFile, QIODevice
from PyQt6.QtGui import QMatrix4x4, QVector3D
from PyQt6.QtOpenGL import QOpenGLBuffer
from PyQt6.QtXml import QDomDocument


class VertexBuffers:
    def __init__(self):
        self.vertPosBuffer = None
        self.normalBuffer = None
        self.texCoordBuffer = None
        self.amountOfVertices = None

class Locations:
    def __init__(self):
        self.uMvpMatrixLocation = None
        self.uModelMatrixLocation = None
        self.uNormalMatrixLocation = None

def initVertexBuffers(path):
    xmlDoc = QDomDocument()
    file = QFile(path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly):
        print("Failed to open the file: " + path)
    xmlDoc.setContent(file)
    file.close()
    
    vertPosArray = []
    normalArray = []
    texCoordArray = []
    indexArray = []
    
    root = xmlDoc.documentElement()
    daeElem = root.firstChildElement()
    while not daeElem.isNull():
        if daeElem.tagName() == "library_geometries":
            geomElem = daeElem.firstChildElement()
            if geomElem.tagName() == "geometry":
                meshElem = geomElem.firstChildElement()
                if meshElem.tagName() == "mesh":
                    meshChildElem = meshElem.firstChildElement()
                    while not meshChildElem.isNull():
                        floatArrayElem = meshChildElem.firstChildElement()
                        strArray = floatArrayElem.firstChild().toText().data().split(" ")
                        if meshChildElem.attribute("id").endswith("-mesh-positions"):
                            vertPosArray = list(map(float, strArray))
                        if meshChildElem.attribute("id").endswith("-mesh-normals"):
                            normalArray = list(map(float, strArray))
                        if meshChildElem.attribute("id").endswith("-mesh-map-0"):
                            texCoordArray = list(map(float, strArray))
                        if meshChildElem.tagName() == "triangles" or meshChildElem.tagName() == "polylist":
                            pChildElem = meshChildElem.firstChildElement()
                            while not pChildElem.isNull():
                                if pChildElem.tagName() == "p":
                                    strIndices = pChildElem.firstChild().toText().data().split(" ")
                                    indexArray = list(map(int, strIndices))
                                pChildElem = pChildElem.nextSiblingElement()
                        meshChildElem = meshChildElem.nextSiblingElement()
        daeElem = daeElem.nextSiblingElement()
    
    numOfAttributes = 3
    vertPositions = []
    normals = []
    texCoords = []
    correctionMatrix = QMatrix4x4()
    correctionMatrix.rotate(-90.0, QVector3D(1.0, 0.0, 0.0))
    for i in range(0, len(indexArray), numOfAttributes):
        vertPosIndex = indexArray[i + 0]
        vx = vertPosArray[vertPosIndex * 3 + 0]
        vy = vertPosArray[vertPosIndex * 3 + 1]
        vz = vertPosArray[vertPosIndex * 3 + 2]
        oldPos = QVector3D(vx, vy, vz)
        newPos = correctionMatrix * oldPos
        vertPositions.append(newPos.x())
        vertPositions.append(newPos.y())
        vertPositions.append(newPos.z())
        
        normalIndex = indexArray[i + 1]
        nx = normalArray[normalIndex * 3 + 0]
        ny = normalArray[normalIndex * 3 + 1]
        nz = normalArray[normalIndex * 3 + 2]
        oldNormal = QVector3D(nx, ny, nz)
        newNormal = correctionMatrix * oldNormal
        normals.append(newNormal.x())
        normals.append(newNormal.y())
        normals.append(newNormal.z())
        
        texCoordIndex = indexArray[i + 2]
        texCoords.append(texCoordArray[texCoordIndex * 2 + 0])
        texCoords.append(texCoordArray[texCoordIndex * 2 + 1])
    
    vertPositions = np.array(vertPositions, dtype=np.float32)
    vertPosBuffer = QOpenGLBuffer()
    vertPosBuffer.create()
    vertPosBuffer.bind()
    vertPosBuffer.allocate(vertPositions, len(vertPositions) * 4)
    
    normals = np.array(normals, dtype=np.float32)
    normalBuffer = QOpenGLBuffer()
    normalBuffer.create()
    normalBuffer.bind()
    normalBuffer.allocate(normals, len(normals) * 4)
    
    texCoords = np.array(texCoords, dtype=np.float32)
    texCoordBuffer = QOpenGLBuffer()
    texCoordBuffer.create()
    texCoordBuffer.bind()
    texCoordBuffer.allocate(texCoords, len(texCoords) * 4)

    vertBuffers = VertexBuffers()
    vertBuffers.vertPosBuffer = vertPosBuffer
    vertBuffers.normalBuffer = normalBuffer
    vertBuffers.texCoordBuffer = texCoordBuffer
    vertBuffers.amountOfVertices = int(len(indexArray) / 3)
    
    return vertBuffers
