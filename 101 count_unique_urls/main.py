from typing import Dict

def normalize_url(url: str) -> str:
    # Extract protocol
    protocol, rest = url.split("://", 1)
    
    # Delete www, if available
    if rest.startswith("www."):
        rest = rest[4:]
    
    # Try to split by '?'
    parts = rest.split("?", 1)
    if len(parts) == 2:
        domain_and_path, query = parts
        domain_part, path_part = (domain_and_path.split("/", 1) + [""])[:2]
        path_and_query = path_part + "?" + query
    else:
        domain_part, path_and_query = (rest.split("/", 1) + [""])[:2]
    
    # Check if URL has params; if so, sort them
    if '?' in path_and_query:
        path, query = path_and_query.split('?', 1)
        if query:
            params = [tuple(p.split('=', 1)) for p in query.split('&') if '=' in p]
            sorted_query = '&'.join(f"{k}={v}" for k, v in sorted(params))
            path_and_query = path + '?' + sorted_query
        else:
            path_and_query = path  # If no params after '?', return path
    else:
        # Delete final "/" in path if no "?"
        path_and_query = path_and_query.rstrip('/')
    
    # Rebuild URL
    return f"{protocol}://{domain_part}/{path_and_query}"

def get_top_level_domain(url: str) -> str:
    # Check if URL starts with a scheme
    if "://" not in url:
        url = "http://" + url

    # Extract domain
    domain = url.split("://", 1)[1].split("/", 1)[0]
    
    # Get high-level domain
    return ".".join(domain.split(".")[-2:])

"""
* This function counts how many unique normalized valid URLs were passed to the function
*
* Accepts a list of URLs
*
* Example:
*
* input: ['https://example.com']
* output: 1
*
* Notes:
*  - assume none of the URLs have authentication information (username, password).
*
* Normalized URL:
*  - process in which a URL is modified and standardized: https://en.wikipedia.org/wiki/URL_normalization
*
#    For example.
#    These 2 urls are the same:
#    input: ["https://example.com", "https://example.com/"]
#    output: 1
#
#    These 2 are not the same:
#    input: ["https://example.com", "http://example.com"]
#    output 2
#
#    These 2 are the same:
#    input: ["https://example.com?", "https://example.com"]
#    output: 1
#
#    These 2 are the same:
#    input: ["https://example.com?a=1&b=2", "https://example.com?b=2&a=1"]
#    output: 1
"""

def count_unique_urls(urls: list[str]) -> int:
    # print(({normalize_url(url) for url in urls}))
    return len({normalize_url(url) for url in urls})


"""
 * This function counts how many unique normalized valid URLs were passed to the function per top level domain
 *
 * A top level domain is a domain in the form of example.com. Assume all top level domains end in .com
 * subdomain.example.com is not a top level domain.
 *
 * Accepts a list of URLs
 *
 * Example:
 *
 * input: ["https://example.com"]
 * output: Hash["example.com" => 1]
 *
 * input: ["https://example.com", "https://subdomain.example.com"]
 * output: Hash["example.com" => 2]
 *
"""

def count_unique_urls_per_top_level_domain(urls: list[str]) -> Dict[str, int]:
    # Normalize URLs and extract domain and path (no params)
    normalized_urls = {normalize_url(url).split('?')[0] for url in urls}
    
    # Create a dict so as to count URLs by domain
    domain_count = {}
    
    for url in normalized_urls:
        protocol, rest = url.split("://", 1)
        domain = rest.split("/", 1)[0]
        top_level_domain = ".".join(domain.split(".")[-2:])
        
        if top_level_domain not in domain_count:
            domain_count[top_level_domain] = 0
        domain_count[top_level_domain] += 1

    return domain_count

if __name__ == "__main__":
    # Test count_unique_urls

    assert count_unique_urls(["https://example.com"]) == 1
    assert count_unique_urls(["https://example.com", "https://example.com/"]) == 1
    assert count_unique_urls(["https://example.com", "http://example.com"]) == 2
    assert count_unique_urls(["https://example.com?a=1&b=2", "https://example.com?b=2&a=1"]) == 1
    assert count_unique_urls(["https://example.com?", "https://example.com"]) == 1

    # Test count_unique_urls_per_top_level_domain

    assert count_unique_urls_per_top_level_domain(["https://example.com"]) == {"example.com": 1}
    assert count_unique_urls_per_top_level_domain(["https://example.com", "https://sub.example.com"]) == {"example.com": 2}
    assert count_unique_urls_per_top_level_domain(["https://example.com", "https://test.org"]) == {"example.com": 1, "test.org": 1}
    assert count_unique_urls_per_top_level_domain(["https://example.com?a=1", "https://example.com?b=2"]) == {"example.com": 1}

    print("¡All tests were successful!")