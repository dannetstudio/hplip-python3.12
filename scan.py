#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2015 HP Development Company, L.P.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# Author: Don Welch
# Contributors: Sarbeswar Meher
#



__version__ = '2.2'
__mod__ = 'hp-scan'
__title__ = 'Scan Utility'
__doc__ = "SANE-based scan utility for HPLIP supported all-in-one/mfp devices."

# Std Lib
import sys
import os
import os.path
import getopt
import signal
import time
import socket
import operator

# Local
from base.g import *
from base.sixext import PY3
from base import tui, device, module, utils, os_utils
from prnt import cups
from scan import sane

scanext = utils.import_ext('scanext')
#if con_device == 5000 or con_device == 7500:
import platform
#from datetime import datetime
try:
    from base import imageprocessing
except ImportError:
    print (" ")

#from PIL import ImageStat

username = prop.username
r = res = 300
scan_mode = 'gray'
tlx = None
tly = None
brx = None
bry = None
units = "mm"
output = ''
dest = []
email_from = ''
email_to = []
email_subject = 'hp-scan from %s' % socket.gethostname()
email_note = ''
resize = 100
brightness = 0
set_brightness = False
color_dropout_red = 0
set_color_dropout = False
color_dropout_green = 0
color_dropout_blue = 0
color_range_value = 0
edge_erase = False
edge_erase_value = 0
contrast = 0
set_contrast = False

page_size = ''
size_desc = ''
page_units = 'mm'
default_res = 300
scanner_compression = 'JPEG'
adf = False
duplex = False
dest_printer = None
dest_devUri = None
uiscan = False
#if con_device == 5000 or con_device == 7500:
sharpness = 0
set_sharpness = False
color_value = 0
set_color_value = False
barcode_found = 0
barcode_data = list()
barcode_count =0
barcode_first_occurence = True
barcode_first_page = False
save_file = ''
output_path = os.getcwd()
ext = ".png"
multipick = False
blank_page = False
isBlankPage = False
auto_orient = False
crushed = False
bg_color_removal = False
punchhole_removal = False
auto_crop = False
deskew_image = False
lineart_mode = False
document_merge = False
mixed_feed = False
back_side = False
batchsepBC = False
batchsepBP = False
barcode = False
merge_ADF_Flatbed = False
temp_list = []
blankpage_found = 0
bp_no = 0
pyPlatform = 0
blankpage_data = list()
blankpage_count =0
blankpage_first_occurence = True
blankpage_first_page = False
orient = 0
orient_list = []
multipick_error_message = "The scan operation has been cancelled or a multipick or paper is jammed in the ADF.\nIf you cancelled the scan,click OK.\nIf the scan was terminated due to a multi-feed or paper jam in the ADF,\ndo the following:\n\n1)Clear the ADF path. For instructions see your product documentation.\n2)Check the sheets are not stuck together. Remove any staples, sticky notes,tape or other objects.\n3)Restart the scan\n\nNote:If necessary, turn off automatic detection of multi-pick before starting a new scan\n"
SANE_STATUS_MULTIPICK=12
SANE_STATUS_JAMMED=6
MAX_EDGE_ERASE_VALUE_INCH=1
ProcessBW = False

PAGE_SIZES = { # in mm
    '5x7' : (127, 178, "5x7 photo", 'mm'),
    '4x6' : (102, 152, "4x6 photo", 'mm'),
    '3x5' : (76, 127, "3x5 index card", 'mm'),
    'a2_env' : (111, 146, "A2 Envelope", 'mm'),
    'a3' : (297, 420, "A3", 'mm'),
    "a4" : (210, 297, "A4", 'mm'),
    "a5" : (148, 210, "A5", 'mm'),
    "a6" : (105, 148, "A6", 'mm'),
    "b4" : (257, 364, "B4", 'mm'),
    "b5" : (182, 257, "B5", 'mm'),
    "c6_env" : (114, 162, "C6 Envelope", 'mm'),
    "dl_env" : (110, 220, "DL Envelope", 'mm'),
    "exec" : (184, 267, "Executive", 'mm'),
    "flsa" : (216, 330, "Flsa", 'mm'),
    "higaki" : (100, 148, "Hagaki", 'mm'),
    "japan_env_3" : (120, 235, "Japanese Envelope #3", 'mm'),
    "japan_env_4" : (90, 205, "Japanese Envelope #4", 'mm'),
    "legal" : (215, 356, "Legal", 'mm'),
    "letter" : (215, 279, "Letter", 'mm'),
    "no_10_env" : (105, 241, "Number 10 Envelope", 'mm'),
    "oufufu-hagaki" : (148, 200, "Oufuku-Hagaki", 'mm'),
    "photo" : (102, 152, "Photo", 'mm'),
    "super_b" : (330, 483, "Super B", 'mm'),
    }

def createPagesFile(adf_page_files,pages_file,file_type='.png'):
    #print ("called create page files")
    #print (adf_page_files)
    if not 'hpscan' in pages_file:
        pages_file=pages_file+'_'
    output = utils.createBBSequencedFilename(pages_file, file_type, output_path)

    if file_type == '.pdf':
        if len(adf_page_files):
            try:      
                output = imageprocessing.generatePdfFile(adf_page_files,output)
            except ImportError:
                try:
                    output = imageprocessing.generatePdfFile_canvas(adf_page_files,output,orient_list,brx,bry,tlx,tly,output_path)
                except ImportError as error:
                    if error.message.split(' ')[-1] == 'PIL':
                        log.error("PDF output requires PIL.")
                    else:
                        log.error("PDF output requires ReportLab.")
                    sys.exit(1)				
            temp_list.append(output)
            #print temp_list
            #imageprocessing.merge_PDF_viewer(output)
            #cmd = "%s %s &" % (pdf_viewer, output)               
            #os_utils.execute(cmd)
    elif file_type == '.tiff':
         file_name = ''
         #print "entered tiff"
         #print adf_page_files
         for p in adf_page_files:           
             file_name = file_name + " " + p
             cmd = "convert %s %s" %(file_name,output)
             status = utils.run(cmd)
             #print ("***********************")
             #print (status[0])
             #print (status[1])
             if status[0] == -1:
                 #print ("entered status -1")  
                 log.error("Convert command not found.")
                 sys.exit(6)
         #print adf_page_files
         for p in adf_page_files:
             os.remove(p)
         #temp_list.append(output)
    else:
        for p in adf_page_files:
            im = Image.open(p)
            output = utils.createBBSequencedFilename(pages_file, file_type, output_path)
            try:
                im.save(output,compress_level=1,quality=55)
            except:
                im = im.convert("RGB")
                im.save(output,compress_level=1,quality=55)
            os.unlink(p)

