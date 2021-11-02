"""Default runtime config."""
import src
import pathlib
import torch
import os

# General config
STAGE = "extract"  # "extract" | "curate "
SEED = 42

if os.getenv("AUTOMATION"):
    ROOT =  pathlib.Path("/opt/app-root")
else:
    ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

CONFIG_FOLDER = ROOT
CHECKPOINT_FOLDER = ROOT / "models"
DATA_FOLDER = ROOT / "data"
BASE_PDF_FOLDER = DATA_FOLDER / "pdfs"
BASE_ANNOTATION_FOLDER = DATA_FOLDER / "annotations"
BASE_EXTRACTION_FOLDER = DATA_FOLDER / "extraction"
BASE_CURATION_FOLDER = DATA_FOLDER / "curation"

CHECKPOINT_S3_PREFIX = "corpdata/saved_models"
DATA_S3_PREFIX = "corpdata/ESG"
BASE_ANNOTATION_S3_PREFIX = f"{DATA_S3_PREFIX}/annotations"
BASE_CURATION_S3_PREFIX = f"{DATA_S3_PREFIX}/curation"
BASE_INFER_S3_PREFIX = f"{DATA_S3_PREFIX}/infer"

if os.getenv("AUTOMATION"):
    BASE_PDF_S3_PREFIX = f"{DATA_S3_PREFIX}/pdfs_sample"
    BASE_EXTRACTION_S3_PREFIX = f"{DATA_S3_PREFIX}/extraction_sample"
else:
    BASE_PDF_S3_PREFIX = f"{DATA_S3_PREFIX}/pdfs_sample"
    BASE_EXTRACTION_S3_PREFIX = f"{DATA_S3_PREFIX}/extraction_sample"
    
ckpt = "icdar_19b2_v2.pth"
config_file = "cascade_mask_rcnn_hrnetv2p_w32_20e_v2.py"
PDFTableExtractor_kwargs = {
    "batch_size": -1,
    "cscdtabnet_config": CONFIG_FOLDER / config_file,
    "cscdtabnet_ckpt": CHECKPOINT_FOLDER / ckpt,
    "bbox_thres": 0.85,
    "dpi": 200,
}

# PDFTextExtractor
PDFTextExtractor_kwargs = {
    "min_paragraph_length": 30,
    "annotation_folder": None,
    "skip_extracted_files": False,
}

TableCurator_kwargs = {
    "neg_pos_ratio": 1,
    "create_neg_samples": True,
    "columns_to_read": [
        "company",
        "source_file",
        "source_page",
        "kpi_id",
        "year",
        "answer",
        "data_type",
    ],
    "company_to_exclude": ["CEZ"],
    "seed": SEED,
}

TextCurator_kwargs = {
    "retrieve_paragraph": False,
    "neg_pos_ratio": 1,
    "columns_to_read": [
        "company",
        "source_file",
        "source_page",
        "kpi_id",
        "year",
        "answer",
        "data_type",
        "relevant_paragraphs",
    ],
    "company_to_exclude": [],
    "create_neg_samples": True,
    "seed": SEED,
}

# Components
EXTRACTORS = [
    # ("PDFTableExtractor", PDFTableExtractor_kwargs),
    ("PDFTextExtractor", PDFTextExtractor_kwargs)
]

CURATORS = [
    ("TextCurator", TextCurator_kwargs)
    # ,("TableCurator", TableCurator_kwargs)
]
