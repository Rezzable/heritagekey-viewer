# -*- cmake -*-

# The copy_win_libs folder contains file lists and a script used to 
# copy dlls, exes and such needed to run the SecondLife from within 
# VisualStudio. 

include(CMakeCopyIfDifferent)

set(gst_plugin_debug_dir "${CMAKE_SOURCE_DIR}/../libraries/i686-win32/lib/debug/gstreamer-plugins")
set(gst_plugin_debug_files
    libgstadder.dll
    libgstalaw.dll
    libgstaudioconvert.dll
    libgstaudiorate.dll
    libgstaudioresample.dll
    libgstaudiotestsrc.dll
    libgstautodetect.dll
    libgstavi.dll
    libgstcutter.dll
    libgstdecodebin2.dll
    libgstdecodebin.dll
    libgstdirectdraw.dll
    libgstdirectsound.dll
    libgsteffectv.dll
    libgstffmpeg.dll
    libgstffmpegcolorspace.dll
    libgstgdp.dll
    libgstjpeg.dll
    libgstmulaw.dll
    libgstogg.dll
    libgstplaybin.dll
    libgstqtdemux.dll
    libgstrtp.dll    
    libgstrtsp.dll
    libgsttheora.dll
    libgsttypefindfunctions.dll
    libgstudp.dll
    libgstvideobalance.dll
    libgstvideobox.dll
    libgstvideocrop.dll
    libgstvideoflip.dll
    libgstvideomixer.dll
    libgstvideorate.dll
    libgstvideoscale.dll
    libgstvideotestsrc.dll
    libgstvolume.dll
    libgstvorbis.dll
    )

copy_if_different(
    ${gst_plugin_debug_dir} 
    "${CMAKE_CURRENT_BINARY_DIR}/Debug/lib/gstreamer-plugins"
    out_targets 
    ${gst_plugin_debug_files}
    )
set(all_targets ${all_targets} ${out_targets})

set(gst_plugin_release_dir "${CMAKE_SOURCE_DIR}/../libraries/i686-win32/lib/release/gstreamer-plugins")
set(gst_plugin_release_files
    libgstadder.dll
    libgstalaw.dll
    libgstaudioconvert.dll
    libgstaudiorate.dll
    libgstaudioresample.dll
    libgstaudiotestsrc.dll
    libgstautodetect.dll
    libgstavi.dll
    libgstcutter.dll
    libgstdecodebin2.dll
    libgstdecodebin.dll
    libgstdirectdraw.dll
    libgstdirectsound.dll
    libgsteffectv.dll
    libgstffmpeg.dll
    libgstffmpegcolorspace.dll
    libgstgdp.dll
    libgstjpeg.dll
    libgstmulaw.dll
    libgstogg.dll
    libgstplaybin.dll
    libgstqtdemux.dll
    libgstrtp.dll    
    libgstrtsp.dll
    libgsttheora.dll
    libgsttypefindfunctions.dll
    libgstudp.dll
    libgstvideobalance.dll
    libgstvideobox.dll
    libgstvideocrop.dll
    libgstvideoflip.dll
    libgstvideomixer.dll
    libgstvideorate.dll
    libgstvideoscale.dll
    libgstvideotestsrc.dll
    libgstvolume.dll
    libgstvorbis.dll
    )

copy_if_different(
    ${gst_plugin_release_dir} 
    "${CMAKE_CURRENT_BINARY_DIR}/Release/lib/gstreamer-plugins"
    out_targets 
    ${gst_plugin_release_files}
    )
set(all_targets ${all_targets} ${out_targets})

set(vivox_src_dir "${CMAKE_SOURCE_DIR}/newview/vivox-runtime/i686-win32")
set(vivox_files
    tntk.dll
    libeay32.dll
    SLVoice.exe
    ssleay32.dll
    SLVoiceAgent.exe
    srtp.dll
    vivoxsdk.dll
    ortp.dll
    wrap_oal.dll
    )

set(debug_src_dir "${CMAKE_SOURCE_DIR}/../libraries/i686-win32/lib/debug")
set(debug_files
    alut.dll
    freebl3.dll
    gksvggdiplus.dll
    js3250.dll
    nspr4.dll
    nss3.dll
    nssckbi.dll
    openal32.dll
    openjpegd.dll
    plc4.dll
    plds4.dll
    smime3.dll
    softokn3.dll
    ssl3.dll
    xpcom.dll
    xul.dll
    windbgdlg.exe
    iconv.dll
    libxml2.dll
    libgio-2.0-0.dll
    libglib-2.0-0.dll
    libgmodule-2.0-0.dll
    libgobject-2.0-0.dll
    libgthread-2.0-0.dll
    avcodec-51.dll
    avformat-52.dll
    avutil-49.dll
    intl.dll
    libgstapp-0.10.dll
    libgstaudio-0.10.dll
    libgstbase-0.10.dll
    libgstcdda-0.10.dll
    libgstcontroller-0.10.dll
    libgstdataprotocol-0.10.dll
    libgstdshow-0.10.dll
    libgstfft-0.10.dll
    libgstinterfaces-0.10.dll
    libgstnet-0.10.dll
    libgstnetbuffer-0.10.dll
    libgstpbutils-0.10.dll
    libgstreamer-0.10.dll
    libgstriff-0.10.dll
    libgstrtp-0.10.dll
    libgstrtsp-0.10.dll
    libgstsdp-0.10.dll
    libgsttag-0.10.dll
    libgstvideo-0.10.dll
    libjpeg.dll
    libmms.dll
    liboil-0.3-0.dll
    libpng13.dll
    xvidcore.dll
    zlib1.dll
    ogg.dll
    vorbis.dll
    )

