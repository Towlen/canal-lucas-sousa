from xml.etree import ElementTree as et

"""

A simple code to implement custom icons

"""

class icons(object):
    def __init__(self):
        self.root = et.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
        self.doc = et.SubElement(self.root, 'Document')
        self.placemarks = []
        self.styles = []
        self.multipoint = []

    def addicon(self, name, iconid, color, description, lat, long, height):
        styleid = icons.addstyle(self, iconid, color)
        self.placemarks.append(placemark(name, description, styleid, '{},{},{}'.format(long,lat,height)))
        return self.placemarks[-1]

    def multiicon(self, name, iconid, color, description):
        styleid = icons.addstyle(self, iconid, color)
        self.multipoint.append(multigeo(name, description, styleid))
        return self.multipoint[-1]

    def addstyle(self, iconid, color):
        iconstyle = '{}-{}'.format(iconid,color)
        if not iconstyle in self.styles:
            self.styles.append(iconstyle)
        return self.styles.index(iconstyle)

    def write(self, filename):
        for stylesid in self.styles:

            styleid = et.SubElement(self.doc,'Style', id='icon-' + stylesid + '-nodesc-normal')
            iconstyle = et.SubElement(styleid, 'IconStyle')
            href = et.SubElement(iconstyle, 'Icon')
            et.SubElement(href, 'href').text = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

            stylemap = et.SubElement(self.doc,'StyleMap', id='icon-' + stylesid + '-nodesc')
            pair = et.SubElement(stylemap, 'Pair')
            et.SubElement(pair, 'key').text = 'normal'
            et.SubElement(pair, 'styleUrl').text = '#icon-' + stylesid + '-nodesc-normal'

        for plcemark in self.placemarks:

            placemark = et.SubElement(self.doc,'Placemark')
            et.SubElement(placemark,'name').text = plcemark.name
            et.SubElement(placemark,'description').text = plcemark.description
            et.SubElement(placemark,'styleUrl').text = '#icon-' + self.styles[plcemark.styleid] + '-nodesc'
            point = et.SubElement(placemark,'Point')
            et.SubElement(point,'coordinates').text = plcemark.coordinates

        for multi in self.multipoint:

            placemark = et.SubElement(self.doc,'Placemark')
            et.SubElement(placemark,'name').text = multi.name
            et.SubElement(placemark,'description').text = multi.description
            et.SubElement(placemark,'styleUrl').text = '#icon-' + self.styles[multi.styleid] + '-nodesc'
            multigeometry = et.SubElement(placemark,'MultiGeometry')

            for j in multi.coordinates:
                point = et.SubElement(multigeometry,'Point')
                et.SubElement(point,'coordinates').text = j

        tree = et.ElementTree(self.root)
        tree.write(filename)

class multigeo():
    def __init__(self, name, description, styleid):
        self.name = name
        self.description = description
        self.styleid = styleid
        self.coordinates = []

    def addicon(self, lat, long, height):
        self.coordinates.append('{},{},{}'.format(long,lat,height))

class placemark():
    def __init__(self, name, description, styleid, coordinates):
        self.name = name
        self.description = description
        self.styleid = styleid
        self.coordinates = coordinates


class transport:
    bus = 1532
    subway = 1719
