#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      PauloS
#
# Created:     09/03/2014
# Copyright:   (c) PauloS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    with open("municipios.json") as _in:
        d = json.load(_in)
    with open("municipios.tsv", "wb") as _out:
        keys = d['features'][0]['properties'].keys()
        _out.write("\t".join(keys)+"\n")
        for f in d['features']:
            p = f['properties']
            line = []
            for k in keys:
                v = p[k]
                if isinstance(v, unicode):
                    v = v.encode("utf-8")
                elif not isinstance(v, str):
                    v = str(v)
                line.append(v)
            _out.write("\t".join(line)+"\n")

if __name__ == '__main__':
    main()
