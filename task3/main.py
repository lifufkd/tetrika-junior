def merge_intervals(intervals: list[list[int]]):
    if not intervals:
        return []

    intervals.sort()
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged


def clip_intervals_by_lesson(intervals: list[int], lesson_interval: list[int]) -> list[list[int]]:
    start, end = lesson_interval

    clipped = []
    for i in range(0, len(intervals), 2):
        s = max(intervals[i], start)
        e = min(intervals[i + 1], end)
        if s < e:
            clipped.append([s, e])
    return clipped


def find_intervals_overlap(intervals1, intervals2):
    interval1 = 0
    interval2 = 0
    total = 0

    while interval1 < len(intervals1) and interval2 < len(intervals2):
        start1, end1 = intervals1[interval1]
        start2, end2 = intervals2[interval2]

        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)

        if overlap_start < overlap_end:
            total += overlap_end - overlap_start

        if end1 < end2:
            interval1 += 1
        else:
            interval2 += 1

    return total


def appearance(intervals: dict[str, list[int]]) -> int:
    # Фильтр интервалов активности ученика и преподавателя по границам урока
    pupil_intervals = clip_intervals_by_lesson(intervals['pupil'], intervals['lesson'])
    tutor_intervals = clip_intervals_by_lesson(intervals['tutor'], intervals['lesson'])

    # Объединение коррелирующихинтервалов для оптимизации
    pupil_intervals = merge_intervals(pupil_intervals)
    tutor_intervals = merge_intervals(tutor_intervals)

    # Поиск суммарного времени ученика с преподавателем
    return find_intervals_overlap(pupil_intervals, tutor_intervals)

tests = [
    {'intervals':
         {'lesson': [1594663200, 1594666800],
          'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
          'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
         },
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
