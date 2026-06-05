"""
Taobao/Tmall Advanced Scraper - Push beyond page 6 login wall
=============================================================
Strategies:
  1. Continue pagination from page 6 with enhanced stealth
  2. Try alternative search URLs (s.taobao.com, different SEM params)
  3. Fresh browser context per page to avoid session-based tracking
  4. Mobile UA variant
  5. Scroll-based infinite loading
  6. If login wall detected, auto-switch strategy
"""

import csv
import json
import logging
import random
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, quote

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ── Configuration ──────────────────────────────────────────────────────────────
KEYWORD = "蕉内"
START_PAGE = 6          # Continue from where we left off
MAX_PAGE = 30           # Try to push as far as possible
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
EXISTING_DATA = DATA_DIR / "taobao_bananain_products.json"
OUTPUT_DIR = DATA_DIR
CSV_PATH = OUTPUT_DIR / "taobao_bananain_products_full.csv"
JSON_PATH = OUTPUT_DIR / "taobao_bananain_products_full.json"
LOG_PATH = LOGS_DIR / "scraper_advanced.log"

# Multiple URL templates to try
URL_TEMPLATES = {
    "sem": (
        "https://uland.taobao.com/sem/tbsearch"
        "?keyword={keyword}&q={keyword}&search_type=item"
        "&sourceId=tb.index&tab=all&page={page}"
    ),
    "search": "https://s.taobao.com/search?q={keyword}&s={offset}",
    "tmall": "https://list.tmall.com/search_product.htm?q={keyword}&from=mallfp..pc_1_searchbutton&style=g&page={page}",
}

# Desktop + Mobile UAs for rotation
USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    # Edge Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
]

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 "
    "Mobile/15E148 Safari/604.1"
)

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(LOG_PATH), mode="a", encoding="utf-8"),
    ],
)
log = logging.getLogger("advanced_scraper")


# ── Load existing data ─────────────────────────────────────────────────────────
def load_existing_data() -> tuple[list[dict], set[str]]:
    """Load previously scraped data and return (products, seen_item_ids)."""
    if EXISTING_DATA.exists():
        with open(EXISTING_DATA, "r", encoding="utf-8") as f:
            data = json.load(f)
        seen = set()
        for item in data:
            link = item.get("link", "")
            m = re.search(r'[?&]id=(\d+)', link)
            if m:
                seen.add(m.group(1))
        log.info("Loaded %d existing products, %d unique IDs", len(data), len(seen))
        return data, seen
    return [], set()


# ── Detection helpers ──────────────────────────────────────────────────────────
def is_login_page(page) -> bool:
    title = page.title().lower()
    url = page.url.lower()
    if "登录" in title or "login" in title:
        return True
    if "login.taobao" in url or "login.tmall" in url:
        return True
    return False


def is_captcha_page(page) -> bool:
    """Check if page shows a captcha or security challenge."""
    try:
        content = page.content().lower()
        captcha_signals = [
            "captcha", "验证码", "滑块", "请验证",
            "punish", "sec.taobao", "acm.aliyun",
            "baxia", "nocaptcha",
        ]
        hits = sum(1 for s in captcha_signals if s in content)
        return hits >= 2
    except Exception:
        return False


def is_empty_page(page) -> bool:
    """Check if page has any product content."""
    try:
        content = page.content()
        # Check for product-related patterns
        has_products = bool(re.search(r'(?:detail\.tmall|item\.taobao|item\.htm\?id=)', content))
        has_alicdn = "alicdn" in content
        return not (has_products or has_alicdn)
    except Exception:
        return True


# ── Product extraction (reuse proven strategies) ──────────────────────────────
def extract_products(page, page_num: int) -> list[dict]:
    """Extract product data using multiple strategies."""
    strategies = [
        _extract_js_eval,
        _extract_card_selectors,
        _extract_link_scan,
    ]
    for idx, strategy in enumerate(strategies, 1):
        try:
            products = strategy(page, page_num)
            if products:
                log.info(f"  Strategy #{idx}: {len(products)} products")
                return products
        except Exception as exc:
            log.debug(f"  Strategy #{idx} failed: {exc}")
    return []


