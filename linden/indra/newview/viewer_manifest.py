#!/usr/bin/python
# @file viewer_manifest.py
# @author Ryan Williams
# @brief Description of all installer viewer files, and methods for packaging
#        them into installers for all supported platforms.
#
# $LicenseInfo:firstyear=2006&license=viewergpl$
# 
# Copyright (c) 2006-2008, Linden Research, Inc.
# 
# Second Life Viewer Source Code
# The source code in this file ("Source Code") is provided by Linden Lab
# to you under the terms of the GNU General Public License, version 2.0
# ("GPL"), unless you have obtained a separate licensing agreement
# ("Other License"), formally executed by you and Linden Lab.  Terms of
# the GPL can be found in doc/GPL-license.txt in this distribution, or
# online at http://secondlifegrid.net/programs/open_source/licensing/gplv2
# 
# There are special exceptions to the terms and conditions of the GPL as
# it is applied to this Source Code. View the full text of the exception
# in the file doc/FLOSS-exception.txt in this software distribution, or
# online at http://secondlifegrid.net/programs/open_source/licensing/flossexception
# 
# By copying, modifying or distributing this software, you acknowledge
# that you have read and understood your obligations described above,
# and agree to abide by those obligations.
# 
# ALL LINDEN LAB SOURCE CODE IS PROVIDED "AS IS." LINDEN LAB MAKES NO
# WARRANTIES, EXPRESS, IMPLIED OR OTHERWISE, REGARDING ITS ACCURACY,
# COMPLETENESS OR PERFORMANCE.
# $/LicenseInfo$
import sys
import os.path
import re
import tarfile
viewer_dir = os.path.dirname(__file__)
# add llmanifest library to our path so we don't have to muck with PYTHONPATH
sys.path.append(os.path.join(viewer_dir, '../lib/python/indra/util'))
from llmanifest import LLManifest, main, proper_windows_path, path_ancestors

