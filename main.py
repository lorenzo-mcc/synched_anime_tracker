from script.anilist_fetcher import fetch_anime_info
from script.formatter import format_data_for_notion
from script.notion_updater import create_notion_page
import re


def split_title_and_season(title: str):
    """
    Splits the title into:
    - Main title (used for AniList search).
    - Full title (used for season parsing in the formatter).
    """
    match = re.match(r"^(.*?)\s*(\((.*?)\))?$", title.strip())
    if match:
        main_title = match.group(1).strip()  # Part before the parentheses
        return main_title, title.strip()  # Main title, full title
    return title.strip(), title.strip()


def main():
    # Notion database IDs
    database_id = "13ac92f4c7428010b10df03b4d511b55"
    genre_database_id = "13ac92f4c742801bb860fa7b58fd850f"

    # File containing anime titles
    file_path = "script/anime_list.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # Read anime titles and split them into main and full titles
            anime_data = [split_title_and_season(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return

    # Process each anime in the list
    for main_title, full_title in anime_data:
        print(f"\nSearching for information about '{main_title}'...")
        anime_results = fetch_anime_info(main_title)

        if not anime_results:
            print(f"\033[43mNo results found for '{main_title}'..\033[0m")
            continue

        print("\nResults found:")

        # Sort results by format (TV first) and then by year (ascending)
        anime_results_sorted = sorted(
            anime_results,
            key=lambda x: (
                0 if (x.get('format') or "").upper() == "TV" else 1,  # TV first
                x.get('startDate', {}).get('year') or float('inf')  # Use float('inf') if year is None
            )
        )

        # Display sorted results
        for i, anime in enumerate(anime_results_sorted, start=1):
            title_romaji = anime.get('title', {}).get('romaji', 'Unknown')
            title_english = anime.get('title', {}).get('english', 'Unknown')
            start_year = anime.get('startDate', {}).get('year', 'Unknown')
            anime_format = anime.get('format', 'Unknown')
            status = anime.get('status', 'Unknown')
            print(f"{i}. {title_romaji} / {title_english} - Format: {anime_format}, Status: {status}, Year: {start_year}")

        # Allow user to select an anime or skip
        choice = input("\nSelect a number (or 'skip' to skip this title): ").strip()
        if choice.lower() == 'skip':
            continue

        try:
            choice = int(choice)
            if choice < 1 or choice > len(anime_results_sorted):
                print("Error: Invalid selection.")
                continue

            selected_anime = anime_results_sorted[choice - 1]

            # Format data for Notion and parse season from the full title
            formatted_data = format_data_for_notion(selected_anime, full_title)

            print("\nData prepared for Notion:")
            for key, value in formatted_data.items():
                print(f"{key}: {value}")

            # Create the page in Notion
            create_notion_page(database_id, formatted_data, genre_database_id)

        except ValueError:
            print("Error: Please enter a valid number.")
            continue


if __name__ == "__main__":
    main()
