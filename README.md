# aaapi
Collection of audio and music processing API with massive amount of dependencies

## Modules

- AudioUtils

  - loading wav files
  - splitting audio based on volumn peaks
  - extracting audio features of MFCC and spectral entropy
  - f0 estimation using CREPE
  
- MidiUtils

  - converting frequencies to musical notes
  - converting frequencies to musical label
  - converting pandas pd into midi files
  - grouping consecutive notes into one note
  - grouping multiple notes into weighted-averaged note
  
- MusicUtils

  - identifying the scale of the musical notes


## Dependencies

All dependencies can be install either via `conda` or `pip` unless specified otherwise
- pandas
- numpy
- librosa
- scipy
- mido
- tensorflow
- crepe (install from pip only)

You can also automatically install dependencies using `pip`:

```bash
$ pip -r requirements.txt
```

or using `conda`:

```bash
$ conda env create -f conda-req.yml
```
