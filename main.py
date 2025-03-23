from server import serve

if __name__ == "__main__":
    try:
        serve()
    except Exception as e:
        print(f"Fatal error: {e}")