import dotenv
from src.Classes.Bots import PodcastToShorts 
dotenv.load_dotenv('.env')

def main():
    podcastToShorts = PodcastToShorts(podcast_url="https://youtu.be/nDLb8_wgX50?si=d8jgLM_KO68OZHZI")

    shorts = podcastToShorts.get_shorts()
    print(shorts)

if "__name__" == "__main__":
   main()
