import vtk
from glob import glob
import os

def readnrrd(filename):
    # Leitura de arquivo NRRD
    reader = vtk.vtkNrrdReader()
    reader.SetFileName(filename)
    reader.Update()
    info = reader.GetInformation()
    return reader.GetOutput(), info

def writenifti(image,filename, info):
    # Criando arquivo NIFTII
    writer = vtk.vtkNIFTIImageWriter()
    writer.SetInputData(image)
    writer.SetFileName(filename)
    writer.SetInformation(info)
    writer.Write()

InDir = 'C:/UNESP/dataset/nrrd'
OutDir = 'C:/UNESP/dataset/nii'
files = glob(os.path.join(InDir, '**/*.nrrd'), recursive=True)

for file in files:
    print(f"Convertendo: {file}")
    m, info = readnrrd(file)

    relative_path = os.path.relpath(file, InDir)
    output_subdir = os.path.join(OutDir, os.path.dirname(relative_path))

    os.makedirs(output_subdir, exist_ok=True)

    base_filename = os.path.basename(file)
    output_filename = os.path.join(output_subdir, base_filename[:-5] + '.nii')

    writenifti(m, output_filename, info)
