from ddgs import DDGS


def search_duckduckgo(query, max_results=10):
    backends = [
        "bing",
        "brave",
        "yahoo",
        "duckduckgo",
        "yandex",
    ]

    for backend in backends:
        try:
            print(f"Trying backend: {backend}")

            results = DDGS().text(
                query,
                max_results=max_results,
                backend=backend,
            )

            results = list(results)

            if results:
                print(f"Success with {backend}: {len(results)} results")
                return results

        except Exception as e:
            print(f"{backend} failed: {e}")

    return []