class ViewerManifest(LLManifest):
    def construct(self):
        super(ViewerManifest, self).construct()
        self.exclude("*.svn*")
        self.path(src="../../scripts/messages/message_template.msg", dst="app_settings/message_template.msg")
        self.path(src="../../etc/message.xml", dst="app_settings/message.xml")

        if self.prefix(src="app_settings"):
            self.exclude("logcontrol.xml")
            self.exclude("logcontrol-dev.xml")
            self.path("*.pem")
            self.path("*.ini")
            self.path("*.xml")
            self.path("*.vp")
            self.path("*.db2")

            # include the entire shaders directory recursively
            self.path("shaders")
            # ... and the entire windlight directory
            self.path("windlight")
            self.end_prefix("app_settings")

        if self.prefix(src="character"):
            self.path("*.llm")
            self.path("*.xml")
            self.path("*.tga")
            self.end_prefix("character")


        # Include our fonts
        if self.prefix(src="fonts"):
            self.path("LiberationSans-Bold.ttf")
            self.path("LiberationSans-Regular.ttf")
            self.path("VeraMono.ttf")
            self.path("*.txt")
            self.end_prefix("fonts")

        # skins
        if self.prefix(src="skins"):
            self.path("paths.xml")
            
            # include the entire textures directory recursively
            if self.prefix(src="*/textures"):
                self.path("*.tga")
                self.path("*.j2c")
                self.path("*.jpg")
                self.path("*.png")
                self.path("textures.xml")
                self.end_prefix("*/textures")

            self.path("*/xui/*/*.xml")
            self.path("*/*.xml")

            # Local HTML files (e.g. loading screen)
            if self.prefix(src="*/html"):
                self.path("*.png")
                self.path("*/*/*.html")
                self.path("*/*/*.gif")
                self.end_prefix("*/html")
                
            self.end_prefix("skins")
            
        self.path("lsl_guide.html")
        self.path("gpu_table.txt")


    # Gather up the README file, etc.
    def gather_documents(self):
        # From the top level directory (imprudence)
        if self.prefix("../../..", dst=""):
            self.path("README.txt")
            self.path("MANIFESTO.txt")
            self.path("CONTRIBUTE.txt")
            self.path("RELEASE_NOTES.txt")
            self.path("ChangeLog.txt")
            self.end_prefix("../../..")

        # From the linden directory
        if self.prefix("../..", dst="doc"):
            self.path("LICENSE-source.txt")
            self.path("LICENSE-logos.txt", "LICENSE-artwork.txt")
            self.end_prefix("../..")

        # From the linden/doc directory
        if self.prefix("../../doc", dst="doc"):
            self.path("contributions.txt")
            self.path("GPL-license.txt", "GPL.txt")
            self.path("FLOSS-exception.txt")
            self.end_prefix("../../doc")


    def login_channel(self):
        """Channel reported for login and upgrade purposes ONLY;
        used for A/B testing"""
        # NOTE: Do not return the normal channel if login_channel
        # is not specified, as some code may branch depending on
        # whether or not this is present
        return self.args.get('login_channel')

    def channel(self):
        return self.args['channel']
    def channel_unique(self):
        return self.channel().replace("Second Life", "").strip()
    def channel_oneword(self):
        return "".join(self.channel_unique().split())
    def channel_lowerword(self):
        return self.channel_oneword().lower()

    def flags_list(self):
        """ Convenience function that returns the command-line flags
        for the grid"""
        channel_flags = ''
        grid_flags = ''
        if not self.default_grid():
            if self.default_channel():
                # beta grid viewer
                channel_flags = '--settings settings_beta.xml'
            grid_flags = "--grid %(grid)s --helperuri http://preview-%(grid)s.secondlife.com/helpers/" % {'grid':self.args['grid']}

        if not self.default_channel():
            # some channel on some grid
            channel_flags = '--settings settings_%s.xml --channel "%s"' % (self.channel_lowerword(), self.channel())
        elif self.login_channel():
            # Report a special channel during login, but use default
            channel_flags = '--channel "%s"' % (self.login_channel())
                        
        return " ".join((channel_flags, grid_flags)).strip()


class WindowsManifest(ViewerManifest):
    def final_exe(self):
        if self.default_channel():
            if self.default_grid():
                return "imprudence.exe"
            else:
                return "imprudencepreview.exe"
        else:
            return ''.join(self.channel().split()) + '.exe'


    def construct(self):
        super(WindowsManifest, self).construct()
        # the final exe is complicated because we're not sure where it's coming from,
        # nor do we have a fixed name for the executable
        self.path(self.find_existing_file('debug/imprudence-bin.exe', 'release/imprudence-bin.exe', 'relwithdebinfo/imprudence-bin.exe'), dst=self.final_exe())

        self.gather_documents()

        if self.prefix("../..", dst="doc"):
            self.path("LICENSE-libraries-win32.txt")
            self.end_prefix("../..")


        self.path("featuretable.txt")

        # For use in crash reporting (generates minidumps)
        self.path("dbghelp.dll")

        # For using FMOD for sound... DJS
        #self.path("fmod.dll")

        # For textures
        if self.prefix(src="../../libraries/i686-win32/lib/release", dst=""):
            self.path("openjpeg.dll")
            self.end_prefix()

        # For sound
        if self.prefix(src="../../libraries/i686-win32/lib/release", dst=""):
            self.path("openal32.dll")
            self.path("alut.dll")
            self.end_prefix()           

        # Mozilla appears to force a dependency on these files so we need to ship it (CP)
        self.path("msvcr71.dll")
        self.path("msvcp71.dll")

        # Mozilla runtime DLLs (CP)
        if self.prefix(src="../../libraries/i686-win32/lib/release", dst=""):
            self.path("freebl3.dll")
            self.path("gksvggdiplus.dll")
            self.path("js3250.dll")
            self.path("nspr4.dll")
            self.path("nss3.dll")
            self.path("nssckbi.dll")
            self.path("plc4.dll")
            self.path("plds4.dll")
            self.path("smime3.dll")
            self.path("softokn3.dll")
            self.path("ssl3.dll")
            self.path("xpcom.dll")
            self.path("xul.dll")
            self.end_prefix()

        # Mozilla runtime misc files (CP)
        if self.prefix(src="app_settings/mozilla"):
            self.path("chrome/*.*")
            self.path("components/*.*")
            self.path("greprefs/*.*")
            self.path("plugins/*.*")
            self.path("res/*.*")
            self.path("res/*/*")
            self.end_prefix()

        # Vivox runtimes
        if self.prefix(src="vivox-runtime/i686-win32", dst=""):
        #    self.path("alut.dll")
            self.path("wrap_oal.dll")

        #    self.path("SLVoice.exe")
        #    self.path("SLVoiceAgent.exe")
        #    self.path("libeay32.dll")
        #    self.path("srtp.dll")
        #    self.path("ssleay32.dll")
        #    self.path("tntk.dll")
        #    self.path("vivoxsdk.dll")
        #    self.path("ortp.dll")

            self.end_prefix()

