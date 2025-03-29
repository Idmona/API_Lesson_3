import argparse
import requests
import os
import sys
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(token, url):
    parsed_url = urlparse(url)
    if parsed_url.netloc != "vk.cc":
        return False

    if not parsed_url.path.strip("/"):
        return False

    response = requests.get(
        "https://api.vk.com/method/utils.checkLink",
        params={
            "url": url,
            "access_token": token,
            "v": "5.131"
        }
    )
    response.raise_for_status()
    response_data = response.json()

    if "error" in response_data:
        error_msg = response_data["error"].get("error_msg", "Unknown error")
        raise requests.exceptions.HTTPError(
            f"{error_msg} (Code: {response_data['error'].get('error_code', 'Unknown')})")

    return response_data.get("response", {}).get("link_type") == "shortened"


def shorten_link(token, url):
    response = requests.get(
        "https://api.vk.com/method/utils.getShortLink",
        params={
            "url": url,
            "access_token": token,
            "v": "5.131"
        }
    )
    response.raise_for_status()
    response_data = response.json()

    if "error" in response_data:
        error_msg = response_data["error"].get("error_msg", "Unknown error")
        raise requests.exceptions.HTTPError(
            f"{error_msg} (Code: {response_data['error'].get('error_code', 'Unknown')})")

    return response_data["response"]["short_url"]


def count_clicks(token, short_url):
    parsed_url = urlparse(short_url)
    link_key = parsed_url.path.lstrip('/')

    response = requests.get(
        "https://api.vk.com/method/utils.getLinkStats",
        params={
            "key": link_key,
            "access_token": token,
            "v": "5.131",
            "interval": "forever"
        }
    )
    response.raise_for_status()
    response_data = response.json()

    if "error" in response_data:
        error_msg = response_data["error"].get("error_msg", "Unknown error")
        raise requests.exceptions.HTTPError(
            f"{error_msg} (Code: {response_data['error'].get('error_code', 'Unknown')})")

    return sum(period.get("clicks", 0) for period in response_data.get("response", {}).get("stats", []))


def main():
    load_dotenv()
    token = os.environ.get("VK_API_TOKEN")

    if not token:
        print("Ошибка: Токен не найден")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Сокращение ссылок и подсчёт кликов через VK API")
    parser.add_argument("url", help="Ссылка для обработки")
    args = parser.parse_args()

    try:
        if is_shorten_link(token, args.url):
            clicks = count_clicks(token, args.url)
            print(f"Общее количество кликов за всё время: {clicks}")
        else:
            short_url = shorten_link(token, args.url)
            print(f"Сокращённая ссылка: {short_url}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка API: {str(e)}")
    except ValueError as e:
        print(f"Ошибка ввода: {str(e)}")
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    finally:
        sys.exit(1)


if __name__ == "__main__":
    main()
