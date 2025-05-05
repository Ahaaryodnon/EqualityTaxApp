"""Spider for scraping UK MPs' Register of Members' Financial Interests."""
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Generator, Optional

import scrapy
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from services.ingestion.items import FinancialInterestItem, PersonItem


class UKRegisterOfInterestsSpider(CrawlSpider):
    """Spider for UK Register of Members' Financial Interests.

    This spider scrapes the UK Parliament website for MPs' financial
    interests as declared in the Register of Members' Financial Interests.
    """

    name = "uk_register_of_interests"
    allowed_domains = ["parliament.uk"]
    start_urls = [
        "https://www.parliament.uk/mps-lords-and-offices/standards-and-financial-interests/parliamentary-commissioner-for-standards/registers-of-interests/register-of-members-financial-interests/",
    ]

    # Define rules for following links
    rules = (
        Rule(
            LinkExtractor(
                allow=r"register-of-members-financial-interests/\d+",
                restrict_css="div.article-body",
            ),
            callback="parse_register_index",
        ),
    )

    def parse_register_index(self, response: Response) -> Generator[scrapy.Request, None, None]:
        """Parse the index page of a register.

        Args:
            response: Response object

        Yields:
            Requests to individual MP pages
        """
        self.logger.info(f"Parsing register index: {response.url}")

        # Get all MP links on the page
        mp_links = response.css("div.article-body a::attr(href)").getall()
        
        for link in mp_links:
            if "/financial-interests/" in link:
                yield response.follow(link, callback=self.parse_mp_interests)

    def parse_mp_interests(self, response: Response) -> Generator[Dict[str, Any], None, None]:
        """Parse an individual MP's interests page.

        Args:
            response: Response object

        Yields:
            Person and FinancialInterest items
        """
        self.logger.info(f"Parsing MP interests: {response.url}")

        # Extract MP name from the page title
        mp_name = response.css("h1::text").get()
        if not mp_name:
            self.logger.warning(f"Could not find MP name on {response.url}")
            return

        # Clean the name
        mp_name = mp_name.strip()
        
        # Extract constituency from subtitle if available
        constituency = response.css("h1 + p::text").get()
        if constituency:
            constituency = constituency.strip()
            if "Member for" in constituency:
                constituency = constituency.replace("Member for", "").strip()
        
        # Create person item
        person = PersonItem(
            full_name=mp_name,
            type="politician",
            parliament_id=self._extract_mp_id(response.url),
            constituency=constituency,
            is_current_mp=True,
            source_url=response.url,
        )
        
        yield person
        
        # Parse interests
        interests_sections = response.css("div.article-body h2, div.article-body h3")
        
        current_category = None
        
        for section in interests_sections:
            # Check if this is a category header
            if section.css("::text").re_first(r"^\d+\.\s"):
                current_category = section.css("::text").get().strip()
                continue
                
            # This is an MP's interest entry
            interest_title = section.css("::text").get().strip()
            
            # Get all paragraphs until the next section
            interest_paragraphs = []
            next_elem = section.xpath("following-sibling::*[1]")
            
            while next_elem and next_elem.root.tag != "h2" and next_elem.root.tag != "h3":
                if next_elem.root.tag == "p":
                    text = next_elem.css("::text").get()
                    if text and text.strip():
                        interest_paragraphs.append(text.strip())
                next_elem = next_elem.xpath("following-sibling::*[1]")
            
            # Join all paragraphs
            interest_description = "\n".join(interest_paragraphs)
            
            if not interest_description:
                continue
                
            # Determine interest type based on category
            interest_type = self._determine_interest_type(current_category)
            
            # Try to extract dates and amounts
            dates = self._extract_dates(interest_description)
            amount = self._extract_amount(interest_description)
            
            # Create interest item
            interest = FinancialInterestItem(
                person_name=mp_name,
                type=interest_type,
                description=interest_description,
                amount=amount["amount"] if amount else None,
                currency=amount["currency"] if amount else "GBP",
                registered_date=dates.get("registered_date"),
                start_date=dates.get("start_date"),
                source_document=f"Register of Members' Financial Interests - {datetime.now().strftime('%B %Y')}",
                source_url=response.url,
            )
            
            yield interest

    def _extract_mp_id(self, url: str) -> Optional[str]:
        """Extract MP ID from URL.

        Args:
            url: URL string

        Returns:
            MP ID or None if not found
        """
        match = re.search(r"/financial-interests/([^/]+)", url)
        if match:
            return match.group(1)
        return None

    def _determine_interest_type(self, category: Optional[str]) -> str:
        """Determine interest type based on category.

        Args:
            category: Category string from the register

        Returns:
            Interest type
        """
        if not category:
            return "miscellaneous"
            
        category = category.lower()
        
        if "employment" in category or "earnings" in category:
            return "employment"
        elif "donation" in category or "funding" in category:
            return "donation"
        elif "gift" in category or "hospitality" in category:
            return "gift"
        elif "visit" in category:
            return "gift"  # Overseas visits are treated as gifts
        elif "shareholding" in category:
            return "shareholding"
        elif "property" in category or "land" in category:
            return "property"
        elif "directorship" in category:
            return "directorship"
        else:
            return "miscellaneous"

    def _extract_dates(self, text: str) -> Dict[str, datetime]:
        """Extract dates from interest description.

        Args:
            text: Interest description text

        Returns:
            Dictionary of extracted dates
        """
        dates = {}
        
        # Look for registered date patterns
        registered_patterns = [
            r"Registered\s+on\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
            r"Registered\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
        ]
        
        for pattern in registered_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    date_str = match.group(1)
                    dates["registered_date"] = datetime.strptime(date_str, "%d %B %Y")
                    break
                except ValueError:
                    pass
        
        # Look for start date patterns
        start_patterns = [
            r"received\s+on\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
            r"received\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
            r"from\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
        ]
        
        for pattern in start_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    date_str = match.group(1)
                    dates["start_date"] = datetime.strptime(date_str, "%d %B %Y")
                    break
                except ValueError:
                    pass
        
        return dates

    def _extract_amount(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract monetary amount from interest description.

        Args:
            text: Interest description text

        Returns:
            Dictionary with amount and currency, or None if not found
        """
        # Common patterns for UK money
        patterns = [
            r"£([\d,]+)(?:\.(\d+))?",  # £1,234.56
            r"(\d+)(?:,(\d+))?\s+pounds",  # 1,234 pounds
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    if match.group(1):
                        amount_str = match.group(1).replace(",", "")
                        amount = float(amount_str)
                        
                        # Add decimal part if present
                        if match.group(2):
                            decimal = match.group(2)
                            amount += float(f"0.{decimal}")
                            
                        return {"amount": amount, "currency": "GBP"}
                except (ValueError, IndexError):
                    pass
        
        return None 