#        # pull in the crash logger and updater from other projects
#        self.path(src=self.find_existing_file( # tag:"crash-logger" here as a cue to the exporter
#                "../win_crash_logger/debug/windows-crash-logger.exe",
#                "../win_crash_logger/release/windows-crash-logger.exe",
#                "../win_crash_logger/relwithdebinfo/windows-crash-logger.exe"),
#                  dst="win_crash_logger.exe")
        self.path(src=self.find_existing_file(
                "../win_updater/debug/windows-updater.exe",
                "../win_updater/release/windows-updater.exe",
                "../win_updater/relwithdebinfo/windows-updater.exe"),
                  dst="updater.exe")

    def nsi_file_commands(self, install=True):
        def wpath(path):
            if path.endswith('/') or path.endswith(os.path.sep):
                path = path[:-1]
            path = path.replace('/', '\\')
            return path

        result = ""
        dest_files = [pair[1] for pair in self.file_list if pair[0] and os.path.isfile(pair[1])]
        # sort deepest hierarchy first
        dest_files.sort(lambda a,b: cmp(a.count(os.path.sep),b.count(os.path.sep)) or cmp(a,b))
        dest_files.reverse()
        out_path = None
        for pkg_file in dest_files:
            rel_file = os.path.normpath(pkg_file.replace(self.get_dst_prefix()+os.path.sep,''))
            installed_dir = wpath(os.path.join('$INSTDIR', os.path.dirname(rel_file)))
            pkg_file = wpath(os.path.normpath(pkg_file))
            if installed_dir != out_path:
                if install:
                    out_path = installed_dir
                    result += 'SetOutPath ' + out_path + '\n'
            if install:
                result += 'File ' + pkg_file + '\n'
            else:
                result += 'Delete ' + wpath(os.path.join('$INSTDIR', rel_file)) + '\n'
        # at the end of a delete, just rmdir all the directories
        if not install:
            deleted_file_dirs = [os.path.dirname(pair[1].replace(self.get_dst_prefix()+os.path.sep,'')) for pair in self.file_list]
            # find all ancestors so that we don't skip any dirs that happened to have no non-dir children
            deleted_dirs = []
            for d in deleted_file_dirs:
                deleted_dirs.extend(path_ancestors(d))
            # sort deepest hierarchy first
            deleted_dirs.sort(lambda a,b: cmp(a.count(os.path.sep),b.count(os.path.sep)) or cmp(a,b))
            deleted_dirs.reverse()
            prev = None
            for d in deleted_dirs:
                if d != prev:   # skip duplicates
                    result += 'RMDir ' + wpath(os.path.join('$INSTDIR', os.path.normpath(d))) + '\n'
                prev = d

        return result

    def package_finish(self):
        # a standard map of strings for replacing in the templates
        substitution_strings = {
            'version' : '.'.join(self.args['version']),
            'version_short' : '.'.join(self.args['version'][:-1]),
            'version_dashes' : '-'.join(self.args['version']),
            'final_exe' : self.final_exe(),
            'grid':self.args['grid'],
            'grid_caps':self.args['grid'].upper(),
            # escape quotes becase NSIS doesn't handle them well
            'flags':self.flags_list().replace('"', '$\\"'),
            'channel':self.channel(),
            'channel_oneword':self.channel_oneword(),
            'channel_unique':self.channel_unique(),
            }

        version_vars = """
        !define INSTEXE  "%(final_exe)s"
        !define VERSION "%(version_short)s"
        !define VERSION_LONG "%(version)s"
        !define VERSION_DASHES "%(version_dashes)s"
        """ % substitution_strings
        if self.default_channel():
            if self.default_grid():
                # release viewer
                installer_file = "Imprudence_%(version_dashes)s_Setup.exe"
                grid_vars_template = """
                OutFile "%(installer_file)s"
                !define INSTFLAGS "%(flags)s"
                !define INSTNAME   "Imprudence"
                !define SHORTCUT   "Imprudence"
                !define URLNAME   "imprudence"
                Caption "Imprudence ${VERSION}"
                """
            else:
                # beta grid viewer
                installer_file = "Imprudence_%(version_dashes)s_(%(grid_caps)s)_Setup.exe"
                grid_vars_template = """
                OutFile "%(installer_file)s"
                !define INSTFLAGS "%(flags)s"
                !define INSTNAME   "Imprudence%(grid_caps)s"
                !define SHORTCUT   "Imprudence (%(grid_caps)s)"
                !define URLNAME   "imprudence%(grid)s"
                !define UNINSTALL_SETTINGS 1
                Caption "Imprudence %(grid)s ${VERSION}"
                """
        else:
            # some other channel on some grid
            installer_file = "Imprudence_%(version_dashes)s_%(channel_oneword)s_Setup.exe"
            grid_vars_template = """
            OutFile "%(installer_file)s"
            !define INSTFLAGS "%(flags)s"
            !define INSTNAME   "Imprudence%(channel_oneword)s"
            !define SHORTCUT   "%(channel)s"
            !define URLNAME   "imprudence"
            !define UNINSTALL_SETTINGS 1
            Caption "%(channel)s ${VERSION}"
            """
        if 'installer_name' in self.args:
            installer_file = self.args['installer_name']
        else:
            installer_file = installer_file % substitution_strings
        substitution_strings['installer_file'] = installer_file

        tempfile = "imprudence_setup_tmp.nsi"
        # the following replaces strings in the nsi template
        # it also does python-style % substitution
        self.replace_in("installers/windows/installer_template.nsi", tempfile, {
                "%%VERSION%%":version_vars,
                "%%SOURCE%%":self.get_src_prefix(),
                "%%GRID_VARS%%":grid_vars_template % substitution_strings,
                "%%INSTALL_FILES%%":self.nsi_file_commands(True),
                "%%DELETE_FILES%%":self.nsi_file_commands(False)})

        NSIS_path = 'C:\\Program Files\\NSIS\\makensis.exe'
        self.run_command('"' + proper_windows_path(NSIS_path) + '" ' + self.dst_path_of(tempfile))
        # self.remove(self.dst_path_of(tempfile))
        self.created_path(self.dst_path_of(installer_file))
        self.package_file = installer_file


