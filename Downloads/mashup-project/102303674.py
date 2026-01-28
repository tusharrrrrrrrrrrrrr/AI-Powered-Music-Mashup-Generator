import sys
from mashup_engine import create_mashup

def main():
    if len(sys.argv) != 5:
        print("Usage: python <file.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]
    try:
        n = int(sys.argv[2])
        duration = int(sys.argv[3])
    except:
        print("NumberOfVideos and AudioDuration must be integers")
        sys.exit(1)

    if n <= 10 or duration <= 20:
        print("NumberOfVideos must be >10 and AudioDuration >20")
        sys.exit(1)

    output = sys.argv[4]

    try:
        path = create_mashup(singer, n, duration, output)
        print("Mashup created at:", path)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
