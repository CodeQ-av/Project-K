import ffmpeg

def get_video_stats(file_path):
    # Get video metadata using ffmpeg
    probe = ffmpeg.probe(file_path, v='error', select_streams='v:0', show_entries='stream=width,height,codec_name,codec_long_name,r_frame_rate,bit_rate,sample_fmt,sample_rate')
    
    # Extract video stream details
    video_stream = probe['streams'][0]
    
    width = video_stream['width']
    height = video_stream['height']
    codec_name = video_stream['codec_name']
    codec_long_name = video_stream['codec_long_name']
    frame_rate = video_stream['r_frame_rate']
    bitrate = video_stream['bit_rate']
    
    # Handle variable frame rate (VFR)
    frame_rate = frame_rate.split('/')[0] if frame_rate else "Unknown"

    # Printing video statistics
    print(f"Video Resolution: {width}x{height}")
    print(f"Codec: {codec_long_name} ({codec_name})")
    print(f"Frame Rate: {frame_rate} fps")
    print(f"Bitrate: {bitrate} bps")

    # Optionally, you can also extract audio data if needed
    # audio_stream = probe['streams'][1] if len(probe['streams']) > 1 else None
    # if audio_stream:
    #     sample_rate = audio_stream.get('sample_rate', 'N/A')
    #     print(f"Audio Sample Rate: {sample_rate} Hz")

    return {
        "Resolution": f"{width}x{height}",
        "Codec": codec_long_name,
        "Frame Rate": frame_rate,
        "Bitrate": bitrate
    }

# Replace with your video file path
file_path = 'SampleVideo.mp4'
video_stats = get_video_stats(file_path)