class DarwinManifest(ViewerManifest):
    def construct(self):
        # copy over the build result (this is a no-op if run within the xcode script)
        self.path(self.args['configuration'] + "/Imprudence.app", dst="")

        if self.prefix(src="", dst="Contents"):  # everything goes in Contents
            # Expand the tar file containing the assorted mozilla bits into
            #  <bundle>/Contents/MacOS/
            self.contents_of_tar(self.args['source']+'/mozilla-universal-darwin.tgz', 'MacOS')

            self.path("Info-SecondLife.plist", dst="Info.plist")

            # copy additional libs in <bundle>/Contents/MacOS/
            self.path("../../libraries/universal-darwin/lib_release/libndofdev.dylib", dst="MacOS/libndofdev.dylib")

            # replace the default theme with our custom theme (so scrollbars work).
            if self.prefix(src="mozilla-theme", dst="MacOS/chrome"):
                self.path("classic.jar")
                self.path("classic.manifest")
                self.end_prefix("MacOS/chrome")

            # most everything goes in the Resources directory
            if self.prefix(src="", dst="Resources"):
                super(DarwinManifest, self).construct()

                if self.prefix("cursors_mac"):
                    self.path("*.tif")
                    self.end_prefix("cursors_mac")

                # From the linden directory
                if self.prefix("../..", dst="doc"):
                    self.path("LICENSE-libraries-mac.txt")
                    self.end_prefix("../..")

                self.gather_documents()

                self.path("featuretable_mac.txt")
                self.path("SecondLife.nib")

                self.path("secondlife.icns")
                
                # Translations
                self.path("English.lproj")
                self.path("German.lproj")
                self.path("Japanese.lproj")
                self.path("Korean.lproj")


                # SLVoice and vivox lols
                self.path("vivox-runtime/universal-darwin/libalut.dylib", "libalut.dylib")
                self.path("vivox-runtime/universal-darwin/libopenal.dylib", "libopenal.dylib")
                #self.path("vivox-runtime/universal-darwin/libortp.dylib", "libortp.dylib")
                #self.path("vivox-runtime/universal-darwin/libvivoxsdk.dylib", "libvivoxsdk.dylib")
                #self.path("vivox-runtime/universal-darwin/SLVoice", "SLVoice")
                #self.path("vivox-runtime/universal-darwin/SLVoiceAgent.app", "SLVoiceAgent.app")

                #libfmodwrapper.dylib
                #self.path(self.args['configuration'] + "/libfmodwrapper.dylib", "libfmodwrapper.dylib")
                
                # our apps
