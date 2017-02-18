# coding: utf-8
import re

hex_array = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15
}


class ColorParser():

    def getStyledString(self, string, match, col, wide, narrow, caps, italic, stripColors):
        string = string[len(match[0]):]
        string = string.strip()
        if caps:
            string = string.upper()
        if (col or wide or narrow or italic) and string:
            start1 = "<span style='"
            start2 = "'>"
            styles = ""
            end = "</span>"
            if (col and not stripColors):
                colRGB = self.get_rgb('#'+col)
                # colRGBNew = self.getContrastCorrectedColor(colRGB)
                # colNew = self.get_hex(colRGBNew)
                styles += "color:"+colRGB+";"
            if italic:
                styles += "font-style:italic;"
            if wide:
                styles += "font-weight:bold;"
            if narrow:
                styles += "letter-spacing: -0.1em;font-size:smaller"
            string = start1+styles+start2+string+end
        return string

    def replace_hexa(self, hexa):
        keys = hex_array.keys()
        hexas = hexa
        for key in keys:
            hexas = hexas.replace(key, '')
        return hexas

    def get_rgb(self, hexa):
        hexa = hexa.upper().replace('#', '')
        length = len(hexa)
        rgb = {}
        if length == 3:
            hexa = hexa[0]+hexa[0]+hexa[1]+hexa[1]+hexa[2]+hexa[2]
            length = 6
        if length != 6:
            return False
        rgb['r'] = hex_array[hexa[0]] * 16 + hex_array[hexa[1]]
        rgb['g'] = hex_array[hexa[2]] * 16 + hex_array[hexa[3]]
        rgb['b']= hex_array[hexa[4]] * 16 + hex_array[hexa[5]]
        return 'rgb(%d, %d, %d)' % (rgb['r'], rgb['g'], rgb['b'])

    def toHTML(self, nick, stripColors=False, stripLinks=False, stripTags=''):
        col = False
        wide = False
        narrow = False
        caps = False
        italic = False
        counter = 0

        if stripTags.lower() == 'all':
            stripTags = 'iwonstmgaxz'

        for i in range(len(stripTags)):
            toStrip = stripTags[i]
            nick = nick.replace(''+toStrip, '')

        nick = nick.replace('$$','[DOLLAR]')
        nick = nick.replace(' ','&nbsp;')
        # nick = this->parseLinks(str, !stripLinks)
        chunks = nick.split('$')
        new_chunks = []
        for chunk in chunks:
            matches = re.findall(r"^[0-9a-f]{2,3}", chunk, re.IGNORECASE)
            if matches:
                col = matches[0]
                if len(col) < 3:
                    col = col+"8"
                col = col[0]+col[0]+col[1]+col[1]+col[2]+col[2]
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(i)", chunk, re.IGNORECASE)
            if matches:
                italic = True;
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(w)", chunk, re.IGNORECASE)
            if matches:
                narrow = False
                wide = True
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(o)", chunk, re.IGNORECASE)
            if matches:
                narrow = False
                wide = True
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(n)", chunk, re.IGNORECASE)
            if matches:
                wide = False
                narrow = True
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(s)", chunk, re.IGNORECASE)
            if matches:
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(t)", chunk, re.IGNORECASE)
            if matches:
                caps = True
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(m)", chunk, re.IGNORECASE)
            if matches:
                wide = False
                bold = False
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(g)", chunk, re.IGNORECASE)
            if matches:
                col = False
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(a)", chunk, re.IGNORECASE)
            if matches:
                colSave= col
                wideSave = wide
                narrowSave = narrow
                capsSave = caps
                italicSave = italic
                col = False
                wide = False
                narrow = False
                caps = False
                italic = False
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(x)", chunk, re.IGNORECASE)
            if matches:
                col = colSave
                wide = wideSave
                narrow = narrowSave
                caps = capsSave
                italic = italicSave
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            matches = re.findall(r"^(z)", chunk, re.IGNORECASE)
            if matches:
                col = False
                wide = False
                narrow = False
                caps = False
                italic = False
                chunk = self.getStyledString(chunk, matches, col, wide, narrow, caps, italic, stripColors)
            new_chunks.append(chunk)
        for chunk in new_chunks:
            chunk = chunk.replace('[DOLLAR]', '')
            chunk = chunk.replace('&NBSP;', '&nbsp;')
        nick = ''.join(new_chunks)
        return nick

        def autoContrastColor(self, bgColor=''):
            return self.get_rgb(bgColor)

        """
        def getContrastCorrectedColor(self, rgb):
            background = self.autoContrastColor()
            lighter = rgb
            darker = rgb
            diff = self.getColorDifference(rgb, background)
            white = self.get_rgb('#ffffff')
            black = self.get_rgb('#000000')
            limit = 15
            steps = 50
            diffDarkerFromRealColor = 255
            diffLighterFromRealColor = 255
            for ($i = 1; $i<=$steps; $i++){
                $diffLight = $this->getColorDifference($lighter, $this->background);
                $diffDark = $this->getColorDifference($darker, $this->background);
                if ($diffLight < $limit){
                    $lighter['r'] = ($steps-$i)/$steps * $rgb['r'] + $i/$steps * $white['r'];
                    $lighter['g'] = ($steps-$i)/$steps * $rgb['g'] + $i/$steps * $white['g'];
                    $lighter['b'] = ($steps-$i)/$steps * $rgb['b'] + $i/$steps * $white['b'];
                } else {
                    $diffLighterFromRealColor = $this->getColorDifference($lighter, $rgb);
                }
                if ($diffDark < $limit){
                    $darker['r'] = ($steps-$i)/$steps * $rgb['r'] + $i/$steps * $black['r'];
                    $darker['g'] = ($steps-$i)/$steps * $rgb['g'] + $i/$steps * $black['g'];
                    $darker['b'] = ($steps-$i)/$steps * $rgb['b'] + $i/$steps * $black['b'];
                } else {
                    $diffDarkerFromRealColor = $this->getColorDifference($darker, $rgb);
                }
            }
            $totalDiffLight = abs($limit - $this->getColorDifference($lighter, $this->background));
            $totalDiffDark = abs($limit - $this->getColorDifference($darker, $this->background));
            if ($this->forceDarken) return $darker;
            if ($this->forceBrighten) return $lighter;
            if ($diffLighterFromRealColor < $diffDarkerFromRealColor){
                return $lighter;
            } else if ($diffLighterFromRealColor > $diffDarkerFromRealColor){
                return $darker;
            } else {
                if ($totalDiffDark < $totalDiffLight) return $darker; else return $lighter;
            }
        }
        """
