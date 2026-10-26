# TWIST Image Reduction and Photometry Pipeline

A Python pipeline for reducing TWIST instrument FITS images, performing astrometric calibration, measuring image quality, and extracting stellar photometry.

## Overview

The pipeline automates the processing of TWIST observations, from raw FITS images to calibrated science images, astrometric solutions, diagnostic plots, and photometric time series.

The main entry point is `run_pipeline.sh`, which orchestrates the Python scripts in this repository.

The pipeline includes the following stages:

1. **Image organisation** — sorts observations into date- and target-specific directories.
2. **Flat-field calibration** — constructs a master flat from flat-field exposures.
3. **Science image calibration** — subtracts master bias and exposure-scaled dark frames, then applies the master flat.
4. **Reference catalogue generation** — queries Gaia DR3 for reference stars and filters unsuitable or blended sources.
5. **Astrometric calibration** — determines image astrometry using detected sources and a reference catalogue.
6. **Image quality measurement** — measures the half-flux diameter (HFD).
7. **Image rejection** — separates images flagged as unsuitable by the rejection script.
8. **Diagnostic plots** — produces plots of observing conditions, image quality, and photometric performance.
9. **Photometry extraction** — measures stellar fluxes and magnitudes and calculates Julian-date, heliocentric, and barycentric observation times.

The pipeline is under development and currently contains machine-specific paths and instrument-specific parameters. Review the configuration requirements below before running it on a new machine or dataset.

## Repository contents

| File | Purpose |
|---|---|
| `run_pipeline.sh` | Main orchestration script |
| `bias.py` | Creates master bias images |
| `dark.py` | Dark-frame processing |
| `flats.py` | Creates master flat-field images |
| `calibrate.py` | Calibrates raw science exposures |
| `fetch_reference_catalogue.py` | Retrieves and filters Gaia DR3 reference stars |
| `solve-astrometry.py` | Performs astrometric calibration |
| `measure_hfd.py` | Measures half-flux diameter |
| `remove_bad_files.py` | Identifies and separates rejected images |
| `diagnostic_plots.py` | Generates diagnostic plots |
| `extract_photometry.py` | Extracts photometry and generates light curves |
| `utilities.py` | Shared instrument parameters and utility functions |
| `scratch.py` | Experimental or auxiliary code |

## Requirements

The current implementation is designed for a Unix-like environment, with macOS-specific paths in some scripts.

The following are required or used by the current code:

- Python 3
- A Conda environment
- NumPy, Astropy, fitsio, and the `path` package
- SEP, Photutils, and tqdm
- Matplotlib, imageio, and ephem
- Astroquery for accessing Gaia DR3
- `fitsheader` for reading FITS header information
- Astrometry.net's `solve-field` executable for astrometric solving
- A working LaTeX installation for plots that use Matplotlib's TeX rendering

The main shell script currently activates a Conda environment named `w1m`. Create an environment with the required packages, or change the environment name in `run_pipeline.sh` to match your own.

A complete, pinned dependency specification is not yet provided. The packages listed above should therefore be treated as a starting point, not a tested installation recipe.

## Data directory structure

The pipeline expects observational data and calibration files to live outside the source-code repository.

The intended layout is approximately:

```text
twist_data/
├── dates/
│   ├── YYYYMMDD/
│   │   ├── flat/
│   │   │   ├── flat-exposure-1.fits
│   │   │   └── master-flat.fits
│   │   └── target_name/
│   │       ├── raw/
│   │       │   └── science-exposure.fits
│   │       ├── calibrated/
│   │       ├── rejected/
│   │       └── plots/
│   └── ...
├── calibration_frames/
│   ├── master-bias-<binning>.fits
│   └── master-dark-<binning>.fits
└── reference_catalogues/
    └── target_name/
        └── YYYYMMDD-target_name.fits
```

This is the intended organisation; the current shell script performs automatic sorting and should be checked before relying on it to create this structure correctly.

### Input data

- Raw science exposures should be FITS files.
- Flat-field exposures should be identifiable by `-flat-` in their filenames.
- Dark and bias files must be identified correctly by the script and kept separate from science exposures.
- Master bias and dark files must match the detector binning and be placed in `calibration_frames/`.
- The pipeline expects relevant TWIST FITS headers, including keywords such as `CAM-BIN`, `IMAG-RGN`, `EXPTIME`, and `DATE-OBS`.

The exact filename conventions matter because `run_pipeline.sh` uses filename patterns to classify and organise images.

## Configuration

Before running the pipeline on another machine, review the hardcoded settings in `run_pipeline.sh` and the shared utilities.