#                self.path("../mac_crash_logger/" + self.args['configuration'] + "/mac-crash-logger.app", "mac-crash-logger.app")
                self.path("../mac_updater/" + self.args['configuration'] + "/mac-updater.app", "mac-updater.app")

                # command line arguments for connecting to the proper grid
                self.put_in_file(self.flags_list(), 'arguments.txt')

                self.end_prefix("Resources")

            self.end_prefix("Contents")

        # NOTE: the -S argument to strip causes it to keep enough info for
        # annotated backtraces (i.e. function names in the crash log).  'strip' with no
        # arguments yields a slightly smaller binary but makes crash logs mostly useless.
        # This may be desirable for the final release.  Or not.
        if ("package" in self.args['actions'] or 
            "unpacked" in self.args['actions']):
            self.run_command('strip -S "%(viewer_binary)s"' %
                             { 'viewer_binary' : self.dst_path_of('Contents/MacOS/Second Life')})


    def package_finish(self):
        channel_standin = 'Imprudence'  # hah, our default channel is not usable on its own
        if not self.default_channel():
            channel_standin = self.channel()

        imagename="Imprudence_" + '_'.join(self.args['version'])

        # MBW -- If the mounted volume name changes, it breaks the .DS_Store's background image and icon positioning.
        #  If we really need differently named volumes, we'll need to create multiple DS_Store file images, or use some other trick.

        volname="Imprudence Installer"  # DO NOT CHANGE without understanding comment above

        if self.default_channel():
            if not self.default_grid():
                # beta case
                imagename = imagename + '_' + self.args['grid'].upper()
        else:
            # first look, etc
            imagename = imagename + '_' + self.channel_oneword().upper()

        sparsename = imagename + ".sparseimage"
        finalname = imagename + ".dmg"
        # make sure we don't have stale files laying about
        self.remove(sparsename, finalname)

        self.run_command('hdiutil create "%(sparse)s" -volname "%(vol)s" -fs HFS+ -type SPARSE -megabytes 300 -layout SPUD' % {
                'sparse':sparsename,
                'vol':volname})

        # mount the image and get the name of the mount point and device node
        hdi_output = self.run_command('hdiutil attach -private "' + sparsename + '"')
        devfile = re.search("/dev/disk([0-9]+)[^s]", hdi_output).group(0).strip()
        volpath = re.search('HFS\s+(.+)', hdi_output).group(1).strip()

        # Copy everything in to the mounted .dmg

        if self.default_channel() and not self.default_grid():
            app_name = "Imprudence " + self.args['grid']
        else:
            app_name = channel_standin.strip()

        # Hack:
        # Because there is no easy way to coerce the Finder into positioning
        # the app bundle in the same place with different app names, we are
        # adding multiple .DS_Store files to svn. There is one for release,
        # one for release candidate and one for first look. Any other channels
        # will use the release .DS_Store, and will look broken.
        # - Ambroff 2008-08-20
        dmg_template = os.path.join(
            'installers', 
            'darwin',
            '%s-dmg' % "".join(self.channel_unique().split()).lower())

        if not os.path.exists (self.src_path_of(dmg_template)):
            dmg_template = os.path.join ('installers', 'darwin', 'release-dmg')

        # To reinstate the linden scripting guide, add this to the list below:
        #            "lsl_guide.html":"Linden Scripting Language Guide.html",

        for s,d in {self.get_dst_prefix():app_name + ".app",
                    os.path.join(dmg_template, "_VolumeIcon.icns"): ".VolumeIcon.icns",
                    os.path.join(dmg_template, "background.jpg"): "background.jpg",
                    os.path.join(dmg_template, "_DS_Store"): ".DS_Store"}.items():
            print "Copying to dmg", s, d
            self.copy_action(self.src_path_of(s), os.path.join(volpath, d))

        # Hide the background image, DS_Store file, and volume icon file (set their "visible" bit)
        self.run_command('SetFile -a V "' + os.path.join(volpath, ".VolumeIcon.icns") + '"')
        self.run_command('SetFile -a V "' + os.path.join(volpath, "background.jpg") + '"')
        self.run_command('SetFile -a V "' + os.path.join(volpath, ".DS_Store") + '"')

        # Create the alias file (which is a resource file) from the .r
        self.run_command('rez "' + self.src_path_of("installers/darwin/release-dmg/Applications-alias.r") + '" -o "' + os.path.join(volpath, "Applications") + '"')

        # Set the alias file's alias and custom icon bits
        self.run_command('SetFile -a AC "' + os.path.join(volpath, "Applications") + '"')

        # Set the disk image root's custom icon bit
        self.run_command('SetFile -a C "' + volpath + '"')

        # Unmount the image
        self.run_command('hdiutil detach -force "' + devfile + '"')

        print "Converting temp disk image to final disk image"
        self.run_command('hdiutil convert "%(sparse)s" -format UDZO -imagekey zlib-level=9 -o "%(final)s"' % {'sparse':sparsename, 'final':finalname})
        # get rid of the temp file
        self.package_file = finalname
        self.remove(sparsename)