def _extract_js_eval(page, page_num: int) -> list[dict]:
    """Most robust: JS-based extraction from rendered DOM."""
    products = page.evaluate("""
    () => {
        const results = [];
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

            let card = link;
            for (let i = 0; i < 8; i++) {
                if (card.parentElement) card = card.parentElement;
                else break;
            }

            let title = '';
            const allTextEls = link.querySelectorAll('span, div, p');
            let maxLen = 0;
            for (const el of allTextEls) {
                const t = (el.textContent || '').trim();
                if (t.length > maxLen && t.length > 4) {
                    maxLen = t.length;
                    title = t;
                }
            }
            if (!title) {
                title = (link.getAttribute('title') || link.textContent || '').trim();
            }
            if (title.length < 4) continue;

            let price = '';
            const priceMatch = card.textContent.match(/[\\u00a5\\uffe5]?\\s*(\\d+\\.?\\d*)/);
            if (priceMatch) price = priceMatch[1];

            let img = '';
            const imgEl = link.querySelector('img') || card.querySelector('img');
            if (imgEl) img = imgEl.src || imgEl.getAttribute('data-src') || '';

            let shop = '';
            const shopEls = card.querySelectorAll(
                '[class*="shop"], [class*="Shop"], [class*="store"], [class*="Store"], '
                + '[class*="seller"], [class*="Seller"]'
            );
            for (const el of shopEls) {
                const t = (el.textContent || '').trim();
                if (t.length > 1 && t.length < 50) { shop = t; break; }
            }

            results.push({ title: title.substring(0, 200), price, shop, link: href, image: img });
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


def _extract_card_selectors(page, page_num: int) -> list[dict]:
    """CSS selector-based extraction."""
    selectors = [
        '[class*="Card--doubleCard"]',
        '[class*="Content--contentInner"] a[href*="detail"]',
        '[class*="Content--content"] a[href*="item"]',
        '[class*="Card"] a[href*="detail"]',
    ]
    cards = []
    for sel in selectors:
        cards = page.query_selector_all(sel)
        if cards:
            break
    if not cards:
        return []

    products = []
    for card in cards:
        try:
            title = ""
            for sel in ['[class*="title"]', '[class*="Title"]', '[class*="name"]']:
                el = card.query_selector(sel)
                if el:
                    title = el.inner_text().strip()
                    break
            if not title:
                title = (card.get_attribute("title") or card.inner_text() or "").strip()[:200]

            link_el = card.query_selector("a[href]")
            link = ""
            if link_el:
                href = link_el.get_attribute("href") or ""
                if href.startswith("//"):
                    href = "https:" + href
                link = href

            price_el = card.query_selector('[class*="price"], [class*="Price"]')
            price = ""
            if price_el:
                m = re.search(r'(\d+\.?\d*)', price_el.inner_text())
                price = m.group(1) if m else ""

            img_el = card.query_selector("img")
            image = ""
            if img_el:
                image = img_el.get_attribute("src") or img_el.get_attribute("data-src") or ""
                if image.startswith("//"):
                    image = "https:" + image

            shop = ""
            for sel in ['[class*="shop"]', '[class*="Shop"]', '[class*="store"]']:
                el = card.query_selector(sel)
                if el:
                    shop = el.inner_text().strip()
                    break

            if title and len(title) > 2:
                products.append({
                    "title": title[:200], "price": price, "shop": shop,
                    "link": link, "image": image, "page": page_num,
                })
        except Exception:
            continue
    return products


def _extract_link_scan(page, page_num: int) -> list[dict]:
    """Scan all links on the page for product patterns."""
    products = page.evaluate("""
    () => {
        const results = [];
        const seen = new Set();
        document.querySelectorAll('a[href]').forEach(a => {
            const href = a.href || '';
            if (!href.match(/(?:detail\\.tmall|item\\.taobao|item\\.htm\\?id=)/)) return;
            const idMatch = href.match(/[?&]id=(\\d+)/);
            const key = idMatch ? idMatch[1] : href;
            if (seen.has(key)) return;
            seen.add(key);

            const title = (a.getAttribute('title') || a.textContent || '').trim().substring(0, 200);
            if (title.length < 4) return;

            let img = '';
            const imgEl = a.querySelector('img');
            if (imgEl) img = imgEl.src || imgEl.getAttribute('data-src') || '';
            if (img.startsWith('//')) img = 'https:' + img;

            results.push({ title, link: href, image: img });
        });
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


# ── Browser context factory ────────────────────────────────────────────────────
def create_stealth_context(playwright, ua=None, viewport_w=1920, viewport_h=1080):
    """Create a new browser context with stealth settings."""
    if ua is None:
        ua = random.choice(USER_AGENTS)

    context = playwright.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars",
            "--disable-extensions",
        ],
    ).new_context(
        user_agent=ua,
        viewport={"width": viewport_w, "height": viewport_h},
        locale="zh-CN",
        timezone_id="Asia/Shanghai",
        color_scheme="light",
    )

    context.add_init_script("""
        // Remove webdriver flag
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        // Fake chrome object
        window.chrome = { runtime: {}, loadTimes: function(){}, csi: function(){} };
        // Fake plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => {
                const arr = [];
                for (let i = 0; i < 5; i++) arr.push({name: 'Plugin ' + i});
                return arr;
            },
        });
        // Fake languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en-US', 'en'],
        });
        // Override permissions query
        const origQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (params) => (
            params.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                origQuery(params)
        );
        // Prevent canvas fingerprint detection
        const origToBlob = HTMLCanvasElement.prototype.toBlob;
        HTMLCanvasElement.prototype.toBlob = function(cb, type, quality) {
            return origToBlob.call(this, cb, type, quality);
        };
    """)

    return context


