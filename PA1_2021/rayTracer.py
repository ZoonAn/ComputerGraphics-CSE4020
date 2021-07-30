#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below
import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)

#Classes for spheres and boxes
class Sphere:
    def __init__(self, s, r, c):
        self.shader = s
        self.radius = r
        self.center = c

class Box:
    def __init__(self, s, minP, maxP):
        self.shader = s
        self.minPt = minP
        self.maxPt = maxP
        
#Classes for shaders
class Shader:
    def __init__(self, n):
        self.name = n

class ShaderP(Shader):
    def __init__(self, n, d, s, e):
        super().__init__(n)
        self.diffuseColor = d
        self.specularColor = s
        self.exponent = e

class ShaderL(Shader):
    def __init__(self, n, d):
        super().__init__(n)
        self.diffuseColor = d

def rayTrace(surfaceList, ray, viewPoint):
    m = sys.maxsize
    idx = -1
    cnt = 0
    
    for surface in surfaceList:
        if isinstance(surface, Sphere):
            a = np.sum(ray * ray)
            b = np.sum((viewPoint - surface.center) * ray)
            c = np.sum((viewPoint - surface.center)**2) - surface.radius**2
            if b**2 - a * c >= 0:
                delta = np.sqrt(b**2 - a * c)
                if -b + delta >= 0 and m >= (-b + delta) / a:
                    m = (-b + delta) / a
                    idx = cnt
                if -b - delta >= 0 and m >= (-b - delta) / a:
                    m = (-b - delta) / a
                    idx = cnt
        elif isinstance(surface, Box):
            txMin = (surface.minPt[0] - viewPoint[0]) / ray[0]
            txMax = (surface.maxPt[0] - viewPoint[0]) / ray[0]
            if txMin > txMax:
                txMin, txMax = txMax, txMin
            
            tyMin = (surface.minPt[1] - viewPoint[1]) / ray[1]
            tyMax = (surface.maxPt[1] - viewPoint[1]) / ray[1]
            if tyMin > tyMax:
                tyMin, tyMax = tyMax, tyMin
            
            tzMin = (surface.minPt[2] - viewPoint[2]) / ray[2]
            tzMax = (surface.maxPt[2] - viewPoint[2]) / ray[2]
            if tzMin > tzMax:
                tzMin, tzMax = tzMax, tzMin
            
            tMin = max(txMin, tyMin, tzMin)
            tMax = min(txMax, tyMax, tzMax)
            
            if (tMin > txMax or tMax < txMin or tMin > tyMax or tMax < tyMin or tMin > tzMax or tMax < tzMin) == False and m >= tMin:
                m = tMin
                idx = cnt
            
        cnt = cnt + 1
    return [m, idx]

def getNormalVector(x, y, z):
    direction = np.cross((y-x), (z-x))
    d = np.sum(direction * z)
    return np.array([direction[0], direction[1], direction[2], d])
    
def shade(m, ray, viewPoint, surfaceList, idx, lightList):
    surface = surfaceList[idx]
    r = 0
    g = 0
    b = 0
    n = np.array([0,0,0])
    v = -m * ray
    
    if isinstance(surface, Sphere):
        n = viewPoint + m * ray - surface.center
    elif isinstance(surface, Box):
        point_i = viewPoint + m * ray
        diff = sys.maxsize
        i = -1
        cnt = 0
        
        normalVecList = []
        
        point_1 = np.array([surface.minPt[0], surface.minPt[1], surface.maxPt[2]])
        point_2 = np.array([surface.minPt[0], surface.maxPt[1], surface.minPt[2]])
        point_3 = np.array([surface.maxPt[0], surface.minPt[1], surface.minPt[2]])
        point_4 = np.array([surface.minPt[0], surface.maxPt[1], surface.maxPt[2]])
        point_5 = np.array([surface.maxPt[0], surface.minPt[1], surface.maxPt[2]])
        point_6 = np.array([surface.maxPt[0], surface.maxPt[1], surface.minPt[2]])
        
        normalVecList.append(getNormalVector(point_1, point_3, point_5))
        normalVecList.append(getNormalVector(point_2, point_3, point_6))
        normalVecList.append(getNormalVector(point_1, point_2, point_4))
        normalVecList.append(getNormalVector(point_1, point_5, point_4))
        normalVecList.append(getNormalVector(point_5, point_3, point_6))
        normalVecList.append(getNormalVector(point_4, point_6, point_2))
        
        for normalVec in normalVecList:
            if abs(np.sum(normalVec[:3] * point_i) - normalVec[3]) < diff:
                diff = abs(np.sum(normalVec[:3] * point_i) - normalVec[3])
                i = cnt
            cnt = cnt + 1
        n = normalVecList[i][:3]
            
        
    n = n / np.sqrt(np.sum(n * n))    
    
    for light in lightList:
        light_i = v + light[0] - viewPoint
        light_i = light_i / np.sqrt(np.sum(light_i * light_i))
        
        checker = rayTrace(surfaceList, -light_i, light[0])
        
        if checker[1] == idx:
            if isinstance(surface.shader, ShaderL):
                r = r + surface.shader.diffuseColor[0] * light[1][0] * max(0, np.dot(light_i, n))
                g = g + surface.shader.diffuseColor[1] * light[1][1] * max(0, np.dot(light_i, n))
                b = b + surface.shader.diffuseColor[2] * light[1][2] * max(0, np.dot(light_i, n))
            elif isinstance(surface.shader, ShaderP):
                vUnit = v / np.sqrt(np.sum(v * v))
                h = vUnit + light_i
                h = h / np.sqrt(np.sum(h * h))
                l_sR = surface.shader.specularColor[0] * light[1][0] * pow(max(0, np.dot(n, h)), surface.shader.exponent)
                l_sG = surface.shader.specularColor[1] * light[1][1] * pow(max(0, np.dot(n, h)), surface.shader.exponent)
                l_sB = surface.shader.specularColor[2] * light[1][2] * pow(max(0, np.dot(n, h)), surface.shader.exponent)
                r = r + surface.shader.diffuseColor[0] * light[1][0] * max(0, np.dot(light_i, n)) + l_sR
                g = g + surface.shader.diffuseColor[1] * light[1][1] * max(0, np.dot(light_i, n)) + l_sG
                b = b + surface.shader.diffuseColor[2] * light[1][2] * max(0, np.dot(light_i, n)) + l_sB
            
    res = Color(r,g,b)
    res.gammaCorrect(2.2)
    return res.toUINT8()
        