class LinuxManifest(ViewerManifest):
    def construct(self):
        super(LinuxManifest, self).construct()

        self.path("res/imprudence_icon.png","imprudence_icon.png")
        if self.prefix("linux_tools", dst=""):
            #self.path("client-readme.txt","README-linux.txt")
            #self.path("client-readme-voice.txt","README-linux-voice.txt")
            self.path("wrapper.sh","imprudence")
            self.path("handle_secondlifeprotocol.sh")
            self.path("register_secondlifeprotocol.sh")
            self.end_prefix("linux_tools")

        self.gather_documents()

        # From the linden directory
        if self.prefix("../..", dst="doc"):
            self.path("LICENSE-libraries-linux.txt")
            self.end_prefix("../..")

        # Create an appropriate gridargs.dat for this package, denoting required grid.
        self.put_in_file(self.flags_list(), 'gridargs.dat')


    def package_finish(self):
        # stripping all the libs removes a few megabytes from the end-user package
        for s,d in self.file_list:
            if re.search("lib/lib.+\.so.*", d):
                self.run_command('strip -S %s' % d)
            if re.search("app_settings/mozilla-runtime-.*/lib.+\.so.*", d):
                self.run_command('strip %s' % d)

        if 'installer_name' in self.args:
            installer_name = self.args['installer_name']
        else:
            installer_name_components = ['Imprudence_', self.args.get('arch')]
            installer_name_components.extend(self.args['version'])
            installer_name = "_".join(installer_name_components)
            if self.default_channel():
                if not self.default_grid():
                    installer_name += '_' + self.args['grid'].upper()
            else:
                installer_name += '_' + self.channel_oneword().upper()

                # Fix access permissions
                self.run_command("""
                find %(dst)s -type d | xargs --no-run-if-empty chmod 755;
                find %(dst)s -type f -perm 0700 | xargs --no-run-if-empty chmod 0755;
                find %(dst)s -type f -perm 0500 | xargs --no-run-if-empty chmod 0555;
                find %(dst)s -type f -perm 0600 | xargs --no-run-if-empty chmod 0644;
                find %(dst)s -type f -perm 0400 | xargs --no-run-if-empty chmod 0444;
                true""" %  {'dst':self.get_dst_prefix() })

        self.package_file = installer_name + '.tar.bz2'

        if("package" in self.args['actions'] or
           "unpacked" in self.args['actions']):

            # temporarily move directory tree so that it has the right
            # name in the tarfile
            self.run_command("mv %(dst)s %(inst)s" % {
                'dst': self.get_dst_prefix(),
                'inst': self.build_path_of(installer_name)})
            try:
                # --numeric-owner hides the username of the builder for
                # security etc.
                self.run_command('tar -C %(dir)s --numeric-owner -cjf '
                                 '%(inst_path)s.tar.bz2 %(inst_name)s' % {
                    'dir': self.get_build_prefix(),
                    'inst_name': installer_name,
                    'inst_path':self.build_path_of(installer_name)})
            finally:
                self.run_command("mv %(inst)s %(dst)s" % {
                    'dst': self.get_dst_prefix(),
                    'inst': self.build_path_of(installer_name)})


