"""
Taobao/Tmall "蕉内" (Bananain) Product Scraper
==============================================
Uses Playwright sync API to scrape product data from Taobao SEM search pages.
No login required for the first ~6 pages.
"""

import csv
import json
import logging
import random
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ── Configuration ──────────────────────────────────────────────────────────────
KEYWORD = "蕉内"
MAX_PAGES = 6
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = OUTPUT_DIR / "taobao_bananain_products.csv"
JSON_PATH = OUTPUT_DIR / "taobao_bananain_products.json"

URL_TEMPLATE = (
    "https://uland.taobao.com/sem/tbsearch"
    "?keyword={keyword}&q={keyword}&search_type=item"
    "&sourceId=tb.index&tab=all&page={page}"
)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("taobao_scraper")


# ── Helper: detect login redirect ────────────────────────────────────────────
def is_login_page(page) -> bool:
    """Return True when the browser has been redirected to a login page."""
    title = page.title().lower()
    url = page.url.lower()
    if "登录" in title or "login" in title:
        return True
    if "login.taobao" in url or "login.tmall" in url:
        return True
    return False


# ── Extraction logic (multiple selector strategies) ───────────────────────────
def extract_products(page, page_num: int) -> list[dict]:
    """
    Try several CSS selector strategies to pull product card data from the
    current search results page.  Returns a list of dicts.
    """
    strategies = [
        _extract_strategy_card_double,
        _extract_strategy_content_inner,
        _extract_strategy_generic_cards,
        _extract_strategy_js_eval,
    ]

    for idx, strategy in enumerate(strategies, 1):
        try:
            products = strategy(page, page_num)
            if products:
                log.info(f"  Strategy #{idx} succeeded: {len(products)} products")
                return products
        except Exception as exc:
            log.debug(f"  Strategy #{idx} failed: {exc}")

    log.warning(f"  All strategies failed for page {page_num}")
    return []


# Strategy 1 -- Card--doubleCard (modern React-based layout)
def _extract_strategy_card_double(page, page_num: int) -> list[dict]:
    cards = page.query_selector_all('[class*="Card--doubleCard"]')
    if not cards:
        return []
    products = []
    for card in cards:
        product = _parse_card_element(card, page_num)
        if product and product.get("title"):
            products.append(product)
    return products


# Strategy 2 -- Content--contentInner wrapper (element-based with smart text split)
def _extract_strategy_content_inner(page, page_num: int) -> list[dict]:
    cards = page.query_selector_all('[class*="Content--contentInner"] a[href*="detail"]')
    if not cards:
        cards = page.query_selector_all('[class*="Content--content"] a[href*="item"]')
    if not cards:
        return []
    products = []
    for card in cards:
        product = _parse_link_card(card, page_num)
        if product and product.get("title"):
            products.append(product)
    return products


# Strategy 3 -- Generic card-like containers with price info
def _extract_strategy_generic_cards(page, page_num: int) -> list[dict]:
    # Try multiple generic selectors
    selectors = [
        '[class*="item"]',
        '[class*="card"]',
        '[class*="Card"]',
        '[class*="product"]',
        '[class*="Product"]',
    ]
    cards = []
    for sel in selectors:
        cards = page.query_selector_all(sel)
        if len(cards) >= 10:
            break

    if len(cards) < 5:
        return []

    products = []
    for card in cards:
        product = _parse_card_element(card, page_num)
        if product and product.get("title"):
            products.append(product)
    return products


