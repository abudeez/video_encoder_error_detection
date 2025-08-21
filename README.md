# Video Frame Gap Detector

This project provides a function `find_missing_ranges` to detect missing video frames from a list of received frame numbers.

## Usage

```bash
python main.py

```

### Example input:

frames = [1, 5, 3 ,8, 7]

### Example output:

{
  "missing_frames": 37,
  "missing_gaps": [[1, 3], [5, 5], [7, 8], [10, 43]],
  "longest_gap_range": [10, 43],
  "longest_gap_size": 34
}
