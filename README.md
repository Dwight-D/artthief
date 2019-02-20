# Art Thief

Simple python program that reads a list of imgur album hashes and downloads a random image from a random album.

## Usage

Create config directory and place a list of imgur gallery/album hashes under `~/.config/artthief/albums.conf`.

Run with `artthief` to download a random image from your configured imgur albums. Image will be automatically downloaded and the path to the downloaded file will be output to stdout for redirecting to other apps such as background setters. 

This program works nicely together with something like [pywal](https://github.com/dylanaraps/pywal) (shoutout to dylanaraps and thanks for a great program!). Example:

```wal -i $(artthief) [other options]```

Switches:

`-c / --clean` to clean the image library (delete previously downloaded files) before running. Use this to avoid taking up too much memory space.

### Configuration

Config file should be stored under ~/.config/artthief/albums.conf
The list should contain imgur album hashes separated by newline.
I.e. if the imgur link is `https://imgur.com/a/A123BC456` the entry should contain only `A123BC456`

### Hey, what's this cool image I downloaded?

Image names have the following format:

datestamp-galleryHash-imageHash-[imageTitleIfItExists].jpg. 

If the image title doesn't give you a clue you can recreate the link with these hashes and maybe find some more information there.

### Notes

If your python interpreter sits in a different path than the shebang in the script you may need to edit the file or run it with `python /path/to/artthief`.

### About download location

Images are downloaded to ~/.config/artthief/library currently. While this may not be great design I didn't want to pollute the home directory unnecessarily for such a simple program, so I opted to place them together with the config. I may add in the possibility to configure different download directories at a later time.
