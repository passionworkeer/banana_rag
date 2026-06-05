#!/usr/bin/env python3
"""
合并和去重淘宝浏览器抓取的商品数据。

用法:
    python merge_and_save.py --input browser_raw.json --output products.json [--existing existing.json]

输入格式 (browser_raw.json):
    JSON 数组: [{"i": "itemId", "t": "title", "p": "price", "s": "shop"}, ...]

输出:
    - products.json  (完整 JSON，包含所有字段)
    - products.csv   (CSV，表头: itemId, title, price, shop, link, source)
"""
import json
import csv
import re
import argparse
import sys


def extract_item_id(link):
    """从淘宝/天猫商品链接中提取 itemId。"""
    m = re.search(r'[?&]id=(\d+)', link)
    return m.group(1) if m else None


def clean_shop_name(shop):
    """去除店铺名中的 '9年老店' 等前缀。"""
    return re.sub(r'^\d+年老店', '', shop).strip()


def is_bananain_product(title, shop):
    """判断商品是否可能是蕉内 (Bananain) 品牌商品。"""
    bananain_keywords = ['蕉内', 'Bananain', 'banana', '蕉内儿童', '蕉内旗舰']
    text = (title + ' ' + shop).lower()
    return any(kw.lower() in text for kw in bananain_keywords)


def merge_products(existing_file, raw_file, output_json, output_csv, brand_filter=None):
    """将已有的脚本抓取数据与新的浏览器抓取数据合并。"""
    merged = {}

    # 加载已有数据
    if existing_file:
        with open(existing_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        for p in existing_data:
            link = p.get('link', '')
            iid = extract_item_id(link) or p.get('itemId', '')
            if iid and iid not in merged:
                merged[iid] = {
                    'itemId': iid,
                    'title': p.get('title', ''),
                    'price': p.get('price', ''),
                    'shop': clean_shop_name(p.get('shop', '')),
                    'link': f'https://item.taobao.com/item.htm?id={iid}',
                    'source': 'script'
                }
        print(f"Loaded {len(merged)} existing products from {existing_file}")

    # 加载浏览器抓取数据
    with open(raw_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    browser_count = 0
    for item in raw_data:
        iid = item.get('i', '') or item.get('itemId', '')
        if not iid:
            continue

        title = item.get('t', '') or item.get('title', '')
        price = item.get('p', '') or item.get('price', '')
        shop = item.get('s', '') or item.get('shop', '')
        shop = clean_shop_name(shop)

        # 可选的品牌过滤
        if brand_filter and not brand_filter(title, shop):
            continue

        merged[iid] = {
            'itemId': iid,
            'title': title,
            'price': price,
            'shop': shop,
            'link': f'https://item.taobao.com/item.htm?id={iid}',
            'source': 'browser'
        }
        browser_count += 1

    print(f"Processed {browser_count} browser products")

    # 转为排序后的列表
    all_products = sorted(merged.values(), key=lambda x: x['itemId'])

    # 保存 JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(all_products)} products to {output_json}")

    # 保存 CSV
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['itemId', 'title', 'price', 'shop', 'link', 'source'])
        writer.writeheader()
        for p in all_products:
            writer.writerow({k: p.get(k, '') for k in writer.fieldnames})
    print(f"Saved {len(all_products)} products to {output_csv}")

    # 输出统计信息
    script_count = sum(1 for p in all_products if p.get('source') == 'script')
    browser_final = sum(1 for p in all_products if p.get('source') == 'browser')
    print(f"\n=== Statistics ===")
    print(f"Total products: {len(all_products)}")
    print(f"From script: {script_count}")
    print(f"From browser: {browser_final}")

    # 店铺分布
    shops = {}
    for p in all_products:
        s = p.get('shop', 'unknown')
        shops[s] = shops.get(s, 0) + 1
    print(f"\nTop 10 shops:")
    for shop, count in sorted(shops.items(), key=lambda x: -x[1])[:10]:
        print(f"  {shop}: {count}")


def collect_browser_data_to_file(extracted_data_list, output_file):
    """
    将多次提取结果汇总到一个 JSON 文件中。
    每次提取结果应为 [{"i", "t", "p", "s"}] 格式的列表。
    """
    all_items = []
    for page_data in extracted_data_list:
        if isinstance(page_data, str):
            page_data = json.loads(page_data)
        if isinstance(page_data, dict) and 'd' in page_data:
            all_items.extend(page_data['d'])
        elif isinstance(page_data, list):
            all_items.extend(page_data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    print(f"Collected {len(all_items)} raw items to {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge Taobao product data')
    parser.add_argument('--input', required=True, help='Browser raw JSON file')
    parser.add_argument('--output', required=True, help='Output JSON file path')
    parser.add_argument('--csv', help='Output CSV file path (default: same name .csv)')
    parser.add_argument('--existing', help='Existing products JSON to merge with')
    parser.add_argument('--brand-filter', choices=['bananain'], help='Filter by brand')

    args = parser.parse_args()
    csv_path = args.csv or args.output.replace('.json', '.csv')

    brand_fn = None
    if args.brand_filter == 'bananain':
        brand_fn = is_bananain_product

    merge_products(args.existing, args.input, args.output, csv_path, brand_filter=brand_fn)