copy_if_different(
    ${debug_src_dir} 
    "${CMAKE_CURRENT_BINARY_DIR}/Debug"
    out_targets 
    ${debug_files}
    )
set(all_targets ${all_targets} ${out_targets})

copy_if_different(
    ${vivox_src_dir} 
    "${CMAKE_CURRENT_BINARY_DIR}/Debug"
    out_targets 
    ${vivox_files}
    )
set(all_targets ${all_targets} ${out_targets})

set(release_src_dir "${CMAKE_SOURCE_DIR}/../libraries/i686-win32/lib/release")
set(release_files
    alut.dll
    freebl3.dll
    gksvggdiplus.dll
    js3250.dll
    nspr4.dll
    nss3.dll
    nssckbi.dll
    openal32.dll
    openjpeg.dll
    plc4.dll
    plds4.dll
    smime3.dll
    softokn3.dll
    ssl3.dll
    xpcom.dll
    xul.dll
    iconv.dll
    libxml2.dll
    libgio-2.0-0.dll
    libglib-2.0-0.dll
    libgmodule-2.0-0.dll
    libgobject-2.0-0.dll
    libgthread-2.0-0.dll
    avcodec-51.dll
    avformat-52.dll
    avutil-49.dll
    intl.dll
    libgstapp-0.10.dll
    libgstaudio-0.10.dll
    libgstbase-0.10.dll
    libgstcdda-0.10.dll
    libgstcontroller-0.10.dll
    libgstdataprotocol-0.10.dll
    libgstdshow-0.10.dll
    libgstfft-0.10.dll
    libgstinterfaces-0.10.dll
    libgstnet-0.10.dll
    libgstnetbuffer-0.10.dll
    libgstpbutils-0.10.dll
    libgstreamer-0.10.dll
    libgstriff-0.10.dll
    libgstrtp-0.10.dll
    libgstrtsp-0.10.dll
    libgstsdp-0.10.dll
    libgsttag-0.10.dll
    libgstvideo-0.10.dll
    libjpeg.dll
    libmms.dll
    liboil-0.3-0.dll
    libpng13.dll
    xvidcore.dll
    zlib1.dll
    ogg.dll
    vorbis.dll
    )
    
copy_if_different(
    ${release_src_dir} 
    "${CMAKE_CURRENT_BINARY_DIR}/Release"
    out_targets 
    ${release_files}
    )
set(all_targets ${all_targets} ${out_targets})

copy_if_different(
    ${vivox_src_dir} 
    "${CMAKE_CURRENT_BINARY_DIR}/Release"
    out_targets 
    ${vivox_files}
    )
set(all_targets ${all_targets} ${out_targets})

copy_if_different(
    ${release_src_dir} 
    "${CMAKE_CURRENT_BINARY_DIR}/RelWithDebInfo"
    out_targets 
    ${release_files}
    )
set(all_targets ${all_targets} ${out_targets})

copy_if_different(
    ${vivox_src_dir} 
    "${CMAKE_CURRENT_BINARY_DIR}/RelWithDebInfo"
    out_targets 
    ${vivox_files}
    )
set(all_targets ${all_targets} ${out_targets})


# Copy MS C runtime dlls, required for packaging.
# *TODO - Adapt this to support VC9
if (MSVC80)
    FIND_PATH(debug_msvc8_redist_path msvcr80d.dll
        PATHS
        [HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\VisualStudio\\8.0\\Setup\\VC;ProductDir]/redist/Debug_NonRedist/x86/Microsoft.VC80.DebugCRT
        )

    if(EXISTS ${debug_msvc8_redist_path})
        set(debug_msvc8_files
            msvcr80d.dll
            msvcp80d.dll
            Microsoft.VC80.DebugCRT.manifest
            )

        copy_if_different(
            ${debug_msvc8_redist_path} 
            "${CMAKE_CURRENT_BINARY_DIR}/Debug"
            out_targets 
            ${debug_msvc8_files}
            )
        set(all_targets ${all_targets} ${out_targets})
    endif (EXISTS ${debug_msvc8_redist_path})

    FIND_PATH(release_msvc8_redist_path msvcr80.dll
        PATHS
        [HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\VisualStudio\\8.0\\Setup\\VC;ProductDir]/redist/x86/Microsoft.VC80.CRT
        )

    if(EXISTS ${release_msvc8_redist_path})
        set(release_msvc8_files
            msvcr80.dll
            msvcp80.dll
            Microsoft.VC80.CRT.manifest
            )

        copy_if_different(
            ${release_msvc8_redist_path} 
            "${CMAKE_CURRENT_BINARY_DIR}/Release"
            out_targets 
            ${release_msvc8_files}
            )
        set(all_targets ${all_targets} ${out_targets})

        copy_if_different(
            ${release_msvc8_redist_path} 
            "${CMAKE_CURRENT_BINARY_DIR}/RelWithDebInfo"
            out_targets 
            ${release_msvc8_files}
            )
        set(all_targets ${all_targets} ${out_targets})

    endif (EXISTS ${release_msvc8_redist_path})
endif (MSVC80)

add_custom_target(copy_win_libs ALL DEPENDS ${all_targets})
