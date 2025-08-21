def find_missing_ranges(frames: list[int]) -> dict: 
    """
    Documentation:
    Analyze a list of received video frame numbers and report:
      - total number of missing frames,
      - list of missing ranges as [start, end],
      - the longest missing-range and its size.

    Assumptions:
      - `frames` contains positive integers (>=1).
      - No duplicates (caller guarantees this).
      - The highest observed frame number equals the expected final frame number.
      - Function does not mutate the caller's list.
    Returns a dict with keys:
      - "missing_frames": int
      - "missing_gaps": list of [start, end]
      - "longest_gap_range": [start, end] or None
      - "longest_gap_size": int
    """

    # ---------- Validation ----------
    if not isinstance(frames, list):
        raise TypeError("frames must be a list")
    if len(frames) == 0:
        return {
            "missing_frames": 0,
            "missing_gaps": [],
            "longest_gap_range": None,
            "longest_gap_size": 0
        }
    # ensure all items are positive integers
    for x in frames:
        if not isinstance(x, int) or x <= 0:
            raise ValueError("frames list must contain positive integers only")

    # process copy of the list
    arr = frames.copy()

    # merge sort 
    def merge(left, right):
        i = 0
        j = 0
        out = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
        if i < len(left):
            out.extend(left[i:])
        if j < len(right):
            out.extend(right[j:])
        return out

    def merge_sort_iteration(a):
        if len(a) <= 1:
            return a.copy() 
        width = 1
        res = a.copy()
        n = len(res)
        while width < n:
            i = 0
            new_res = []
            while i < n:
                left = res[i:i + width]
                right = res[i + width:i + 2 * width]
                if right:
                    merged = merge(left, right)
                else:
                    merged = left.copy()  
                new_res.extend(merged)
                i += 2 * width
            res = new_res
            width *= 2
        return res

    sorted_frames = merge_sort_iteration(arr)

    # gap detection
    missing_frames = 0
    missing_gaps = []
    longest_gap_size = 0
    longest_gap_range = None

    # missing before the first received frame (frames start at 1)
    first = sorted_frames[0]
    if first > 1:
        start = 1
        end = first - 1
        size = end - start + 1
        missing_frames += size
        missing_gaps.append([start, end])
        longest_gap_size = size
        longest_gap_range = [start, end]

    # internal gaps between adjacent frames
    for k in range(len(sorted_frames) - 1):
        a = sorted_frames[k]
        b = sorted_frames[k + 1]
        size = b - a - 1  # number of missing frames between a and b
        if size > 0:
            start = a + 1
            end = b - 1
            missing_frames += size
            missing_gaps.append([start, end])
            if size > longest_gap_size:
                longest_gap_size = size
                longest_gap_range = [start, end]

    return {
        "missing_frames": missing_frames,
        "missing_gaps": missing_gaps,
        "longest_gap_range": longest_gap_range,
        "longest_gap_size": longest_gap_size
    }