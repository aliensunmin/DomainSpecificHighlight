##[Domain-specific Highlights in Personal Videos](http://aliensunmin.github.io/project/at-a-glance/)

[![Watch the concept video](http://img.youtube.com/vi/H5wW6LsubKc/0.jpg)](http://www.youtube.com/watch?v=H5wW6LsubKc)

Here are the data and some codes used in paper [1].
[1] described a fully automatic method to train domain-specific highlight ranker for raw personal videos.
Given a keyword such as surfing, the proposed method automatically harvests YouTube for both raw and edited pairs of personal videos for training a domain-specific highlight ranker.
Experimental results demonstrate state-of-the-art highlight detection ability on surfing, skating, skiing, gymnastics, parkour, and dog related domains.
If you use the data and/or codes, please cite our paper using the following bibtex.

	@inproceedings{ECCV14HL,
		author = "Min Sun and Ali Farhadi and Steve Seitz",
		title = "Ranking Domain-specific Highlights by Analyzing Edited Videos",
		booktitle = "ECCV",
		year = "2014",
	}

## Notations
1. $BaseDir: the path to the dataset (e.g., /path/to/dataset/).
2. $Domain: the keyword for each domain (e.g., surfing, skating, skiing, gymnastics, parkour, and dog).
3. $Vid: video index (a hash key) used by YouTube. The link to the YouTube video is https://www.youtube.com/watch?v=$Vid (e.g., https://www.youtube.com/watch?v=0-fstXuo_Pw)
4. *matched* clip: a clip in a raw video which matched the edited video, which means it is a candidate highlight that the user selected to create the edited video.
5. $JsonFile: a json file typically with *.json format.

## Contents
1. $BaseDir/code : python and matlab codes 
2. $BaseDir/$Domain : vlist.json/vlist_sel.json specifies the list of videos. There are also a number of subfolders, each contains information about a YouTube video mentioned in the vlist.json/vlist_sel.json file.
3. $BaseDir/missingVideos : a number of subfolders containing the missing YouTube videos. Please update this information by opening an issue in this repository.

## Video list
1. vlist.json : specify the automatically harvested $Vid used in four sets.
	1. TraiTightL (Training Tight Label) is a set of videos for training where only a few clips are *matched* in each video.
	2. TraiLooseL (Training Loose Label) is a set of videos for training where many clips are *matched* in each video.
	3. TestTightL (Testing Tight Label) is a set of videos for testing where only a few clips are *matched* in each video.
	4. TestLooseL (Testing Loose Label) is a set of videos for testing where many clips are *matched* in each video.

Note that it can be read into python or matlab as shown in the "Read annotation" section.

2. vlist_sel.json : specify domain-relevant (manually selected) $Vid used in four sets.

	Same definition of four sets as above.

Note that vlist_sel.json is a subset of vlist.json.

## Definition of clip
In each folder (e.g., $BaseDir/#Domain/$Vid), clip.json specifies a number of clips, each about 2 seconds. Each clip is defined by [start_frame, end_frame].
For instance,
	
	[[0.0, 100.0], [50.0, 150.0], [100.0, 200.0]]

contains 3 clips. The first clip starts from frame 0 and ends at frame 100.

## Harvested Highlight
In each folder (e.g., $BaseDir/#Domain/$Vid), match_label.json specifies if each clip is *matched* in the edited video (selected by user as highlight).
Label 1 denotes *matched* clip, label -1 denotes *unmatched* clip, and label 0 denotes borderline cases.
For instance,

	[[[0.0, 100.0], [50.0, 150.0], [100.0, 200.0]],[-1, 0, 1]]

means the first clip is not *matched*, the second clip is a borderline cae, and the last clip is a *matched* clip.

## Mturk Highlight
In each folder (e.g., $BaseDir/#Domain/$Vid), mturk_label.json specifies how many turkers select a clip as highlight.
For instance,

	[[[0.0, 100.0], [50.0, 150.0], [100.0, 200.0]],[2.0, 3.0, 0.0]]

means the first clip is selected by 2 people, the second clip is selected by 3 people,  and the last clipis not selected.
Note that turkers cast soft votes (i.e., not integer) depending on the coverage between the clip and tuker selected video segment.

## Download videos from YouTube

First, install [youtube-dl](http://rg3.github.io/youtube-dl/).
Then, please issue the following command.

    cd $BaseDir
    python code/downloadVideo.py ./ 2> err.out

Note that these videos are publicly available for download during the time the work is conducted.
However, it is possible that the videos are not publicly available on YouTube at the time you run this script.
You can find which videos are missing in err.out. For instance,

    missing_vid
    ./dog/fxOfeQdFrVE

means that fxOfeQdFrVE in the dog domain is missing.

### Backup missing videos
If a backup of a missing video can be found in $BaseDir/missingVideos/$Vid, the video will not be considered as missing anymore.
Note that `cat $BaseDir/missingVideos/$Vid` should return the new YouTube video hash key that backup the original $Vid.
Please open an issue on github, once additional videos are missing.
People who has the missing videos, feel free to back it up on YouTube and specify its new YouTube hash key into $BaseDir/missingVideos/$Vid.

## Read annotation
1. In python,
	* Do,
	```
	cd $BaseDir/code
	python
	import downloadVideo as dv
	data = dv.loadJson($JsonFile)
	```
	* Get,
	```
	>>> len(data)
	4
	>>> data[0]
	[[u'U4w0PucbcOc', u'iWO6io44-Fs', u'p9yW6FxsrJ4', u'L10kN7Btk90', u'AZDkqJaOgJU', u'iyYiqa0QZXM', u't-kc6G4SpAk', u'uJ81Us4mBOc'], u'TraiTightL']
	>>> data[0][0][0]
	u'U4w0PucbcOc'
	```	
2. In matlab,
	* Do,
	```
	cd $BaseDir/code
	matlab -nodisplay
	addpath('jsonlab')
	data = loadjson($JsonFile)
	```
	* Get,
	```
	>>who data
	Name      Size            Bytes  Class    Attributes
	data      1x4             11340  cell
	>>datao{1}
	ans =
    {1x8 cell}    'TraiTightL'
	>> oo{1}{1}
	ans = 
		'U4w0PucbcOc'    'iWO6io44-Fs'    'p9yW6FxsrJ4'    'L10kN7Btk90'    'AZDkqJaOgJU'    'iyYiqa0QZXM'    't-kc6G4SpAk'    'uJ81Us4mBOc'
	```
## References
[1] M. Sun, A. Farhadi, and S. Seitz. Ranking Domain-specific Highlights by Analyzing Edited Videos. ECCV 2014 [pdf](https://drive.google.com/file/d/0ByJgUdTb1N2CQk9ROVJHLVAxY00/edit?usp=sharing)