# Strategy 4 -- Full JS evaluation (most robust, extracts from rendered DOM)
def _extract_strategy_js_eval(page, page_num: int) -> list[dict]:
    products = page.evaluate("""
    () => {
        const results = [];
        // Find all anchor tags that look like product links
        const links = document.querySelectorAll(
            'a[href*="detail.tmall"], a[href*="item.taobao"], '
            + 'a[href*="detail.taobao"], a[href*="click.simba"], '
            + 'a[href*="item.htm"], a[href*="detail.1688"]'
        );
        const seen = new Set();
        for (const link of links) {
            const href = link.href || '';
            if (seen.has(href)) continue;
            seen.add(href);

            // Walk up to find the card container (look for an element with price text)
            let card = link;
            for (let i = 0; i < 8; i++) {
                if (card.parentElement) card = card.parentElement;
                else break;
            }

            // Extract title: look for long text inside the link or card
            let title = '';
            const titleEl = link.querySelector('span, div, p');
            if (titleEl) {
                // Find the element with the longest text
                const allTextEls = link.querySelectorAll('span, div, p');
                let maxLen = 0;
                for (const el of allTextEls) {
                    const t = (el.textContent || '').trim();
                    if (t.length > maxLen && t.length > 4) {
                        maxLen = t.length;
                        title = t;
                    }
                }
            }
            if (!title) {
                title = (link.getAttribute('title') || link.textContent || '').trim();
            }
            if (title.length < 4) continue;

            // Extract price
            let price = '';
            const priceMatch = card.textContent.match(/[\\u00a5\\uffe5]?\\s*(\\d+\\.?\\d*)/);
            if (priceMatch) price = priceMatch[1];

            // Extract image
            let img = '';
            const imgEl = link.querySelector('img') || card.querySelector('img');
            if (imgEl) img = imgEl.src || imgEl.getAttribute('data-src') || '';

            // Extract shop name - look for small text near the bottom of the card
            let shop = '';
            const shopEls = card.querySelectorAll(
                '[class*="shop"], [class*="Shop"], [class*="store"], [class*="Store"], '
                + '[class*="seller"], [class*="Seller"]'
            );
            for (const el of shopEls) {
                const t = (el.textContent || '').trim();
                if (t.length > 1 && t.length < 50) { shop = t; break; }
            }

            results.push({
                title: title.substring(0, 200),
                price: price,
                shop: shop,
                link: href,
                image: img,
            });
        }
        return results;
    }
    """)

    result = []
    for p in products:
        result.append({
            "title": p.get("title", "").strip(),
            "price": p.get("price", "").strip(),
            "shop": p.get("shop", "").strip(),
            "link": p.get("link", "").strip(),
            "image": p.get("image", "").strip(),
            "page": page_num,
        })
    return result


# ── Element-level parsers ─────────────────────────────────────────────────────
def _parse_card_element(card, page_num: int) -> dict | None:
    """Parse a generic card element for product data."""
    try:
        # Title
        title = ""
        title_el = card.query_selector(
            '[class*="title"], [class*="Title"], '
            '[class*="name"], [class*="Name"]'
        )
        if title_el:
            title = title_el.inner_text().strip()
        if not title:
            title = (card.get_attribute("title") or "").strip()
        if not title:
            # Try getting longest text from links
            link_el = card.query_selector("a")
            if link_el:
                title = (link_el.get_attribute("title") or link_el.inner_text() or "").strip()

        # Link
        link = ""
        link_el = card.query_selector("a[href]")
        if link_el:
            raw_href = link_el.get_attribute("href") or ""
            if raw_href.startswith("//"):
                raw_href = "https:" + raw_href
            elif raw_href.startswith("/"):
                raw_href = urljoin("https://www.taobao.com", raw_href)
            link = raw_href

        # Price
        price = ""
        price_el = card.query_selector(
            '[class*="price"], [class*="Price"], '
            '[class*="amount"], [class*="Amount"]'
        )
        if price_el:
            price = price_el.inner_text().strip()
            # Clean price: keep only numeric + dot
            import re
            m = re.search(r'(\d+\.?\d*)', price)
            price = m.group(1) if m else price

        # Image
        image = ""
        img_el = card.query_selector("img")
        if img_el:
            image = (
                img_el.get_attribute("src")
                or img_el.get_attribute("data-src")
                or ""
            )
            if image.startswith("//"):
                image = "https:" + image

        # Shop
        shop = ""
        shop_el = card.query_selector(
            '[class*="shop"], [class*="Shop"], '
            '[class*="store"], [class*="Store"], '
            '[class*="seller"], [class*="Seller"]'
        )
        if shop_el:
            shop = shop_el.inner_text().strip()

        if title and len(title) > 2:
            return {
                "title": title[:200],
                "price": price,
                "shop": shop,
                "link": link,
                "image": image,
                "page": page_num,
            }
    except Exception:
        pass
    return None


def _parse_link_card(link_el, page_num: int) -> dict | None:
    """Parse a link-based card element, splitting combined text into fields."""
    try:
        raw_text = (
            link_el.get_attribute("title")
            or link_el.inner_text()
            or ""
        ).strip()

        href = link_el.get_attribute("href") or ""
        if href.startswith("//"):
            href = "https:" + href

        image = ""
        img_el = link_el.query_selector("img")
        if img_el:
            image = img_el.get_attribute("src") or img_el.get_attribute("data-src") or ""
            if image.startswith("//"):
                image = "https:" + image

        if raw_text and len(raw_text) > 2:
            title, price, shop = _split_card_text(raw_text)
            return {
                "title": title,
                "price": price,
                "shop": shop,
                "link": href,
                "image": image,
                "page": page_num,
            }
    except Exception:
        pass
    return None


