import os
import logging



if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
    )

    vk_token = os.environ["VK_API_KEY"]
