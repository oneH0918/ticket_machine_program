FARE_TABLE = [
    (4.9, 170),
    (9.9, 200),
    (14.9, 240),
    (19.9, 280),
    (26.9, 290),
    (33.9, 330),
    (42.9, 390),
    (51.9, 410),
    (60.9, 480),
    (70.9, 540),
    (76.9, 640),
]

def calculate_fare(distance):
    """距離に応じて運賃を計算"""
    if distance is None or distance <= 0:
        return "運賃不明"
    
    # 運賃テーブルを参照して計算
    for max_distance, fare in FARE_TABLE:
        if distance <= max_distance:
            return fare
    
    return "運賃不明"