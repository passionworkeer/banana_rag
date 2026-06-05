"""
Taobao Scraper Round 3 - Expanded keyword mining
===================================================
Round 2 results: keyword variations were extremely effective.
This round expands with many more category-specific keywords
and tries multi-page for each variant.
"""

import csv
import json
import logging
import random
import re
import time
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ── Configuration ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
EXISTING_DATA = DATA_DIR / "taobao_bananain_products_full.json"
OUTPUT_DIR = DATA_DIR
CSV_PATH = OUTPUT_DIR / "taobao_bananain_products_full.csv"
JSON_PATH = OUTPUT_DIR / "taobao_bananain_products_full.json"

URL_TEMPLATE = (
    "https://uland.taobao.com/sem/tbsearch"
    "?keyword={keyword}&q={keyword}&search_type=item"
    "&sourceId=tb.index&tab=all&page={page}"
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
]

# Expanded keyword list covering all Bananain product categories
KEYWORDS = [
    # Core categories
    "蕉内T恤", "蕉内短袖", "蕉内长袖",
    "蕉内卫衣", "蕉内外套", "蕉内夹克",
    "蕉内睡衣", "蕉内睡裤", "蕉内睡裙",
    "蕉内文胸", "蕉内胸罩", "蕉内内衣",
    "蕉内内裤男", "蕉内内裤女",
    "蕉内袜子男", "蕉内袜子女",
    "蕉内保暖", "蕉内秋衣", "蕉内秋裤",
    "蕉内瑜伽", "蕉内运动",
    "蕉内防晒衣", "蕉内防晒帽",
    "蕉内凉席", "蕉内被子", "蕉内四件套",
    "蕉内毛巾", "蕉内浴巾",
    "蕉内儿童", "蕉内宝宝",
    "蕉内情侣",
    # Product line names
    "蕉内银皮", "蕉内凉皮", "蕉内氧气",
    "蕉内棉棉", "蕉内热皮", "蕉内舒服蕾",
    "蕉内氮气", "蕉内丝丝",
    # Brand variations
    "Bananain", "蕉内官方",
    "蕉内家居", "蕉内居家",
    "蕉内拖鞋", "蕉内围巾",
    "蕉内背心", "蕉内吊带",
    "蕉内连衣裙", "蕉内半身裙",
    "蕉内衬衫", "蕉内POLO",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("round3_scraper")


def load_existing() -> tuple[list[dict], set[str]]:
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


def is_login_page(page) -> bool:
    title = page.title().lower()
    url = page.url.lower()
    return ("登录" in title or "login" in title or
            "login.taobao" in url or "login.tmall" in url)


def extract_products_js(page) -> list[dict]:
    return page.evaluate("""
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
                    maxLen = t.length; title = t;
                }
            }
            if (!title) title = (link.getAttribute('title') || link.textContent || '').trim();
            if (title.length < 4) continue;
            let price = '';
            const pm = card.textContent.match(/[¥￥]?\\s*(\\d+\\.?\\d*)/);
            if (pm) price = pm[1];
            let img = '';
            const imgEl = link.querySelector('img') || card.querySelector('img');
            if (imgEl) img = imgEl.src || imgEl.getAttribute('data-src') || '';
            let shop = '';
            card.querySelectorAll('[class*="shop"], [class*="Shop"], [class*="store"], [class*="seller"]').forEach(el => {
                const t = (el.textContent || '').trim();
                if (t.length > 1 && t.length < 50 && !shop) shop = t;
            });
            results.push({ title: title.substring(0, 200), price, shop, link: href, image: img });
        }
        return results;
    }
    """)


def save_results(products, csv_path, json_path):
    if not products:
        return
    fieldnames = ["title", "price", "shop", "link", "image", "page"]
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


def scrape_round3():
    all_products, seen_ids = load_existing()
    starting_count = len(all_products)
    total_new = 0
    login_wall_count = 0
    keywords_tried = 0
    keywords_successful = []

    log.info("=" * 70)
    log.info("ROUND 3 - Expanded keyword mining")
    log.info("Starting products: %d | Keywords to try: %d",
             len(all_products), len(KEYWORDS))
    log.info("=" * 70)

    with sync_playwright() as pw:
        for kw_idx, keyword in enumerate(KEYWORDS, 1):
            # Try page 1-3 for each keyword
            kw_new = 0
            for page_num in range(1, 4):
                url = URL_TEMPLATE.format(keyword=quote(keyword), page=page_num)
                log.info("[%d/%d] '%s' page %d ...", kw_idx, len(KEYWORDS), keyword, page_num)

                browser = pw.chromium.launch(
                    headless=True,
                    args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
                )
                context = browser.new_context(
                    user_agent=random.choice(USER_AGENTS),
                    viewport={"width": 1920, "height": 1080},
                    locale="zh-CN",
                    timezone_id="Asia/Shanghai",
                )
                context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    window.chrome = { runtime: {} };
                    Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });
                """)
                page = context.new_page()

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(random.randint(2500, 4000))

                    # Scroll to load lazy content
                    for _ in range(3):
                        page.evaluate(f"window.scrollBy(0, {random.randint(300, 700)})")
                        page.wait_for_timeout(random.randint(300, 800))
                    page.evaluate("window.scrollTo(0, 0)")
                    page.wait_for_timeout(300)

                    if is_login_page(page):
                        login_wall_count += 1
                        log.info("  Login wall (total: %d)", login_wall_count)
                        browser.close()
                        break  # Skip remaining pages for this keyword

                    products = extract_products_js(page)
                    new_this_page = 0
                    for p in products:
                        link = p.get("link", "")
                        m = re.search(r'[?&]id=(\d+)', link)
                        item_id = m.group(1) if m else None
                        if item_id and item_id not in seen_ids:
                            seen_ids.add(item_id)
                            p["page"] = page_num
                            all_products.append(p)
                            new_this_page += 1

                    if new_this_page > 0:
                        kw_new += new_this_page
                        log.info("  +%d new (kw total: %d, global: %d)",
                                 new_this_page, kw_new, len(all_products))
                    else:
                        # No new data on page 1 -> skip remaining pages
                        if page_num == 1:
                            log.info("  0 new on page 1, skipping pages 2-3")
                        break  # All subsequent pages likely have same data

                except PlaywrightTimeout:
                    log.info("  Timeout")
                except Exception as exc:
                    log.info("  Error: %s", str(exc)[:80])
                finally:
                    try:
                        browser.close()
                    except Exception:
                        pass

                time.sleep(random.uniform(3.0, 6.0))

            keywords_tried += 1
            if kw_new > 0:
                keywords_successful.append((keyword, kw_new))
                total_new += kw_new
                # Save intermediate
                save_results(all_products, CSV_PATH, JSON_PATH)

            time.sleep(random.uniform(1.0, 3.0))

    # Final save
    save_results(all_products, CSV_PATH, JSON_PATH)

    # Statistics
    log.info("\n" + "=" * 70)
    log.info("ROUND 3 FINAL STATISTICS")
    log.info("=" * 70)
    log.info("  Starting products       : %d", starting_count)
    log.info("  New products added      : %d", total_new)
    log.info("  Total products          : %d", len(all_products))
    log.info("  Keywords tried          : %d", keywords_tried)
    log.info("  Keywords with new data  : %d", len(keywords_successful))
    log.info("  Login walls encountered : %d", login_wall_count)
    log.info("")
    log.info("  Keyword breakdown:")
    for kw, count in sorted(keywords_successful, key=lambda x: -x[1]):
        log.info("    %-20s : +%d", kw, count)
    log.info("=" * 70)

    return all_products


if __name__ == "__main__":
    products = scrape_round3()
    print(f"\n[RESULT] Total {len(products)} products saved.")
