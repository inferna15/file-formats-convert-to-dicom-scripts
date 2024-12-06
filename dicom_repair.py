import pydicom
import os
from pydicom.uid import generate_uid

INPUT_FOLDER = "Input-Folder"
OUTPUT_FOLDER = "Output-FOlder"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

PIXEL_SPACING = [0.5, 0.5]
SLICE_THICKNESS = 0.5
STUDY_UID = generate_uid()
SERIES_UID = generate_uid()

# İşleme
for idx, file_name in enumerate(sorted(os.listdir(INPUT_FOLDER))):
    if not file_name.endswith(".dcm"):
        continue

    input_file = os.path.join(INPUT_FOLDER, file_name)
    output_file = os.path.join(OUTPUT_FOLDER, f"{idx + 1:04d}.dcm")

    try:
        ds = pydicom.dcmread(input_file)

        ds.PatientName = "UpdatedPatient"
        ds.PatientID = "67890"
        ds.StudyInstanceUID = STUDY_UID
        ds.SeriesInstanceUID = SERIES_UID
        ds.SOPInstanceUID = generate_uid()

        ds.PixelSpacing = PIXEL_SPACING
        ds.SliceThickness = SLICE_THICKNESS

        ds.InstanceNumber = idx + 1
        ds.ImagePositionPatient = [0.0, 0.0, idx * SLICE_THICKNESS]
        ds.ImageOrientationPatient = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
        ds.SliceLocation = idx * SLICE_THICKNESS

        ds.save_as(output_file, write_like_original=False)
        print(f"Updated and saved DICOM: {output_file}")

    except Exception as e:
        print(f"Error processing file {input_file}: {e}")

print("DICOM update completed.")