def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir = np.array([0,0,-1]).astype(np.float64)
    viewUp = np.array([0,1,0]).astype(np.float64)
    viewProjNormal = -1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth = 1.0
    viewHeight = 1.0
    projDistance = 1.0
    intensity = np.array([1,1,1]).astype(np.float64)  # how bright the light is.

    imgSize=np.array(root.findtext('image').split()).astype(np.int64)
    #parse camera
    for c in root.findall('camera'):
        viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float64)
        if(c.findtext('viewDir')):
            viewDir = np.array(c.findtext('viewDir').split()).astype(np.float64)
        if(c.findtext('projNormal')):
            viewProjNormal = np.array(c.findtext('projNormal').split()).astype(np.float64)
        if(c.findtext('viewUp')):
            viewUp = np.array(c.findtext('viewUp').split()).astype(np.float64)
        if(c.findtext('projDistance')):
            projDistance = np.array(c.findtext('projDistance').split()).astype(np.float64)
        if(c.findtext('viewWidth')):
            viewWidth=np.array(c.findtext('viewWidth').split()).astype(np.float64)
        if(c.findtext('viewHeight')):
            viewHeight = np.array(c.findtext('viewHeight').split()).astype(np.float64)
    
    shaderList = []
    
    #parse shader
    for c in root.findall('shader'):
        diffuseColor_c = np.array(c.findtext('diffuseColor').split()).astype(np.float64)
        new_shader_name = c.get('name')
        if(c.get('type') == 'Lambertian'):
            new_shader = ShaderL(new_shader_name, diffuseColor_c)
            shaderList.append(new_shader)
        elif(c.get('type') == 'Phong'):
            specularColor_c = np.array(c.findtext('specularColor').split()).astype(np.float64)
            exponent_c = np.array(c.findtext('exponent').split()).astype(np.float64)[0]
            new_shader = ShaderP(new_shader_name, diffuseColor_c, specularColor_c, exponent_c)
            shaderList.append(new_shader)
    
    surfaceList = []
    
    #parse surface
    for c in root.findall('surface'):
        type_c = c.get('type')    
        ref = ''
        for d in c:
            if(d.tag == 'shader'):
                ref = d.get('ref')
        surface_shader = [x for x in shaderList if(x.name == ref)][0]
        
        if(type_c == 'Sphere'):
            radius_c = np.array(c.findtext('radius')).astype(np.float64)
            center_c = np.array(c.findtext('center').split()).astype(np.float64)
            surfaceList.append(Sphere(surface_shader, radius_c, center_c))
        elif(type_c == 'Box'):
            minPt_c = np.array(c.findtext('minPt').split()).astype(np.float64)
            maxPt_c = np.array(c.findtext('maxPt').split()).astype(np.float64)
            surfaceList.append(Box(surface_shader, minPt_c, maxPt_c))
    
    lightList = []
    
    #parse light
    for c in root.findall('light'):
        position_c = np.array(c.findtext('position').split()).astype(np.float64)
        intensity_c = np.array(c.findtext('intensity').split()).astype(np.float64)
        lightList.append((position_c, intensity_c))
    #code.interact(local=dict(globals(), **locals()))  

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0
    
    pixelWidth = viewWidth / imgSize[0]
    pixelHeight = viewHeight / imgSize[1]
    
    w = viewDir
    u = np.cross(w, viewUp)
    v = np.cross(w, u)
    
    w = w / np.sqrt(np.sum(w * w))
    u = u / np.sqrt(np.sum(u * u))
    v = v / np.sqrt(np.sum(v * v))
    
    s = w * projDistance - u * pixelWidth * (imgSize[0]/2 + 1/2) - v * pixelHeight * (imgSize[1]/2 + 1/2)
    
    for x in np.arange(imgSize[0]):
        for y in np.arange(imgSize[1]):
            ray = s + u * x * pixelWidth + v * y * pixelHeight
            raytraced = rayTrace(surfaceList, ray, viewPoint)
            if(raytraced[1] != -1):
                img[y][x] = shade(raytraced[0], ray, viewPoint, surfaceList, raytraced[1], lightList)
            else:
                img[y][x] = np.array([0, 0, 0])



    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
    main()
