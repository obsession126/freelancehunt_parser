from django.core.management.base import BaseCommand
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path


class Command(BaseCommand):
    help = "Parse jobs info"

    def handle(self, *args, **kwargs):
        while True:
            driver = webdriver.Chrome()
            jobs = []
            seen_jobs = set()
            page = 1

            try:
                while True:
                    url = f"https://freelancehunt.com/ua/projects/skill/python/22.html?page={page}"
                    driver.get(url)
                    time.sleep(2)

                    soup = BeautifulSoup(driver.page_source, "lxml")
                    rows = soup.find_all("tr", style="vertical-align: top")

                    if not rows:
                        break


                    new_job_found = False

                    for row in rows:
                        title_tag = row.find("a", class_="biggest visitable")
                        href = title_tag["href"] if title_tag else ""

                        if href in seen_jobs:
                            continue
                        seen_jobs.add(href)
                        new_job_found = True

                        desc_tag = row.find("p")
                        price_tag = row.find("div", class_="text-green price")

                        jobs.append({
                            "title": title_tag.text.strip() if title_tag else "",
                            "href": href,
                            "description": desc_tag.text.strip() if desc_tag else "",
                            "price": price_tag.text.strip() if price_tag else "",
                        })

                    if not new_job_found:
                        break
                    page += 1
            finally:
                driver.quit()
            Path("jobs.json").write_text(
                json.dumps(jobs, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            self.stdout.write(self.style.SUCCESS(
                f"Saved {len(jobs)} jobs. Sleeping 5 minutes..."
            ))

            time.sleep(300)