class Linux_i686Manifest(LinuxManifest):
    def construct(self):
        super(Linux_i686Manifest, self).construct()
        self.path("imprudence-stripped","bin/do-not-directly-run-imprudence-bin")
#        self.path("../linux_crash_logger/linux-crash-logger-stripped","linux-crash-logger.bin")
        self.path("linux_tools/launch_url.sh","launch_url.sh")
        if self.prefix("res-sdl"):
            self.path("*")
            # recurse
            self.end_prefix("res-sdl")

        self.path("featuretable_linux.txt")
        #self.path("secondlife-i686.supp")

        self.path("app_settings/mozilla-runtime-linux-i686")

        if self.prefix("../../libraries/i686-linux/lib_release_client", dst="lib"):
            self.path("libapr-1.so.0")
            self.path("libaprutil-1.so.0")
            self.path("libdb-4.2.so")
            self.path("libcrypto.so.0.9.7")
            self.path("libexpat.so.1")
            self.path("libssl.so.0.9.7")
            self.path("libuuid.so", "libuuid.so.1")
            self.path("libSDL-1.2.so.0")
            self.path("libELFIO.so")
            self.path("libopenjpeg.so.2")

            self.path("libopenal.so") # symlink
            self.path("libopenal.so.1")
            self.path("libalut.so")

            # Gstreamer libs
            self.path("libgstbase-0.10.so") # symlink
            self.path("libgstbase-0.10.so.0")
            self.path("libgstreamer-0.10.so") # symlink
            self.path("libgstreamer-0.10.so.0")
            self.path("libgstaudio-0.10.so.0")
            self.path("libgstbase-0.10.so.0")
            self.path("libgstcontroller-0.10.so.0")
            self.path("libgstdataprotocol-0.10.so.0")
            self.path("libgstinterfaces-0.10.so.0")
            self.path("libgstnetbuffer-0.10.so.0")
            self.path("libgstpbutils-0.10.so.0")
            self.path("libgstriff-0.10.so.0")
            self.path("libgstrtp-0.10.so.0")
            self.path("libgstrtsp-0.10.so.0")
            self.path("libgstsdp-0.10.so.0")
            self.path("libgsttag-0.10.so.0")
            self.path("libgstvideo-0.10.so.0")

            # Gstreamer plugin dependencies
            self.path("libavcodec.so.52")
            self.path("libavformat.so.52")
            self.path("libavutil.so.49")
            self.path("libxvidcore.so.4")
            self.path("libfaac.so.0")
            self.path("libfaad.so.1")
            self.path("libmp3lame.so.0")
            self.path("libogg.so.0")
            self.path("libvorbis.so.0")
            self.path("libvorbisenc.so.2")
            self.path("libxml2.so.2")
            self.path("libxvidcore.so.4")

            # Gstreamer plugins
            if self.prefix("gstreamer-plugins"):
                self.path("libgstalsa.so")
                self.path("libgstasf.so")
                self.path("libgstaudioconvert.so")
                self.path("libgstaudioresample.so")
                self.path("libgstautodetect.so")
                self.path("libgstavi.so")
                self.path("libgstcoreelements.so")
                self.path("libgstcoreindexers.so")
                self.path("libgstdecodebin2.so")
                self.path("libgstdecodebin.so")
                self.path("libgstesd.so")
                self.path("libgstffmpegcolorspace.so")
                self.path("libgstffmpeg.so")
                self.path("libgstgnomevfs.so")
                self.path("libgsticydemux.so")
                self.path("libgstid3demux.so")
                self.path("libgstmpegdemux.so")
                self.path("libgstmultifile.so")
                self.path("libgstmultipart.so")
                self.path("libgstogg.so")
                self.path("libgstossaudio.so")
                self.path("libgstplaybin.so")
                self.path("libgstqtdemux.so")
                self.path("libgstqueue2.so")
                self.path("libgsttcp.so")
                self.path("libgsttheora.so")
                self.path("libgsttypefindfunctions.so")
                self.path("libgstudp.so")
                self.path("libgstvideoscale.so")
                self.path("libgstvolume.so")
                self.path("libgstvorbis.so")
                self.path("libgstwavparse.so")
                
                self.end_prefix("gstreamer-plugins")
            
            self.end_prefix("lib")

            # Vivox runtimes
            #if self.prefix(src="vivox-runtime/i686-linux", dst="bin"):
            #        self.path("SLVoice")
            #        self.end_prefix()
            

class Linux_x86_64Manifest(LinuxManifest):
    def construct(self):
        super(Linux_x86_64Manifest, self).construct()
        self.path("imprudence-stripped","bin/do-not-directly-run-imprudence-bin")
#        self.path("../linux_crash_logger/linux-crash-logger-stripped","linux-crash-logger.bin")
        self.path("linux_tools/launch_url.sh","launch_url.sh")
        if self.prefix("res-sdl"):
            self.path("*")
            # recurse
            self.end_prefix("res-sdl")

        self.path("featuretable_linux.txt")
        self.path("secondlife-i686.supp")

if __name__ == "__main__":
    main()
