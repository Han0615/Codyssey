print("Hello Mars")

def read_log(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            contents = file.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: '{filename}'")
    except PermissionError:
        print(f"[ERROR] Permission denied: '{filename}'")
    except UnicodeDecodeError:
        print(f"[ERROR] Failed to decode file: '{filename}'")
    except OSError as e:
        print(f"[ERROR] OS error occurred: {e}")
    else:
        print(contents)
    finally:
        print("Log reading process complete.")

def main():
    log_filename = 'mission_computer_main.log'
    read_log(log_filename)

if __name__ == '__main__':
    main()