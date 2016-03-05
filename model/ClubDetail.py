__author__ = '祥祥'


class Club():
    name = ''
    area = ''
    location = ''
    cover = ''
    phone = ''
    latitude = 0.0
    longitude = 0.0
    meituan_category = ''
    club_intro = ''

    def __init__(self, name='', area='', location='', cover='', phone='', latitude=0.0, longitude=0.0, meituan_category='', club_intro=''):
        self.name = name
        self.area = area
        self.location = location
        self.cover = cover
        self.phone = phone
        self.latitude = latitude
        self.longitude = longitude
        self.meituan_category = meituan_category
        self.club_intro = club_intro

    def to_string(self,):
        result = []
        result.append(self.name)
        result.append(self.area)
        result.append(self.location)
        result.append(self.cover)
        result.append(self.phone)
        result.append(self.latitude)
        result.append(self.longitude)
        result.append(self.meituan_category)
        result.append(self.club_intro)
        return result

    def setLatiLongi(self, location):
        if location is not None:
            l = location.split(',')
            if len(l) == 2:
                try:
                    self.longitude = float(l[0])
                    self.latitude = float(l[1])
                except Exception:
                    print('获取的经纬度不合法：', location)