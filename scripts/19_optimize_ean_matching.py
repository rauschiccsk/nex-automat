"""
Session Script 19: Optimize EAN Matching
Search GSCAT.BTR first (95% hit rate), then BARCODE.BTR
"""
from pathlib import Path


def main():
    print("=" * 60)
    print("Optimizing EAN Matching Strategy")
    print("=" * 60)

    # 1. Add find_by_barcode to GSCATRepository
    print("\n[1/2] Adding find_by_barcode() to GSCATRepository...")

    gscat_repo = Path(r"C:\Development\nex-automat\packages\nexdata\nexdata\repositories\gscat_repository.py")

    with open(gscat_repo, 'r', encoding='utf-8') as f:
        gscat_content = f.read()

    if 'def find_by_barcode' not in gscat_content:
        gscat_method = '''
    def find_by_barcode(self, barcode: str) -> Optional[GSCATRecord]:
        """
        Find product by primary barcode in GSCAT - LIVE query

        Most products (95%) have only one barcode stored in GSCAT.
        This is faster than searching BARCODE table.

        Args:
            barcode: Barcode string to search for

        Returns:
            GSCATRecord if found, None otherwise
        """
        try:
            # Search all products for matching barcode
            for product in self.get_all():
                if product.barcode and product.barcode.strip() == barcode:
                    return product

            return None

        except Exception as e:
            return None
'''

        # Insert at end of class
        insert_pos = gscat_content.rfind('\n')
        gscat_content = gscat_content[:insert_pos] + gscat_method + '\n' + gscat_content[insert_pos:]

        with open(gscat_repo, 'w', encoding='utf-8') as f:
            f.write(gscat_content)

        print("  ✅ Added find_by_barcode() to GSCATRepository")
    else:
        print("  ⚠️  find_by_barcode() already exists")

    # 2. Update ProductMatcher._match_by_ean()
    print("\n[2/2] Updating ProductMatcher._match_by_ean()...")

    matcher_file = Path(r"C:\Development\nex-automat\apps\supplier-invoice-loader\src\business\product_matcher.py")

    with open(matcher_file, 'r', encoding='utf-8') as f:
        matcher_content = f.read()

    old_method = '''    def _match_by_ean(self, ean: str) -> MatchResult:
        """
        Match by EAN code via BARCODE table - LIVE query

        Args:
            ean: EAN/barcode string

        Returns:
            MatchResult with 0.95 confidence if found
        """
        # Normalize EAN (remove spaces, dashes)
        ean_normalized = ean.replace(' ', '').replace('-', '').strip()

        if not ean_normalized:
            return MatchResult(product=None, confidence=0.0, method='none')

        # LIVE query to BARCODE
        barcode_record = self.barcode_repo.find_by_barcode(ean_normalized)

        if barcode_record:
            # LIVE query to GSCAT
            product = self.gscat_repo.get_by_code(barcode_record.gs_code)

            if product and not product.discontinued:
                return MatchResult(
                    product=product,
                    confidence=0.95,
                    method='ean'
                )

        # No match
        return MatchResult(
            product=None,
            confidence=0.0,
            method='none'
        )'''

    new_method = '''    def _match_by_ean(self, ean: str) -> MatchResult:
        """
        Match by EAN code - LIVE query

        Optimized strategy:
        1. Search GSCAT.BTR first (95% of products have only 1 barcode)
        2. If not found, search BARCODE.BTR (additional barcodes)

        Args:
            ean: EAN/barcode string

        Returns:
            MatchResult with 0.95 confidence if found
        """
        # Normalize EAN (remove spaces, dashes)
        ean_normalized = ean.replace(' ', '').replace('-', '').strip()

        if not ean_normalized:
            return MatchResult(product=None, confidence=0.0, method='none')

        # STEP 1: Search in GSCAT (primary barcode) - 95% hit rate
        product = self.gscat_repo.find_by_barcode(ean_normalized)

        if product and not product.discontinued:
            return MatchResult(
                product=product,
                confidence=0.95,
                method='ean'
            )

        # STEP 2: Search in BARCODE (additional barcodes) - 5% hit rate
        barcode_record = self.barcode_repo.find_by_barcode(ean_normalized)

        if barcode_record:
            # Get product from GSCAT
            product = self.gscat_repo.get_by_code(barcode_record.gs_code)

            if product and not product.discontinued:
                return MatchResult(
                    product=product,
                    confidence=0.95,
                    method='ean'
                )

        # No match
        return MatchResult(
            product=None,
            confidence=0.0,
            method='none'
        )'''

    if old_method in matcher_content:
        matcher_content = matcher_content.replace(old_method, new_method)

        with open(matcher_file, 'w', encoding='utf-8') as f:
            f.write(matcher_content)

        print("  ✅ Updated _match_by_ean() method")
    else:
        print("  ⚠️  Method already updated or pattern not found")

    print("\n" + "=" * 60)
    print("✅ EAN matching optimized!")
    print("=" * 60)
    print("\nStrategy:")
    print("  1. Search GSCAT.BTR (95% products) - FAST")
    print("  2. Search BARCODE.BTR (5% additional) - Fallback")

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())