def _split_card_text(raw: str) -> tuple[str, str, str]:
    """
    Split a combined card text block into (title, price, shop).

    Typical raw text pattern from Taobao SEM results:
        Product title line 1
        Optional tag/label
        ...badges...
        ¥
        89.00
        Province
        City
        ...service badges...
        X年老店ShopName
    """
    lines = [l.strip() for l in raw.split("\n") if l.strip()]

    # ── Extract price ──────────────────────────────────────────────────────
    price = ""
    price_idx = -1
    for i, line in enumerate(lines):
        m = re.match(r'^[¥￥]\s*$', line)
        if m and i + 1 < len(lines):
            # Next line should be the price number
            pm = re.match(r'^(\d+\.?\d*)$', lines[i + 1])
            if pm:
                price = pm.group(1)
                price_idx = i
                break
        # Also try inline price like ¥89.00
        m2 = re.match(r'^[¥￥]\s*(\d+\.?\d*)$', line)
        if m2:
            price = m2.group(1)
            price_idx = i
            break

    # ── Extract shop name ──────────────────────────────────────────────────
    shop = ""
    shop_idx = -1
    # Look from the end for shop-like patterns
    shop_patterns = [
        re.compile(r'(\d+年老店.+)$'),           # "9年老店Bananain蕉内旗舰店"
        re.compile(r'(.+(?:旗舰店|专卖店|官方店|专营店|企业店).*)$'),
        re.compile(r'(.+旗舰店)$'),
        re.compile(r'(Bananain.+)$'),
        re.compile(r'(.+店)$'),
    ]
    for i in range(len(lines) - 1, -1, -1):
        for pat in shop_patterns:
            m = pat.search(lines[i])
            if m:
                shop = m.group(1).strip()
                # Clean up: remove leading badges like "9年老店" prefix if already in shop
                shop_idx = i
                break
        if shop:
            break

    # ── Extract title ──────────────────────────────────────────────────────
    # Title is typically the first line of text in the card.
    # The first line is the actual product name; subsequent lines are
    # badges, rankings, attributes, price, shop info, etc.
    # Some products have the title split across 2 lines, so we take up
    # to 2 lines but stop at the first "non-title" line.
    title_lines = []
    # These patterns mean the line is NOT part of the title
    non_title_patterns = [
        r'^[¥￥]',                             # price symbol
        r'^\d+\.?\d*$',                        # bare number (price)
        r'^榜[·.]',                             # ranking badge
        r'热卖',                                # hot-selling badge
        r'^\d+年老店',                          # shop age badge
        r'^(浙江|广东|上海|北京|江苏|福建|四川|山东|湖北|安徽|河南|河北)',  # province
        r'^(杭州|深圳|广州|上海|北京|南京|成都|武汉|苏州)',     # city
        r'^(退货宝|包邮|正品|7天|假一赔)',       # service badges
        r'^(Bananain|蕉内).*(?:旗舰店|专卖店|官方店)',  # full shop name
    ]

    for i, line in enumerate(lines):
        if i == price_idx or i == price_idx + 1:
            break
        if i == shop_idx:
            break

        # Check if this line is a non-title line
        is_non_title = False
        for pat in non_title_patterns:
            if re.search(pat, line):
                is_non_title = True
                break

        if is_non_title and len(title_lines) > 0:
            # We already have title, stop here
            break
        if is_non_title:
            # Haven't found title yet, skip this line and keep looking
            continue

        if len(line) >= 4:
            title_lines.append(line)
        elif len(line) >= 2 and len(title_lines) > 0:
            # Short continuation line, might be part of title
            title_lines[-1] += line
        # If first title line is already long enough (typical product title),
        # don't collect more lines - they're likely attribute tags
        if title_lines and len(title_lines[0]) >= 15:
            break
        # Stop at 2 lines max for title
        if len(title_lines) >= 2:
            break

    title = " ".join(title_lines) if title_lines else (lines[0] if lines else "")
    title = title[:200]

    return title, price, shop