# ── Scroll simulation ──────────────────────────────────────────────────────────
def simulate_human_scroll(page, scroll_count=5):
    """Simulate human-like scrolling to trigger lazy loading."""
    for i in range(scroll_count):
        distance = random.randint(300, 800)
        page.evaluate(f"window.scrollBy(0, {distance})")
        page.wait_for_timeout(random.randint(400, 1200))

    # Scroll back to top
    page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
    page.wait_for_timeout(500)


# ── Main advanced scraper ──────────────────────────────────────────────────────
def scrape_advanced():
    # Load existing data
    existing_products, seen_ids = load_existing_data()
    all_products = list(existing_products)
    new_products_count = 0

    log.info("=" * 70)
    log.info("ADVANCED SCRAPER - Push beyond page 6")
    log.info("Keyword: %s | Start page: %d | Max page: %d", KEYWORD, START_PAGE, MAX_PAGE)
    log.info("Existing products: %d | Known item IDs: %d", len(existing_products), len(seen_ids))
    log.info("=" * 70)

    # Track which strategies have been tried
    login_wall_hit = False
    strategies_tried = []
    consecutive_failures = 0

    with sync_playwright() as pw:
        # ── Strategy A: Continue standard pagination with fresh contexts ──
        log.info("\n>>> STRATEGY A: Fresh context per page with enhanced stealth")
        for page_num in range(START_PAGE, MAX_PAGE + 1):
            offset = (page_num - 1) * 44
            url = URL_TEMPLATES["sem"].format(keyword=quote(KEYWORD), page=page_num)
            log.info("\n--- Page %d (Strategy A) ---", page_num)
            log.info("URL: %s", url)

            # Fresh browser per page to avoid session tracking
            context = create_stealth_context(pw, ua=random.choice(USER_AGENTS))
            page = context.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(random.randint(2500, 4500))
                simulate_human_scroll(page)

                # Check status
                if is_login_page(page):
                    log.warning("LOGIN WALL on page %d (Strategy A)", page_num)
                    login_wall_hit = True
                    context.close()
                    consecutive_failures += 1
                    if consecutive_failures >= 3:
                        log.info("3 consecutive login walls, switching strategy")
                        break
                    continue

                if is_captcha_page(page):
                    log.warning("CAPTCHA detected on page %d (Strategy A)", page_num)
                    debug_path = OUTPUT_DIR / f"captcha_page_{page_num}.png"
                    page.screenshot(path=str(debug_path), full_page=True)
                    context.close()
                    consecutive_failures += 1
                    continue

                # Extract
                products = extract_products(page, page_num)
                new_on_page = 0
                for p in products:
                    link = p.get("link", "")
                    m = re.search(r'[?&]id=(\d+)', link)
                    item_id = m.group(1) if m else None
                    if item_id and item_id not in seen_ids:
                        seen_ids.add(item_id)
                        all_products.append(p)
                        new_on_page += 1
                    elif not item_id:
                        # Keep if title is unique enough
                        if not any(p["title"][:20] in ep["title"] for ep in all_products):
                            all_products.append(p)
                            new_on_page += 1

                if new_on_page > 0:
                    new_products_count += new_on_page
                    log.info("Page %d: %d extracted, %d NEW (total: %d)",
                             page_num, len(products), new_on_page, len(all_products))
                    consecutive_failures = 0
                else:
                    log.info("Page %d: %d extracted, 0 new (all duplicates)",
                             page_num, len(products))
                    consecutive_failures += 1

                if consecutive_failures >= 5:
                    log.info("5 consecutive pages with no new data, switching strategy")
                    context.close()
                    break

                # Save intermediate results
                _save_results(all_products, CSV_PATH, JSON_PATH)

            except PlaywrightTimeout:
                log.error("Page %d: timeout", page_num)
                consecutive_failures += 1
            except Exception as exc:
                log.error("Page %d: error - %s", page_num, exc)
                consecutive_failures += 1
            finally:
                try:
                    context.close()
                except Exception:
                    pass

            # Rate limiting
            delay = random.uniform(4.0, 8.0)
            log.info("Sleeping %.1fs ...", delay)
            time.sleep(delay)

        # ── Strategy B: Try s.taobao.com search ──
        if login_wall_hit or consecutive_failures >= 3:
            log.info("\n>>> STRATEGY B: Try s.taobao.com search URL")
            strategies_tried.append("s.taobao.com")
            consecutive_failures = 0

            for page_num in range(1, 15):
                offset = (page_num - 1) * 44
                url = URL_TEMPLATES["search"].format(keyword=quote(KEYWORD), offset=offset)
                log.info("\n--- Page %d (Strategy B: s.taobao.com) ---", page_num)

                context = create_stealth_context(pw)
                page = context.new_page()

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(random.randint(3000, 5000))
                    simulate_human_scroll(page)

                    if is_login_page(page):
                        log.warning("LOGIN WALL on s.taobao.com page %d", page_num)
                        context.close()
                        consecutive_failures += 1
                        if consecutive_failures >= 3:
                            log.info("s.taobao.com also login-walled, switching")
                            break
                        continue

                    if is_captcha_page(page):
                        log.warning("CAPTCHA on s.taobao.com page %d", page_num)
                        debug_path = OUTPUT_DIR / f"captcha_s_taobao_{page_num}.png"
                        page.screenshot(path=str(debug_path), full_page=True)
                        context.close()
                        consecutive_failures += 1
                        continue

                    products = extract_products(page, page_num + 100)  # Offset page num for tracking
                    new_on_page = 0
                    for p in products:
                        link = p.get("link", "")
                        m = re.search(r'[?&]id=(\d+)', link)
                        item_id = m.group(1) if m else None
                        if item_id and item_id not in seen_ids:
                            seen_ids.add(item_id)
                            all_products.append(p)
                            new_on_page += 1

                    if new_on_page > 0:
                        new_products_count += new_on_page
                        log.info("s.taobao.com page %d: %d NEW (total: %d)",
                                 page_num, new_on_page, len(all_products))
                        consecutive_failures = 0
                    else:
                        log.info("s.taobao.com page %d: 0 new", page_num)
                        consecutive_failures += 1

                    _save_results(all_products, CSV_PATH, JSON_PATH)

                except Exception as exc:
                    log.error("s.taobao.com page %d: %s", page_num, exc)
                    consecutive_failures += 1
                finally:
                    try:
                        context.close()
                    except Exception:
                        pass

                delay = random.uniform(4.0, 7.0)
                time.sleep(delay)

        # ── Strategy C: Mobile UA ──
        log.info("\n>>> STRATEGY C: Mobile user agent")
        strategies_tried.append("mobile_ua")
        consecutive_failures = 0

        mobile_urls = [
            f"https://s.m.taobao.com/h5?q={quote(KEYWORD)}&page=1",
            f"https://h5.m.taobao.com/app/search/index.html?q={quote(KEYWORD)}",
            URL_TEMPLATES["sem"].format(keyword=quote(KEYWORD), page=7),
        ]

        for url in mobile_urls:
            log.info("\n--- Strategy C: Mobile UA ---")
            log.info("URL: %s", url)

            context = create_stealth_context(
                pw, ua=MOBILE_UA,
                viewport_w=random.choice([375, 390, 414]),
                viewport_h=random.choice([667, 844, 896]),
            )
            page = context.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(random.randint(3000, 5000))
                simulate_human_scroll(page, scroll_count=8)

                if is_login_page(page):
                    log.warning("LOGIN WALL (mobile)")
                    debug_path = OUTPUT_DIR / f"mobile_login.png"
                    page.screenshot(path=str(debug_path), full_page=True)
                    context.close()
                    consecutive_failures += 1
                    continue

                products = extract_products(page, 200)
                new_on_page = 0
                for p in products:
                    link = p.get("link", "")
                    m = re.search(r'[?&]id=(\d+)', link)
                    item_id = m.group(1) if m else None
                    if item_id and item_id not in seen_ids:
                        seen_ids.add(item_id)
                        all_products.append(p)
                        new_on_page += 1

                if new_on_page > 0:
                    new_products_count += new_on_page
                    log.info("Mobile: %d NEW products (total: %d)", new_on_page, len(all_products))
                    consecutive_failures = 0
                else:
                    log.info("Mobile: 0 new products")
                    consecutive_failures += 1
                    # Save debug screenshot
                    debug_path = OUTPUT_DIR / f"mobile_empty.png"
                    page.screenshot(path=str(debug_path), full_page=True)

                _save_results(all_products, CSV_PATH, JSON_PATH)

            except Exception as exc:
                log.error("Mobile error: %s", exc)
                consecutive_failures += 1
            finally:
                try:
                    context.close()
                except Exception:
                    pass

            if consecutive_failures >= 3:
                log.info("Mobile strategy exhausted, moving on")
                break

            time.sleep(random.uniform(3.0, 6.0))

        # ── Strategy D: Scroll-based infinite loading on page 6 ──
        log.info("\n>>> STRATEGY D: Aggressive scrolling on page 6 to load more items")
        strategies_tried.append("scroll_page6")

        context = create_stealth_context(pw)
        page = context.new_page()
        url = URL_TEMPLATES["sem"].format(keyword=quote(KEYWORD), page=6)

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)

            for scroll_round in range(20):
                # Scroll down aggressively
                page.evaluate(f"window.scrollBy(0, {random.randint(600, 1200)})")
                page.wait_for_timeout(random.randint(800, 2000))

                # Check if new content loaded
                products = extract_products(page, 6)
                new_on_page = 0
                for p in products:
                    link = p.get("link", "")
                    m = re.search(r'[?&]id=(\d+)', link)
                    item_id = m.group(1) if m else None
                    if item_id and item_id not in seen_ids:
                        seen_ids.add(item_id)
                        all_products.append(p)
                        new_on_page += 1

                if new_on_page > 0:
                    new_products_count += new_on_page
                    log.info("Scroll round %d: %d NEW (total: %d)",
                             scroll_round + 1, new_on_page, len(all_products))
                else:
                    log.info("Scroll round %d: 0 new", scroll_round + 1)

                # Check for login wall during scrolling
                if is_login_page(page):
                    log.warning("Login wall during scroll round %d", scroll_round + 1)
                    break

                _save_results(all_products, CSV_PATH, JSON_PATH)

        except Exception as exc:
            log.error("Scroll strategy error: %s", exc)
        finally:
            try:
                context.close()
            except Exception:
                pass

        # ── Strategy E: Try different keyword variations ──
        log.info("\n>>> STRATEGY E: Keyword variations")
        strategies_tried.append("keyword_variations")

        keyword_variants = [
            "蕉内旗舰店",
            "蕉内内裤",
            "蕉内家居服",
            "蕉内防晒",
            "蕉内袜子",
            "Bananain蕉内",
        ]

        for kw in keyword_variants:
            url = URL_TEMPLATES["sem"].format(keyword=quote(kw), page=1)
            log.info("\n--- Strategy E: keyword='%s' ---", kw)

            context = create_stealth_context(pw)
            page = context.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(random.randint(3000, 5000))
                simulate_human_scroll(page, scroll_count=6)

                if is_login_page(page):
                    log.warning("LOGIN WALL for keyword '%s'", kw)
                    context.close()
                    consecutive_failures += 1
                    if consecutive_failures >= 3:
                        log.info("3 login walls on keyword variants, stopping")
                        break
                    continue

                products = extract_products(page, 300)
                new_on_page = 0
                for p in products:
                    link = p.get("link", "")
                    m = re.search(r'[?&]id=(\d+)', link)
                    item_id = m.group(1) if m else None
                    if item_id and item_id not in seen_ids:
                        seen_ids.add(item_id)
                        all_products.append(p)
                        new_on_page += 1

                if new_on_page > 0:
                    new_products_count += new_on_page
                    log.info("Keyword '%s': %d NEW (total: %d)",
                             kw, new_on_page, len(all_products))
                    consecutive_failures = 0
                else:
                    log.info("Keyword '%s': 0 new", kw)

                _save_results(all_products, CSV_PATH, JSON_PATH)

            except Exception as exc:
                log.error("Keyword '%s' error: %s", kw, exc)
            finally:
                try:
                    context.close()
                except Exception:
                    pass

            time.sleep(random.uniform(4.0, 7.0))

    # ── Final save ─────────────────────────────────────────────────────────────
    _save_results(all_products, CSV_PATH, JSON_PATH)

    # ── Statistics ─────────────────────────────────────────────────────────────
    log.info("\n" + "=" * 70)
    log.info("FINAL STATISTICS")
    log.info("=" * 70)
    log.info("  Starting products       : %d", len(existing_products))
    log.info("  New products added      : %d", new_products_count)
    log.info("  Total products          : %d", len(all_products))
    log.info("  Strategies tried        : %s", ", ".join(strategies_tried))
    log.info("  Login wall encountered  : %s", login_wall_hit)
    log.info("  CSV output              : %s", CSV_PATH)
    log.info("  JSON output             : %s", JSON_PATH)
    log.info("=" * 70)

    return all_products


def _save_results(products: list[dict], csv_path: Path, json_path: Path):
    """Save current results to CSV and JSON."""
    if not products:
        return
    fieldnames = ["title", "price", "shop", "link", "image", "page"]
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    products = scrape_advanced()
    if not products:
        print("\n[RESULT] No products scraped.")
    else:
        print(f"\n[RESULT] Total {len(products)} products saved.")
