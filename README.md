##Audio Machine Learning project using CNNs

This machine learning project attempts to generate a rhythm game beatmap from a single audio file.

Information regarding the type of [rhythm game beatmap creation]([url](https://en.wikipedia.org/wiki/Osu!)) I will be automating

Data Preprocessing Steps:
- Grab .osz files
- Convert .osz files to .zip
- Extract .zip files to a regular directory file
- Each .osz file contains a .mp3 audio file and .osu file containing the beatmap data.
- Each .osu file contains numerous "hit objects". A hit objects contains data such as when it occured and what lane it occured on.

Training steps:
For each .osu file and it's associated .mp3 audio file:
- Partition the .mp3 file into n partitions.
- Each partition contains mel spectrogram data.
- Ground truth is taken from the .osu file at the given partition's time (The .osu file contains numerous hit objects with a time attribute)
- The CNN is then fed the partition(s) and will attempt to predict if a partition should contain a note or not (Will change in the future)
- The predicted values are compared to ground truth, and backpropagation is performed to improve the model.
