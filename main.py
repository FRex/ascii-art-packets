import sys


BIT_SIZE = 3

def field_width(bits):
    return BIT_SIZE * bits + (bits - 1)

def adjust(s, bits):
    #print(f"adjusting {s} to {bits}", file=sys.stderr)
    ret = str(s).center(field_width(bits))
    #print(f"got >{ret}< of len {len(ret)}", file=sys.stderr)
    return ret

BITS_PER_LINE = 32
PARTS_PER_LINE = 4
BITS_PER_PART = BITS_PER_LINE // PARTS_PER_LINE

class Diagram:
    def __init__(self) -> None:
        self.elements = []

    def add(self, name, size):
        self.elements.append((name, size))

    def print(self):
        bits = 0
        ret = []
        HEADER = '+' + '|'.join(['-' * field_width(BITS_PER_PART)] * PARTS_PER_LINE) + '+'
        ret.append(HEADER)
        for n, w in self.elements:

            if n is None:
                assert bits % BITS_PER_LINE == 0
                ret.append(HEADER)
                bits += BITS_PER_LINE
                continue

            if bits % BITS_PER_LINE == 0:
                ret.append('|')

            left = BITS_PER_LINE - bits % BITS_PER_LINE
            if left >= w:
                ret[-1] += adjust(n, w) + '|'
                bits += w
            else:
                ret[-1] += adjust(n, left) + ':'
                ret.append(':')
                bits += w

                w -= left
                while w > BITS_PER_LINE:
                    ret[-1] += adjust(n, BITS_PER_LINE) + ':'
                    ret.append(':')
                    w -= BITS_PER_LINE
                if w > 0:
                    ret[-1] += adjust(n, w) + '|'
        #padding
        if bits % BITS_PER_LINE != 0:
            left = BITS_PER_LINE - bits % BITS_PER_LINE
            ret[-1] += adjust('', left) + '|'
        ret.append(HEADER)
        return '\n'.join(ret)

d = Diagram()

d.add('Oct 0', 8)
d.add('Oct 1', 8)
d.add('Oct 2', 8)
d.add('Oct 3', 8)
d.add(None, None)

d.add('Version', 4)
d.add('IHL', 4)
d.add('DSCP', 6)
d.add('ECN', 2)
d.add('Total Length', 16)

d.add('Identification', 16)
d.add('Flags', 3)
d.add('Fragment Offset', 13)

d.add('Time To Live', 8)
d.add('Protocol', 8)
d.add('Header Checksum', 16)
d.add('Source IP Address', 32)
d.add('Destination IP Address', 32)

print(d.print())

# TODO: reading text files