In particular, configure:

- The root directory containing observations.
- The absolute path to this repository.
- The first observation date to process.
- The location of master calibration frames and reference catalogues.
- The Conda environment name.
- The Gaia reference-catalogue query dimensions.
- The path to the Astrometry.net executable.
- Instrument-specific gain and plate scale.

See the sections below for the specific settings and their locations.

## Running the pipeline

After configuring the paths, environment, and input data:

```bash
cd /path/to/twist_pipeline
chmod +x run_pipeline.sh
./run_pipeline.sh
```

The script currently does not expose a complete command-line configuration interface. Processing dates and directories are selected within the script itself.

The pipeline creates calibrated images, rejection outputs, diagnostic plots, reference catalogues, and photometric FITS tables under the data directory.

Existing outputs may cause some processing stages to be skipped. Check the corresponding scripts and output directories before rerunning a dataset.

## Outputs

Depending on the stage and available input data, the pipeline produces:

- Master bias, dark, and flat calibration products.
- Calibrated science FITS images.
- Gaia DR3 reference catalogues.
- Astrometrically calibrated FITS images.
- HFD measurements stored in FITS headers.
- Rejected images.
- Diagnostic plots.
- Photometric FITS tables containing fluxes, uncertainties, magnitudes, and time information.
- Light curves for supported target identifiers.

## Hardcoded settings to review

The following settings should be reviewed before running the pipeline on a different machine or dataset. Line numbers can change as the code is updated.

### `run_pipeline.sh`

- **Data root (`home_dir`)**: currently points to `/Volumes/SanDisk-2TB-SSD/twist`. Change this to the absolute path of the directory containing your observational data.
- **Source directory (`bin`)**: currently points to `/Users/nagro/PycharmProjects/twist_pipeline`. Change this to the repository directory, or make it relative to the script location.
- **First date (`first_date`)**: currently `20260208`. Change this to the first observation date to process, in `YYYYMMDD` format. Check that the date-selection logic handles dates that are not exact matches in the available directory list.
- **Conda environment**: currently activates `w1m`. Create an environment with this name and the required dependencies, or change the script to use your environment name. Conda must be initialised in the shell used to run the script.
- **Gaia field dimensions**: the reference-catalogue call passes `0.262` and `0.392` as field dimensions in degrees. Adjust these only if the detector field of view or catalogue-query requirements differ.

### Other Python files

| File | Setting | Guidance |
|---|---|---|
| `solve-astrometry.py` | `/opt/homebrew/bin/solve-field` | Change to the location of Astrometry.net's `solve-field` executable on your system. |
| `utilities.py` | `plate_scale = 0.226`, `gain = 0.75` | Verify these values against the relevant TWIST detector configuration. They affect scientific measurements. |
| `extract_photometry.py` | Observatory coordinates and elevation | The current site metadata are for La Palma. Change them if observations were taken elsewhere; they affect heliocentric and barycentric timing corrections. |
| `extract_photometry.py` | Aperture radii `[5, 10, 15, 20, 25, 30]` pixels | These define the photometric apertures. Change only if you intend to alter the measurement strategy. |
| `measure_hfd.py` | Detection threshold and source-selection cuts | Validate these settings for your image quality and observing conditions before changing them. |
| `flats.py` | Moon-separation criterion (`MOONSEP < 30` degrees) | Review this flat-field selection criterion if your observing strategy differs. |

Not all these values are file paths. Some are instrument parameters, observatory metadata, or analysis thresholds and should be treated as scientifically meaningful settings.

## Known portability issues to check

- The shell script uses a `cam` variable when moving flat frames; verify that it is defined or derived correctly before running the script.
- Target-directory construction in the file-sorting section should be checked to ensure that it uses the target name rather than a full file path.
- Paths and environment names are currently embedded in source code rather than centralised in a configuration file.
- The dependency list has not been pinned to tested versions.
- Validate intermediate products before relying on the output for scientific analysis.

## Recommended setup improvements

For a more reproducible and portable setup:

1. Move paths, date selection, catalogue dimensions, and instrument settings into a single configuration file.
2. Derive the repository path from `run_pipeline.sh` instead of hardcoding a user-specific path.
3. Add a tested `environment.yml` or `requirements.txt`.
4. Validate the input directory structure and required calibration files before processing.
5. Add a small test dataset and checks for intermediate products.

## Scientific validation

The pipeline is under development. Check calibration products, astrometric solutions, image-quality measurements, photometric uncertainties, and time corrections before using results for scientific interpretation.