# ── Main scraper ──────────────────────────────────────────────────────────────
def scrape_taobao():
    all_products: list[dict] = []
    pages_scraped = 0
    pages_failed = 0
    start_time = time.time()

    log.info("=" * 60)
    log.info("Taobao Scraper - Keyword: %s", KEYWORD)
    log.info("Pages to scrape: %d", MAX_PAGES)
    log.info("=" * 60)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )

        # Stealth: remove webdriver flag
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en'],
            });
        """)

        page = context.new_page()

        for page_num in range(1, MAX_PAGES + 1):
            url = URL_TEMPLATE.format(keyword=KEYWORD, page=page_num)
            log.info("\n--- Page %d/%d ---", page_num, MAX_PAGES)
            log.info("URL: %s", url)

            try:
                # Navigate
                page.goto(url, wait_until="domcontentloaded", timeout=30000)

                # Extra wait for dynamic content
                page.wait_for_timeout(3000)

                # Scroll down to trigger lazy-loading
                for _ in range(3):
                    page.evaluate("window.scrollBy(0, window.innerHeight)")
                    page.wait_for_timeout(500)
                # Scroll back to top
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(500)

                # Check for login redirect
                if is_login_page(page):
                    log.warning(
                        "Login redirect detected on page %d! "
                        "Title: '%s', URL: %s. Stopping.",
                        page_num, page.title(), page.url,
                    )
                    break

                # Extract products
                products = extract_products(page, page_num)

                if products:
                    all_products.extend(products)
                    pages_scraped += 1
                    log.info(
                        "Page %d: extracted %d products (total: %d)",
                        page_num, len(products), len(all_products),
                    )
                else:
                    pages_failed += 1
                    log.warning(
                        "Page %d: no products found. "
                        "Saving page screenshot for debugging.",
                        page_num,
                    )
                    debug_path = OUTPUT_DIR / f"debug_page_{page_num}.png"
                    page.screenshot(path=str(debug_path), full_page=True)
                    log.info("Screenshot saved: %s", debug_path)

                    # If even page 1 fails, the site structure may have changed
                    if page_num == 1:
                        log.error(
                            "First page returned 0 products. "
                            "The page structure may have changed. Stopping."
                        )
                        break

            except PlaywrightTimeout:
                pages_failed += 1
                log.error("Page %d: timeout after 30s", page_num)
            except Exception as exc:
                pages_failed += 1
                log.error("Page %d: error - %s", page_num, exc)

            # Rate limiting: random delay between pages (skip after last page)
            if page_num < MAX_PAGES:
                delay = random.uniform(3.0, 5.0)
                log.info("Sleeping %.1fs ...", delay)
                time.sleep(delay)

        browser.close()

    elapsed = time.time() - start_time

    # ── Deduplicate by item ID (extracted from URL) ─────────────────────────
    seen_ids: set[str] = set()
    unique_products: list[dict] = []
    for p in all_products:
        link = p.get("link", "")
        # Extract item ID from URL like ...item.htm?id=546670945516&...
        id_match = re.search(r'[?&]id=(\d+)', link)
        key = id_match.group(1) if id_match else (link or p.get("title", ""))
        if key and key not in seen_ids:
            seen_ids.add(key)
            unique_products.append(p)

    log.info("\nDeduplication: %d -> %d products", len(all_products), len(unique_products))
    all_products = unique_products

    # ── Save CSV ───────────────────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if all_products:
        fieldnames = ["title", "price", "shop", "link", "image", "page"]
        with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_products)
        log.info("CSV saved: %s (%d rows)", CSV_PATH, len(all_products))

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(all_products, f, ensure_ascii=False, indent=2)
        log.info("JSON saved: %s (%d items)", JSON_PATH, len(all_products))
    else:
        log.warning("No products to save!")

    # ── Statistics ─────────────────────────────────────────────────────────────
    log.info("\n" + "=" * 60)
    log.info("SCRAPING STATISTICS")
    log.info("=" * 60)
    log.info("  Keyword          : %s", KEYWORD)
    log.info("  Pages requested  : %d", MAX_PAGES)
    log.info("  Pages scraped OK : %d", pages_scraped)
    log.info("  Pages failed     : %d", pages_failed)
    log.info("  Total products   : %d", len(all_products))
    log.info("  Avg per page     : %.1f", len(all_products) / max(pages_scraped, 1))
    log.info("  Success rate     : %.1f%%", pages_scraped / max(MAX_PAGES, 1) * 100)
    log.info("  Elapsed time     : %.1fs", elapsed)
    log.info("  CSV output       : %s", CSV_PATH)
    log.info("  JSON output      : %s", JSON_PATH)
    log.info("=" * 60)

    return all_products


if __name__ == "__main__":
    products = scrape_taobao()
    if not products:
        print("\n[RESULT] No products scraped. Check logs above for details.")
    else:
        print(f"\n[RESULT] Successfully scraped {len(products)} products.")
