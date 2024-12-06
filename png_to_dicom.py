import pydicom
from pydicom.dataset import Dataset
from pydicom.uid import generate_uid
from PIL import Image
import numpy as np
import os

INPUT_FOLDER = "Input-Folder"
OUTPUT_FOLDER = "Output-Folder"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

PIXEL_SPACING = [0.5, 0.5]
SLICE_THICKNESS = 0.5
STUDY_UID = generate_uid()
SERIES_UID = generate_uid()

for idx, file_name in enumerate(sorted(os.listdir(INPUT_FOLDER))):
    if not file_name.endswith(".png"):
        continue

    input_file = os.path.join(INPUT_FOLDER, file_name)
    img = Image.open(input_file).convert("L")
    np_frame = np.array(img, dtype=np.uint8)

    ds = Dataset()
    ds.file_meta = Dataset()
    ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
    ds.file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    ds.file_meta.MediaStorageSOPInstanceUID = generate_uid()
    ds.file_meta.ImplementationClassUID = generate_uid()

    ds.PatientName = "TestPatient"
    ds.PatientID = "12345"
    ds.StudyInstanceUID = STUDY_UID
    ds.SeriesInstanceUID = SERIES_UID
    ds.SOPInstanceUID = generate_uid()

    ds.Rows = img.height
    ds.Columns = img.width
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.SamplesPerPixel = 1
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelSpacing = PIXEL_SPACING
    ds.SliceThickness = SLICE_THICKNESS

    ds.InstanceNumber = idx + 1
    ds.ImagePositionPatient = [0.0, 0.0, idx * SLICE_THICKNESS]
    ds.ImageOrientationPatient = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    ds.SliceLocation = idx * SLICE_THICKNESS

    ds.PixelData = np_frame.tobytes()

    output_file = os.path.join(OUTPUT_FOLDER, f"{idx + 1:04d}.dcm")
    ds.save_as(output_file, write_like_original=False)
    print(f"Saved DICOM: {output_file}")

print("DICOM conversion completed.")
