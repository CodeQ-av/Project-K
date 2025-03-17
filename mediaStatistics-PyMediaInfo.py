import os
from pymediainfo import MediaInfo

def get_video_stats(file_path):
    """Extract and format video/audio/file metadata using MediaInfo."""
    media_info = MediaInfo.parse(file_path)
    stats = {
        "General": {},
        "Video": [],
        "Audio": [],
        "File": {}
    }

    # Extract metadata from tracks
    for track in media_info.tracks:
        if track.track_type == "General":
            stats["General"] = {
                "Format": track.format,
                "FileSize": f"{os.path.getsize(file_path) / (1024 * 1024):.2f} MB",
                "Duration": f"{track.duration / 60000:.2f} minutes",
                "Metadata": {
                    "Encoded_Date": track.encoded_date if hasattr(track, 'encoded_date') else None,
                    "Title": track.title if hasattr(track, 'title') else None,
                }
            }
        elif track.track_type == "Video":
            video_stats = {
                "Resolution": f"{track.width}x{track.height}",
                "Aspect_Ratio": track.display_aspect_ratio if hasattr(track, 'display_aspect_ratio') else "N/A",
                "Frame_Rate": f"{track.frame_rate} fps" if hasattr(track, 'frame_rate') else "N/A",
                "Scan_Type": "Progressive" if track.scan_type == "Progressive" else "Interlaced",
                "Bitrate": f"{int(track.bit_rate)/1000:.2f} kbps" if hasattr(track, 'bit_rate') else "N/A",
                "Codec": track.codec_id,
                "Color_Depth": f"{track.bit_depth}-bit" if hasattr(track, 'bit_depth') else "N/A",
                "Chroma_Subsampling": track.chroma_subsampling if hasattr(track, 'chroma_subsampling') else "N/A",
                "HDR": track.hdr_format if hasattr(track, 'hdr_format') else "Not detected"
            }
            stats["Video"].append(video_stats)
        elif track.track_type == "Audio":
            audio_stats = {
                "Codec": track.format,
                "Channels": track.channel_s,
                "Sample_Rate": f"{track.sampling_rate / 1000:.1f} kHz",
                "Bit_Depth": f"{track.bit_depth}-bit" if hasattr(track, 'bit_depth') else "N/A",
                "Bitrate": f"{int(track.bit_rate)/1000:.2f} kbps" if hasattr(track, 'bit_rate') else "N/A"
            }
            stats["Audio"].append(audio_stats)

    # File-specific stats
    stats["File"] = {
        "Path": file_path,
        "Container": stats["General"]["Format"],
        "Size": stats["General"]["FileSize"],
        "Duration": stats["General"]["Duration"]
    }

    return stats

# Example usage
if __name__ == "__main__":
    file_path = "SampleVideo.mp4" 
    stats = get_video_stats(file_path)
    
    # Print formatted output
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(stats)