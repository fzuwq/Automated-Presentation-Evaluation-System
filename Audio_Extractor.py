import moviepy.editor

def extract_audio_from_video(video_path, output_audio_path):
    moviepy.video.io.ffmpeg_tools.ffmpeg_extract_audio(video_path,output_audio_path)