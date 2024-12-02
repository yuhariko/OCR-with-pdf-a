def custom_sort(item):
    bbox, _ = item
    x0, y0, _, _ = bbox

    return (round(y0 / 5) * 5, x0)