try:
    viewer = ''
    viewer_list = ['kview', 'display', 'gwenview', 'eog', 'kuickshow',]
    for v in viewer_list:
        vv = utils.which(v)
        if vv:
            viewer = os.path.join(vv, v)
            break


    editor = ''
    editor_list = ['kolourpaint', 'gimp', 'krita', 'cinepaint', 'mirage',]
    for e in editor_list:
        ee = utils.which(e)
        if ee:
            editor = os.path.join(ee, e)
            break

    pdf_viewer = ''
    pdf_viewer_list = ['kpdf', 'acroread', 'xpdf', 'evince', 'xdg-open']
    for v in pdf_viewer_list:
        vv = utils.which(v)
        if vv:
            pdf_viewer = os.path.join(vv, v)
            break

    mod = module.Module(__mod__, __title__, __version__, __doc__, None,
                        (INTERACTIVE_MODE,))

    
    extra_options=[utils.USAGE_SPACE,
        ("[OPTIONS] (General)", "", "header", False),
        ("Scan destinations:", "-s<dest_list> or --dest=<dest_list>", "option", False),
        ("", "where <dest_list> is a comma separated list containing one or more of: 'file', ", "option", False),
        ("", "'viewer', 'editor', 'pdf', or 'print'. Use only commas between values, no spaces.", "option", False),
        ("Scan mode:", "-m<mode> or --mode=<mode>. Where <mode> is 'gray', 'color' or 'lineart'.", "option", False),
        ("Scanning resolution:", "-r<resolution_in_dpi> or --res=<resolution_in_dpi> or --resolution=<resolution_in_dpi>", "option", False),
        ("", "where 300 is default.", "option", False),
        ("Image resize:", "--resize=<scale_in_%> (min=1%, max=400%, default=100%)", "option", False),
        ("Color Dropout Red :", "-color_dropout_red_value=<color_dropout_red_value> or --color_dropout_red_value=<color_dropout_red_value>", "option", False),
        ("Color Dropout Green :", "-color_dropout_green_value=<color_dropout_green_value> or --color_dropout_green_value=<color_dropout_green_value>", "option", False),
        ("Color Dropout Blue :", "-color_dropout_blue_value=<color_dropout_blue_value> or --color_dropout_blue_value=<color_dropout_blue_value>", "option", False),
        ("Color Dropout Range :", "-color_range=<color_range> or --color_range=<color_range>", "option", False),
        ("Image contrast:", "-c=<contrast> or --contrast=<contrast>", "option", False),
        ("", "The contrast range varies from device to device.", "option", False),
        ("Image brightness:", "-b=<brightness> or --brightness=<brightness>", "option", False),
        ("", "The brightness range varies from device to device.", "option", False),
        ("ADF mode:", "--adf (Note, only PDF output is supported when using the ADF)", "option", False),
        ("", "--duplex or --dup for duplex scanning using ADF.", "option", False),
        utils.USAGE_SPACE,
        ("[OPTIONS] (Scan area)", "", "header", False),
        ("Specify the units for area/box measurements:", "-t<units> or --units=<units>", "option", False),
        ("", "where <units> is 'mm', 'cm', 'in', 'px', or 'pt' ('mm' is default).", "option", False),
        ("Scan area:", "-a<tlx>,<tly>,<brx>,<bry> or --area=<tlx>,<tly>,<brx>,<bry>", "option", False),
        ("", "Coordinates are relative to the upper left corner of the scan area.", "option", False),
        ("", "Units for tlx, tly, brx, and bry are specified by -t/--units (default is 'mm').", "option", False),
        ("", "Use only commas between values, no spaces.", "option", False),
        ("Scan box:", "--box=<tlx>,<tly>,<width>,<height>", "option", False),
        ("", "tlx and tly coordinates are relative to the upper left corner of the scan area.", "option", False),
        ("", "Units for tlx, tly, width, and height are specified by -t/--units (default is 'mm').", "option", False),
        ("", "Use only commas between values, no spaces.", "option", False),
        ("Top left x of the scan area:", "--tlx=<tlx>", "option", False),
        ("", "Coordinates are relative to the upper left corner of the scan area.", "option", False),
        ("", "Units are specified by -t/--units (default is 'mm').", "option", False),
        ("Top left y of the scan area:", "--tly=<tly>", "option", False),
        ("", "Coordinates are relative to the upper left corner of the scan area.", "option", False),
        ("", "Units are specified by -t/--units (default is 'mm').", "option", False),
        ("Bottom right x of the scan area:", "--brx=<brx>", "option", False),
        ("", "Coordinates are relative to the upper left corner of the scan area.", "option", False),
        ("", "Units are specified by -t/--units (default is 'mm').", "option", False),
        ("Bottom right y   of the scan area:", "--bry=<bry>", "option", False),
        ("", "Coordinates are relative to the upper left corner of the scan area.", "option", False),
        ("", "Units are specified by -t/--units (default is 'mm').", "option", False),
        ("Specify the scan area based on a paper size:", "--size=<paper size name>", "option", False),
        ("", "where <paper size name> is one of: %s" % ', '.join(list(PAGE_SIZES.keys())), "option", False),
        ("Crop out edges from the scan area:", "--edge_erase_value=<border crop value in inch>", "option", False),
        ("", "where <border crop value in inch> is in range of: [0-1]inch", "option", False),
        utils.USAGE_SPACE,
        ("[OPTIONS] ('file' dest)", "", "header", False),
        ("Filename for 'file' destination:", "-o<file> or -f<file> or --file=<file> or --output=<file>", "option", False),
        #("Destination:", "--path=<destination>", "option", False),
        utils.USAGE_SPACE,
        ("[OPTIONS] ('pdf' dest)", "", "header", False),
        ("PDF viewer application:", "--pdf=<pdf_viewer>", "option", False),
        utils.USAGE_SPACE,
        ("[OPTIONS] ('viewer' dest)", "", "header", False),
        ("Image viewer application:", "-v<viewer> or --viewer=<viewer>", "option", False),
        utils.USAGE_SPACE,
        ("[OPTIONS] ('editor' dest)", "", "header", False),
        ("Image editor application:", "-e<editor> or --editor=<editor>", "option", False),
        utils.USAGE_SPACE,
        ("[OPTIONS] ('email' dest)", "", "header", False),
        ("From: address for 'email' dest:", "--email-from=<email_from_address> (required for 'email' dest.)", "option", False),
        ("To: address for 'email' dest:", "--email-to=<email__to_address> (required for 'email' dest.)", "option", False),
        ("Email subject for 'email' dest:", '--email-subject="<subject>" or --subject="<subject>"', "option", False),
        ("", 'Use double quotes (") around the subject if it contains space characters.', "option", False),
        ("Note or message for the 'email' dest:", '--email-msg="<msg>" or --email-note="<note>"', "option", False),
        ("", 'Use double quotes (") around the note/message if it contains space characters.', "option", False),
        utils.USAGE_SPACE,
        ("[OPTIONS] ('printer' dest)", "", "header", False),
        ("Printer queue/printer dest:", "--dp=<printer_name> or --dest-printer=<printer_name>", "option", False),
        ("Printer device-URI dest:", "--dd=<device-uri> or --dest-device=<device-uri>", "option", False),
        utils.USAGE_SPACE,
        ("[OPTIONS] (advanced)", "", "header", False),
        ("Set the scanner compression mode:", "-x<mode> or --compression=<mode>, <mode>='raw', 'none' or 'jpeg' ('jpeg' is default) ('raw' and 'none' are equivalent)", "option", False),]

    
    scan_parseStdOpts = ['dest=', 'mode=', 'res=', 'resolution=',
                          'resize=', 'adf', 'duplex', 'dup', 'unit=',
                          'units=', 'area=', 'box=', 'tlx=',
                          'tly=', 'brx=', 'bry=', 'size=',
                          'file=', 'output=', 'pdf=', 'viewer=',
                          'email-from=', 'from=', 'email-to=',
                          'to=', 'email-msg=', 'msg=',
                          'printer=', 'compression=' , 'raw',
                          'jpeg', 'color', 'lineart', 'colour',
                          'bw', 'gray', 'grayscale', 'grey',
                          'greyscale', 'email-subject=',
                          'subject=', 'to=', 'from=', 'jpg',
                          'grey-scale', 'gray-scale', 'about=',
                          'editor=', 'dp=', 'dest-printer=', 'dd=',
                          'dest-device=', 'brightness=', 'contrast=','filetype=',
                            'path=', 'uiscan', 'sharpness=',
                            'color_dropout_red_value=','color_dropout_green_value=','color_dropout_blue_value=','color_range=',
                              'color_value=','multipick','autoorient','blankpage',
                              'batchsepBP','mixedfeed', 'crushed', 'bg_color_removal',
                              'punchhole_removal','docmerge','adf_flatbed_merge',
                              'batchsepBC','deskew','autocrop','backside','edge_erase_value=']

    mod.setUsage(module.USAGE_FLAG_DEVICE_ARGS, extra_options, see_also_list=[])
    opts, device_uri, printer_name, mode, ui_toolkit, lang = \
        mod.parseStdOpts('s:m:r:c:t:a:b:o:v:f:c:x:e:', scan_parseStdOpts)

    '''
    #If the call was made from uiscan then pass device uri in argument
    #otherwise for command line pass device URI from commandline
    # device URI can be obtained by hp-makeuri command
    '''
    if(not device_uri):
        sane.init()
        sane_devices = sane.getDevices()
        devicelist = {}
        for d, mfg, mdl, t in sane_devices:
            try:
                devicelist[d]
            except KeyError:
                devicelist[d] = [mdl]
            else:
                devicelist[d].append(mdl)
        sane.deInit()

        #print devicelist
        #print "near getdevice uri"
        device_uri = mod.getDeviceUri(device_uri, printer_name,
            back_end_filter=['hpaio'], filter={'scan-type': (operator.gt, 0)}, devices=devicelist)
        #print device_uri
    
    if not device_uri:
        log.error("empty device URI found!")
        sys.exit(1)

    for o, a in opts:
        if o in ('-x', '--compression'):
            a = a.strip().lower()

            if a in ('jpeg', 'jpg'):
                scanner_compression = 'JPEG'

            elif a in ('raw', 'none'):
                scanner_compression = 'None'

            else:
                log.error("Invalid compression value. Valid values are 'jpeg', 'raw', and 'none'.")
                log.error("Using default value of 'jpeg'.")
                scanner_compression = 'JPEG'

        elif o == '--filetype':
            #a=a.strp().lower()
            #print (a)
            if a == 'png':
                save_file = 'png'
                ext = ".png"
            elif a == 'jpg':
                save_file = 'jpg'
                ext = ".jpg"
            elif a == 'pdf':
                save_file = 'pdf'
                ext = ".pdf"
            elif a == 'tiff':
                save_file = 'tiff'
                ext = '.tiff'
            elif a == 'bmp':
                save_file = 'bmp'
                ext = '.bmp'
            else:
                save_file = 'png'
                ext = ".png"
        
        elif o == '--path':
            output_path = a
        
        elif o == 'raw':
            scanner_compression = 'None'

        elif o == 'jpeg':
            scanner_compression = 'JPEG'

        elif o in ('--color', '--colour'):
            scan_mode = 'color'

        elif o in ('--lineart', '--line-art', '--bw'):
            scan_mode = 'lineart'

        elif o in ('--gray', '--grayscale', '--gray-scale', '--grey', '--greyscale', '--grey-scale'):
            scan_mode = 'gray'

        elif o in ('-m', '--mode'):
            a = a.strip().lower()

            if a in ('color', 'colour'):
                scan_mode = 'color'

            elif a in ('lineart', 'bw', 'b&w'):
                if (re.search(r'_7500', device_uri)):
                    log.error("lineart mode is not supported for this device.")
                    sys.exit(1)
                scan_mode = 'lineart'

            elif a in ('gray', 'grayscale', 'grey', 'greyscale'):
                scan_mode = 'gray'

            elif a in ('BlackAndWhite','blackandwhite'):
                scan_mode = "gray"
                ProcessBW = True


            else:
                log.error("Invalid mode. Using default of 'gray'.")
                log.error("Valid modes are 'color', 'lineart', or 'gray'.")
                scan_mode = 'gray'

        elif o in ('--res', '--resolution', '-r'):
            try:
                r = int(a.strip())
            except ValueError:
                log.error("Invalid value for resolution.")
                res = default_res
            else:
                res = r

        elif o in ('-t', '--units', '--unit'):
            a = a.strip().lower()

            if a in ('in', 'inch', 'inches'):
                units = 'in'

            elif a in ('mm', 'milimeter', 'milimeters', 'millimetre', 'millimetres'):
                units = 'mm'

            elif a in ('cm', 'centimeter', 'centimeters', 'centimetre', 'centimetres'):
                units = 'cm'

            elif a in ('px', 'pixel', 'pixels', 'pel', 'pels'):
                units = 'px'

            elif a in ('pt', 'point', 'points', 'pts'):
                units = 'pt'

            else:
                log.error("Invalid units. Using default of 'mm'.")
                units = 'mm'

        elif o == '--tlx':
            a = a.strip().lower()
            try:
                f = float(a)
            except ValueError:
                log.error("Invalid value for tlx.")
            else:
                tlx = f

        elif o == '--tly':
            a = a.strip().lower()
            try:
                f = float(a)
            except ValueError:
                log.error("Invalid value for tly.")
            else:
                tly = f

        elif o == '--brx':
            a = a.strip().lower()
            try:
                f = float(a)
            except ValueError:
                log.error("Invalid value for brx.")
            else:
                brx = f

        elif o == '--bry':
            a = a.strip().lower()
            try:
                f = float(a)
            except ValueError:
                log.error("Invalid value for bry.")
            else:
                bry = f

        elif o in ('-a', '--area'): # tlx, tly, brx, bry
            a = a.strip().lower()
            try:
                tlx, tly, brx, bry = a.split(',')[:4]
            except ValueError:
                log.error("Invalid scan area. Using defaults.")
            else:
                try:
                    tlx = float(tlx)
                except ValueError:
                    log.error("Invalid value for tlx. Using defaults.")
                    tlx = None

                try:
                    tly = float(tly)
                except ValueError:
                    log.error("Invalid value for tly. Using defaults.")
                    tly = None

                try:
                    brx = float(brx)
                except ValueError:
                    log.error("Invalid value for brx. Using defaults.")
                    brx = None

                try:
                    bry = float(bry)
                except ValueError:
                    log.error("Invalid value for bry. Using defaults.")
                    bry = None

        elif o == '--box': # tlx, tly, w, h
            a = a.strip().lower()
            try:
                tlx, tly, width, height = a.split(',')[:4]
            except ValueError:
                log.error("Invalid scan area. Using defaults.")
            else:
                try:
                    tlx = float(tlx)
                except ValueError:
                    log.error("Invalid value for tlx. Using defaults.")
                    tlx = None

                try:
                    tly = float(tly)
                except ValueError:
                    log.error("Invalid value for tly. Using defaults.")
                    tly = None

                if tlx is not None:
                    try:
                        brx = float(width) + tlx
                    except ValueError:
                        log.error("Invalid value for width. Using defaults.")
                        brx = None
                else:
                    log.error("Cannot calculate brx since tlx is invalid. Using defaults.")
                    brx = None

                if tly is not None:
                    try:
                        bry = float(height) + tly
                    except ValueError:
                        log.error("Invalid value for height. Using defaults.")
                        bry = None
                else:
                    log.error("Cannot calculate bry since tly is invalid. Using defaults.")
                    bry = None

        elif o == '--size':
            size = a.strip().lower()
            if size in PAGE_SIZES:
                brx, bry, size_desc, page_units = PAGE_SIZES[size]
                tlx, tly = 0, 0
                page_size = size
            else:
                log.error("Invalid page size. Valid page sizes are: %s" % ', '.join(list(PAGE_SIZES.keys())))
                log.error("Using defaults.")

        elif o in ('-o', '--output', '-f', '--file'):
            output = os.path.abspath(os.path.normpath(os.path.expanduser(a.strip())))

            try:
                ext = os.path.splitext(output)[1]
            except IndexError:
                log.error("Invalid filename extension.")
                output = ''
                if 'file' in dest:
                    dest.remove('file')
            else:
                if ext.lower() not in ('.jpg', '.png', '.pdf'):
                    log.error("Only JPG (.jpg), PNG (.png) and PDF (.pdf) output files are supported.")
                    output = ''
                    if 'file' in dest:
                        dest.remove('file')
                else:
                    if os.path.exists(output):
                        log.warn("Output file '%s' exists. File will be overwritten." % output)

                    if 'file' not in dest:
                        dest.append('file')

        elif o in ('-s', '--dest', '--destination'):
            a = a.strip().lower().split(',')
            for aa in a:
                aa = aa.strip()
                if aa in ('file', 'viewer', 'editor', 'print', 'email', 'pdf') \
                    and aa not in dest:
                    dest.append(aa)

        elif o in ('--dd', '--dest-device'):
            dest_devUri = a.strip()
            if 'print' not in dest:
                dest.append('print')

        elif o in ('--dp', '--dest-printer'):
            dest_printer = a.strip()
            if 'print' not in dest:
                dest.append('print')

        elif o in ('-v', '--viewer'):
            a = a.strip()
            b = utils.which(a)
            if not b:
                log.error("Viewer application not found.")
            else:
                viewer = os.path.join(b, a)
                if 'viewer' not in dest:
                    dest.append('viewer')

        elif o in ('-e', '--editor'):
            a = a.strip()
            b = utils.which(a)
            if not b:
                log.error("Editor application not found.")
            else:
                editor = os.path.join(b, a)
                if 'editor' not in dest:
                    dest.append('editor')

        elif o == '--pdf':
            a = a.strip()
            b = utils.which(a)
            if not b:
                log.error("PDF viewer application not found.")
            else:
                pdf_viewer = os.path.join(b, a)
                if 'pdf' not in dest:
                    dest.append('pdf')


        elif o in ('--email-to', '--to'):
            email_to = a.split(',')
            if 'email' not in dest:
                dest.append('email')

        elif o in ('--email-from', '--from'):
            email_from = a
            if 'email' not in dest:
                dest.append('email')

        elif o in ('--email-subject', '--subject', '--about'):
            email_subject = a
            if 'email' not in dest:
                dest.append('email')

        elif o in ('--email-note', '--email-msg', '--msg', '--message', '--note', '--notes'):
            email_note = a
            if 'email' not in dest:
                dest.append('email')

        elif o == '--resize':
            a = a.replace("%", "")
            try:
                resize = int(a)
            except ValueError:
                resize = 100
                log.error("Invalid resize value. Using default of 100%.")
        elif o in ('-color_dropout_red_value', '--color_dropout_red_value'):
            try:
                set_color_dropout = True
                color_dropout_red = int(a)
            except ValueError:
                log.error("Invalid color dropout value. Using default 0 .")
                color_dropout_red = 0
        elif o in ('-color_dropout_green_value', '--color_dropout_green_value'):
            try:
                set_color_dropout = True
                color_dropout_green = int(a)
            except ValueError:
                log.error("Invalid color dropout value. Using default 0 .")
                color_dropout_green = 0
        elif o in ('-color_dropout_blue_value', '--color_dropout_blue_value'):
            try:
                set_color_dropout = True
                color_dropout_blue = int(a)
            except ValueError:
                log.error("Invalid color dropout value. Using default of [0:0:0] .")
                color_dropout_blue = 0
        elif o in ('-color_range', '--color_range'):
            try:
                set_color_dropout = True
                color_range_value = int(a)
            except ValueError:
                log.error("Invalid color dropout value. Using default of [0:0:0] .")
                color_range_value = 49
        elif o in ('-edge_erase_value', '--edge_erase_value'):
            try:
                edge_erase = True
                edge_erase_value = float(a)
                if edge_erase_value > MAX_EDGE_ERASE_VALUE_INCH:
                    log.error("Invalid edge erase value. Setting Max Value of  %f" %MAX_EDGE_ERASE_VALUE_INCH)
                    edge_erase_value = MAX_EDGE_ERASE_VALUE_INCH 
                if edge_erase_value < 0:
                    log.error("Invalid edge erase value. Setting Max Value of  %d" %0)
                    edge_erase_value = 0
            except ValueError:
                log.error("Invalid edge erase value. Using default of 0.")
                edge_erase_value = 0
        elif o in ('-b', '--brightness'):
            try:
                set_brightness = True
                brightness = float(a.strip())
            except ValueError:
                log.error("Invalid brightness value. Using default of 0.")
                brightness = 0

        elif o in ('-c', '--contrast'):
            try:
                set_contrast = True
                contrast = float(a.strip())
            except ValueError:
                log.error("Invalid contrast value. Using default of 0.")
                contrast = 0
                
        elif o in ('--sharpness'):
            try:
                set_sharpness = True
                #contrast = int(a.strip())
                sharpness = float(a.strip())
                #print sharpness
            except ValueError:
                log.error("Invalid sharpness value. Using default of 0.")
                sharpness = 0
                
        elif o in ('--color_value'):
            try:
                set_color_value = True
                #contrast = int(a.strip())
                color_value = float(a.strip())
                #print color_value
            except ValueError:
                log.error("Invalid color_value. Using default of 0.")
                color_value = 0

        elif o == '--adf':
            adf = True
            if uiscan == False:
                output_type = 'pdf'
        elif o in ('--dup', '--duplex'):
            duplex = True
            adf = True
            if uiscan == False:
                output_type = 'pdf'
        elif o == '--blankpage':
            try:
                blank_page = True		
            except ValueError:
                log.error("Invalid Option.Using default of False")
                blank_page = False
        elif o == '--multipick':
            try:
                multipick = True
                #scanext.setMultipick(multipick)	
            except ValueError:
                log.error("Invalid Option.Using default of False")
                multipick = False
        elif o == '--autocrop':
            try:
                auto_crop = True	
            except ValueError:
                log.error("Invalid Option.Using default of False")
                auto_crop = False
        elif o == '--deskew':
            try:
                deskew_image = True		
            except ValueError:
                log.error("Invalid Option.Using default of False")
                deskew_image = False
        elif o == '--autoorient':
            #print o
            try:
                auto_orient = True                
            except ValueError:
                log.error("Invalid Option.Using default of False")
                auto_orient = False
        elif o == '--crushed':
            #print o
            try:
                crushed = True                
            except ValueError:
                log.error("Invalid Option.Using default of False")
                crushed = False
        elif o == '--bg_color_removal':
            #print o
            try:
                bg_color_removal = True                
            except ValueError:
                log.error("Invalid Option.Using default of False")
                bg_color_removal = False

        elif o == '--punchhole_removal':
            #print o
            try:
                punchhole_removal = True                
            except ValueError:
                log.error("Invalid Option.Using default of False")
                punchhole_removal = False
        elif o == '--mixedfeed':
            try:
                mixed_feed = True
            except ValueError:
                log.error("Invalid Option.Using default of False")
                mixed_feed = False
        elif o == '--backside':
            try:
                back_side = True
                duplex = True
            except ValueError:
                log.error("Invalid Option.Using default of False")
                back_side = False
        elif o == '--docmerge':
            try:
                document_merge = True                
            except ValueError:
                log.error("Invalid Option.Using default of False")
                document_merge = False
        elif o == '--adf_flatbed_merge':
            try:
                merge_ADF_Flatbed = True                
            except ValueError:
                log.error("Invalid Option.Using default of False")
                merge_ADF_Flatbed = False					
        elif o == '--batchsepBC':
            try:
                batchsepBC = True
            except ValueError:
                log.error("Invalid Option.Using default of False")
                batchsepBC = False
        elif o == '--batchsepBP':
            try:
                batchsepBP = True
            except ValueError:
                log.error("Invalid Option.Using default of False")
                batchsepBP = False
        elif o == '--uiscan':
            try:
                uiscan = True	
            except ValueError:
                log.error("Invalid Option.Using default of False")
                uiscan = False

    if not dest:
        if uiscan == False:
            log.warn("No destinations specified. Adding 'file' destination by default.")
        dest.append('file')

    if 'email' in dest and (not email_from or not email_to):
        log.error("Email specified, but email to and/or email from address(es) were not specified.")
        log.error("Disabling 'email' destination.")
        dest.remove("email")

    if page_size:
        units = 'mm'

    if units == 'in':
        if tlx is not None: tlx = tlx * 25.4
        if tly is not None: tly = tly * 25.4
        if brx is not None: brx = brx * 25.4
        if bry is not None: bry = bry * 25.4

    elif units == 'cm':
        if tlx is not None: tlx = tlx * 10.0
        if tly is not None: tly = tly * 10.0
        if brx is not None: brx = brx * 10.0
        if bry is not None: bry = bry * 10.0

    elif units == 'pt':
        if tlx is not None: tlx = tlx * 0.3528
        if tly is not None: tly = tly * 0.3528
        if brx is not None: brx = brx * 0.3528
        if bry is not None: bry = bry * 0.3528

    elif units == 'px':
        log.warn("Units set to pixels. Using resolution of %ddpi for area calculations." % res)
        if tlx is not None: tlx = tlx / res * 25.4
        if tly is not None: tly = tly / res * 25.4
        if brx is not None: brx = brx / res * 25.4
        if bry is not None: bry = bry / res * 25.4

    if tlx is not None and brx is not None and tlx >= brx:
        log.error("Invalid values for tlx (%d) and brx (%d) (tlx>=brx). Using defaults." % (tlx, brx))
        tlx = brx = None

    if tly is not None and bry is not None and tly >= bry:
        log.error("Invalid values for tly (%d) and bry (%d) (tly>=bry). Using defaults." % (tly, bry))
        tly = bry = None

    if not prop.scan_build:
        log.error("Scanning disabled in build. Exiting")
        sys.exit(1)

    if mode == GUI_MODE:
        log.error("GUI mode is not implemented yet. Refer to 'hp-scan -h' for help.")
        sys.exit(1)


    else: # INTERACTIVE_MODE
        from base.sixext.moves import queue

        try:
            import subprocess
        except ImportError:
            # Pre-2.4 Python
            from base import subproc as subprocess

        try:
            from PIL import Image
        except ImportError:
            log.error("%s requires the Python Imaging Library (PIL). Exiting." % __mod__)
            if PY3:          # Workaround due to incomplete Python3 support in Linux distros.
                log.notice(log.bold("Manually install the PIL package. More information is available at http://hplipopensource.com/node/369"))
            sys.exit(1)

        sane.init()
		# Commenting redundant getDevices() call since device list are already fetched in the beginning
        #devices = sane.getDevices()

        # Make sure SANE backend sees the device...
        #for d, mfg, mdl, t in devices:
        #    if d == device_uri:
        #        break
        #else:
        #    log.error("Unable to locate device %s using SANE backend hpaio:. Please check HPLIP installation." % device_uri)
        #    sys.exit(1)

        if uiscan == False:
            log.info(log.bold("Using device %s" % device_uri))
            log.info("Opening connection to device...")

        try:
            device = sane.openDevice(device_uri)
        except scanext.error as e:
            if multipick and e.args[0] == SANE_STATUS_MULTIPICK:
                 log.error(multipick_error_message)
                 sys.exit(2)
            if e.args[0] == SANE_STATUS_JAMMED:
                 log.error(multipick_error_message)
                 sys.exit(7)
            sane.reportError(e.args[0])
            sys.exit(1)

        try:
            source_option = device.getOptionObj("source").constraint
            log.debug("Supported source Options: %s size=%d" % (source_option,len(source_option)))
            if source_option is None:
                log.error("Device doesn't have scanner.")
                sys.exit(1)
        except:
            log.error("Failed to get the source from device.")

        #check if device has only ADF
        if len(source_option) == 1 and 'ADF' in source_option:
             log.debug("Device has only ADF support")
             adf = True
        elif len(source_option) == 3 and ('ADF-SinglePage' in source_option) and ('ADF-MultiPage-Simplex' in source_option) and ('ADF-MultiPage-Duplex' in source_option):
             log.debug("Device has only ADF support")
             adf = True
        elif len(source_option) == 2 and ('ADF' in source_option) and ('Duplex' in source_option):
             log.debug("Device has only ADF support")
             adf = True
        if adf:
            try:
                if ('ADF' not in source_option) and ('ADF-SinglePage' not in source_option) and ('ADF-MultiPage-Simplex' not in source_option) and ('ADF-MultiPage-Duplex' not in source_option) and ('ADF Simplex' not in source_option) and ('ADF Duplex' not in source_option):
                        log.error("Failed to set ADF mode. This device doesn't support ADF.")
                        sys.exit(1)               
                else:
                    if duplex == True:
                        if 'Duplex' in source_option:
                            device.setOption("source", "Duplex")
                        elif 'ADF-MultiPage-Duplex' in source_option:
                            device.setOption("source", "ADF-MultiPage-Duplex")
                        elif 'ADF Duplex' in source_option:
                            device.setOption("source", "ADF Duplex")
                        else:
                            log.warn("Device doesn't support Duplex scanning. Continuing with Simplex ADF scan.")
                            if 'ADF-SinglePage' in source_option:
                                device.setOption("source", "ADF-SinglePage")
                            elif 'ADF-MultiPage-Simplex' in source_option:
                                device.setOption("source", "ADF-MultiPage-Simplex")
                            else:
                                device.setOption("source", "ADF")
                    else:
                        if 'ADF-SinglePage' in source_option:
                            device.setOption("source", "ADF-SinglePage")
                        elif 'ADF-MultiPage-Simplex' in source_option:
                            device.setOption("source", "ADF-MultiPage-Simplex")
                        elif 'ADF Simplex' in source_option:
                            device.setOption("source", "ADF Simplex")
                        else:
                            device.setOption("source", "ADF")
                    device.setOption("batch-scan", True)
            except scanext.error:
                log.error("Error in setting ADF mode Duplex=%d." % duplex)
                sys.exit(1)

        else:
            try:
                device.setOption("source", "Flatbed")
                device.setOption("batch-scan", False)
            except scanext.error:
                log.debug("Error setting source or batch-scan option (this is probably OK).")

        if multipick and (not re.search(r'_2000_s2', device_uri)) : 
            MPICK = 1
            device.setOption("multi-pick", int(MPICK))
        else: 
            MPICK = 0
            device.setOption("multi-pick", int(MPICK))

        tlx = device.getOptionObj('tl-x').limitAndSet(tlx)
        tly = device.getOptionObj('tl-y').limitAndSet(tly)
        brx = device.getOptionObj('br-x').limitAndSet(brx)
        bry = device.getOptionObj('br-y').limitAndSet(bry)

        scan_area = (brx - tlx) * (bry - tly) # mm^2

        valid_res = device.getOptionObj('resolution').constraint
        log.debug("Device supported resolutions %s" % (valid_res,))
        if 0 in valid_res: #min-max range in tuple
           if res < valid_res[0] or res > valid_res[1]:
             log.warn("Invalid resolution. Using closest valid resolution of %d dpi" % res)
           if res < valid_res[0]:
              res = valid_res[0]
           elif res > valid_res[1]:
              res = valid_res[1]

        else:
          if res not in valid_res:
            log.warn("Invalid resolution. Using closest valid resolution of %d dpi" % res)
            log.warn("Valid resolutions are %s dpi." % ', '.join([str(x) for x in valid_res]))
            res = valid_res[0]
            min_dist = sys.maxsize
            for x in valid_res:
                  if abs(r-x) < min_dist:
                        min_dist = abs(r-x)
                        res = x

        res = device.getOptionObj('resolution').limitAndSet(res)
        scan_px = scan_area * res * res / 645.16 # res is in DPI

        if scan_mode == 'color':
            scan_size = scan_px * 3 # 3 bytes/px
        elif scan_mode == 'gray':
            scan_size = scan_px # 1 byte/px
        else: # lineart
            scan_size = scan_px // 8 

        if scan_size > 52428800: # 50MB
            if res > 600:
                log.warn("Using resolutions greater than 600 dpi will cause very large files to be created.")
            else:
                log.warn("The scan current parameters will cause very large files to be created.")

            log.warn("This can cause the scan to take a long time to complete and may cause your system to slow down.")
            log.warn("Approx. number of bytes to read from scanner: %s" % utils.format_bytes(scan_size, True))

        device.setOption('compression', scanner_compression)

        if uiscan == False and set_contrast:
            contrast = int(contrast)
            try:
                valid_contrast = device.getOptionObj('contrast').constraint
                if contrast >= int(valid_contrast[0]) and contrast <= int(valid_contrast[1]):
                    contrast = device.getOptionObj('contrast').limitAndSet(contrast)
                else:
                    log.warn("Invalid contrast. Contrast range is (%d, %d). Using closest valid contrast of %d " % (int(valid_contrast[0]), int(valid_contrast[1]), contrast))
                    if contrast < int(valid_contrast[0]):
                        contrast = int(valid_contrast[0])
                    elif contrast > int(valid_contrast[1]):
                        contrast = int(valid_contrast[1])
                device.setOption('contrast', contrast)
            except:
                log.warn("Unable to set contrast for this device. Using default of 0.")
                contrast = 0

        if uiscan == False and set_brightness:
            brightness = int(brightness)
            #print device
            try:
                valid_brightness = device.getOptionObj('brightness').constraint
                if brightness >= int(valid_brightness[0]) and brightness <= int(valid_brightness[1]):
                    brightness = device.getOptionObj('brightness').limitAndSet(brightness)
                else:
                    log.warn("Invalid brightness. Brightness range is (%d, %d). Using closest valid brightness of %d " % (int(valid_brightness[0]), int(valid_brightness[1]), brightness))
                    if brightness < int(valid_brightness[0]):
                        brightness = int(valid_brightness[0])
                    elif brightness > int(valid_brightness[1]):
                        brightness = int(valid_brightness[1])
                device.setOption('brightness', brightness)
            except:
                log.warn("Unable to set brightness for this device. Using default of 0.")
                brightness = 0
        if brx - tlx <= 0.0 or bry - tly <= 0.0:
            log.error("Invalid scan area (width or height is negative).")
            sys.exit(1)

        if uiscan == False:
            log.info("")
            log.info("Resolution: %ddpi" % res)
            log.info("Mode: %s" % scan_mode)
            log.info("Compression: %s" % scanner_compression)
        if(set_contrast):
            if uiscan == False:
                log.info("Contrast: %d" % contrast)
        if(set_brightness):
            if uiscan == False:
                log.info("Brightness: %d" % brightness)
        if units == 'mm':
            if uiscan == False:
                log.info("Scan area (mm):")
                log.info("  Top left (x,y): (%fmm, %fmm)" % (tlx, tly))
                log.info("  Bottom right (x,y): (%fmm, %fmm)" % (brx, bry))
                log.info("  Width: %fmm" % (brx - tlx))
                log.info("  Height: %fmm" % (bry - tly))

        if page_size:
            units = page_units # for display purposes only
            if uiscan == False:
                log.info("Page size: %s" % size_desc)
            if units != 'mm':
                if uiscan == False:
                    log.note("This scan area below in '%s' units may not be exact due to rounding errors." % units)

        if units == 'in':
            if uiscan == False:
                log.info("Scan area (in):")
                log.info("  Top left (x,y): (%fin, %fin)" % (tlx/25.4, tly/25.4))
                log.info("  Bottom right (x,y): (%fin, %fin)" % (brx/25.4, bry/25.4))
                log.info("  Width: %fin" % ((brx - tlx)/25.4))
                log.info("  Height: %fin" % ((bry - tly)/25.4))

        elif units == 'cm':
            if uiscan == False:
                log.info("Scan area (cm):")
                log.info("  Top left (x,y): (%fcm, %fcm)" % (tlx/10.0, tly/10.0))
                log.info("  Bottom right (x,y): (%fcm, %fcm)" % (brx/10.0, bry/10.0))
                log.info("  Width: %fcm" % ((brx - tlx)/10.0))
                log.info("  Height: %fcm" % ((bry - tly)/10.0))

        elif units == 'px':
            if uiscan == False:
                log.info("Scan area (px @ %ddpi):" % res)
                log.info("  Top left (x,y): (%fpx, %fpx)" % (tlx*res/25.4, tly*res/25.4))
                log.info("  Bottom right (x,y): (%fpx, %fpx)" % (brx*res/25.4, bry*res/25.4))
                log.info("  Width: %fpx" % ((brx - tlx)*res/25.4))
                log.info("  Height: %fpx" % ((bry - tly)*res/25.4))

        elif units == 'pt':
            if uiscan == False:
                log.info("Scan area (pt):")
                log.info("  Top left (x,y): (%fpt, %fpt)" % (tlx/0.3528, tly/0.3528))
                log.info("  Bottom right (x,y): (%fpt, %fpt)" % (brx/0.3528, bry/0.3528))
                log.info("  Width: %fpt" % ((brx - tlx)/0.3528))
                log.info("  Height: %fpt" % ((bry - tly)/0.3528))
        if uiscan == False:
            log.info("Destination(s): %s" % ', '.join(dest))

        if 'file' in dest:
            if uiscan == False:
                log.info("Output file: %s" % output)

        update_queue = queue.Queue()
        event_queue = queue.Queue()

        available_scan_mode = device.getOptionObj("mode").constraint
        available_scan_mode = [x.lower() for x in available_scan_mode]
        log.debug("Supported modes: %s size=%d" % (available_scan_mode,len(available_scan_mode)))
        if scan_mode.lower() not in available_scan_mode:
            log.warn("Device doesn't support %s mode. Continuing with %s mode."%(scan_mode,available_scan_mode[0]))
            scan_mode = available_scan_mode[0]

        if re.search(r'hp2000S1', device_uri) or re.search(r'hpgt2500', device_uri):
            if scan_mode == 'gray':
                device.setOption("mode", 'Gray')
            elif scan_mode == 'color':
                device.setOption("mode", 'Color')
            elif scan_mode == 'lineart':
                device.setOption("mode", 'Lineart')
        else:
            device.setOption("mode", scan_mode)


        #For some devices, resolution is changed when we set 'source'.
        #Hence we need to set resolution here, after setting the 'source'
        device.setOption("resolution", res)
        if uiscan == False:
            if 'file' in dest and not output:
                if uiscan == False:
                    log.warn("File destination enabled with no output file specified.")

                if adf:
                    if uiscan == False:
                        log.info("Setting output format to PDF for ADF mode.")
                    '''if merge_ADF_Flatbed == True:
                        output = utils.createSequencedFilename("hpscanMerge", ext,output_path)
                    else:'''
                    output = utils.createSequencedFilename("hpscan", ".pdf")
                    output_type = 'pdf'
                else:
                    if scan_mode == 'gray':
                        if uiscan == False:
                            log.info("Setting output format to PNG for greyscale mode.")
                        output = utils.createSequencedFilename("hpscan", ".png")
                        output_type = 'png'
                    else:
                        if uiscan == False:
                            log.info("Setting output format to JPEG for color/lineart mode.")
                        output = utils.createSequencedFilename("hpscan", ".jpg")
                        output_type = 'jpeg'
                if uiscan == False:
                    log.warn("Defaulting to '%s'." % output)
                #print (output_type)
            else:
                try:
                    output_type = os.path.splitext(output)[1].lower()[1:]
                    if output_type == 'jpg':
                        output_type = 'jpeg'
                except IndexError:
                    output_type = ''

            if output_type and output_type not in ('jpeg', 'png', 'pdf'):
                log.error("Invalid output file format. File formats must be 'jpeg', 'png' or 'pdf'.")
                sys.exit(1)

            if adf and output_type and output_type != 'pdf':
                log.error("ADF scans must be saved in PDF file format.")
                sys.exit(1)
            log.info("\nWarming up...")

        no_docs = False
        page = 1
        backpage_count = 1
        barcode_index=0
        blankpage_index=0
        adf_page_files = []
        blank_cnt=0
        page_list=[]
        cleanup_spinner()
        log.info("")
        try:
            #start=datetime.now()
            while True:
                if adf:
                    if uiscan == False:
                        log.info("\nPage %d: Scanning..." % page)
                else:
                    if uiscan == False:
                        log.info("\nScanning...")

                bytes_read = 0

                try:
                    try:
                        ok, expected_bytes, status = device.startScan("RGBA", update_queue, event_queue)
                        # Note: On some scanners (Marvell) expected_bytes will be < 0 (if lines == -1)
                        log.debug("expected_bytes = %d" % expected_bytes)
                    except scanext.error as e:
                        if adf and e.args[0] == SANE_STATUS_MULTIPICK and multipick:
                            log.error(multipick_error_message)
                            sys.exit(2)
                        if adf and (e.args[0] == SANE_STATUS_JAMMED) :
                            log.error(multipick_error_message)
                            sys.exit(7)
                        sane.reportError(e.args[0])
                        sys.exit(1)
                    except KeyboardInterrupt:
                        log.error("Aborted.")
                        device.cancelScan()
                        sys.exit(1)
                    if adf and status == scanext.SANE_STATUS_NO_DOCS:
                        if page-1 == 0:
                            if uiscan == False:
                                log.error("No document(s). Please load documents and try again.")
                            sys.exit(3)
                        else:
                            if uiscan == False:
                                log.info("Out of documents. Scanned %d pages total." % (page-1))
                            no_docs = True
                            break
                    if adf and status == SANE_STATUS_MULTIPICK:
                        if multipick:
                            log.error(multipick_error_message)
                            sys.exit(2)
                    if adf and status == SANE_STATUS_JAMMED:
                        log.error(multipick_error_message)
                        sys.exit(7)

                    if expected_bytes > 0:
                        if adf:
                            if uiscan == False:
                                log.debug("Expecting to read %s from scanner (per page)." % utils.format_bytes(expected_bytes))
                        else:
                            if uiscan == False:
                                log.debug("Expecting to read %s from scanner." % utils.format_bytes(expected_bytes))

                    device.waitForScanActive()
                    
                    if uiscan == False:
                        pm = tui.ProgressMeter("Reading data:")

                    while device.isScanActive():
                        while update_queue.qsize():
                            try:
                                status, bytes_read = update_queue.get(0)

                                if not log.is_debug():
                                    if expected_bytes > 0:
                                        if uiscan == False:
                                            pm.update(int(100*bytes_read/expected_bytes),
                                                utils.format_bytes(bytes_read))
                                    else:
                                        if uiscan == False:
                                            pm.update(0,
                                                utils.format_bytes(bytes_read))

                                if status != scanext.SANE_STATUS_GOOD:
                                    if (status == SANE_STATUS_MULTIPICK and multipick) or (status == SANE_STATUS_JAMMED):
                                        log.error("ADF_MPD multipick or Jam error %d" % (status))
                                        log.error("Error in reading data. Status=%d " % (status))
					#sys.exit(2)
					
				#device.cancelScan()		#Added by wipro
                                #sys.exit(1)

                            except queue.Empty:
                                break


                        time.sleep(0.5)

                except KeyboardInterrupt:
                    log.error("Aborted.")
                    device.cancelScan()
                    sys.exit(1)

                # Make sure queue is cleared out...
                while update_queue.qsize():
                    status, bytes_read = update_queue.get(0)

                    if not log.is_debug():
                        if expected_bytes > 0:
                            if uiscan == False:
                                pm.update(int(100*bytes_read/expected_bytes),
                                    utils.format_bytes(bytes_read))
                        else:
                            if uiscan == False:
                                pm.update(0,
                                    utils.format_bytes(bytes_read))

                # For Marvell devices, making scan progress bar to 100%
                if bytes_read and bytes_read != expected_bytes:
                     if uiscan == False:
                         pm.update(int(100),utils.format_bytes(bytes_read))
                log.info("")

                if bytes_read:
                    if uiscan == False:
                        log.info("Read %s from scanner." % utils.format_bytes(bytes_read))

                    buffer, format, format_name, pixels_per_line, \
                        lines, depth, bytes_per_line, pad_bytes, total_read, total_write = device.getScan()
                    
                    if uiscan == False:
                        log.debug("PPL=%d lines=%d depth=%d BPL=%d pad=%d total_read=%d total_write=%d" %
                        (pixels_per_line, lines, depth, bytes_per_line, pad_bytes, total_read, total_write))

                    #For Marvell devices, expected bytes is not same as total_read
                    if lines == -1 or total_read != expected_bytes:
                        lines = int(total_read / bytes_per_line)

                    if scan_mode in ('color', 'gray'):
                       try:
                           im = Image.frombuffer('RGBA', (pixels_per_line, lines), buffer.read(),
                                'raw', 'RGBA', 0, 1)
                       except ValueError:
                            log.error("Did not read enough data from scanner (I/O Error?)")
                            sys.exit(1)
                    elif scan_mode == 'lineart':
                        try:
                            pixels_per_line = bytes_per_line * 8          # Calculation of pixels_per_line for Lineart must be 8 time of bytes_per_line
                            lineart_mode = True                                              # Otherwise, scanned image will be corrupted (slanted)
                            im = Image.frombuffer('RGBA', (pixels_per_line, lines), buffer.read(),
                                'raw', 'RGBA', 0, 1).convert('L')
                        except ValueError:
                            log.error("Did not read enough data from scanner (I/O Error?)")
                            sys.exit(1)
                    if uiscan == True and back_side and backpage_count%2 != 0:
                        pass
                    else:       

                        #if blank_page:
                        isBlankPage = imageprocessing.blankpage(im,lineart_mode)
                        
                        if document_merge and duplex and blank_page:   
                            if isBlankPage:
                                if blank_cnt == 0:
                                    if page%2 != 0:
                                        blank_cnt += 1
                                        page_list.append(page)
                                else:
                                    if page-1 in page_list:
                                        blank_cnt += 1
                                    else:
                                        if page%2 != 0:
                                            blank_cnt = 1
                                            page_list[:]
                                            page_list.append(page)			  
                        if blank_page and isBlankPage:
                            if adf:
                                if batchsepBP:
                                    blankpage_found=1
                                    blankpage_count=blankpage_count+1
                                    blankpage_index=blankpage_index+1
                                    if page == 1:
                                        blankpage_first_page = True
                                if not (document_merge and duplex): 
                                    page += 1
                                    continue
                            else:
                                sys.exit(0)
                        elif isBlankPage:
                            if adf and batchsepBP:
                                blankpage_found=1
                                blankpage_count=blankpage_count+1
                                blankpage_index=blankpage_index+1
                                if page == 1:
                                    blankpage_first_page = True
                        #if crushed:
                            #im = imageprocessing.crushed(im)
                        if deskew_image and (isBlankPage == False):
                            if adf:
                                im = imageprocessing.deskew(im)
                            else:
                                #im = imageprocessing.autocrop(im)
                                im = imageprocessing.deskew(im) 
                        #if mixed_feed:
                            #im = imageprocessing.mixedfeed(im)
                        if auto_crop and (isBlankPage == False):
                            im = imageprocessing.autocrop(im)
                        if auto_orient:
                            if not isBlankPage:
                                orient = imageprocessing.orientangle(im)
                                orient_list.append(orient)                                                     
                                im = imageprocessing.autoorient(im, orient)
                            else:
                                orient_list.append(0)
                        if uiscan == True and set_brightness:
                            factor = brightness/100
                            #print factor
                            im = imageprocessing.adjust_brightness(im, factor)
                        if uiscan == True and set_contrast:
                            factor = contrast/100
                            #print factor
                            im = imageprocessing.adjust_contrast(im, factor)
                        if set_sharpness:
                            factor = sharpness/100
                            #print factor
                            im = imageprocessing.adjust_sharpness(im, factor)  
                        if set_color_value:
                            factor = color_value/100
                            #print factor
                            im = imageprocessing.adjust_color(im, factor)  
                        pyPlatform = platform.python_version()
                        num = pyPlatform.split('.')       					
                        if batchsepBC and num[0] < '3':
                            import zbar
                            scanner = zbar.ImageScanner()
                            scanner.parse_config('enable')
                            log.debug("Here in barcode detection")
			
                            bar_image = im.convert('L')

                            width, height = bar_image.size
                       
                            raw_bar = bar_image.tobytes()

                            my_stream = zbar.Image(width, height, 'Y800', raw_bar)
                            scanner.scan(my_stream)
                        
                            #if barcode and batchsep:
                            for symbol in my_stream:
                                #print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
                                if symbol.data!='':
                                    barcode_found=1
                                    barcode_data.append(symbol.data)
                                    barcode_count=barcode_count+1
                                    barcode_index=barcode_index+1
                                    if page == 1:
                                        barcode_first_page = True
                                    break;
                                else:
                                    barcode_found=0

                        if punchhole_removal:
                            im = imageprocessing.punchhole_removal(im)
                        if set_color_dropout:
                            im = imageprocessing.color_dropout(im,[color_dropout_red,color_dropout_green,color_dropout_blue],color_range_value)
                        if bg_color_removal:
                            im = imageprocessing.bg_color_removal(im)
                        if crushed:
                            im = imageprocessing.crushed(im)

                        if edge_erase:
                            edge_erase_value_px = int(res*edge_erase_value)
                            im = imageprocessing.edge_erase(im,edge_erase_value_px)
                        
                        if uiscan == True:
                            if adf:
                                if (save_file == 'pdf'):
                                    if (not (document_merge and duplex and save_file == 'pdf')) or (imageprocessing.check_pypdf2() == None):
                                        #ext = ".png"
                                        if ProcessBW:
                                            if im.mode != "L":
                                                im = im.convert("L")
                                            im = imageprocessing.convert_to_BW(im)
                                        else:
                                            im = im.convert("RGB")
                                        im = imageprocessing.resize_to_scan_area(im,PAGE_SIZES[size],res)
                                if barcode_count>0:
                                    if barcode_first_occurence == True:
                                        if barcode_first_page == False:
                                            createPagesFile(adf_page_files,'hpscan', ext)
                                        barcode_first_occurence = False
                                    else:
                                        createPagesFile(adf_page_files,barcode_data[len(barcode_data)-2], ext)                                    
                                    barcode_count=barcode_count-1
                                    del adf_page_files[:]
                                if blankpage_count>0:
                                    if blankpage_first_occurence == True:
                                        if blankpage_first_page == False:
                                            createPagesFile(adf_page_files,'hpscan', ext)
                                        blankpage_first_occurence = False
                                    else:
                                        createPagesFile(adf_page_files,"batchSep_00%d"%bp_no, ext)
                                    blankpage_count=blankpage_count-1
                                    bp_no += 1
                                    del adf_page_files[:]
                                '''if (save_file == 'pdf'):
                                    #ext = ".png"
                                    im = im.convert("RGB")'''
                                if merge_ADF_Flatbed == True and save_file == 'pdf':
                                    temp_output = utils.createSequencedFilename("hpscanMerge", ext,output_path)
                                if save_file == 'pdf': #pdf save temp file in png and generate pdf using reportlab
                                    temp_output = utils.createSequencedFilename("hpscan", '.png', output_path)
                                else:
                                    temp_output = utils.createSequencedFilename("hpscan", ext, output_path)
                                adf_page_files.append(temp_output)
                                #print "entered flatbed save"
                                '''pyPlatform = platform.python_version()
                                num = pyPlatform.split('.')
                                if num[0] >= '3':
                                    im = im.convert("RGB")'''                           
                                try:
                                    im.save(temp_output,compress_level=1,quality=55)
                                except:
                                    im = im.convert("RGB")
                                    im.save(temp_output,compress_level=1,quality=55)
                                '''if (save_file == 'pdf'):
                                    ext = ".pdf"'''        
                                if document_merge and duplex and blank_page:
                                    if blank_cnt == 2:
                                        os.unlink(adf_page_files.pop())
                                        os.unlink(adf_page_files.pop())
                                        blank_cnt = 0
                                        page_list[:]

                        elif uiscan == False:
                            if adf or output_type == 'pdf':
                                temp_output = utils.createSequencedFilename("hpscan_pg%d_" % page, ".png")
                                adf_page_files.append(temp_output)
                                im.save(temp_output,compress_level=1,quality=55)
                elif uiscan == True and status == scanext.SANE_STATUS_MULTIPICK and multipick:
                    log.error("ADF_MPD multipick error %d" % (status))
                    log.error("Error in reading data. Status=%d bytes_read=%d." % (status, bytes_read))
                    sys.exit(2)
                elif uiscan == True and (status == SANE_STATUS_JAMMED):
                    log.error("ADF_MPD multipick or Jam error %d" % (status))
                    log.error("Error in reading data. Status=%d bytes_read=%d." % (status, bytes_read))
                    sys.exit(7)
                else:
                    log.error("No data read.")
                    sys.exit(1)

                if not adf or (adf and no_docs):
                    break
                
                page += 1
                backpage_count += 1
            #print "*** Total Time Taken \n"
            #print datetime.now()-start
        finally:
            if uiscan == False:
                log.info("Closing device.")
            device.cancelScan()     
        #print "outside while"   
        #if adf or output_type == 'pdf':
        #print (output_type)
        #print(PAGE_SIZES[size])
        #Post-processing images
        if ProcessBW:
            #for BLackAndWhite scan mode call image processor to convert 
            # grayscale images to 1bit Black and white images
            
            #for Flatbad 
            if im:    
                if im.mode != "L":
                    im = im.convert("L")
                im = imageprocessing.convert_to_BW(im)
            #for ADF
            for Image_file in adf_page_files:
                image = Image.open(Image_file)
                if image.mode != "L":
                    image = image.convert("L")
                BWimage = imageprocessing.convert_to_BW(image)
                BWimage.save(Image_file)
        
        #resize the image here to the original scan area size, 
        #so that the output image size matches with the input scan area
        #for Flatbad 
        if im:    
            im = imageprocessing.resize_to_scan_area(im,PAGE_SIZES[size],res)
        #for ADF
        for Image_file in adf_page_files:
            image = Image.open(Image_file)
            resized_image = imageprocessing.resize_to_scan_area(image,PAGE_SIZES[size],res)
            resized_image.save(Image_file)

        if adf and (save_file =='jpg' or save_file == 'png' or save_file == 'tiff' or save_file == 'pdf' or save_file == 'bmp'):
            #print save_file
            #start = datetime.now()
            #print "**** Starting Save File Process\n"     
            if barcode_found == 1:
                createPagesFile(adf_page_files,barcode_data[len(barcode_data)-1], ext)
                #print "Saving File process Over\n"
                #print datetime.now()-start
                #print "\n#######################\n"
                #print temp_list
                if save_file == 'pdf':
                    if len(temp_list):
                        if uiscan == True:          
                            log.error("%s" % (temp_list))
                            sys.exit(5)
                sys.exit(0)
            if blankpage_found == 1:
                createPagesFile(adf_page_files,"batchSep_00%d"%bp_no, ext)
                #print "Saving File process Over\n"
                #print datetime.now()-start
                if save_file == 'pdf':
                    if len(temp_list):
                        if uiscan == True:
                            log.error("%s" % (temp_list))
                            sys.exit(5)
                sys.exit(0)
            if document_merge and duplex :
                #print "entered docmerge"
                #print adf_page_files
                if len(adf_page_files):
                    '''if document_merge and duplex and save_file == 'pdf':             
                        output = imageprocessing.documentmerge(adf_page_files,'.png',output_path)
                    else:'''
                    output = imageprocessing.documentmerge(adf_page_files,ext,output_path)
                    if (save_file == 'pdf'):
                        #cmd = "%s %s &" % (pdf_viewer, output)               
                        #os_utils.execute(cmd)
                        if uiscan == True:
                            log.error("%s" % (output))
                            #print "Saving File process Over\n"
                            #print datetime.now()-start
                            sys.exit(4)
                sys.exit(0)  
            elif (save_file == 'tiff'):
                if len(adf_page_files) > 1:
                    outputtiff = utils.createSequencedFilename("hpscandoc", ext,output_path)
                    #print outputtiff
                    file_name = '' 
                    for p in adf_page_files:
                        file_name = file_name + " " + p
                        cmd = "convert %s %s" %(file_name,outputtiff)
                        status = utils.run(cmd)
                        #print ("***********************")
                        #print (status[0])
                        #print (status[1])
                        if status[0] == -1: 
                            #print ("entered status -1") 
                            log.error("Convert command not found.")
                            sys.exit(6)
                    for p in adf_page_files:
                        #print p
                        os.unlink(p) 
                sys.exit(0)                
            elif (save_file == 'pdf'):        
                '''if not output:
                    if merge_ADF_Flatbed == True:
                        output = utils.createSequencedFilename("hpscanMerge", ext,output_path)
                    else:
                        output = utils.createSequencedFilename("hpscan", ext,output_path)'''
                if len(adf_page_files) > 0:
                    #print "adf page files greater than 1"
                    if merge_ADF_Flatbed == True:
                        output = utils.createSequencedFilename("hpscanMerge", ext,output_path)
                    else:
                        output = utils.createSequencedFilename("hpscandoc", ext,output_path)
                    try:
                        if mixed_feed:
                            output = imageprocessing.generatePdfFile(adf_page_files,output)
                        else:
                            output = imageprocessing.generatePdfFile_canvas(adf_page_files,output,orient_list,brx,bry,tlx,tly,output_path)
                    except:
                        try:
                            if mixed_feed:
                                output = imageprocessing.generatePdfFile_canvas(adf_page_files,output,orient_list,brx,bry,tlx,tly,output_path)                                
                            else:
                                output = imageprocessing.generatePdfFile(adf_page_files,output)
                        except ImportError as error:
                            if error.message.split(' ')[-1] == 'PIL':
                                log.error("PDF output requires PIL.")
                            else:
                                log.error("PDF output requires ReportLab.")
                            sys.exit(1)  
                if merge_ADF_Flatbed == False:
                    #cmd = "%s %s &" % (pdf_viewer, output)               
                    #os_utils.execute(cmd)
                    #imageprocessing.merge_PDF_viewer(output)
                    if len(adf_page_files):
                        if uiscan == True:
                            if output:
                                log.error("%s" % (output))
                            elif temp_output:
                                log.error("%s" % (temp_output))
                            sys.exit(4)
                #print "Saving File process Over\n"
                #print datetime.now()-start
                sys.exit(0)
            else:
                sys.exit(0)
        elif  (uiscan == False) and (adf or output_type == 'pdf'):
            try:
                from reportlab.pdfgen import canvas
            except ImportError:
                log.error("PDF output requires ReportLab.")
                sys.exit(1)

            if not output:
                output = utils.createSequencedFilename("hpscan", ".pdf")

            c = canvas.Canvas(output, (brx/0.3528, bry/0.3528))

            for p in adf_page_files:
                #log.info("Processing page %s..." % p)
                image = Image.open(p)

                try:
                    c.drawInlineImage(image, (tlx/0.3528), (tly/0.3528), ((brx-tlx)/0.3528),((bry-tly)/0.3528))
                except NameError:
                    log.error("A problem has occurred with PDF generation. This is a known bug in ReportLab. Please update your install of ReportLab to version 2.0 or greater.")
                    sys.exit(1)
                except AssertionError as e:
                    log.error(e)
                    if PY3:
                        log.note("You might be running an older version of reportlab. Please update to the latest version")
                        log.note("More information is available at http://hplipopensource.com/node/369")
                        sys.exit(1)
                except Exception as e:
                    log.error(e)
                    log.note("Try Updating to reportlab version >= 3.2")
                    sys.exit(1)

                c.showPage()
                os.unlink(p)

            log.info("Saving to file %s" % output)
            c.save()
            if uiscan == True:
                log.info("Viewing PDF file in %s" % pdf_viewer)
                cmd = "%s %s &" % (pdf_viewer, output)
                os_utils.execute(cmd)
            sys.exit(0)

        if resize != 100:
            if resize < 1 or resize > 400:
                log.error("Resize parameter is incorrect. Resize must be 0% < resize < 400%.")
                log.error("Using resize value of 100%.")
            else:
                new_w = int(pixels_per_line * resize / 100)
                new_h = int(lines * resize / 100)
                if uiscan == False:
                    log.info("Resizing image from %dx%d to %dx%d..." % (pixels_per_line, lines, new_w, new_h))
                im = im.resize((new_w, new_h), Image.ANTIALIAS)

        file_saved = False
        if 'file' in dest:
            if (save_file == 'png' or save_file == 'jpg' or save_file == 'tiff' or save_file == 'pdf' or save_file == 'bmp'):
                if barcode_found == 1:
                    output = utils.createBBSequencedFilename(barcode_data[0]+'_', ext, output_path)
                else:
                    if (save_file == 'pdf') and (merge_ADF_Flatbed == True):
                         output = utils.createSequencedFilename("hpscanMerge", ext,output_path)
                    else:
                         output = utils.createSequencedFilename("hpscan",ext,output_path)

            if uiscan == False:
                log.info("\nOutputting to destination 'file':")

            try:
                if uiscan == True:
                    log.info("Saving to file %s" % output)
                
                    if save_file != 'pdf':
                        '''pyPlatform = platform.python_version()
                        num = pyPlatform.split('.')
                        if num[0] >= '3':
                            im = im.convert("RGB")'''
                        try:
                            im.save(output,compress_level=1,quality=55)
                        except:
                            im = im.convert("RGB")
                            im.save(output,compress_level=1,quality=55)
                    else:                    
                        try:
                            from reportlab.pdfgen import canvas
                            #print()"entered canvas")
                            c = canvas.Canvas(output, (brx/0.3528, bry/0.3528))
                            try:
                                if auto_orient and (orient == 1 or orient == 3):
                                    c.setPageSize(((bry-tly)/0.3528, (brx-tlx)/0.3528))
                                    c.drawInlineImage(im, (tlx/0.3528), (tly/0.3528), ((bry-tly)/0.3528), ((brx-tlx)/0.3528))
                                else:
                                    c.setPageSize(((brx-tlx)/0.3528, (bry-tly)/0.3528))
                                    c.drawInlineImage(im, (tlx/0.3528), (tly/0.3528), ((brx-tlx)/0.3528),((bry-tly)/0.3528))
                            except NameError:
                                #log.error("A problem has occurred with PDF generation. This is a known bug in ReportLab. Please update your install of ReportLab to version 2.0 or greater.")
                                sys.exit(1)
                            except AssertionError as e:
                                log.error(e)
                                if PY3:
                                    #log.note("You might be running an older version of reportlab. Please update to the latest version")
                                    #log.note("More information is available at http://hplipopensource.com/node/369")
                                    sys.exit(1)
                            except Exception as e:
                                #log.error(e)
                                #log.note("Try Updating to reportlab version >= 3.2")
                                sys.exit(1)
                            c.showPage()
                            c.save()
                        except:
                            im = im.convert("RGB")
                            im.save(output,compress_level=1,quality=55)
                        '''from reportlab.pdfgen import canvas
                        print "entered canvas"
                        c = canvas.Canvas(output)
                        if auto_orient and (orient == 1 or orient == 3):
                                c.setPageSize(((bry-tly)/0.3528, (brx-tlx)/0.3528))
                                c.drawInlineImage(im, (tlx/0.3528), (tly/0.3528), ((bry-tly)/0.3528), ((brx-tlx)/0.3528))
                        else:
                            c.setPageSize(((brx-tlx)/0.3528, (bry-tly)/0.3528))
                            c.drawInlineImage(im, (tlx/0.3528), (tly/0.3528), ((brx-tlx)/0.3528),((bry-tly)/0.3528))
                        c.showPage()
                        c.save()'''
                        #For Doc Merge feature, updating Flatbed to use pdfmerger instead of canvas for PDF creation.  
                        '''temp = 'temp.png'
                        im.save(temp,compress_level=1)
                        adf_page_files.append(temp)
                        output = imageprocessing.generatePdfFile(adf_page_files,output)'''
                        if uiscan == False:
                            log.info("Viewing PDF file in %s" % pdf_viewer)
                            log.info("Saving to file %s" % output)
                        if merge_ADF_Flatbed == False:
                            #cmd = "%s %s &" % (pdf_viewer, output)                        
                            #os_utils.execute(cmd)
                            log.error("%s" % (output))
                            sys.exit(4)
                            #imageprocessing.merge_PDF_viewer(output)
                elif uiscan == False:
                    im.save(output,compress_level=1,quality=55)
            except IOError as e:
                im = im.convert("RGB")
                try:
                  im.save(output,compress_level=1,quality=55)
                except IOError as e:
                  log.error("Error saving file: %s (I/O)" % e)
                  try:
                      os.remove(output)
                  except OSError:
                      pass
                  sys.exit(1)
            except ValueError as e:
                log.error("Error saving file: %s (PIL)" % e)
                try:
                    os.remove(output)
                except OSError:
                    pass
                sys.exit(1)

            file_saved = True
            dest.remove("file")

        temp_saved = False
        if ('editor' in dest or 'viewer' in dest or 'email' in dest or 'print' in dest) \
            and not file_saved:

            output_fd, output = utils.make_temp_file(suffix='.png')
            try:
                '''pyPlatform = platform.python_version()
                num = pyPlatform.split('.')
                if num[0] >= '3':
                    im = im.convert("RGB")'''
                try:
                    im.save(output,compress_level=1,quality=55)
                except:
                    im = im.convert("RGB")
                    im.save(output,compress_level=1,quality=55)
            except IOError as e:
                log.error("Error saving temporary file: %s" % e)

                try:
                    os.remove(output)
                except OSError:
                    pass

                sys.exit(1)

            os.close(output_fd)
            temp_saved = True

        for d in dest:
            log.info("\nSending to destination '%s':" % d)

            if d == 'pdf':
                try:
                    from reportlab.pdfgen import canvas
                except ImportError:
                    log.error("PDF output requires ReportLab.")
                    continue
                if merge_ADF_Flatbed == True:
                    pdf_output = utils.createSequencedFilename("hpscanMerge", ".pdf",output_path)
                else:
                    pdf_output = utils.createSequencedFilename("hpscan", ".pdf", output_path)
                c = canvas.Canvas(pdf_output, (brx/0.3528, bry/0.3528))

                try:
                    c.drawInlineImage(im, (tlx/0.3528), (tly/0.3528), ((brx-tlx)/0.3528),((bry-tly)/0.3528))
                except NameError:
                    log.error("A problem has occurred with PDF generation. This is a known bug in ReportLab. Please update your install of ReportLab to version 2.0 or greater.")
                    continue

                c.showPage()
                if uiscan == False:
                    log.info("Saving to file %s" % pdf_output)
                c.save()
                if uiscan == False:
                    log.info("Viewing PDF file in %s" % pdf_viewer)
                #cmd = "%s %s &" % (pdf_viewer, pdf_output)
                #os_utils.execute(cmd)
                #sys.exit(0)
                if uiscan == True:
                    log.error("%s" % (pdf_output))
                    sys.exit(4)
                else:
                    sys.exit(0)

            elif d == 'print':
                hp_print = utils.which("hp-print", True)
                if not hp_print:
                    hp_print = 'python ./print.py'
                 
                if dest_printer is not None:
                   cmd = '%s -p %s %s &' % (hp_print, dest_printer, output)
                elif dest_devUri is not None:
                   tmp = dest_devUri.partition(":")[2]
                   dest_devUri = "hp:" + tmp
                   cmd = '%s -d %s %s &' % (hp_print, dest_devUri, output)
                else:
                   cmd = '%s %s &' % (hp_print, output)
                
                os_utils.execute(cmd)

            elif d == 'email':
                try:
                    from email.mime.image import MIMEImage
                    from email.mime.multipart import MIMEMultipart
                    from email.mime.text import MIMEText
                except ImportError:
                    try:
                        from email.MIMEImage import MIMEImage
                        from email.MIMEMultipart import MIMEMultipart
                        from email.MIMEText import MIMEText
                    except ImportError:
                        log.error("hp-scan email destination requires Python 2.2+.")
                        continue

                msg = MIMEMultipart()
                msg['Subject'] = email_subject
                msg['From'] = email_from
                msg['To'] = ','.join(email_to)
                msg.preamble = 'Scanned using hp-scan'

                if email_note:
                    txt = MIMEText(email_note)
                    msg.attach(txt)

                if file_saved:
                    txt = MIMEText("attached: %s: %dx%d %s PNG image." %
                        (os.path.basename(output), pixels_per_line, lines, scan_mode))
                else:
                    txt = MIMEText("attached: %dx%d %s PNG image." % (pixels_per_line, lines, scan_mode))

                msg.attach(txt)

                fp = open(output, 'r')
                img = MIMEImage(fp.read())
                fp.close()

                if file_saved:
                    img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(output))

                msg.attach(img)

                sendmail = utils.which("sendmail")

                if sendmail:
                    sendmail = os.path.join(sendmail, 'sendmail')
                    cmd = [sendmail,'-t','-r',email_from]

                    log.debug(repr(cmd))
                    err = None
                    try:
                        sp = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        std_out, std_err = sp.communicate(msg.as_string())
                        if std_err != '':
                            err = std_err
                    except OSError as e:
                        err = str(e)
                    cleanup_spinner()

                    if err:
                        log.error(repr(err))

                else:
                    log.error("Mail send failed. 'sendmail' not found.")

            elif d == 'viewer':
                if viewer:
                    log.info("Viewing file in %s" % viewer)
                    cmd = "%s %s &" % (viewer, output)
                    os_utils.execute(cmd)
                else:
                    log.error("Viewer not found.")

            elif d == 'editor':
                if editor:
                    log.info("Editing file in %s" % editor)
                    cmd = "%s %s &" % (editor, output)
                    os_utils.execute(cmd)
                else:
                    log.error("Editor not found.")

        device.freeScan()
        device.closeScan()
        sane.deInit()


except KeyboardInterrupt:
    log.error("User exit")

log.info("")
log.info("Done.")

