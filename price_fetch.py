#!/usr/bin/env python3
"""
Fetch live NQ futures price from Yahoo Finance.
Outputs just the price number to stdout.
"""

import sys
import json
import signal
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import time

# NQ futures symbol on Yahoo Finance
SYMBOL = "NQ=F"
API_URL = f"https://query2.finance.yahoo.com/v8/finance/chart/{SYMBOL}?range=1d&interval=1m"


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Request timed out")


def fetch_price():
    """Fetch NQ futures price from Yahoo Finance with 10s timeout."""
    # Set 10 second timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(10)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = Request(API_URL, headers=headers)
        response = urlopen(req, timeout=10)
        data = json.loads(response.read().decode())

        signal.alarm(0)  # Cancel the alarm

        # Extract price from Yahoo Finance response
        try:
            result = data['chart']['result'][0]
            meta = result['meta']
            price = meta.get('regularMarketPrice') or meta.get('previousClose')

            if price is None:
                # Try to get from indicators
                indicators = result.get('indicators', {})
                quote = indicators.get('quote', [{}])[0]
                closes = quote.get('close', [])
                # Get last non-null close
                for c in reversed(closes):
                    if c is not None:
                        price = c
                        break

            if price is not None:
                print(f"{price:.2f}")
                return 0
            else:
                print("ERROR: No price data available", file=sys.stderr)
                return 1
        except (KeyError, IndexError, TypeError) as e:
            print(f"ERROR: Failed to parse response: {e}", file=sys.stderr)
            return 1

    except TimeoutError:
        print("ERROR: Request timed out after 10 seconds", file=sys.stderr)
        return 1
    except HTTPError as e:
        print(f"ERROR: HTTP {e.code}: {e.reason}", file=sys.stderr)
        return 1
    except URLError as e:
        print(f"ERROR: Network error: {e.reason}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid response format: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        return 1
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    sys.exit(fetch_price())
