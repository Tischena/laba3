import NemAll_Python_Geometry as geometry
import NemAll_Python_BaseElements as baseElements
import NemAll_Python_BasisElements as basisElements
import NemAll_Python_Utility as utility
import geometryValidate as geometryValidate
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties

def create_el(build_ele, doc):
    element = balka(doc)
    return element.create(build_ele)

def check_allplan_version(build_ele, version):
    del build_ele
    del version
    return True

def move_handle(build_ele, handle_prop, input_pnt, doc):
    build_ele.change_property(handle_prop, input_pnt)
    return create_el(build_ele, doc)

class balka:

    def create(self, build_ele):
        self.top(build_ele)
        self.handle(build_ele)
        return (self.model_ele_list, self.handle_list)

    def __init__(self, doc):
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def top(self, build_ele):
        com_prop = baseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.pen = 1
        com_prop.color = 3
        com_prop.stroke = 1
        polyhedron_bottom = self.handle(build_ele)
        polyhedron_center = self.center(build_ele)
        polyhedron_top = self.top_part(build_ele)
        err, polyhedron = geometry.union(polyhedron_bottom, polyhedron_center)
        if err:
            return
        err, polyhedron = geometry.union(polyhedron, polyhedron_top)
        if err:
            return 
        self.model_ele_list.append(
            basisElements.Modelelem(com_prop, polyhedron))

    def center(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(0, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(0, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - (build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value),  build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - build_ele.lengthTransition.value, build_ele.lengthbottomCut.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value, build_ele.lengthbottomCut.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(0, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path = geometry.line()
        path += geometry.point(0, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path += geometry.point(0, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def handle(self, build_ele):
        polyhedron = self.low_part1(build_ele)
        err, polyhedron = geometry.union(polyhedron, self.low_part2(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.low_part3(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.low_part4(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.low_part2_2(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.low_part3_2(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.low_part4_2(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.low_part2_3(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.low_part3_3(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.low_part2_4(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.low_part3_4(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.low_part5(build_ele))
        return polyhedron

    def top_part(self, build_ele):
        polyhedron = self.top_part1(build_ele)
        err, polyhedron = geometry.union(polyhedron, self.top_part3(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.top_part2(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.top_part3(build_ele, plus=(build_ele.length.value - build_ele.lengthcentrwidth.value)))
        err, polyhedron = geometry.union(polyhedron, self.top_part4(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.top_part2_2(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.top_part4(build_ele, build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2, build_ele.widthTop.value, 10))
        err, polyhedron = geometry.union(polyhedron, self.top_part2_3(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.top_part4_2(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.top_part4_2(build_ele, build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2, build_ele.widthTop.value, 10))
        err, polyhedron = geometry.union(polyhedron, self.top_part3_3(build_ele))
        err, polyhedron = geometry.union(polyhedron, self.top_part5(build_ele))
        return polyhedron

    def top_part1(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2,build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthTop.value - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, -(build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2,build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2,build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path = geometry.line()
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2,build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def top_part2(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - build_ele.lengthTransition.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2 , build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - build_ele.lengthTransition.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2 , build_ele.widthbottom.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2 + (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value + (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path = geometry.line()
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value + 10, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - 10, build_ele.Heightbottom.value + build_ele.HeightCenter.value + 10)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def top_part3(self, build_ele, plus=0):
        base_pol = geometry.p()
        base_pol += geometry.point(plus, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(plus, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(plus, build_ele.widthbottom.value + (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(plus, -(build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(plus, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path = geometry.line()
        path += geometry.point(plus, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path += geometry.point(plus + build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def top_part4(self, build_ele, minus_1 = 0, minus_2 = 0, digit = -10):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - minus_1, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthTop.value - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2 - minus_2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value + (build_ele.widthTop.value - build_ele.widthbottom.value) / 2 - minus_2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - minus_1, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path = geometry.line()
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - minus_1, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value + digit - minus_1, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        print(base_pol)
        print(path)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def top_part2_2(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - build_ele.lengthTransition.value, build_ele.lengthbottomCut.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - build_ele.lengthTransition.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2 - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, -(build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path = geometry.line()
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value + 10, build_ele.lengthbottomCut.value + 10, build_ele.Heightbottom.value + build_ele.HeightCenter.value + 10)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def top_part2_3(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2 + (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value + (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path = geometry.line()
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path += geometry.point(build_ele.lengthcentrwidth.value - 10, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - 10, build_ele.Heightbottom.value + build_ele.HeightCenter.value - 10)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def top_part4_2(self, build_ele, minus_1 = 0, minus_2 = 0, digit = -10):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - minus_1, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value + (build_ele.widthTop.value - build_ele.widthbottom.value) / 2 - minus_2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value + (build_ele.widthTop.value - build_ele.widthbottom.value) / 2 - minus_2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - minus_1, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path = geometry.line()
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - minus_1, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - minus_1 + digit, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def top_part3_3(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value, build_ele.lengthbottomCut.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2 - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, -(build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path = geometry.line()
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value)
        path += geometry.point(build_ele.lengthcentrwidth.value - 10, build_ele.lengthbottomCut.value + 10, build_ele.Heightbottom.value + build_ele.HeightCenter.value - 10)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def top_part5(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(0, -(build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(0, build_ele.widthTop.value - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        base_pol += geometry.point(0, build_ele.widthTop.value - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTop.value)
        base_pol += geometry.point(0, build_ele.widthTop.value - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2 - build_ele.Identation.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTop.value)
        base_pol += geometry.point(0, build_ele.widthTop.value - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2 - build_ele.Identation.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTop.value + build_ele.HeightPlate.value)
        base_pol += geometry.point(0, - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2 + build_ele.Identation.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTop.value + build_ele.HeightPlate.value)
        base_pol += geometry.point(0, - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2 + build_ele.Identation.value, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTop.value)
        base_pol += geometry.point(0, - (build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTop.value)
        base_pol += geometry.point(0, -(build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        path = geometry.line()
        path += geometry.point(0, -(build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        path += geometry.point(build_ele.length.value, -(build_ele.widthTop.value - build_ele.widthbottom.value) / 2, build_ele.Heightbottom.value + build_ele.HeightCenter.value + build_ele.HeightTopCut.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part1(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2,build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2 - build_ele.widthCentralLittle.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, 0, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        path = geometry.line()
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron
    
    def low_part2(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path = geometry.line()
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path += geometry.point(build_ele.lengthcentrwidth.value - 10 , build_ele.widthbottom.value - build_ele.lengthbottomCut.value - 10, build_ele.Heightbottom.value - 10)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part3(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(0, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(0, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(0, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(0, 0, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(0, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        path = geometry.line()
        path += geometry.point(0, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part4(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path = geometry.line()
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - 10, build_ele.Heightbottom.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part2_2(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value, build_ele.lengthbottomCut.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + build_ele.lengthTransition.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, 0, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value,build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path = geometry.line()
        path += geometry.point(build_ele.lengthcentrwidth.value,build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path += geometry.point(build_ele.lengthcentrwidth.value - 10 ,build_ele.lengthbottomCut.value + 10, build_ele.Heightbottom.value - 10)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part3_2(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, 0, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        path = geometry.line()
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        path += geometry.point(build_ele.length.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part4_2(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, 0, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, 0, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path = geometry.line()
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path += geometry.point(build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value + 10, build_ele.Heightbottom.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part2_3(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - build_ele.lengthTransition.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - build_ele.lengthTransition.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path = geometry.line()
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value + 10, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - 10, build_ele.Heightbottom.value + 10)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part3_3(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path = geometry.line()
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.widthbottom.value - build_ele.lengthbottomCut.value - 10, build_ele.Heightbottom.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part2_4(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - build_ele.lengthTransition.value, build_ele.lengthbottomCut.value + (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - build_ele.lengthTransition.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, 0, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path = geometry.line()
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - 10, build_ele.lengthbottomCut.value + 10, build_ele.Heightbottom.value - 10)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part3_4(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, 0, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value - (build_ele.widthbottom.value - build_ele.lengthbottomCut.value * 2 - build_ele.widthCentralLittle.value) / 2, 0, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path = geometry.line()
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value, build_ele.Heightbottom.value)
        path += geometry.point(build_ele.length.value - build_ele.lengthcentrwidth.value, build_ele.lengthbottomCut.value + 10, build_ele.Heightbottom.value)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron

    def low_part5(self, build_ele):
        base_pol = geometry.p()
        base_pol += geometry.point(0, 20, 0)
        base_pol += geometry.point(0, build_ele.widthbottom.value - 20, 0)
        base_pol += geometry.point(0, build_ele.widthbottom.value, 20)
        base_pol += geometry.point(0, build_ele.widthbottom.value, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(0, 0, build_ele.Heightbottom.value - build_ele.HeightbottomCut.value)
        base_pol += geometry.point(0, 0, 20)
        base_pol += geometry.point(0, 20, 0)
        if not geometryValidate.is_valid(base_pol):
            return
        path = geometry.line()
        path += geometry.point(0, 20, 0)
        path += geometry.point(build_ele.length.value,20,0)
        err, polyhedron = geometry.CreatePolyhedron(base_pol, path)
        if err:
            return []
        return polyhedron
