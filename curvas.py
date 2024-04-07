curves=slicer.util.getNodesByClass("vtkMRMLMarkupsClosedCurveNode")
for curve in curves:
    surfaceAreaMm2 = slicer.modules.markups.logic().GetClosedCurveSurfaceArea(curve)
    print("Curve {0}: surface area = {1:.2f} mm2".format(curve.GetName(), surfaceAreaMm2))


curvas=slicer.util.getNodesByClass("vtkMRMLMarkupsClosedCurveNode")
for curva in curvas:
    area_defeito = slicer.modules.markups.logic().GetClosedCurveSurfaceArea(curva)
    print("Curva fechada n{0}: Área do defeito = {1:.2f} mm2".format(curva.GetName(), area_defeito))
