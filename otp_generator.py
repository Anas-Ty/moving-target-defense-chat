    import hmac
    import hashlib
    import struct
    import time


    def generate_token(secret_key, time_interval=10):
        # 1) Get the time window (changes every 10 seconds)
        time_window = int(time.time()) // time_interval

        # 2) Convert that window into bytes (stable format)
        msg = struct.pack(">Q", time_window)

        # 3) HMAC-SHA256(secret_key, msg) -> unpredictable without the secret
        digest = hmac.new(secret_key.encode(), msg, hashlib.sha256).digest()

        # 4) Turn digest into a big integer
        num = int.from_bytes(digest, "big")

        # 5) Map into valid port range [1024, 65535]
        min_port = 1024
        max_port = 65535
        port = min_port + (num % (max_port - min_port))
        return port


    if __name__ == "__main__":
        while True:
            print(generate_token("project_phantom_key"))
            time.sleep(1)
