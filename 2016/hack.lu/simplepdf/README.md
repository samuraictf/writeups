# simplepdf

The given PDF seemed to have some data in stream 6, so I extracted that stream out to a new file. The stream was another PDF file, so I repeated the process. I eventually realized that there were many PDFs nested in stream 6.

I originally used `dumppdf` to recursively extract the PDFs, but this was slow, so I manually dumped them with zlib:

``` python
#!/usr/bin/env python2

import zlib

f = open('simplepdf_f8004a3ad0acde31c40267b9856e63fc.pdf').read()
open('dump.pdf', 'w').write(f)

while True:
    f = open('dump.pdf').read()
    index = f.find('6 0 obj')
    start_index = f.find('/Length', index)
    end_index = f.find('\n', start_index)
    length = int(f[start_index + 8:end_index].strip())
    stream = f.find('stream', end_index)
    new_file = f[stream + 7:stream + 7 + length]
    open('dump.pdf', 'w').write(zlib.decompress(new_file))
```

After running the script, you will have a PDF with the flag: flag{pdf_packing_is_fun}
