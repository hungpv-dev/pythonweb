
"""
    modal = Modal bài viết
    content = Nội dung (chữ) bài viết
    media = Hình ảnh, video
    dyamic = lượt like, chia sẻ, comment
    hasMore = Nút xem thêm
    Comment = Danh sách comment
"""

types = {
    'modal': '/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div',
    'content': '/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[3]',
    'media': '/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[3]',
    'dyamic': '/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[1]/div',
    'hasMore': ".//div[text()='Xem thêm']",
    'comments': "div[aria-label*='Bình luận']"
}

# Xoá chữ k cần thiết khi lấy content bài viết
removeString = [
    '\n',
    '·',
    '  ',
    'Xem bản dịch',
    'Xem bản gốc',
    'Xếp hạng bản dịch này'
]

# Xoá chữ k cần thiết khi lấy comment bài viết
removeComment = [
    '·',
    'Tác giả\n',
    '  ',
    'Fan cứngt'
    'Theo dõi',
]


# Xoá thông tin k cần thiết khi lấy lượt like, chia sẻ, comment
removeDyamic = [
    'Tất cả cảm xúc:',
    '',
]

# Lấy bình luận, chia sẻ dựa vào chữ này
selectDyamic = {
    'comment': 'bình luận',
    'share': 'lượt chia sẻ'
}



push = {
    'createPost': '/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[2]/div/div[2]/div[1]/div/div/div/div/div[1]/div'
}