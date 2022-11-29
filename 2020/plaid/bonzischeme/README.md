# bonzi scheme

* category: misc
* points: 300
* author: sael (after the ctf)

## challenge description
Digging around in all those fish took a lot out of you. As you bend over to take a seat on a curb, you see a monkey crouching right in front of you. Skin purple, eyes too close together, the monkey smiles.

“Hey, what are you doing here?”

“I’m just here to help you out,” the monkey replies. “I’m Bonzi. How can I help?”

Bonzi reaches his hand out to you. You really could use a friend right about now. Everything is so confusing, and you have no idea what’s happening with REFUGE. How is it that the one silly little challenge caused everything to go haywire?

You smile back at Bonzi. Maybe they need a friend too.

## resources
* [challenge site](http://bonzi.pwni.ng:31337)
* [web app source](https://play.plaidctf.com/files/bonziapp-77da807e733a6a409b5eee5e12201734926a192a6def2ddc58173198c28b6e1c.tar.gz)
* [spec](http://www.lebeausoftware.org/downloadfile.aspx?ID=25001fc7-18e9-49a4-90dc-21e8ff46aa1d)

## explanation
The web app allowed you to upload an ACS file and retrieve an image from within that file. The app would replace a description field with the flag

### bug
The compression algorithm provided the ability to duplicate bytes that have already been decompressed. This is done by specifying a negative offset relative to your current position in the decompression buffer. The primitive is the ability to read bytes before your current location.

### method
Parse the file format for at least the data structures needed. Modified a provided example ACS file to include a new image information struct as close as we can after where the flag will be placed.

I tried both an 010 template and kaitai struct. Both useful but the latter converts direct to python for easy scripting. The [webIDE](https://ide.kaitai.io) was great for developing the struct [definition](./acs.ksy) using the example [file](./bonz.acs) given and then generating the [python](./acs.py) used in the [solution](./soln.py).

Having modified the ACS, we can upload to the site and specify our favourite number as 0, which extracts the image at position 0, which we have relocated to the end of the file after the flag.

There is only one section in the decompression stream and it instructs the decompression to copy a number of bytes from an offset which corresponds with a description field, where the flag was placed.

The last step is to extract the flag from the downloaded image. The file is a bitmap with RGB byte triples, one for each byte we copied. Each byte was used as an index into the palette of the ACS to find the correct pixel, so we can do the reverse lookup to get the flag back.

``` shell
$ python soln.py
<upload newbons.acs / download f4e13b63-d5b9-456b-a12f-0645543bcaad.bmp> 
PCTF{th3_re4l_tr34sure_w4s_the_bonz_we_m4d3_along_the_w4y}
```