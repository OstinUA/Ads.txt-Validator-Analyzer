import pandas as pd
import requests
import io

class AdsTxtParser:
    def __init__(self):
        # Standard DataFrame columns
        self.columns = ['Domain', 'Publisher_ID', 'Account_Type', 'Certification_ID', 'Comment']

    def fetch_from_url(self, url):
        """Fetches the file from a URL (appends app-ads.txt if missing)."""
        if not url.startswith("http"):
            url = "https://" + url
        
        # If user enters a root domain, append standard path
        if not url.endswith("ads.txt") and not url.endswith("app-ads.txt"):
            url = url.rstrip("/") + "/app-ads.txt"
            
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text, url
        except Exception as e:
            return None, str(e)

    def parse_content(self, raw_text):
        """Parses ads.txt content and returns a DataFrame + list of syntax errors."""
        lines = raw_text.split('\n')
        parsed_data = []
        errors = []

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Handle comments
            comment = ""
            if '#' in line:
                parts = line.split('#', 1)
                line = parts[0].strip()
                comment = parts[1].strip()

            # If line is empty after comment removal
            if not line:
                continue

            # Split by comma (IAB standard)
            chunks = [chunk.strip() for chunk in line.split(',')]
            
            # VALIDATION LOGIC
            error_msg = None
            
            # Check 1: Field count (min 3: Domain, ID, Type)
            if len(chunks) < 3:
                error_msg = "Insufficient parameters (minimum 3 required)"
            
            # Check 2: Account Type (DIRECT/RESELLER)
            elif len(chunks) >= 3:
                acc_type = chunks[2].upper()
                if acc_type not in ['DIRECT', 'RESELLER']:
                    error_msg = f"Invalid Account Type: {chunks[2]} (Expected DIRECT or RESELLER)"

            if error_msg:
                errors.append({"Line": line_num, "Content": line, "Error": error_msg})
                continue

            # Collect valid data
            domain = chunks[0].lower()
            pub_id = chunks[1]
            acc_type = chunks[2].upper()
            cert_id = chunks[3] if len(chunks) > 3 else "" # 4th param is optional
            
            parsed_data.append({
                'Domain': domain,
                'Publisher_ID': pub_id,
                'Account_Type': acc_type,
                'Certification_ID': cert_id,
                'Comment': comment
            })

        df = pd.DataFrame(parsed_data, columns=self.columns)
        return df, errors

    def get_stats(self, df):
        """Calculates basic statistics."""
        if df.empty:
            return None
        return {
            "total_lines": len(df),
            "unique_partners": df['Domain'].nunique(),
            "direct_count": len(df[df['Account_Type'] == 'DIRECT']),
            "reseller_count": len(df[df['Account_Type'] == 'RESELLER'])
        }
