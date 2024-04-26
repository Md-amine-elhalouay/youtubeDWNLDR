from pytube import YouTube
import requests
import os

class MusicDownloader():
    def __init__(self):
        super(MusicDownloader, self).__init__()
        self.musixmatch_api_key = "882e68fc39688c3ca0c71d752e4e19a8" 

    def download_song_with_lyrics(self, youtube_url, output_folder):
        try:
            print("Downloading YouTube video...")
            yt = YouTube(youtube_url)
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(output_folder)
            print("YouTube video downloaded successfully.")

            song_title = yt.title
            artist_name = yt.author

            print("Fetching lyrics...")
            lyrics = self.get_lyrics(song_title, artist_name)

            if lyrics:
                lyrics_filename = os.path.join(output_folder, f'{song_title} - Lyrics.txt')
                with open(lyrics_filename, "w") as lyrics_file:
                    lyrics_file.write(lyrics)
                print("Lyrics saved to file.")
            else:
                print("No lyrics found.")
        except Exception as e:
            print(f"Error: {e}")

    def get_lyrics(self, track_title, artist_name):
        try:
            url = f"https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?apikey={self.musixmatch_api_key}&q_track={track_title}&q_artist={artist_name}&format=json"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "body" in data["message"] and "lyrics" in data["message"]["body"]:
                    lyrics_body = data["message"]["body"]["lyrics"]["lyrics_body"]
                    return lyrics_body
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(f"Error fetching lyrics: {e}")

# Example usage
if __name__ == "__main__":
    downloader = MusicDownloader()
    youtube_url = "https://youtu.be/AIOAlaACuv4" 
    output_folder = "path/to/output/folder" 
    downloader.download_song_with_lyrics(youtube_url, output_folder)
